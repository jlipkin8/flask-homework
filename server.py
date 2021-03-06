from flask import Flask, redirect, request, render_template, session 
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined


app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Getting our list of MOST LOVED MELONS
MOST_LOVED_MELONS = {
    'cren': {
        'img': 'http://www.rareseeds.com/assets/1/14/DimRegular/crenshaw.jpg',
        'name': 'Crenshaw',
        'num_loves': 584,
    },
    'jubi': {
        'img': 'http://www.rareseeds.com/assets/1/14/DimThumbnail/Jubilee-Watermelon-web.jpg',
        'name': 'Jubilee Watermelon',
        'num_loves': 601,
    },
    'sugb': {
        'img': 'http://www.rareseeds.com/assets/1/14/DimThumbnail/Sugar-Baby-Watermelon-web.jpg',
        'name': 'Sugar Baby Watermelon',
        'num_loves': 587,
    },
    'texb': {
        'img': 'http://www.rareseeds.com/assets/1/14/DimThumbnail/Texas-Golden-2-Watermelon-web.jpg',
        'name': 'Texas Golden Watermelon',
        'num_loves': 598,
    },
}

# YOUR ROUTES GO HERE
@app.route("/")
def show_homepage(): 
    """Displays homepage and asks for user's name""" 

    if 'user_name' not in session: 
        print "user_name is not stored"
        return render_template("homepage.html")
    else: 
        return redirect("/top-melons")


@app.route("/top-melons")
def show_top_melons(): 
    """Displays page of top melons""" 

    if 'user_name' not in session: 
        print "redirect to homepage"
        return redirect("/")
    else: 
        return render_template("top-melons.html", melons=MOST_LOVED_MELONS)
        

@app.route("/get-name")
def get_user_name(): 
    """Adds user's name to the session"""

    user = request.args.get("firstname")
    if user: 
        session['user_name'] = user
        
    return redirect("/top-melons")


@app.route("/love-melon", methods=["POST"])
def increase_num_loves(): 
    """Increases the num_loves of a melon""" 

    chosen_melon = request.form.get("melonvote")
    MOST_LOVED_MELONS[chosen_melon]['num_loves'] += 1

    return render_template("thank-you.html")



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
