# cURL Commands Used by Tutorial

## GET

```
$ curl -X GET http://127.0.0.1:5000/api/v1/subscribers

$ curl -X GET http://127.0.0.1:5000/api/v1/subscribers/1
```

## POST

```
$ curl -H "Content-Type: application/json" -X POST -d '{"id":5,"name":"monkeypaw","email":"monkeypaw@mail.com"}' http://127.0.0.1:5000/api/v1/subscribers
```

## PUT

```
$ curl -H "Content-Type: application/json" -X PUT -d '{"id":1, "name":"vinegarluvr","email":"vinagerluvr@mail.com"}' http://127.0.0.1:5000/api/v1/subscribers/1
```

## DELETE

```
$ curl -X DELETE http://127.0.0.1:5000/api/v1/subscribers/1
```

## Passing User Credentials

```
$ curl -X GET http://127.0.0.1:5000/api/v1/private --user admin:SecretPassword
```

## Post a User with Credentials for JWT

```
$ curl -H "Content-Type: application/json" -X POST -d '{"username":"ttg","password":"password"}' http://localhost:5000/auth
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE1MDc1ODYyNDksImV4cCI6MTUwNzU4NjU0OSwiaWRlbnRpdHkiOjEyMywiaWF0IjoxNTA3NTg2MjQ5fQ.R7IxmueUiQlEvSuFXnjemkSUP9UCvDuqqzwHGp5IoXA"
}
```

## Access Restricted Resource Using JWT Token

```
$ curl -X GET http://localhost:5000/api/v1/private -H "Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE1MDc1ODYyNDksImV4cCI6MTUwNzU4NjU0OSwiaWRlbnRpdHkiOjEyMywiaWF0IjoxNTA3NTg2MjQ5fQ.R7IxmueUiQlEvSuFXnjemkSUP9UCvDuqqzwHGp5IoXA"
{
    "meaning_of_life": 42
}
```
