# PyConJP MCP Tool

PyConJP 2025 座長の日報（https://pyconjp-2025-chair.nishimotz.com/）から最新記事のタイトルを取得するMCPツールです。

**注意**: このツールは実用目的ではなく、学習・実験目的で作成されたものです。実際の運用には適していない可能性があります。

このツールは、Software Design誌「実践LLMアプリケーション開発」第19回のサンプルコード（[GitHub](https://github.com/mahm/softwaredesign-llm-application/tree/main)）を参考に作成されています。

## インストール方法

このリポジトリをクローンし、依存関係をインストールします。

```bash
git clone https://github.com/nishimotz/pyconjp-mcp-tool.git
cd pyconjp-mcp-tool
uv sync
```

## 使用方法

### サーバーの起動

#### stdioモード（デフォルト）

```bash
uv run server.py
```

#### sseモード

```bash
uv run server.py --transport sse --host 0.0.0.0 --port 8080
```

sseモードでは、サーバーは指定されたホストとポートでリッスンし、SSEプロトコルを使用してクライアントからの接続を受け付けます。

### Clineへの組み込み方

Clineエディタにこのツールを組み込むには、以下の設定を行います。

1. Clineの設定ファイル（`~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`）を開きます。
2. 以下の設定を追加します：

```json
{
  "mcpServers": {
    "pyconjp": {
      "command": "uv",
      "args": ["--directory", "[プロジェクトのパス]", "run", "server.py"],
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

**注意**: `[プロジェクトのパス]`は、あなたの環境に合わせて変更してください。例えば、このプロジェクトを`/Users/yourname/projects/pyconjp-mcp-tool`にクローンした場合、そのパスを指定します。

3. Clineを再起動します。

### ツールの使用

Clineで以下のように使用できます：

```
<use_mcp_tool>
<server_name>pyconjp</server_name>
<tool_name>get_pyconjp_latest_article</tool_name>
<arguments>
{}
</arguments>
</use_mcp_tool>
```

## 機能

- `get_pyconjp_latest_article`: PyConJP 2025 座長の日報から最新記事のタイトルを取得します。
