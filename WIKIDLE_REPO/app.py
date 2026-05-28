from flask import Flask, render_template, request, session
import re

# TODO:
# hints (billede og bogstav?)
# wikiapi til sql db + regex til at fjerne navn/whatever
# implementer sql delen
# E/R diagram
# start/slut skærm
# automatiser valg af wikiside

app = Flask(__name__)
app.secret_key = "dev-secret-key"

# EKSEMPEL
example_dict = {
    "Michael Jackson": {
        "wiki_name": "Michael Jackson",
        "wiki_category": "People",
        "wiki_theme": "Singers",
        "wiki_text": (
            "...(August 29, 1958 – June 25, 2009) was an American singer, "
            "songwriter, dancer, and philanthropist. Dubbed the King of Pop, "
            "he is widely regarded as one of the most culturally significant "
            "figures of the 20th century. His musical achievements broke "
            "American racial barriers and made him a dominant figure worldwide..."
        ),
    },

    "Donald Trump": {
        "wiki_name": "Donald Trump",
        "wiki_category": "People",
        "wiki_theme": "Politicians",
        "wiki_text": (
            "...(born June 14, 1946) is an American politician, media personality, "
            "and businessman who is the 47th president of the United States. "
            "A member of the Republican Party, he served as the 45th president "
            "from 2017 to 2021..."
        ),
    },
}


@app.route("/", methods=["GET", "POST"])
def home():
    search_text = "..."

    # EKSEMPEL, SKAL AUTOMATISERES:
    wiki_name = example_dict["Michael Jackson"]["wiki_name"]
    wiki_text = example_dict["Michael Jackson"]["wiki_text"]
    wiki_category = example_dict["Michael Jackson"]["wiki_category"]
    wiki_theme = example_dict["Michael Jackson"]["wiki_theme"]

    wiki_name_blurred = re.sub(r"\S", "_", wiki_name)

    guess_name = ""
    guess_category = ""
    guess_theme = ""

    guess_color = "white"
    category_color = "white"
    theme_color = "white"

    if request.method == "POST":
        action = request.form.get("action")

        if action == "reset":
            session["guess_count"] = 0
            session["guesses"] = []

            search_text = "..."
            guess_name = ""
            guess_category = ""
            guess_theme = ""
            wiki_name_blurred = re.sub(r"\S", "_", wiki_name)

            guess_color = "white"
            category_color = "white"
            theme_color = "white"

        else:
            search_text = request.form.get("search", "").strip()
            guesses = session.get("guesses", [])

            already_guessed = any(
                guess["name"] == search_text for guess in guesses
            )

            # Only accept the guess if:
            # 1. it exists in example_dict
            # 2. it has not already been guessed
            if search_text in example_dict and not already_guessed:
                guess_name = example_dict[search_text]["wiki_name"]
                guess_category = example_dict[search_text]["wiki_category"]
                guess_theme = example_dict[search_text]["wiki_theme"]

                if search_text == wiki_name:
                    guess_color = "green"
                    wiki_name_blurred = wiki_name
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

    # Restore latest valid guess, so invalid or duplicate guesses do not change display.
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
        autocomplete_options=example_dict.keys(),
        guesses=guesses,
        guess_count=guess_count,
        wiki_name_blurred=wiki_name_blurred
    )


# runs the shit
if __name__ == "__main__":
    app.run(debug=True)