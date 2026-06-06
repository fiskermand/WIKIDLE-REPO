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

<img width="1198" height="549" alt="WIKIDLE_ER" src="https://github.com/user-attachments/assets/c8efa90b-b0d4-4287-aadf-e86381515ca2" />


## AI Declaration:
No AI was used to generate code in the creation of our project.
