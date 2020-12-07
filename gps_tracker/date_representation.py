from datetime import datetime
from gps_tracker import route_length


def date_representation(date):
    return {"date": date.strftime("%Y-%m-%d"), "route_ids": route_length.get_longest_route_for_given_day(date)}
