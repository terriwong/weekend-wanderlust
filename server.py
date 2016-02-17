"""Weekend Wanderlust - Interactive Map & Weekend Trip Planner."""

from jinja2 import StrictUndefined
from flask import Flask, render_template, jsonify, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, Marker

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "exploooooooooore"

# Use StrictUndefined to raise an error when there is undefined variable in Jinja2.
app.jinja_env.undefined = StrictUndefined

#-------------------------------------------------------------------#


@app.route('/')
def index():
    """Show homepage."""

    return render_template("homepage.html")


@app.route('/weekend-wanderlust')
def map():
    """Show map."""

    return render_template("map.html")


@app.route('/features-20160210.geojson')
def send_features():
    """send static file for map to download."""

    return app.send_static_file("features-20160210.geojson")


# file contains all markers geojsonj
@app.route('/events0215.geojson')
def marker_info():
    """Testing: Geojson marker information from database."""

    geojson = {
                "type": "FeatureCollection",
                "features": [
                    {
                    "type": "Feature",
                    "properties": {
                        "title": marker.title,
                        "date": marker.date,
                        "time": marker.time,
                        "name": marker.name,
                        "address": marker.address,
                        "cost": marker.cost,
                        "img_url": marker.img_url,
                        "event_url": marker.event_url,
                        "description": marker.description,
                        "marker-type": marker.marker_type,
                        "marker-symbol": marker.marker_symbol,
                        "marker-color": "#33cccc"
                        },
                    "geometry": {
                        "coordinates": [
                            marker.longitude,
                            marker.latitude],
                        "type": "Point"
                    },
                    "id": marker.marker_id
                    }
                for marker in Marker.query.all()
                ]
            }

    return jsonify(geojson)


# @app.route('/trip/<int:trip_id') # parallax scrolling helps story-telling

@app.route('/add_marker_to_trip', methods=['GET', 'POST'])
def add_marker_to_trip():

    flash("Added to trip!")

    return redirect("/weekend-wanderlust")

#---------------------------------#

if __name__ == "__main__":

    app.debug = True

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run()
