import streamlit as st
from xai_sdk import Client
from xai_sdk.chat import user, system
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="GrokKOL Manager", page_icon="🔍", layout="wide")

# ==================== パスワード保護 ====================
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False

    if not st.session_state.password_correct:
        st.title("🔐 GrokKOL Manager")
        password = st.text_input("パスワードを入力してください", type="password")

        if st.button("ログイン", type="primary"):
            correct_password = st.secrets.get("APP_PASSWORD", "Pmjp")
            if password == correct_password:
                st.session_state.password_correct = True
                st.rerun()
            else:
                st.error("パスワードが違います")
        st.stop()

check_password()

# ==================== Clientの初期化（修正済み） ====================
def get_client():
    api_key = st.secrets.get("XAI_API_KEY") or os.getenv("XAI_API_KEY")
    if not api_key:
        st.error("XAI_API_KEYが設定されていません。Secretsを確認してください。")
        st.stop()
    return Client(api_key=api_key)

# ==================== メイン処理 ====================
st.title("🔍 GrokKOL Manager")
st.caption("SuperGrok Heavy × Sub-Agent検証システム")

if "results" not in st.session_state:
    st.session_state.results = []

query = st.text_input("検索テーマを入力", value="AIツール マーケティング", placeholder="例: AIマーケティング / Web3 / 美容")

col1, col2 = st.columns([1, 3])
with col1:
    max_kols = st.slider("取得件数", 3, 10, 6)

if st.button("🚀 KOL検索＋Sub-Agent検証を実行", type="primary", use_container_width=True):
    client = get_client()

    with st.spinner("Main AgentがKOL候補を抽出中..."):
        main_prompt = f"""テーマ「{query}」でX上で有望なKOLを最大{max_kols}件リストアップしてください。
以下のJSON配列のみを出力してください：
[
  {{
    "username": "@ユーザー名",
    "display_name": "表示名",
    "estimated_followers": 数値,
    "engagement_trend": "上昇中/安定/下降",
    "compatibility": "自社との相性一文"
  }}
]
"""
        chat = client.chat.create(model="grok-4.3")
        chat.append(system(main_prompt))
        chat.append(user(query))
        response = chat.sample().text

        json_match = re.search(r'\[.*\]', response, re.DOTALL)
        candidates = json.loads(json_match.group(0)) if json_match else []

    # Sub-Agent検証
    verified_results = []
    progress = st.progress(0, text="Sub-Agent検証中...")

    for i, kol in enumerate(candidates):
        progress.progress((i + 1) / len(candidates), text=f"検証中: @{kol['username']}")

        sub_prompt = f"""以下のKOLを最新のXデータに基づいて検証してください。
ユーザー名: {kol['username']}
表示名: {kol.get('display_name')}
推定フォロワー: {kol.get('estimated_followers')}

出力は以下のJSONのみにしてください：
{{
  "username": "{kol['username']}",
  "verified": true または false,
  "notes": "検証コメント（活動状況・スパム傾向など）",
  "adjusted_engagement": 1.0〜10.0の数値
}}"""

        chat2 = client.chat.create(model="grok-4.3")
        chat2.append(system(sub_prompt))
        chat2.append(user("検証を実行してください"))
        sub_response = chat2.sample().text

        try:
            sub_json = json.loads(re.search(r'\{.*\}', sub_response, re.DOTALL).group(0))
        except:
            sub_json = {
                "username": kol['username'],
                "verified": False,
                "notes": "検証に失敗しました",
                "adjusted_engagement": 0
            }

        kol.update(sub_json)
        verified_results.append(kol)

    progress.empty()
    st.session_state.results = verified_results
    st.success(f"Sub-Agent検証完了！（{len(verified_results)}件）")

# ==================== 結果表示 ====================
if st.session_state.results:
    st.subheader(f"📋 検証済みKOL一覧（{len(st.session_state.results)}件）")

    for kol in st.session_state.results:
        verified = kol.get("verified", False)
        status = "✅ 検証済み" if verified else "⚠️ 要注意"

        with st.container(border=True):
            c1, c2, c3 = st.columns([3, 2.5, 2])
            with c1:
                st.markdown(f"**@{kol['username']}**　{kol.get('display_name', '')}")
                st.caption(f"推定フォロワー: {kol.get('estimated_followers', '不明')}人")
            with c2:
                st.markdown(f"**検証結果**: {status}")
                st.caption(kol.get("notes", ""))
            with c3:
                st.metric(label="調整後エンゲージメント", value=kol.get("adjusted_engagement", "-"))

    if st.button("🗑️ 結果をクリア"):
        st.session_state.results = []
        st.rerun()
