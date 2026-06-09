import streamlit as st
from xai_sdk import Client
from xai_sdk.chat import user, system
import os
import json
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="GrokKOL Manager", page_icon="🔍", layout="wide")
st.title("🔍 GrokKOL Manager")
st.markdown("**SuperGrok Heavy** でリアルタイムKOL検索 + サブエージェント验証")

client = Client(api_key=os.getenv("XAI_API_KEY"))

MAIN_PROMPT = """You are a professional KOL marketing consultant.
For the user's theme, list up to 8 promising KOL candidates on X.
For each candidate, include:
- @username
- Estimated follower count
- Engagement trend
- Compatibility with our company (1 sentence)
- Recommended contact message
Respond in Japanese."""

SUB_AGENT_PROMPT = """You are a Verification Sub-Agent specialized in fact-checking.
Verify the following KOL information against the latest X data.
Output ONLY valid JSON in this format:
{
  "username": "@example",
  "verified": true,
  "notes": "验証コメント",
  "adjusted_engagement": 5.2
}
If suspicious, set verified: false."""

query = st.text_input("検索テーマを入力してください", placeholder="例: AIマーケティング / 大阪 美容 / Web3 インフルエンサー", value="AIツール マーケティング")

if st.button("🔍 KOL検索を実行", type="primary", use_container_width=True):
    with st.spinner("Grok Heavy が検索 + 验証中..."):
        try:
            # Main Agent
            chat = client.chat.create(model="grok-4.3")
            chat.append(system(MAIN_PROMPT))
            chat.append(user(f"テーマ: {query} で8件のKOL候補をリストアップ"))
            main_response = chat.sample().text

            st.success("Main Agent 検索完了")
            st.write(main_response)

            # Simple verification display (can be expanded)
            st.subheader("✅ Sub-Agent 验証結果")
            st.info("验証機能は次バージョンで完全実装予定です。現在はMain Agentの結果を表示中です。")

        except Exception as e:
            st.error(f"エラー: {e}")

st.caption("Powered by Grok 4 Heavy + Streamlit | SuperGrok Heavy 活用中")