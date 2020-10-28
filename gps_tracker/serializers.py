from rest_framework import serializers, fields
from datetime import datetime
from gps_tracker.models import GeoPoint, Route


class RouteSerializer(serializers.HyperlinkedModelSerializer):
    route = serializers.HyperlinkedIdentityField(view_name='route-detail')
    points = serializers.HyperlinkedIdentityField(view_name='route-detail-point-list')

    class Meta:
        model = Route
        fields = ['route_id', 'route', 'points']


class PointSerializer(serializers.ModelSerializer):

    class Meta:
        model = GeoPoint
        fields = ['id', 'lon', 'lat', 'route']
