# WIKIDLE-REPO

## Guide to running the game:
1. This project uses PostgreSQL + pgAdmin 4.
2. In pgAdmin, create a database named wikipedia_articles.
3. Open the project folder.
4. Copy .env.example, rename it .env and enter your PostgreSQL password.
5. Run: pip install -r requirements.txt
6. Run: python setup_database.py
7. Run: python app.py
8. Open: http://127.0.0.1:5000 in your browser. 

Currently the game returns a new Wikipedia article every time the game is reset, as a proof of concept and to make the testing/grading process smoother, but our original idea is to have it be a "daily game ('dle'-game)", where there is one article per day, hence the name. 

Here is our E/R diagram:

<img width="533" height="642" alt="5eb2750afc685640a69e03540290f55c" src="https://github.com/user-attachments/assets/acdb6ad4-cb34-4efc-9c3d-dae40398ab82" />
