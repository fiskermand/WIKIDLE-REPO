from flask import Flask, render_template, request, session
import re, random
import psycopg2
from connection import connection

# TODO:
# wikiapi til sql db + regex til at fjerne navn/whatever
# implementer sql delen
# login / leaderboard

app = Flask(__name__)
app.secret_key = "dev-secret-key"

def example_dict():
    cursor = connection.cursor()
    cursor.execute("""
        SELECT title, summary, category, picture
        FROM wikipedia_articles
    """)
    rows = cursor.fetchall()
    cursor.close()
    articles = {}
    for title, summary, category, picture in rows:
        articles[title] = {
            "wiki_name": title,
            "wiki_category": category,
            "wiki_theme": category,
            "wiki_text": summary,
            "wiki_picture": picture,}
    return articles



@app.route("/", methods=["GET", "POST"])
def home():
    search_text = "..."
    game_state = session.get("game_state", "not_started")
    articles = example_dict()

    invalid_guess = False
    prev_guess = False
    image_blur = "blurred"
    wiki_picture = ""

    guess_name = ""
    guess_category = ""
    guess_theme = ""

    guess_color = "white"
    category_color = "white"
    theme_color = "white"

    #defaults for when the game has not started yet
    wiki_page = session.get("wiki_page")
    wiki_name = ""
    wiki_text = "..."
    wiki_category = ""
    wiki_theme = ""
    wiki_name_blurred = ""
    #restore current wiki page from session
    if wiki_page in articles:
        wiki_name = articles[wiki_page]["wiki_name"]
        wiki_text = articles[wiki_page]["wiki_text"]
        wiki_category = articles[wiki_page]["wiki_category"]
        wiki_theme = articles[wiki_page]["wiki_theme"]
        wiki_name_blurred = re.sub(r"\S", "_", wiki_name)
        wiki_picture = articles[wiki_page]["wiki_picture"]

    if request.method == "POST":
        action = request.form.get("action")

        if action == "start":
            wiki_page = random.choice(list(articles.keys()))

            session["wiki_page"] = wiki_page
            session["image_revealed"] = False
            session["game_state"] = "playing"
            session["guess_count"] = 0
            session["guesses"] = []

            game_state = "playing"

            wiki_name = articles[wiki_page]["wiki_name"]
            wiki_text = articles[wiki_page]["wiki_text"]
            wiki_category = articles[wiki_page]["wiki_category"]
            wiki_theme = articles[wiki_page]["wiki_theme"]
            wiki_picture = articles[wiki_page]["wiki_picture"]
            wiki_name_blurred = re.sub(r"\S", "_", wiki_name)

        elif action == "reset":
            session.clear()
            session["game_state"] = "not_started"
            session["image_revealed"] = False
            session["guesses"] = []
            session["wiki_page"] = None

            game_state = "not_started"
            search_text = "..."

            wiki_page = None
            wiki_name = ""
            wiki_text = "..."
            wiki_category = ""
            wiki_theme = ""
            wiki_name_blurred = ""

            guess_name = ""
            guess_category = ""
            guess_theme = ""

            guess_color = "white"
            category_color = "white"
            theme_color = "white"
        
        elif action == "reveal_image":
            session["image_revealed"] = True

        elif action == "guess" and session.get("game_state") == "playing":
            search_text = request.form.get("search", "").strip()
            guesses = session.get("guesses", [])

            already_guessed = any(
                guess["name"] == search_text for guess in guesses
            )

            if search_text not in articles:
                invalid_guess = True

            elif already_guessed:
                prev_guess = True

            else:
                guess_name = articles[search_text]["wiki_name"]
                guess_category = articles[search_text]["wiki_category"]
                guess_theme = articles[search_text]["wiki_theme"]

                if search_text == wiki_name:
                    guess_color = "green"
                    wiki_name_blurred = wiki_name
                    session["game_state"] = "finished"
                    game_state = "finished"
                else:
                    guess_color = "red"

                if guess_category == wiki_category:
                    category_color = "green"
                else:
                    category_color = "red"

                if guess_theme == wiki_theme:
                    theme_color = "green"
                else:
                    theme_color = "red"

                guesses.append({
                    "name": guess_name,
                    "category": guess_category,
                    "theme": guess_theme,
                    "guess_color": guess_color,
                    "category_color": category_color,
                    "theme_color": theme_color
                })

                session["guesses"] = guesses
                session["guess_count"] = len(guesses)

    guesses = session.get("guesses", [])
    guess_count = len(guesses)

    if guesses:
        latest_guess = guesses[-1]

        guess_name = latest_guess["name"]
        guess_category = latest_guess["category"]
        guess_theme = latest_guess["theme"]

        guess_color = latest_guess["guess_color"]
        category_color = latest_guess["category_color"]
        theme_color = latest_guess["theme_color"]

        if guess_name == wiki_name:
            wiki_name_blurred = wiki_name

        if session.get("image_revealed", False):
            image_blur = ""
        else:
            image_blur = "blurred"

    return render_template(
        "index.html",
        wiki_name=wiki_name,
        search_text=search_text,
        guess_name=guess_name,
        wiki_text=wiki_text,
        wiki_category=wiki_category,
        wiki_theme=wiki_theme,
        guess_color=guess_color,
        category_color=category_color,
        theme_color=theme_color,
        guess_theme=guess_theme,
        guess_category=guess_category,
        autocomplete_options=articles.keys(),
        guesses=guesses,
        guess_count=guess_count,
        wiki_name_blurred=wiki_name_blurred,
        invalid_guess=invalid_guess,
        prev_guess=prev_guess,
        game_state=game_state,
        wiki_page=wiki_page,
        wiki_picture=wiki_picture,
        image_blur=image_blur,
        image_revealed=session.get("image_revealed", False)
    )


# runs the shit
if __name__ == "__main__":
    app.run(debug=True)