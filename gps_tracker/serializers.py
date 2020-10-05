from rest_framework import serializers, fields
from datetime import datetime
from gps_tracker.models import GeoPoint, Route


class RouteSerializer(serializers.HyperlinkedModelSerializer):
    route = serializers.HyperlinkedIdentityField(view_name='route-detail')
    points = serializers.HyperlinkedIdentityField(view_name='route-detail-point-list')
    date = fields.DateField(input_formats=['%Y-%m-%d'], default=datetime.now().date())

    class Meta:
        model = Route
        fields = ['route_id', 'route', 'points', 'date']


class PointSerializer(serializers.ModelSerializer):
    date = fields.DateField(input_formats=['%Y-%m-%d'], default=datetime.now().date())

    class Meta:
        model = GeoPoint
        fields = ['id', 'lon', 'lat', 'route', 'date']
