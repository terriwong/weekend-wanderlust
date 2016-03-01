"""WWM DATABASE: Data model for events, hiddengems, trips."""

from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.dialects.postgresql import ARRAY

db = SQLAlchemy()

#------------------------------------------------#


class Marker(db.Model):
    """Map points for events and hiddengems."""

    __tablename__ = "markers"

    marker_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    title = db.Column(db.String(255), nullable=True)  # hiddengem might have no title
    address = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.String(64), nullable=False)
    longitude = db.Column(db.String(64), nullable=False)
    date = db.Column(db.String(64), nullable=True)
    datetime = db.Column(db.DateTime, nullable=True)  # shop has no date
    date_tier = db.Column(db.String(20), nullable=True)  # hiddengem has not date_tier
    time = db.Column(db.String(64), nullable=True)
    neighborhood = db.Column(db.String(64), nullable=True)  # can be no neighborhood
    city = db.Column(db.String(64), nullable=True)
    description = db.Column(db.String(1000), nullable=True)
    cost = db.Column(db.String(64), nullable=True)
    # cost_tier = db.Column(db.String(5), nullable=True)  # for restaurants: number of dollar signs
    img_url = db.Column(db.String(255), nullable=True)
    event_url = db.Column(db.String(255), nullable=True)
    category = db.Column(db.String(64), nullable=False)
    marker_type = db.Column(db.String(64), nullable=False)
    marker_symbol = db.Column(db.String(64), nullable=True)
    marker_color = db.Column(db.String(64))
    foursquare_id = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        """Clear representation of marker."""

        return "<Marker marker_id=%s name=%s" % (self.marker_id, self.name)

    # restaurant: reservation


# class Trip(db.Model):
#     """table for trips."""

#     __tablename__ = "trips"

#     trip_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     name = db.Column(db.String(64), nullable=False)
#     date = db.Column(db.String(64), nullable=False)
#     waypoints = db.Column(ARRAY(db.Integer), db.ForeignKey('markers.marker_id'), nullable=False)  # using array
#     profile = db.Column(db.String(15), nullable=False)  # driving, walking, cycling
#     start_time = db.Column(db.String, nullable=True)

#     waypoint = db.relationship('Marker', backref='trips')

#     def __repr__(self):
#         """representation of the trip."""

#         return "<Trip trip_id=%s name=%s date=%s" % (self.trip_id, self.name, self.date)


#------------------------------------------------#


def connect_to_db(app):
    """Connect the database to Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///wwm'  # weekend wanderlust map
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    print "Connected to DB."
