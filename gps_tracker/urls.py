from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from gps_tracker import views

urlpatterns = [
    path('route/', views.RouteList.as_view(), name='route-list'),
    path('route/<int:pk>/', views.RouteDetail.as_view(), name='route-detail'),
    path('route/<int:pk>/way_point/', views.RouteAddWayPoint.as_view(), name='route-detail-add-way-point'),
    path('route/<int:pk>/points/', views.RoutePointsList.as_view(), name='route-detail-point-list'),
    path('route/<int:pk>/length/', views.RouteLength.as_view(), name='route-detail-length'),
    path('route/longest_per_day/', views.LongestRoutePerDay.as_view(), name='route-list-longest-per-day'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
