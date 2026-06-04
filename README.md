# WIKIDLE-REPO

## About our project:
Our project is a  game we have called 'Wikidle', the goal of the game is to guess which Wikipedia article you are reading a summary of. We used this page: https://en.wikipedia.org/wiki/Wikipedia:Popular_pages to find the most popular pages within certain categories, from these articles we have gathered article_id's, summaries, titles and pictures using the Wikipedia API. 

Currently the game returns a new Wikipedia article every time the game is reset, as a proof of concept and to make the testing/grading process smoother, but our original idea is to have it be a "daily game" ('dle'-game), hence the name. 

## Guide to running the game:
1. This project uses PostgreSQL + pgAdmin 4.
2. In pgAdmin, create a database named wikipedia_articles.
3. Open the project folder.
4. Copy '.env.example', rename it '.env' and enter your PostgreSQL password.
5. Run: pip install -r requirements.txt
6. Run: python setup_database.py
7. Run: python app.py
8. Open: http://127.0.0.1:5000 in your browser. 

## E/R diagram:

<img width="533" height="642" alt="5eb2750afc685640a69e03540290f55c" src="https://github.com/user-attachments/assets/acdb6ad4-cb34-4efc-9c3d-dae40398ab82" />

## AI Declaration:
-

