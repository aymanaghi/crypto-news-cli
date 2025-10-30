#!/usr/bin/env python3
# 📰 Crypto News CLI by Stinger (API key version)

import requests
import sys
from rich.console import Console
from rich.table import Table
from datetime import datetime

console = Console()

# 👇 paste your CryptoPanic API key here
API_KEY = "6118c26539d7d2b1e82114107d7f98bf481fc82c"

API_URL = "https://cryptopanic.com/api/v1/posts/"

def fetch_news(keyword=None):
    params = {
        "auth_token": API_KEY,
        "currencies": keyword,
        "public": "true",
    }
    try:
        r = requests.get(API_URL, params=params, timeout=10)
        r.raise_for_status()
        return r.json().get("results", [])
    except Exception as e:
        console.print(f"[red]❌ Error fetching news:[/red] {e}")
        return []

def show_news(articles, keyword=None):
    if not articles:
        console.print(f"[yellow]No news found for '{keyword}'[/yellow]" if keyword else "[yellow]No news found[/yellow]")
        return

    table = Table(title=f"🪙 Crypto News {f'({keyword})' if keyword else ''}", show_lines=True)
    table.add_column("Title", style="cyan", no_wrap=True)
    table.add_column("Source", style="magenta")
    table.add_column("Time", style="green")

    for article in articles[:10]:
        title = article.get("title", "No title")
        source = article.get("source", {}).get("title", "Unknown")
        published_at = article.get("published_at", "")
        try:
            time_fmt = datetime.fromisoformat(published_at[:-1]).strftime("%b %d, %H:%M")
        except Exception:
            time_fmt = "N/A"
        table.add_row(title, source, time_fmt)

    console.print(table)
    console.print("[bold blue]🌐 Visit:[/bold blue] https://cryptopanic.com for more")

if __name__ == "__main__":
    keyword = sys.argv[1] if len(sys.argv) > 1 else None
    console.print("[bold yellow]🚀 Fetching latest crypto news...[/bold yellow]")
    news = fetch_news(keyword)
    show_news(news, keyword)
