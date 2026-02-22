from flask import Flask, render_template, request
from newsapi import NewsApiClient
import feedparser
from bs4 import BeautifulSoup

app = Flask(__name__)

news_api = NewsApiClient(api_key="YOUR_API_KEY")

telugu_rss = {
    "sports": "https://telugu.oneindia.com/rss/feeds/telugu-sports-fb.xml",
    "medical": "https://telugu.oneindia.com/rss/feeds/telugu-health-fb.xml",
    "politics": "https://eenadu.net/rss",
    "education": "https://telugu.oneindia.com/rss/feeds/education-jobs-fb.xml",
    "others": "https://telugu.gizbot.com/rss/feeds/telugu-news-fb.xml"
}

hindi_rss = {
    "sports": "https://hindi.oneindia.com/rss/feeds/hindi-sports-fb.xml",
    "medical": "https://hindi.oneindia.com/rss/feeds/hindi-news-fb.xml",
    "politics": "https://hindi.oneindia.com/rss/feeds/hindi-politics-fb.xml",
    "education": "https://hindi.oneindia.com/rss/feeds/hindi-news-fb.xml",
    "others": "https://hindi.gizbot.com/rss/feeds/hindi-news-fb.xml"
}

eng_cat_map = {
    "sports": "sports",
    "medical": "health",
    "politics": "general",
    "education": "general",
    "others": "entertainment"
}

def fetch_english(category):
    cat = eng_cat_map.get(category, "general")
    res = news_api.get_top_headlines(
        language="en", country="in", category=cat, page_size=10
    )
    return res.get("articles", [])

def fetch_rss(url):
    feed = feedparser.parse(url)
    articles = []
    for entry in feed.entries[:10]:
        articles.append({
            "title": entry.get("title",""),
            "description": entry.get("description",""),
            "url": entry.get("link","")
        })
    return articles

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/news", methods=["POST"])
def news():
    lang = request.form["language"]
    category = request.form["category"]

    if lang == "English":
        articles = fetch_english(category)
    elif lang == "Telugu":
        articles = fetch_rss(telugu_rss.get(category))
    elif lang == "Hindi":
        articles = fetch_rss(hindi_rss.get(category))
    else:
        articles = []

    return render_template("news.html", articles=articles, lang=lang)

if __name__ == "__main__":
    app.run(debug=True)
