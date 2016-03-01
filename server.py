"""Weekend Wanderlust - Hiddengems Map & Weekend Trip Planner for Bay Area explorers."""

from jinja2 import StrictUndefined
from flask import Flask, render_template, jsonify, request, session
from flask_debugtoolbar import DebugToolbarExtension
import os
import json
import requests
from polyline.codec import PolylineCodec
from datetime import date, datetime

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

    today = date.today()
    # use date 0225 for testing purpose
    today = today.replace(month=2, day=25)

    e_geojson = {
                "type": "FeatureCollection",
                "features": [
                    {
                    "type": "Feature",
                    "properties": {
                        "title": marker.title,
                        "date": marker.date,
                        "date-tier": marker.date_tier,
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
                for marker in Marker.query.filter(Marker.marker_type == 'event', Marker.datetime >= today).all()
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
        if len(session['waypoints']) < 12:
            if waypoint_id in session['waypoints']:
                return "You have already selected it!"
            else:
                session['waypoints'].append(waypoint_id)
                print session
                return "Waypoint added to trip!"
        else:
            return "You can't select more than 12 waypoints!"
    else:
        session['waypoints'] = [waypoint_id]
        print session
        return "Waypoint added to trip!"

    print "session['waypoints']:", session['waypoints']

    # flash("Added to trip!")


@app.route('/update_waypoint_list')
def update_waypoint_list():
    """Get newly added waypoint id, return name from database.
    ******Fix*******"""

    print "current session:", session['waypoints']
    waypoint_list = session['waypoints']
    new_waypoint_id = waypoint_list[-1]
    marker = Marker.query.filter_by(marker_id=new_waypoint_id).first()
    waypoint_name = marker.name

    return waypoint_name


@app.route('/get_profile')
def get_profile():
    """Get profile, store new or update in session."""

    profile = request.args.get("profile")

    session['profile'] = profile
    print "profile in session: ", session['profile']

    return profile


@app.route('/get_route')
def get_route():
    """Use travel profile and waypoints in session, get route's line points."""

    profile = "mapbox." + str(session['profile'])
    waypoints_id_list = session['waypoints']
    latlngs = ""

    for i in waypoints_id_list:
        marker = Marker.query.filter_by(marker_id=i).one()
        lon = marker.longitude
        lat = marker.latitude
        latlngs += (lon + "," + lat + ";")

    waypoints = latlngs[:-1]

    access_token = os.environ['MAPBOX_ACCESS_TOKEN']

    url = "https://api.mapbox.com/v4/directions/" + profile + "/" + waypoints + ".json?alternatives=false&instructions=text&geometry=geojson&steps=false&&access_token=" + access_token

    r = requests.get(url)
    r = r.json()
    route = r['routes'][0]
    print "route", route

    return jsonify(route)


    # https://api.mapbox.com/v4/directions/{profile}/{waypoints}.json?access_token=MAPBOX_ACCESS_TOKEN
    # https://api.mapbox.com/v4/directions/cycling/-122.4114577,37.759332;-122.4026674,37.7706699;-122.4088275,37.7713244.json?alternatives=false&instructions=html&geometry=polyline&steps=false$access_token=pk.eyJ1IjoidGVycml3bGVlIiwiYSI6ImNpazZlaThsajAwcXdpMm0ycHUyZjhiYjkifQ.zvJK8nAc3HpNOtCAMh5QlQ
    # https://api.mapbox.com/v4/directions/mapbox.driving/-122.42,37.78;-77.03,38.91.json?alternatives=false&instructions=html&geometry=polyline&steps=false&&access_token=pk.eyJ1IjoidGVycml3bGVlIiwiYSI6ImNpazZlaThsajAwcXdpMm0ycHUyZjhiYjkifQ.zvJK8nAc3HpNOtCAMh5QlQ


@app.route('/get_route_polyline')
def get_route_polyline():
    """Use travel profile and waypoints in session, get route's polyline geometry."""

    profile = "mapbox." + str(session['profile'])
    waypoints_id_list = session['waypoints']
    latlngs = ""

    for i in waypoints_id_list:
        marker = Marker.query.filter_by(marker_id=i).one()
        lon = marker.longitude
        lat = marker.latitude
        latlngs += (lon + "," + lat + ";")

    waypoints = latlngs[:-1]

    access_token = os.environ['MAPBOX_ACCESS_TOKEN']

    url = "https://api.mapbox.com/v4/directions/" + profile + "/" + waypoints + ".json?alternatives=false&instructions=text&geometry=polyline&steps=true&&access_token=" + access_token

    r = requests.get(url)
    r = r.json()
    geometry = r['routes'][0]['geometry']
    latlngs = PolylineCodec().decode(geometry)
    geometry = {'geometry': latlngs}
    print geometry

    return jsonify(geometry)


@app.route('/start_over')
def save_trip():
    """Clear session."""

    # commit waypoint sequence to database before clean

    session['waypoints'] = []
    session['profile'] = ""
    print "updated session:", session

    return "Session cleared!"


@app.route('/hi_explorer')
def hi_explorer():
    """Testing page to greet explorers."""

    return render_template("greet.html")


# @app.route('/trip/<int:trip_id') # parallax scrolling helps story-telling


@app.route('/more_info_from_foursquare')
def more_info_from_foursquare(marker_id):
    """Hit Foursquare venue api for more info about hiddengem's venue."""

    CLIENT_ID = os.environ['FOURSQUARE_CLIENT_ID']
    CLIENT_SECRET = os.environ['FOURSQUARE_CLIENT_SECRET']

    # query marker info from database and get venue's foursquare id
    marker = Marker.query.filter_by(marker_id=marker_id).first()
    VENUE_ID = marker.foursquare_id

    # get date string for request url
    today = datetime.utcnow()
    date_str = today.strftime("%Y%m%d")

    # construct request url
    url = "https://api.foursquare.com/v2/venues/" + VENUE_ID + "?client_id=" + CLIENT_ID + "&client_secret=" + CLIENT_SECRET + "&v=" + date_str
    response = requests.get(url)

    # try another way to load json data
    json_data = json.loads(response.text)

    # get first 3 photo objects
    photos = json_data['response']['venue']['photos']['groups'][0]['items'][:3]

    # extract just the photo url and store in a list
    photo_urls = []
    for photo in photos:
        url = photo['prefix'] + "width300" + photo['suffix']
        photo_urls.append(url)

    # get tips
    tips = json_data['response']['venue']['tips']['groups'][0]['items'][:3]
    tips_list = []
    for item in tips:
        tip = {}
        tip['text'] = item['text']
        tip['fname'] = item['user']['firstName']
        tip['lname'] = item['user']['lastName']

        tips_list.append(tip)

    # construct data needed

    data = {
        "photos": photo_urls,
        "tips": tips_list
    }

    return jsonify(data)


#---------------------------------#

if __name__ == "__main__":

    app.debug = True

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run()
