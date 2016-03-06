"""Weekend Wanderlust - Hiddengems Map & Weekend Trip Planner for Bay Area explorers."""

from jinja2 import StrictUndefined
from flask import Flask, render_template, jsonify, request, session
from flask_debugtoolbar import DebugToolbarExtension
import os
import json
import requests
from polyline.codec import PolylineCodec
from datetime import date, datetime
import geocoder
import urllib
from twilio.rest import TwilioRestClient

from model import connect_to_db, Marker

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "exploooooooooorer"

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
    """First trial way to send data for map: 
       send static geojson file for map to download."""

    return app.send_static_file("features-20160210.geojson")


@app.route('/events.geojson')
def events_json():
    """Second and now-in-use way to send data for map:
       construct Geojson from database.
       This is for event layer."""

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
        if len(session['waypoints']) < 6:
            if waypoint_id in session['waypoints']:
                return "You've already selected it!"
            else:
                session['waypoints'].append(waypoint_id)
                return "Waypoint added!"
        else:
            return "Sorry, you can't select more than 6 waypoints."
    else:
        session['waypoints'] = [waypoint_id]
        return "Waypoint added!"

    print "session['waypoints']:", session['waypoints']


@app.route('/get_new_waypoint_name')
def get_new_waypoint_name():
    """Given newly added waypoint id, return name from database."""

    waypoint_list = session['waypoints']
    new_waypoint_id = waypoint_list[-1]
    marker = Marker.query.filter_by(marker_id=new_waypoint_id).first()
    waypoint_name = marker.name

    return waypoint_name


@app.route('/get_travel_profile')
def get_travel_profile():
    """Get travel profile (walking/cycling/driving), 
       store new or update in session."""

    profile = request.args.get("profile")

    session['profile'] = profile
    print "profile in session: ", session['profile']

    return profile


@app.route('/get_route')
def get_route_geojson():
    """Use travel profile and waypoints in session, 
       get route's line points in geojson format,
       using Mapbox directions api."""

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


@app.route('/start_over')
def start_over():
    """Clear waypoint list and profile in session, return message."""

    session['waypoints'] = []
    session['profile'] = ""
    session['trip_note'] = []
    print "updated session:", session

    return "Trip board cleared!"


@app.route('/hi_explorer')
def hi_explorer():
    """Testing cover page to greet explorers."""

    return render_template("greet.html")


# @app.route('/trip/<int:trip_id') # parallax scrolling helps story-telling


@app.route('/more_info_from_foursquare')
def more_info_from_foursquare():
    """Hit Foursquare venue api for more info about hiddengem's venue."""

    marker_id = request.args.get('marker_id')

    CLIENT_ID = os.environ['FOURSQUARE_CLIENT_ID']
    CLIENT_SECRET = os.environ['FOURSQUARE_CLIENT_SECRET']

    # query marker info from database and get venue's foursquare id
    marker = Marker.query.filter_by(marker_id=marker_id).first()
    VENUE_ID = marker.foursquare_id
    name = marker.name
    address = marker.address

    # get date string for request url
    today = datetime.utcnow()
    date_str = today.strftime("%Y%m%d")

    # construct request url
    url = "https://api.foursquare.com/v2/venues/" + VENUE_ID + "?client_id=" + CLIENT_ID + "&client_secret=" + CLIENT_SECRET + "&v=" + date_str
    response = requests.get(url)

    # try another way to load json data
    json_data = json.loads(response.text)

    # get first 3 photo objects
    photos = json_data['response']['venue']['photos']['groups'][0]['items'][:6]

    # extract just the photo url and store in a list
    photo_urls = []
    for photo in photos:
        url = photo['prefix'] + "width300" + photo['suffix']
        photo_urls.append(url)

    # get tips
    tips = json_data['response']['venue']['tips']['groups'][0]['items'][:6]
    tips_list = []
    for item in tips:
        tip = item['text']
        tips_list.append(tip)

    # get hours
    if "hours" in json_data['response']['venue']:
        hours_info = json_data['response']['venue']['hours']['timeframes']
    else:
        hours_info = []

    # get popular hours
    popular_hours_info = json_data['response']['venue']['popular']['timeframes']

    # construct data needed
    data = {
        "marker_id": marker_id,
        "name": name,
        "photos": photo_urls,
        "tips": tips_list,
        "hours": hours_info,
        "popular_hours": popular_hours_info,
        "address": address
    }

    return jsonify(data)


