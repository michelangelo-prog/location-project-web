from ..adapters import AdapterElevationAPI, HTTP_200_OK, ElevationApiException

from unittest import TestCase, mock
from unittest.mock import call

TEST_LATITUDE = 39.90974
TEST_LONGITUDE = -106.17188
TEST_ELEVATION = 2768.5

TEST_LATITUDE_WRONG = 6.6
TEST_LONGITUDE_WRONG = -6.6

def mocked_requests_get(*args, **kwargs):
    url = kwargs.get("url")
    params = kwargs.get("params")

    if url == AdapterElevationAPI.API_URL and params == {"points": "{0},{1}".format(TEST_LATITUDE, TEST_LONGITUDE)}:
        return MockResponse({'elevations': [{'lat': TEST_LATITUDE, 'lon': TEST_LONGITUDE, 'elevation': TEST_ELEVATION}], 'resolution': '5000m'}, HTTP_200_OK)
    elif url == AdapterElevationAPI.API_URL and params == {"points": "{0},{1}".format(TEST_LONGITUDE_WRONG, TEST_LATITUDE_WRONG)}:
        return MockResponse({'elevations': [{'lat': TEST_LATITUDE, 'lon': TEST_LONGITUDE}], 'resolution': '5000m'}, HTTP_200_OK)
    else:
        return MockResponse({"error": "Not found"}, 404)

class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code
    def json(self):
        return self.json_data

class TestAdapterElevationAPI(TestCase):
    def setUp(self):
        self.elevation_adapter = AdapterElevationAPI()

    @mock.patch(
        "location.locations.adapters.requests.get",
        side_effect=mocked_requests_get,
    )
    def test_get_elevation(self, mock_get):
        elevation = self.elevation_adapter.get_elevation(TEST_LONGITUDE, TEST_LATITUDE)

        self.assertEqual(TEST_ELEVATION, elevation)

    @mock.patch(
        "location.locations.adapters.requests.get",
        side_effect=mocked_requests_get,
    )
    def test_get_request_called_once(self, mock_get):
        self.elevation_adapter.get_elevation(TEST_LONGITUDE, TEST_LATITUDE)

        expected_call = call(
            params={"points": "{0},{1}".format(TEST_LATITUDE, TEST_LONGITUDE)},
            url=AdapterElevationAPI.API_URL,
        )

        mock_get.assert_called_once()
        self.assertIn(expected_call, mock_get.call_args_list)

    @mock.patch(
        "location.locations.adapters.requests.get",
        side_effect=mocked_requests_get,
    )
    def test_raise_ElevationApiException_when_status_code_diffrent_than_ok(self, mock_get):
        with self.assertRaises(ElevationApiException):
            self.elevation_adapter.get_elevation(2.2, -1.1)

    @mock.patch(
        "location.locations.adapters.requests.get",
        side_effect=mocked_requests_get,
    )
    def test_raise_ElevationApiException_when_json_data_diffrent_than_ok(self, mock_get):
        with self.assertRaises(ElevationApiException):
            self.elevation_adapter.get_elevation(TEST_LATITUDE_WRONG, TEST_LONGITUDE_WRONG)