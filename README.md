# GrokKOL Manager

SuperGrok Heavyを最大限活用した**社内向けKOLマーケティング支援ツール**です。

## 主な機能

- **KOL Search**: キーワードからX上の有望KOLを検索
- **Sub-Agent検証**: Grok 4 Heavyによる信憑性・活動状況の自動検証
- **パスワード保護**: 簡易認証で社外共有も可能

## 技術スタック

- Frontend: Streamlit
- LLM: Grok 4 Heavy（xAI）
- 検索: GrokネイティブのX検索機能のみ使用（公式API不使用）

---

## セットアップ

### 1. リポジトリをクローン

```bash
git clone https://github.com/hataraku-kobo/grok-kol-manager.git
cd grok-kol-manager
```

### 2. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 3. 環境変数の設定

#### 方法A: `.env` ファイルを使う場合（ローカル開発向け）

`.env` ファイルを作成して以下を記述：

```env
XAI_API_KEY=xai-あなたのAPIキー
```

#### 方法B: Streamlit Secretsを使う場合（推奨・本番向け）

`.streamlit/secrets.toml` を作成：

```toml
XAI_API_KEY = "xai-あなたのAPIキー"
APP_PASSWORD = "Pmjp"
```

> **注意**: `secrets.toml` はGitにコミットしないでください（`.gitignore`に追加済み想定）。

---

## 起動方法

```bash
streamlit run app.py
```

ブラウザで `http://localhost:8501` が開きます。

初回アクセス時にパスワード `Pmjp` の入力が必要です。

---

## Web公開（Streamlit Community Cloud）へのデプロイ

1. [Streamlit Community Cloud](https://share.streamlit.io/) にアクセス
2. GitHubリポジトリを接続
3. **Advanced settings** で以下を設定：
   - `XAI_API_KEY` と `APP_PASSWORD` をSecretsに登録
4. Deploy

---

## パスワードの変更方法

`app.py` 内の以下の部分を編集：

```python
correct_password = st.secrets.get("APP_PASSWORD", "Pmjp")
```

または `secrets.toml` の `APP_PASSWORD` を変更してください。

---

## 今後の予定

- [ ] Sub-Agentの検証精度向上
- [ ] 検証履歴の保存（Supabase）
- [ ] 競合分析機能の追加
- [ ] より堅牢な認証（streamlit-authenticator）

---

Powered by SuperGrok Heavy | Developed by GrokKOL Manager Team
