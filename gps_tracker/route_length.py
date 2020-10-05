from geopy.distance import geodesic
from gps_tracker.models import GeoPoint, Route
from gps_tracker.serializers import PointSerializer, RouteSerializer


def calculate_route_length(points_serialized_data):
    total_length = 0
    for point_obj_id in range(len(points_serialized_data)):
        if point_obj_id < (len(points_serialized_data) - 1):
            current_point_pair_length = geodesic(
                (points_serialized_data[point_obj_id]["lon"], points_serialized_data[point_obj_id]["lat"]),
                (points_serialized_data[point_obj_id + 1]["lon"], points_serialized_data[point_obj_id + 1]["lat"])
            ).km
            total_length += current_point_pair_length

    return total_length


def get_route_length(request, pk):
    points = GeoPoint.objects.filter(route=pk)
    point_serializer = PointSerializer(points, many=True, context={'request': request})
    points_data = point_serializer.data
    route_len = calculate_route_length(points_data)
    return route_len


def get_longest_route_for_given_day(request, date):
    route_ids_and_lengths = {}
    routes = Route.objects.filter(date=date)
    route_serializer = RouteSerializer(routes, many=True, context={'request': request})
    routes_data = route_serializer.data
    for route in routes_data:
        route_ids_and_lengths.update(
            {route["route_id"]: get_route_length(request, route["route_id"])}
        )
    longest_route_length = max(route_ids_and_lengths.values())
    longest_route_ids = [id for id in route_ids_and_lengths if route_ids_and_lengths[id] == longest_route_length]
    return longest_route_ids


