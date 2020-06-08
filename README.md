# location-project-web

## Local Development

Start the dev server for local development:
```bash
docker-compose up
```

Run a command inside the docker container:

```bash
docker-compose run --rm web [command]
```

## Authentication
For clients to authenticate, the token key should be included in the Authorization HTTP header. The key should be prefixed by the string literal "Token", with whitespace separating the two strings. For example:

```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

Unauthenticated responses that are denied permission will result in an HTTP `401 Unauthorized` response with an appropriate `WWW-Authenticate` header. For example:

```
WWW-Authenticate: Token
```

The curl command line tool may be useful for testing token authenticated APIs. For example:

```bash
curl -X GET http://127.0.0.1:8000/api/v1/example/ -H 'Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'
```

### Retrieving Tokens
Authorization tokens are issued and returned when a user registers. A registered user can also retrieve their token with the following request:

**Request**:

`POST` `api-token-auth/`

Parameters:

Name | Type | Description
---|---|---
username | string | The user's username
password | string | The user's password

**Response**:
```json
{ 
    "token" : "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" 
}
```

## Locations
Support adding locations and searching nearest

### Add new location

**Request**:

`POST` `/locations`

Parameters:

```json
Content-Type application/json

{
	"name":"waszyngton",
    "location":{
        "latitude": 38.912517,
        "longitude": -76.999446
    }
}
```

*Note:*

- **[Authorization Protected](authentication.md)**

**Response**:

```
"Location successfully created."
201 Created
```

### Find nearest location

**Request**:

`GET` `/locations/find`

URL parameters:

username (string), longitude (float), latitude (float), distance (float) (optional)

distance unit -> meter
when distance parameter provided, request return list of locations <= distance

**Example 1**:

```
http://192.168.99.100:8000/api/v1/locations/find?username=Michal&longitude=21.156039&latitude=51.418663
```

**Response**:

```json
Content-Type application/json
200 OK
[
    {
        "name": "Kielce",
        "location": [
            {
                "longitude": 20.645882,
                "latitude": 50.862886
            }
        ],
        "distance[m]": 71315.19769046
    }
]
```

**Example 2**:

```
http://192.168.99.100:8000/api/v1/locations/find?username=Michal&longitude=21.156039&latitude=51.418663&distance=90000
```

**Response**:

```json
Content-Type application/json
200 OK
[
    {
        "name": "Kielce",
        "location": [
            {
                "longitude": 20.645882,
                "latitude": 50.862886
            }
        ],
        "distance[m]": 71315.19769046
    },
    {
        "name": "Warsaw",
        "location": [
            {
                "longitude": 21.003778,
                "latitude": 52.212667
            }
        ],
        "distance[m]": 88907.49766853
    }
]
```

*Note:*

- **[Authorization Protected](authentication.md)**

## Users
Supports registering, viewing, and updating user accounts.

### Register a new user account

**Request**:

`POST` `/users/`

Parameters:

Name       | Type   | Required | Description
-----------|--------|----------|------------
username   | string | Yes      | The username for the new user.
password   | string | Yes      | The password for the new user account.
first_name | string | No       | The user's given name.
last_name  | string | No       | The user's family name.
email      | string | No       | The user's email address.

*Note:*

- Not Authorization Protected

**Response**:

```json
Content-Type application/json
201 Created

{
  "id": "6d5f9bae-a31b-4b7b-82c4-3853eda2b011",
  "username": "richard",
  "first_name": "Richard",
  "last_name": "Hendriks",
  "email": "richard@piedpiper.com",
  "auth_token": "132cf952e0165a274bf99e115ab483671b3d9ff6"
}
```

The `auth_token` returned with this response should be stored by the client for
authenticating future requests to the API. See [Authentication](authentication.md).


### Get a user's profile information

**Request**:

`GET` `/users/:id`

Parameters:

*Note:*

- **[Authorization Protected](authentication.md)**

**Response**:

```json
Content-Type application/json
200 OK

{
  "id": "6d5f9bae-a31b-4b7b-82c4-3853eda2b011",
  "username": "richard",
  "first_name": "Richard",
  "last_name": "Hendriks",
  "email": "richard@piedpiper.com",
}
```


### Update your profile information

**Request**:

`PUT/PATCH` `/users/:id`

Parameters:

Name       | Type   | Description
-----------|--------|---
first_name | string | The first_name of the user object.
last_name  | string | The last_name of the user object.
email      | string | The user's email address.



*Note:*

- All parameters are optional
- **[Authorization Protected](authentication.md)**

**Response**:

```json
Content-Type application/json
200 OK

{
  "id": "6d5f9bae-a31b-4b7b-82c4-3853eda2b011",
  "username": "richard",
  "first_name": "Richard",
  "last_name": "Hendriks",
  "email": "richard@piedpiper.com",
}
```
