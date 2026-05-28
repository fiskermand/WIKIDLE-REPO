from collections import Counter
import csv
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import wikipediaapi

# Get Page Titles
browser = webdriver.Chrome()
browser.get("https://en.wikipedia.org/wiki/Wikipedia:Popular_pages")


articles = browser.find_elements(By.CSS_SELECTOR, "table.wikitable tr td:nth-child(2) a")

article_titles = []
for article in articles:
    title = article.text.strip()
    if title:
        article_titles.append(title)

browser.quit()

# Load API
wiki_api = wikipediaapi.Wikipedia(user_agent="WikiProject (bcgamingdk@gmail.com)", language="en")


# Load Stopwords
try:
    with open("stopwords.txt", "r", encoding="utf-8") as stopwords_file:
        stopword_list = stopwords_file.read().split()
except FileNotFoundError:
    stopword_list = []

# Make text cleaning functions
def stopword_killer(data, stopwords):
    return [word for word in data if word not in stopwords]

def clean_words(data):
    data = [word.lower() for word in data]
    return stopword_killer(data, stopword_list)

# Find the most relevant image of the image list
def find_relevant_image(article):
    relevancy_dict = {}

    title_words = re.findall(r"([a-zA-Z0-9]+)", article.title)
    title_words_cleaned = clean_words(title_words)
    title_words_set = set(title_words_cleaned)

    try:
        images = article.images.items()
    except Exception:
        return "API Error fetching images"

    for title, img in images:
        try:
            full_img_titles = re.findall(
                r"([\%\-_a-zA-Z0-9]+)\.(?:jpg|jpeg|png|svg|webp)", img.url, re.IGNORECASE)

            if not full_img_titles:
                continue

            img_title_words = re.findall(r"([a-zA-Z0-9]+)", full_img_titles[0])
            img_title_words_cleaned = clean_words(img_title_words)

            count = sum(
                1 for word in img_title_words_cleaned if word in title_words_set
            )
            relevancy_dict[img.url] = count
        except Exception:
            continue 

    if not relevancy_dict:
        return "No images found"

    counter = Counter(relevancy_dict)
    return counter.most_common(1)[0][0]


# Save articles into lists
headers = ["title", "summary", "image"]
article_elements = []

for article in article_titles:
    wiki_page = wiki_api.page(article)

    if not wiki_page.exists():
        continue

    img_link = find_relevant_image(wiki_page)

    clean_summary = wiki_page.summary.replace("\n", " ").strip()

    print(f"Processed: {wiki_page.title} -> Image: {img_link}")
    article_elements.append([wiki_page.title, clean_summary, img_link])

# Save to CSV
with open("wiki_articles.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerows(article_elements)