from django.test import TestCase
import requests
from datetime import datetime, timedelta
from gps_tracker.models import GeoPoint
from gps_tracker.models import Route


SERVICE_ENDPOINT = 'http://127.0.0.1:8000/'
ROUTE_ENDPOINT = "{}route/".format(SERVICE_ENDPOINT)
ROUTE_ADD_WAY_POINT_ENDPOINT = "{}{}/way_point/".format(ROUTE_ENDPOINT, "{}")
ROUTE_POINTS = "{}{}/points".format(ROUTE_ENDPOINT, "{}")
ROUTE_LENGTH_ENDPOINT = '{}{}/length/'.format(ROUTE_ENDPOINT, "{}")
LONGEST_ROUTE_PER_DAY_ENDPOINT = "{}route/longest_per_day".format(SERVICE_ENDPOINT)


class TestRoute(TestCase):
    wgs84_coordinates = [
        {"lat": -25.4025905, "lon": -49.3124416},
        {"lat": -23.559798, "lon": -46.634971},
        {"lat": 59.3258414, "lon": 17.70188},
        {"lat": 54.273901, "lon": 18.591889}
    ]
    additional_coords = [
        {"lat": 54.273939, "lon": 18.591846},
        {"lat": 54.273994, "lon": 18.591806}
    ]

    def setUp(self):
        self.route_post = requests.post(ROUTE_ENDPOINT)
        route = self.route_post.json()
        route_id = route['route_id']
        self._push_route(route_id)
        self.length_get = requests.get(ROUTE_LENGTH_ENDPOINT.format(route_id))

    def _push_route(self, route_id):
        for coordinates in self.wgs84_coordinates:
            requests.post(ROUTE_ADD_WAY_POINT_ENDPOINT.format(route_id), json=coordinates)

    def test_length_calculation(self):
        length = self.length_get.json()
        assert 11750 < length['km'] < 11900


class TestLongestRoutePerDay(TestCase):
    wgs84_coordinates = [
        {"lat": -25.4025905, "lon": -49.3124416},
        {"lat": -23.559798, "lon": -46.634971},
        {"lat": 59.3258414, "lon": 17.70188},
        {"lat": 54.273901, "lon": 18.591889}
    ]
    additional_coords = [
        {"lat": 54.273939, "lon": 18.591846},
        {"lat": 54.273994, "lon": 18.591806}
    ]

    def setUp(self):
        yesterday = datetime.today().date() - timedelta(days=1)
        self.routes = []
        for i in range(3):
            self.routes.append(self._create_route_with_chosen_date(date=yesterday))

        for coord in self.wgs84_coordinates:
            for route in self.routes:
                self._create_point_with_chosen_date(lon=coord["lon"], lat=coord["lat"], route=route, date=yesterday)

        # create point for middle length route
        self._create_point_with_chosen_date(
            lon=self.additional_coords[0]["lon"],
            lat=self.additional_coords[0]["lat"],
            route=self.routes[1],
            date=yesterday
        )

        # create points for longest route
        for coord in self.additional_coords:
            self._create_point_with_chosen_date(
                lon=coord["lon"],
                lat=coord["lat"],
                route=self.routes[2],
                date=yesterday
            )

    def _create_route_with_chosen_date(self, date):
        route = Route()
        route.save()
        pk = route.pk
        Route.objects.filter(pk=pk).update(date=date)
        return Route.objects.get(pk=pk)

    def _create_point_with_chosen_date(self, lon, lat, route, date):
        point = GeoPoint(lon=lon, lat=lat, route=route)
        point.save()
        pk = point.pk
        GeoPoint.objects.filter(pk=pk).update(date=date)
        return GeoPoint.objects.get(pk=pk)

    def test_returning_longest_route_per_date(self):
        longest_route_per_day_response = requests.get(LONGEST_ROUTE_PER_DAY_ENDPOINT).json()
        print(longest_route_per_day_response)

        for route in self.routes:
            point_response = requests.get(ROUTE_POINTS.format(route.pk)).json()
            response = requests.get(ROUTE_LENGTH_ENDPOINT.format(route.pk)).json()
            print("Points of routes: " + str(point_response))
            print("Lengths: " + str(response))

        yesterday = datetime.today().date() - timedelta(days=1)
        yesterday = yesterday.strftime("%Y-%m-%d")

        result = ''

        for longest_route_per_day_object in longest_route_per_day_response:
            if longest_route_per_day_object["date"] == yesterday:
                result += yesterday

        assert result
