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

## Locations
Support adding locations and searching nearest

`GET/POST` `/api/v1/locations/` - add new location / list locations

`GET/PUT/PATCH/DELETE` `/api/v1/locations/:uuid/` - edit location 

`GET` `/api/v1/locations/?longitude=21.02&latitude=50.86` - find closest location

`GET` `/api/v1/locations/?longitude=21.02&latitude=50.86&distance=200000` - find closest locations (distance [meter])

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
