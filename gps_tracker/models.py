from django.db import models as models


class GeoPoint(models.Model):
    date = models.DateField(auto_now_add=True)
    lon = models.DecimalField(max_digits=9, decimal_places=7)
    lat = models.DecimalField(max_digits=9, decimal_places=7)
    route = models.ForeignKey('Route', related_name='points', on_delete=models.CASCADE)

    class Meta:
        ordering = ['date']


class Route(models.Model):
    date = models.DateField(auto_now_add=True)
    route_id = models.AutoField(primary_key=True)

    class Meta:
        ordering = ['date']
