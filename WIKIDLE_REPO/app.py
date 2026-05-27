from flask import Flask, render_template, request

#TODO:
#implementer hints (billeder?)
#regex til at fjerne navn/whatever
#wikiapi til sql db 
#implementer sql delen
#E/R diagram

app = Flask(__name__)

#bare lige for eksempel indtil vi har sql up-n-runnin'
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
    wiki_name = example_dict["Michael Jackson"]["wiki_name"]
    wiki_text = example_dict["Michael Jackson"]["wiki_text"]
    wiki_category = example_dict["Michael Jackson"]["wiki_category"]
    wiki_theme = example_dict["Michael Jackson"]["wiki_theme"]

    guess_category = ""
    guess_theme = ""

    guess_color = "white"
    category_color = "white"
    theme_color = "white"

    if request.method == "POST":
        #get text from search box
        search_text = request.form.get("search")

        #try to make the guess category = "wiki_category" of the search box entry
        try:
            guess_category = example_dict[search_text]["wiki_category"]
        except:
            guess_category = ""
        
        #try to make the guess theme = "wiki_theme" of the search box entry
        try:
            guess_theme = example_dict[search_text]["wiki_theme"]
        except:
            guess_theme = ""

        #colors of boxes
        if search_text == wiki_name:
            guess_color = "green"
        elif search_text != wiki_name:
            guess_color = "red"

        if guess_category == wiki_category:
            category_color = "green"
        elif guess_category != wiki_category:
            category_color = "red"

        if guess_theme == wiki_theme:
            theme_color = "green"
        elif guess_theme != wiki_theme:
            theme_color = "red"

    #compile allat
    return render_template("index.html", 
                           wiki_name=wiki_name,
                           search_text=search_text,
                           wiki_text=wiki_text,
                           wiki_category=wiki_category,
                           wiki_theme=wiki_theme,
                           guess_color=guess_color,
                           category_color=category_color,
                           theme_color=theme_color,
                           guess_theme=guess_theme,
                           guess_category=guess_category,
                           autocomplete_options=example_dict.keys())

#runs the shit
if __name__ == "__main__":
    app.run(debug=True)