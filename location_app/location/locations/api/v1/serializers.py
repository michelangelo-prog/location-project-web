from rest_framework import serializers

from drf_extra_fields.geo_fields import PointField

from ...models import Location

class LocationSerializer(serializers.ModelSerializer):

    location = PointField()

    class Meta:
        model = Location
        fields = ('uuid', 'name', 'location', 'elevation')
        read_only_fields = ['uuid', 'elevation']

class ClosestLocationSerializer(serializers.ModelSerializer):
    distance = serializers.IntegerField(
        source='distance.m',
        read_only=True
    )
    location = PointField()

    class Meta:
        model = Location
        fields = ('uuid', 'name', 'location', 'elevation', 'distance')
        read_only_fields = ['uuid', 'elevation', 'distance']