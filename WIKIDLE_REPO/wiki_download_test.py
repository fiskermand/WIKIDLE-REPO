import wikipediaapi
import csv

wiki_api = wikipediaapi.Wikipedia(user_agent='WikiProject (bcgamingdk@gmail.com)', language='en')


article_titles = ['Python_(programming_languagge)', 'Michael Jordan']

headers = ['title', 'summary', 'category']
article_elements = []

for article in article_titles:
    wiki_page = wiki_api.page(article)
    article_elements.append([wiki_page.title, wiki_page.summary, wiki_page.categories])

with open('wiki_articles.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerows(article_elements)

