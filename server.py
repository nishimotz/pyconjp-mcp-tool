#!/usr/bin/env python
import os
import requests
from bs4 import BeautifulSoup
from typing import Dict, Any, Optional

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.utilities.logging import configure_logging, get_logger

# 定数定義
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8080
PYCONJP_URL = "https://pyconjp-2025-chair.nishimotz.com/"

logger = get_logger(__name__)
configure_logging()

mcp = FastMCP("pyconjp-mcp-tool")


def get_latest_article_title() -> Dict[str, Any]:
    """
    PyConJP 2025 座長の日報から最新記事のタイトルを取得します。
    
    Returns:
        Dict[str, Any]: 最新記事のタイトル、日付、URLを含む辞書
    """
    try:
        # ウェブサイトの内容を取得
        response = requests.get(PYCONJP_URL)
        response.raise_for_status()  # エラーチェック
        
        # HTMLを解析
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 最新記事の要素を取得
        article_list = soup.select('ul.list-none.ml-0 li')
        if not article_list:
            return {"error": "記事が見つかりませんでした。"}
        
        latest_article = article_list[0]
        
        # タイトル、日付、URLを抽出
        title_element = latest_article.select_one('h3')
        date_element = latest_article.select_one('span.text-sm.text-gray-500')
        link_element = latest_article.select_one('a')
        
        title = title_element.text.strip() if title_element else "タイトルが見つかりません"
        date = date_element.text.strip() if date_element else "日付が見つかりません"
        url = PYCONJP_URL + link_element['href'].lstrip('/') if link_element and 'href' in link_element.attrs else None
        
        return {
            "title": title,
            "date": date,
            "url": url
        }
    except Exception as e:
        logger.error(f"エラーが発生しました: {e}")
        return {"error": f"エラーが発生しました: {e}"}


@mcp.tool()
def get_pyconjp_latest_article() -> str:
    """
    PyConJP 2025 座長の日報から最新記事のタイトルとURLを取得します。
    """
    result = get_latest_article_title()
    
    if "error" in result:
        return result["error"]
    
    url_info = f"URL: {result['url']}" if result.get('url') else "URL: 利用できません"
    return f"最新記事: {result['title']} ({result['date']})\n{url_info}"


def start_server(
    transport: str, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT
) -> None:
    """MCPサーバーを起動する

    Args:
        transport (str): 使用するトランスポートモード ('stdio' または 'sse')
        host (str, optional): SSEモード時のホスト名. デフォルトは DEFAULT_HOST
        port (int, optional): SSEモード時のポート番号. デフォルトは DEFAULT_PORT
    """
    try:
        if transport == "stdio":
            mcp.run(transport="stdio")
        elif transport == "sse":
            mcp.run(transport="sse", host=host, port=port)
        else:
            raise ValueError(f"不正なトランスポートモード: {transport}")
    except Exception as e:
        logger.error(f"サーバー起動エラー: {e}")
        raise


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="MCPサーバーの起動モードを指定")
    parser.add_argument(
        "--transport",
        type=str,
        choices=["stdio", "sse"],
        default="stdio",
        help="使用するトランスポートモード (stdio または sse)",
    )
    parser.add_argument(
        "--host",
        type=str,
        default=DEFAULT_HOST,
        help="ホスト名",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help="ポート番号",
    )
    args = parser.parse_args()
    start_server(
        transport=args.transport,
        host=args.host,
        port=args.port,
    )
