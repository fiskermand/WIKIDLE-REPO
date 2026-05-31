from collections import Counter
import csv
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import wikipediaapi

# Get Page Titles
browser = webdriver.Chrome()
browser.get("https://en.wikipedia.org/wiki/Wikipedia:Popular_pages")


tables = browser.find_elements(By.CSS_SELECTOR, "table.wikitable")

scraped_data = []

for table in tables:
    # Look backwards from the current table to find the nearest preceding heading
    # This completely avoids the Table of Contents confusion
    try:
        # Modern Wikipedia layout uses 'div.mw-heading' wrappers for headings
        heading_element = table.find_element(By.XPATH, "./preceding::div[contains(@class, 'mw-heading')][1]")
        category_text = heading_element.text.strip()
    except:
        try:
            # Fallback to older legacy Wikipedia heading tags if they exist
            heading_element = table.find_element(By.XPATH, "./preceding::h3[1]|./preceding::h2[1]")
            category_text = heading_element.text.strip()
        except:
            category_text = "Top-100"  # Default fallback if no header is found above it

    # Clean up the '[edit]' text Wikipedia attaches to section headers
    if category_text.endswith("[edit]"):
        category_text = category_text[:-6].strip()
        

    if "Navigation box" in category_text or "Contents" in category_text:
        continue

    articles = table.find_elements(By.CSS_SELECTOR, "tr td:nth-child(2) a")
    for article in articles:
        title = article.text.strip()
        # Filter out bad links/empty spaces
        if title and not any(title.startswith(p) for p in ["Special:", "Wikipedia:", "Help:", "Portal:"]):
            scraped_data.append({
                "Category": category_text,
                "Article Title": title
            })

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
headers = ["title", "summary", "image", "category"]
article_elements = []

for article in scraped_data:
    wiki_page = wiki_api.page(article["Article Title"])

    if not wiki_page.exists():
        continue

    img_link = find_relevant_image(wiki_page)

    clean_summary = wiki_page.summary.replace("\n", " ").strip()

    print(f"Processed: {wiki_page.title} -> Image: {img_link}")
    article_elements.append([article["Article Title"], clean_summary, img_link, article["Category"]])

# Save to CSV
with open("wiki_articles.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerows(article_elements)