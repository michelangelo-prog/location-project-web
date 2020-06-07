from rest_framework import serializers

from drf_extra_fields.geo_fields import PointField

from .models import Location

class CreateLocationSerializer(serializers.ModelSerializer):

    location = PointField()

    class Meta:
        model = Location
        fields = ('name', 'location',)
