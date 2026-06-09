import streamlit as st
from xai_sdk import Client
from xai_sdk.chat import user, system
import os
import json
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="GrokKOL Manager", page_icon="🔍", layout="wide")
st.title("🔍 GrokKOL Manager")
st.markdown("**SuperGrok Heavy** でリアルタイムKOL検索 + サブエージェント検証")

client = Client(api_key=os.getenv("XAI_API_KEY"))

MAIN_PROMPT = """あなたはプロのKOLマーケティングコンサルタントです。
ユーザーのテーマでX上の有望KOL候補を最大8人リストアップしてください。
各候補に以下の情報を必ず含めて：
- @username
- 推定フォロワー数
- エンゲージメント傾向
- 自社との相性（1文）
- おすすめ連絡文"""

if st.button("🔍 KOL検索を実行", type="primary", use_container_width=True):
    query = st.text_input("検索テーマ", value="AIツール マーケティング", label_visibility="collapsed")
    with st.spinner("Grok Heavy が検索 + 検証中..."):
        try:
            chat = client.chat.create(model="grok-4.3")
            chat.append(system(MAIN_PROMPT))
            chat.append(user(f"テーマ: {query} でKOL候補をリストアップ"))
            response = chat.sample()
            st.subheader("検索結果")
            st.write(response.text)
        except Exception as e:
            st.error(f"エラー: {e}")
else:
    st.info("上記の検索テーマでKOLを探す" )
st.caption("Powered by Grok 4 Heavy")