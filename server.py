"""Weekend Wanderlust - Interactive Map & Weekend Trip Planner."""

from jinja2 import StrictUndefined
from flask import Flask, render_template, jsonify, flash, redirect, request, session
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


@app.route('/events.geojson')
def events_json():
    """Geojson from database for event layer."""

    e_geojson = {
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
                        "category": marker.category,
                        "marker-type": marker.marker_type,
                        "marker-symbol": marker.marker_symbol,
                        "marker-color": marker.marker_color
                        },
                    "geometry": {
                        "coordinates": [
                            marker.longitude,
                            marker.latitude],
                        "type": "Point"
                    },
                    "id": marker.marker_id
                    }
                for marker in Marker.query.filter(Marker.marker_type == 'event').all()
                ]
            }

    return jsonify(e_geojson)



@app.route('/hiddengems.geojson')
def hiddengems_json():
    """Geojson from database for hiddengem layer."""

    h_geojson = {
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
                        "category": marker.category,
                        "marker-type": marker.marker_type,
                        "marker-symbol": marker.marker_symbol,
                        "marker-color": marker.marker_color
                        },
                    "geometry": {
                        "coordinates": [
                            marker.longitude,
                            marker.latitude],
                        "type": "Point"
                    },
                    "id": marker.marker_id
                    }
                for marker in Marker.query.filter(Marker.marker_type == 'hiddengem').all()
                ]
            }

    return jsonify(h_geojson)


@app.route('/add_waypoint', methods=['GET'])
def add_waypoint():
    """Add waypoint to session."""

    waypoint_id = request.args.get("marker_id")
    print "this is waypoint id:", waypoint_id

    if 'waypoints' in session:
        if waypoint_id in session['waypoints']:
            return "You have already selected it!"
        else:
            session['waypoints'].append(waypoint_id)
            print session
            return "Waypoint added to trip!"
    else:
        session['waypoints'] = [waypoint_id]
        print session
        return "Waypoint added to trip!"

    print "session['waypoints']:", session['waypoints']

    # flash("Added to trip!")


@app.route('/get_waypoint_list')
def get_waypoint_list_from_session():
    """Get waypoint id list from session, return info from database."""

    waypoint_list = session['waypoints']
    print waypoint_list
    waypoint_name_list = []

    for i in waypoint_list:
        # print i
        marker = Marker.query.filter_by(marker_id=int(i)).one()
        name = marker.name
        waypoint_name_list.append(name)

    return jsonify(waypoint_name_list)


# @app.route('/check_duplicate')
# def check_duplicate():


@app.route('/save_trip')
def save_trip():
    """Clear session."""

    # commit waypoint sequence to database before clean

    session['waypoints'] = []
    print "updated session:", session['waypoints']

    return "Trip saved!"




# @app.route('/trip/<int:trip_id') # parallax scrolling helps story-telling


#---------------------------------#

if __name__ == "__main__":

    app.debug = True

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run()
