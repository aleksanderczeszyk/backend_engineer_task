from django.test import TestCase
import requests
from datetime import datetime, timedelta


SERVICE_ENDPOINT = 'http://127.0.0.1:8000/'
ROUTE_ENDPOINT = "{}route/".format(SERVICE_ENDPOINT)
ROUTE_ADD_WAY_POINT_ENDPOINT = "{}{}/way_point/".format(ROUTE_ENDPOINT, "{}")
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

    def _push_additional_coords_to_route(self, route_id, coords):
        if isinstance(coords, dict):
            coords = [coords]
        for coordinates in coords:
            requests.post(ROUTE_ADD_WAY_POINT_ENDPOINT.format(route_id), json=coordinates)

    def test_length_calculation(self):
        length = self.length_get.json()
        assert 11750 < length['km'] < 11900

    def test_returning_longest_route_per_date(self):
        today = datetime.today().date()
        today = today.strftime('%Y-%m-%d')
        route_ids = []
        for i in range(3):
            route_creation_response = requests.post(ROUTE_ENDPOINT)
            route = route_creation_response.json()
            route_id = route['route_id']
            route_ids.append(route_id)

        self._push_route(route_ids[0])

        self._push_route(route_ids[1])
        self._push_additional_coords_to_route(route_ids[1], self.additional_coords[0])

        self._push_route(route_ids[2])
        self._push_additional_coords_to_route(route_ids[2], self.additional_coords)

        longest_route_per_day_response = requests.get(LONGEST_ROUTE_PER_DAY_ENDPOINT).json()

        assert route_ids[2] in longest_route_per_day_response[today]
        print(longest_route_per_day_response)

