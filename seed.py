"""Load data into database."""

from model import Marker, connect_to_db, db
from server import app
import csv

#--------------------------------------------------------#


def load_events(file):
    """Load events from dataset into Marker database."""

    with open(file) as f:
        # next(f)  # skip header row

        # for i, row in enumerate(f):
            # row = row.rstrip()
            # print row.split("\t")

            # title, description, date, time, venue/name, neighborhood, city, address, latitude, longitude, cost, img_url, event_url, category, marker_type, marker_symbol = row.split("\t")

        reader = csv.reader(f)
        for i, row in enumerate(reader):

            marker = Marker(title=row[0],
                            address=row[7],
                            latitude=row[8],
                            longitude=row[9],
                            date=row[2],
                            time=row[3],
                            name=row[4],
                            neighborhood=row[5],
                            city=row[6],
                            description=row[1],
                            cost=row[10],
                            img_url=row[11],
                            event_url=row[12],
                            category=row[13],
                            marker_type=row[14],
                            marker_symbol=row[15],
                            marker_color=row[16])

            db.session.add(marker)

            if i % 10 == 0:
                print i

        db.session.commit()


# def load_hiddengems():
#     """Load hiddengems from dataset into Marker database."""

#     with open('data/hiddengems.csv') as f:
#         next(f)  # skip header row

#         for i, row in enumerate(f):
#             row = row.rstrip()
#             name, address, description, neighborhood, city, category, latitude, longitude = row.split(",")

#             marker = Marker(name=name,
#                             address=address,
#                             latitude=latitude,
#                             longitude=longitude,
#                             # date=date,
#                             # time=time,
#                             # venue=venue,
#                             neighborhood=neighborhood,
#                             city=city,
#                             description=description,
#                             # cost=cost,
#                             # img_url=img_url,
#                             # event_url=event_url,
#                             marker_type=category)

#             db.session.add(hiddengem)

#             if i % 10 == 0:
#                 print i

#         db.session.commit()

#--------------------------------------------------------#

if __name__ == '__main__':
    connect_to_db(app)
    db.create_all()

    load_events('data/markers-20160217.csv')
    # load_hiddengems()
