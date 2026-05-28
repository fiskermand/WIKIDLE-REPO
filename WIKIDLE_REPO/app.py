from flask import Flask, render_template, request, session
import re, random

# TODO:
# hints (billede og bogstav?)
# wikiapi til sql db + regex til at fjerne navn/whatever
# implementer sql delen
# automatiser valg af wikiside
# login / leaderboard

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
        "wiki_picture": "images/Michael_Jackson_1983.jpg.webp"
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
        "wiki_picture": "images/President_Donald_J._Trump.jpg.webp"
    },

    "Mount Everest": {
        "wiki_name": "Mount Everest",
        "wiki_category": "Earth",
        "wiki_theme": "Mountain",
        "wiki_text": (
            "...(known locally as Sagarmāthā[a] in Nepal and Qomolangma[b] in Tibet Autonomous Region of China) "
            "is the highest mountain on Earth above sea level. It lies in the Mahalangur Himal sub-range of the Himalayas and "
            "marks part of the China–Nepal border at its summit.[4] Its height was most recently measured in 2020 through a joint "
            "survey by Nepalese and Chinese authorities as 8,848.86 m (29,031 ft 8+1⁄2 in)..."
        ),
        "wiki_picture": "images/Mt._Everest.jpg"
    },

    "Korean War": {
        "wiki_name": "Korean War",
        "wiki_category": "Civilization",
        "wiki_theme": "Wars",
        "wiki_text": (
            "...(25 June 1950 – 27 July 1953) was an armed conflict fought on the Korean "
            "Peninsula between North Korea (Democratic People's Republic of Korea; DPRK) and South Korea"
            " (Republic of Korea; ROK) and their allies. North Korea was supported by China and the Soviet Union, "
            "while South Korea was supported by the United Nations led by the United States under the auspices of the United Nations Command (UNC)."
        ),
        "wiki_picture": "images/Korean_War_Chosin.jpg"
    },
}


@app.route("/", methods=["GET", "POST"])
def home():
    search_text = "..."
    game_state = session.get("game_state", "not_started")

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
    if wiki_page in example_dict:
        wiki_name = example_dict[wiki_page]["wiki_name"]
        wiki_text = example_dict[wiki_page]["wiki_text"]
        wiki_category = example_dict[wiki_page]["wiki_category"]
        wiki_theme = example_dict[wiki_page]["wiki_theme"]
        wiki_name_blurred = re.sub(r"\S", "_", wiki_name)
        wiki_picture = example_dict[wiki_page]["wiki_picture"]

    if request.method == "POST":
        action = request.form.get("action")

        if action == "start":
            wiki_page = random.choice(list(example_dict.keys()))

            session["wiki_page"] = wiki_page
            session["image_revealed"] = False
            session["game_state"] = "playing"
            session["guess_count"] = 0
            session["guesses"] = []

            game_state = "playing"

            wiki_name = example_dict[wiki_page]["wiki_name"]
            wiki_text = example_dict[wiki_page]["wiki_text"]
            wiki_category = example_dict[wiki_page]["wiki_category"]
            wiki_theme = example_dict[wiki_page]["wiki_theme"]
            wiki_picture = example_dict[wiki_page]["wiki_picture"]
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

            if search_text not in example_dict:
                invalid_guess = True

            elif already_guessed:
                prev_guess = True

            else:
                guess_name = example_dict[search_text]["wiki_name"]
                guess_category = example_dict[search_text]["wiki_category"]
                guess_theme = example_dict[search_text]["wiki_theme"]

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
        autocomplete_options=example_dict.keys(),
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