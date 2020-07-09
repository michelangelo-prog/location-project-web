import requests

HTTP_200_OK = 200


class ElevationApiException(Exception):
    pass


class AdapterElevationAPI:

    API_URL = "https://elevation-api.io/api/elevation"

    def get_elevation(self, longitude, latitude):
        parameters = {"points": "{0},{1}".format(latitude, longitude)}
        response = requests.get(url=self.API_URL, params=parameters)
        if response.status_code == HTTP_200_OK:
            try:
                response_json = response.json()
                return response_json["elevations"][0]["elevation"]
            except:
                self._raise_elevation_api_error()
        else:
            self._raise_elevation_api_error()

    def _raise_elevation_api_error(self):
        raise ElevationApiException()
