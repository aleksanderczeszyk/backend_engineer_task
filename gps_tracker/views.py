from gps_tracker.models import GeoPoint, Route
from gps_tracker.serializers import PointSerializer, RouteSerializer
from gps_tracker import date_checker
from gps_tracker import route_length
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from rest_framework import generics


class RouteList(generics.ListCreateAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer


class RouteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer


class RouteAddWayPoint(APIView):
    """
    Add way point to route
    """
    def get_object(self, pk):
        try:
            Route.objects.get(pk=pk)
        except Route.DoesNotExist:
            raise Http404

    def post(self, request, pk, format=None):
        route = self.get_object(pk)
        req_data = request.data
        req_data['route'] = pk
        point_serializer = PointSerializer(data=req_data)
        route_serializer = RouteSerializer(route, data=request.data, context={'request': request})
        if point_serializer.is_valid() and route_serializer.is_valid():
            if not date_checker.is_point_and_route_date_todays_date(route_serializer, point_serializer):
                return Response(
                    {"Fail": "The point and route creation date must be todays date"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                point_serializer.save()
                return Response(
                    point_serializer.data,
                    status=status.HTTP_201_CREATED
                )
        return Response(point_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoutePointsList(generics.RetrieveAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

    def get(self, request, pk):
        points = GeoPoint.objects.filter(route=pk)
        point_serializer = PointSerializer(points, many=True, context={'request': request})
        return Response(point_serializer.data)


class RouteLength(generics.RetrieveAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

    def get(self, request, pk):
        route_len = route_length.get_route_length(pk)
        return Response({"km": route_len}, status=status.HTTP_200_OK)


class LongestRoutePerDay(APIView):
    def get_previous_days_routes(self, request, format=None):
        today = datetime.today().date()
        routes = Route.objects.exclude(date=today)
        serializer = RouteSerializer(routes, many=True, context={'request': request})
        return serializer.data

    def get(self, request, format=None):
        response_payload = []
        routes_serialized_data = self.get_previous_days_routes(request)
        dates = list(set([route["date"] for route in routes_serialized_data]))
        for date in dates:
            response_payload.append(
                {"date": date, "route_ids": route_length.get_longest_route_for_given_day(date)}
            )
        return Response(response_payload, status=status.HTTP_200_OK)