@app.route('/geocode_address')
def geocode_address_for_coordinates():
    """Given address, hit Google Geocoding API, get geojson coordinates."""

    address = request.args.get("address")

    address_str = urllib.unquote_plus(str(address))  # format string from url
    r = geocoder.google(address_str)
    if r.ok:  # check if api request is ok
        coordinates = r.geojson['geometry']['coordinates']  # [lng, lat]
        data = {
                "status": "ok",
                "coordinates": coordinates}
    else:
        data = {"status": "no found"}

    return jsonify(data)


@app.route('/add_trip_note', methods=['POST'])
def add_trip_note_to_session():
    """Add trip note to session."""

    marker_id = request.form["marker_id"]
    marker = Marker.query.filter_by(marker_id=marker_id).one()
    address = marker.address
    name = request.form["name"]
    selected_day = request.form["selected_day"]
    selected_hour = request.form["selected_hour"]

    info = (marker_id, name, address, selected_day, selected_hour)

    if "trip_note" in session.keys():
        session['trip_note'].append(info)
    else:
        session['trip_note'] = []
        session['trip_note'].append(info)

    if marker_id not in session['waypoints']:
        session['waypoints'].append(marker_id)

    get_new_waypoint_name()

    print "session['trip_note']: ", session['trip_note']

    return "Trip noted added!"


@app.route('/update_trip_note')
def update_trip_note_to_board():
    """Add trip note details to board."""

    print "session['waypoints']: ", session['waypoints']
    print "session['trip_note']: ", session['trip_note']
    data = []

    for marker_id in session['waypoints']:
        info = {
            "name": session['trip_note'][marker_id][0],
            "selectedDay": session['trip_note'][marker_id][1],
            "selectedHour": session['trip_note'][marker_id][2]
        }

        data.append(info)

        data = {data}

    return jsonify(data)


@app.route('/send_sms', methods=['POST'])
def send_sms():
    """Construct sms message with trip notes, send via Twilio."""

    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = TwilioRestClient(account_sid, auth_token)

    to_number = request.form['receiver_number']
    to_number = "+1" + str(to_number)
    print "to_number is: ", to_number

    from_number = "+19163183606"
    print "from_number is: ", from_number

    text = "Hi Explorer! Below is the trip note from Weekend Wanderlust, happy exploring this weekend!>>>" + "\n"

    for note in session['trip_note']:
        marker_id = note[0].encode('ascii', 'ignore')
        marker = Marker.query.filter_by(marker_id=marker_id).one()
        name = marker.name
        address = marker.address
        selected_day = note[3].replace(u'\u2013', u'-').encode('ascii', 'ignore')
        selected_hour = note[4].replace(u'\u2013', u'-').encode('ascii', 'ignore')
        # time = text.replace(u'\u2019', u'\'').replace(u'\u2013', u'-').encode('ascii', 'ignore')

        text = text + name + " \n " + "|" + address + " \n " + "|" + selected_day + " " + selected_hour + "\n"

    # text = text.replace(u'\u2019', u'\'').replace(u'\u2013', u'-').encode('ascii', 'ignore')

    print "text is: ", text

    # return text
    message = client.messages.create(to=to_number, from_=from_number, body=text)

    return "Message sent!"



#---------------------------------#

if __name__ == "__main__":

    # app.debug = True

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run()
