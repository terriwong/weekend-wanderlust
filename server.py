"""WeekendWanderlust Map."""

from jinja2 import StrictUndefined

from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "exploooooooooore"

# Use StrictUndefined to raise an error when there is undefined variable in Jinja2.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


if __name__ == "__main__":

    app.debug = True

    # connect_to_db(app)

    DebugToolbarExtension(app)

    app.run()
