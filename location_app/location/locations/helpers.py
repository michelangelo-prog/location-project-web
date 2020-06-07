import requests
import json

from .exceptions import DefaultElevationApiError

DEFAULT_ELEVATION_API_URL = "https://elevation-api.io/api/elevation"

def get_elevation_from_api(location):
        parameters_to_load = {'points': "{0},{1}".format(location[1], location[0])}

        response_get = requests.get(DEFAULT_ELEVATION_API_URL, params=parameters_to_load)

        if response_get.status_code == 200:
            json_response = json.loads(response_get.text)
            return json_response['elevations'][0]['elevation']

        raise DefaultElevationApiError(
        {'status_code': '{0}'.format(response_get.status_code)}
        )
