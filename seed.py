"""Load data into database."""

from model import Marker, connect_to_db, db
from server import app
import csv
from datetime import datetime

#--------------------------------------------------------#


def load_markers(file):
    """Load markers from dataset into Marker database."""

    with open(file) as csvfile:
        # next(f)  # skip header row

        # for i, row in enumerate(f):
            # row = row.rstrip()
            # print row.split("\t")

            # 0)title, 1)description, 2)date, 3)date-tier, 4)time, 
            # 5)name(venue), 6)foursquare_id, 7)neighborhood, 8)city, 9)address, 
            # 10)latitude, 11)longitude, 12)cost, 13)img_url, 14)event_url, 
            # 15)category, 16)marker_type, 17)marker_symbol, 18)marker_color,
            # 19) datetime_obj (new cell) 

        csvreader = csv.reader(csvfile)

        # Skips the first header row of the CSV file
        next(csvreader)

        for i, row in enumerate(csvreader):

            if row[2]:
                date_str = str(row[2])
                datetime_obj = datetime.strptime(date_str, "%B %d, %Y")
            else:
                datetime_obj = None

            marker = Marker(title=row[0],
                            address=row[9],
                            latitude=row[10],
                            longitude=row[11],
                            date=row[2],
                            date_tier=row[3],
                            time=row[4],
                            name=row[5],
                            neighborhood=row[7],
                            city=row[8],
                            description=row[1],
                            cost=row[12],
                            img_url=row[13],
                            event_url=row[14],
                            category=row[15],
                            marker_type=row[16],
                            marker_symbol=row[17],
                            marker_color=row[18],
                            datetime=datetime_obj,
                            foursquare_id=row[6])

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

    load_markers('data/markers-20160306.csv')
    # load_hiddengems()
