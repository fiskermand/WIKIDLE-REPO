import csv
from selenium import webdriver
from selenium.webdriver.common.by import By

# Initialize the Chrome driver
browser = webdriver.Chrome()

# Navigate to the target page
url = "https://en.wikipedia.org/wiki/Wikipedia:Popular_pages"
browser.get(url)

# Target the specific container where all content lives
# This prevents picking up headers/tables from the sidebar or menus
content_container = browser.find_element(By.CSS_SELECTOR, "div.mw-parser-output")

# Fetch ALL direct children inside the main content text chronologically
elements = content_container.find_elements(By.XPATH, "./*")

scraped_data = []
current_category = "Top-100"  # Fallback/Default category for the very first table

for element in elements:
    tag = element.tag_name
    
    # 1. Look for Wikipedia's modern section heading wrappers
    if tag == "div" and "mw-heading" in element.get_attribute("class"):
        # The actual text sits inside an h3 or h2 within this div
        try:
            heading_text = element.find_element(By.CSS_SELECTOR, "h2, h3").text.strip()
            # Clean up the string to remove the "[edit]" link text
            if heading_text.endswith("[edit]"):
                heading_text = heading_text[:-6].strip()
            current_category = heading_text
        except:
            pass
            
    # 2. Look for the older style headings (just in case)
    elif tag in ["h2", "h3"]:
        heading_text = element.text.strip()
        if heading_text.endswith("[edit]"):
            heading_text = heading_text[:-6].strip()
        current_category = heading_text

    # 3. If the element is a table, scrape all article links inside it
    elif tag == "table" and "wikitable" in element.get_attribute("class"):
        articles = element.find_elements(By.CSS_SELECTOR, "tr td:nth-child(2) a")
        
        for article in articles:
            title = article.text.strip()
            # Filter out empty entries or structural wikipedia pages
            if title and not any(title.startswith(p) for p in ["Special:", "Wikipedia:", "Help:", "Portal:"]):
                scraped_data.append({
                    "Category/List Title": current_category,
                    "Article Title": title
                })

browser.quit()

# Print out a snippet of the results to verify
print(f"Scraped {len(scraped_data)} total articles.\n")
print(f"{'Category/List Title':<30} | {'Article Title'}")
print("-" * 65)
for row in scraped_data[:15]:  # Displaying the first 15 records
    print(f"{row['Category']:<30} | {row['Article Title']}")