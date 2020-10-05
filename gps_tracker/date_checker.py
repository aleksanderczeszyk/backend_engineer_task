from datetime import datetime


def is_point_and_route_date_todays_date(route_serializer, point_serializer):
    today = datetime.today().date()
    return route_serializer.validated_data['date'] == today and point_serializer.validated_data['date'] == today
