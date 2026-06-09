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

# プロンプト（省略せず完全版）
# ... (完全コードをここに)
# 完全なコードは前のメッセージのものをコピーして使う