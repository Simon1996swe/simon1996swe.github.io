import requests
import os
import json
from datetime import datetime
from git import Repo

# === CONFIG (nu via GitHub Secrets) ===
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

GITHUB_REPO_PATH = "."  # kör i repo-root när Actions kör
TRACKED_STOCKS = [
    "Alphabet Inc Class A",
    "Apotea",
    "Black Hills",
    "Broadcom",
    "Cleveland-Cliffs",
    "Coca-Cola",
    "CrowdStrike",
    "EQT",
    "Frequency Electronics",
    "Insplorion",
    "Intel",
    "Joby Aviation",
    "Nebius Group",
    "nVent Electric",
    "NVIDIA",
    "Phillips 66",
    "POET Technologies",
    "Porsche Automobil Holding SE",
    "Rheinmetall",
    "Richetto Robotics",
    "Rusta",
    "SAAB B",
    "Sony ADR",
    "Take-Two Interactive Software",
    "WeRide"
]

NEWS_SOURCES = "bloomberg,business-insider,cnbc,financial-post,fortune,reuters,the-wall-street-journal,the-economist"

IMPORTANT_KEYWORDS = [
    "earnings", "profit", "guidance", "revenue", 
    "subsidy", "tariff", "ban", "lawsuit", 
    "fda", "approval", "merger", "acquisition", "forecast"
]

# === LÄS BEFINTLIGA ALERTS (för duplicate-skydd) ===
def load_existing_alerts():
    file_path = os.path.join(GITHUB_REPO_PATH, "alerts.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return []

# === SPARA NYA ALERTS ===
def save_alerts(alerts):
    file_path = os.path.join(GITHUB_REPO_PATH, "alerts.json")
    with open(file_path, "w") as f:
        json.dump(alerts[:50], f, indent=2)

    repo = Repo(GITHUB_REPO_PATH)
    repo.git.add("alerts.json")
    repo.index.commit(f"Update alerts {datetime.now().isoformat()} [skip ci]")
    origin = repo.remote(name="origin")
    origin.push()

# === HÄMTA NYHETER ===
def get_news(query):
    if not NEWSAPI_KEY:
        return []
    url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&language=en&sources={NEWS_SOURCES}&apiKey={NEWSAPI_KEY}"
    resp = requests.get(url, timeout=20)
    if resp.status_code == 200:
        return resp.json()["articles"][:10]
    return []

# === KOLLA OM NYHETEN ÄR RELEVANT ===
def get_matching_keyword(article, stock):
    text = (article.get("title", "") + " " + (article.get("description") or "")).lower()
    stock_lower = stock.lower()
    for word in IMPORTANT_KEYWORDS:
        if stock_lower in text and word in text:
            return word.upper()
    return None

# === SKICKA ALERT TILL DISCORD ===
def send_discord_alert(stock, title, url, keyword):
    if not DISCORD_WEBHOOK:
        print("❌ Ingen Discord-webhook funnen!")
        return
    data = {
        "content": f"🚨 **{stock}** nyhet [{keyword}]: {title}\n🔗 {url}"
    }
    resp = requests.post(DISCORD_WEBHOOK, json=data)
    print("Discord response:", resp.status_code)

# === MAIN LOOP ===
if __name__ == "__main__":
    existing_alerts = load_existing_alerts()

    # ✅ FIX: skydda mot saknade URL-fält
    existing_urls = {alert.get("url") for alert in existing_alerts if alert.get("url")}

    new_alerts = []

    for stock in TRACKED_STOCKS:
        articles = get_news(stock)
        for art in articles:
            url = art.get("url")
            title = art.get("title")

            if not url or not title:
                continue  # hoppa över trasiga artiklar

            keyword = get_matching_keyword(art, stock)
            if keyword and url not in existing_urls:
                print("Ny alert hittad:", title)
                send_discord_alert(stock, title, url, keyword)

                new_alerts.insert(0, {
                    "stock": stock,
                    "keyword": keyword,
                    "title": title,
                    "url": url,
                    "timestamp": datetime.now().isoformat()
                })

    if new_alerts:
        updated_list = new_alerts + existing_alerts
        save_alerts(updated_list)
    else:
        print("Inga nya nyheter att lägga till ✅")
