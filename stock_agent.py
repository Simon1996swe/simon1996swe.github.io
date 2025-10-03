import requests
import os
import json
from datetime import datetime
from git import Repo

# === CONFIG ===
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1423726522048581753/KZTkOrqkqTaiX67l0xyizTAj3N4NO1943q0lLx6Pyh94vZVhoGI9CjQmPp5eBGgs4DUq"
GITHUB_REPO_PATH = "C:\\Users\\simon kovac\\Desktop\\github-repo\\simon1996swe.github.io"
TRACKED_STOCKS = ["Nvidia", "Intel", "Novo Nordisk", "CrowdStrike"]

NEWS_SOURCES = "bbc-news,bloomberg,reuters,financial-times,cnbc"

IMPORTANT_KEYWORDS = [
    "earnings", "profit", "guidance", "revenue", 
    "subsidy", "tariff", "ban", "lawsuit", 
    "fda", "approval", "merger", "acquisition", "forecast"
]

# === HÄMTA NYHETER ===
def get_news(query):
    url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&language=en&sources={NEWS_SOURCES}&apiKey=2ed02d3066824068ad9e6137aafd63f7"
    resp = requests.get(url)
    if resp.status_code == 200:
        return resp.json()["articles"][:10]
    return []

# === KOLLA OM NYHETEN ÄR RELEVANT ===
def get_matching_keyword(article, stock):
    text = (article["title"] + " " + (article.get("description") or "")).lower()
    stock_lower = stock.lower()
    # Måste innehålla bolagsnamnet OCH ett viktigt ord
    for word in IMPORTANT_KEYWORDS:
        if stock_lower in text and word in text:
            return word.upper()
    return None

# === SKICKA ALERT TILL DISCORD ===
def send_discord_alert(stock, title, url, keyword):
    data = {
        "content": f"🚨 **{stock}** nyhet [{keyword}]: {title}\n🔗 {url}"
    }
    requests.post(DISCORD_WEBHOOK, json=data)

# === UPPDATERA GITHUB REPO ===
def update_github_alert(stock, title, url, keyword):
    file_path = os.path.join(GITHUB_REPO_PATH, "alerts.json")

    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            alerts = json.load(f)
    else:
        alerts = []

    alerts.insert(0, {
        "stock": stock,
        "keyword": keyword,
        "title": title,
        "url": url,
        "timestamp": datetime.now().isoformat()
    })

    with open(file_path, "w") as f:
        json.dump(alerts[:50], f, indent=2)

    repo = Repo(GITHUB_REPO_PATH)
    repo.git.add("alerts.json")
    repo.index.commit(f"Update alerts {datetime.now().isoformat()}")
    origin = repo.remote(name="origin")
    origin.push()

# === MAIN LOOP ===
if __name__ == "__main__":
    for stock in TRACKED_STOCKS:
        articles = get_news(stock)
        for art in articles:
            keyword = get_matching_keyword(art, stock)
            if keyword:  # 🚨 Bara nyheter som är relevanta
                send_discord_alert(stock, art["title"], art["url"], keyword)
                update_github_alert(stock, art["title"], art["url"], keyword)
