# WIKIDLE-REPO

## About our project:
Our project is a  game we have called 'Wikidle', the goal of the game is to guess which Wikipedia article you are reading a summary of. We used this page: https://en.wikipedia.org/wiki/Wikipedia:Popular_pages to find the most popular pages within certain categories, from these articles we have gathered article_id's, summaries, titles and pictures using the Wikipedia API. 

Currently the game returns a new Wikipedia article every time the game is reset, as a proof of concept and to make the testing/grading process smoother, but our original idea is to have it be a "daily game" ('dle'-game), where there is one predetermined article per day, hence the name. 

The game runs on Flask and Render, and the database is hosted on Supabase. 

The game uses SQL to interact with a database, containing the tables:
- wikipedia_articles (title, summary, category, picture)
- users(id, username, password_hash, created_at)
- game_results (id, user_id, article_title, guesses, created_at)

And regular expressions are used to:
- remove the mention of any words from the title in the summary-text.
- giving the blanked out title ('Michael Jackson' -> '_______ _______')

## Guide to running the game:
The game runs on https://wikidle-repo.onrender.com.

## E/R diagram:

<img width="533" height="642" alt="5eb2750afc685640a69e03540290f55c" src="https://github.com/user-attachments/assets/acdb6ad4-cb34-4efc-9c3d-dae40398ab82" />

## AI Declaration:
-

