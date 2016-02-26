"""Load data into database."""

from model import Marker, connect_to_db, db
from server import app
import csv
from datetime import datetime

#--------------------------------------------------------#


def load_markers(file):
    """Load markers from dataset into Marker database."""

    with open(file) as f:
        # next(f)  # skip header row

        # for i, row in enumerate(f):
            # row = row.rstrip()
            # print row.split("\t")

            # 0)title, 1)description, 2)date, 3)date-tier, 4)time, 5)name(venue), 6)neighborhood, 7)city, 8)address, 9)latitude, 10)longitude, 11)cost, 12)img_url, 13)event_url, 14)category, 15)marker_type, 16)marker_symbol, 17)marker_color = row.split("\t")

        reader = csv.reader(f)
        for i, row in enumerate(reader):

            if row[2]:
                date_str = str(row[2])
                # import pdb; pdb.set_trace()
                date_obj = datetime.strptime(date_str, "%B %d, %Y")

            marker = Marker(title=row[0],
                            address=row[8],
                            latitude=row[9],
                            longitude=row[10],
                            date=date_obj,
                            date_tier=row[3],
                            time=row[4],
                            name=row[5],
                            neighborhood=row[6],
                            city=row[7],
                            description=row[1],
                            cost=row[11],
                            img_url=row[12],
                            event_url=row[13],
                            category=row[14],
                            marker_type=row[15],
                            marker_symbol=row[16],
                            marker_color=row[17])

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

    load_markers('data/markers-20160225.csv')
    # load_hiddengems()
