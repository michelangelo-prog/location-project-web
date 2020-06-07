from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.core import serializers

from django.http import HttpResponse

from .serializers import CreateLocationSerializer

from .models import Location

import json

from .exceptions import LocationExist, DefaultElevationApiError

class CreateLocationView(CreateAPIView):

    http_method_names = ['post',]
    permission_classes = (IsAuthenticated,)

    serializer_class = CreateLocationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer_validated_data = serializer.validated_data

        try:
            Location.objects.create_get_elevation_from_from_api(
            serializer_validated_data.get('name'),
            serializer_validated_data.get('location'),
            )
        except LocationExist:
            msg = "Location exist in database with similar coordinates."
            return Response(msg, status=400)
        except DefaultElevationApiError as e:
            msg = "Problem with Elevation API: {}".format(str(e))
            return Response(msg, status=404)

        msg = "Location successfully created."
        return Response(msg, status=201)

class FindLocationView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):

        username = self.request.GET.get('username',None)

        if username != self.request.user.username:
            msg = "Bad request. This is not your username"
            return Response({'message': msg}, status=400)

        try:
            longitude = float(self.request.GET.get('longitude',''))
            latitude = float(self.request.GET.get('latitude',''))
            distance = self.request.GET.get('distance', None)

            if distance != None:
                distance = float(distance)
                qs = Location.objects.find_nearest_locations_by_distance(longitude, latitude, distance)
            else:
                qs = Location.objects.find_nearest_location(longitude, latitude)
                qs = [qs]
            try:
                response_data = [{'name': q.name, 'location': [{'longitude': q.location[0], 'latitude' : q.location[1]}], 'distance[m]': q.distance.m} for q in qs]
                if not len(response_data):
                    raise Exception
            except:
                msg = "Not found"
                return Response({'message': msg}, status=200)

            return HttpResponse(json.dumps(response_data), content_type='application/json')

        except ValueError:
            msg = "Unable to parse one or more parameters provided!."
            return Response({'message': msg}, status=400)
