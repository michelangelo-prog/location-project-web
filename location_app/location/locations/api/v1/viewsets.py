from rest_framework import viewsets, mixins

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import LocationSerializer
from rest_framework import status
from ...models import Location

from ...exceptions import LocationExists

from .serializers import ClosestLocationSerializer


MESSAGE_INCORRECT_PARAMETERS = "Incorrect parameters were provided."

class LocationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing the locations added by users.
    """
    lookup_field = "uuid"
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        longitude = self.request.GET.get('longitude', None)
        latitude = self.request.GET.get('latitude', None)

        if longitude and latitude:
            try:
                longitude = float(longitude)
                latitude = float(latitude)
                distance = self.request.GET.get('distance', None)
                if distance:
                    distance = float(distance)
                    queryset = Location.objects.find_closest_queryset(longitude, latitude, distance)
                else:
                    queryset = Location.objects.find_closest_queryset(longitude, latitude)
            except ValueError:
                return Response({'message': MESSAGE_INCORRECT_PARAMETERS}, status=status.HTTP_400_BAD_REQUEST)
            else:
                page = self.paginate_queryset(queryset)
                if page is not None:
                    serializer = ClosestLocationSerializer(page, many=True)
                    return self.get_paginated_response(serializer.data)

                serializer = ClosestLocationSerializer(queryset, many=True)
                return Response(serializer.data)
        else:
            return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except LocationExists:
            return Response(
                {
                    'message': "Point already exists."
                },
                status=status.HTTP_400_BAD_REQUEST)

