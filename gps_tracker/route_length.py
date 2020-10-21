from geopy.distance import geodesic
from gps_tracker.models import GeoPoint, Route


def calculate_route_length(points_objects):
    total_length = 0
    for point_obj_id in range(len(points_objects)):
        if point_obj_id < (len(points_objects) - 1):
            current_point_pair_length = geodesic(
                (points_objects[point_obj_id].lon, points_objects[point_obj_id].lat),
                (points_objects[point_obj_id + 1].lon, points_objects[point_obj_id + 1].lat)
            ).km
            total_length += current_point_pair_length

    return total_length


def get_route_length(pk):
    points = GeoPoint.objects.filter(route=pk)
    route_len = calculate_route_length(points)
    return route_len


def get_longest_route_for_given_day(date):
    route_ids_and_lengths = {}
    routes = Route.objects.filter(date=date)
    for route in routes:
        route_ids_and_lengths.update(
            {route.route_id: get_route_length(route.route_id)}
        )
    longest_route_length = max(route_ids_and_lengths.values())
    longest_route_ids = [id for id in route_ids_and_lengths if route_ids_and_lengths[id] == longest_route_length]
    return longest_route_ids


