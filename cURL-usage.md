# Using cURL

Note: These commands require a local dev setup and associated user accounts in the MySQL db to execute properly.

## General command structures

### GET
```
$ curl -X GET http://127.0.0.1:5000/api/v1/subscribers

$ curl -X GET http://127.0.0.1:5000/api/v1/subscribers/1
```

### POST
```
$ curl -H "Content-Type: application/json" -X POST -d '{"id":5,"name":"monkeypaw","email":"monkeypaw@mail.com"}' http://127.0.0.1:5000/api/v1/subscribers
```

### PUT
```
$ curl -H "Content-Type: application/json" -X PUT -d '{"id":1, "name":"vinegarluvr","email":"vinagerluvr@mail.com"}' http://127.0.0.1:5000/api/v1/subscribers/1
```

### DELETE
```
$ curl -X DELETE http://127.0.0.1:5000/api/v1/subscribers/1
```

### Passing User Credentials
```
$ curl -X GET http://127.0.0.1:5000/api/v1/private --user admin:SecretPassword
```

### Post a User with Credentials for JWT
```
$ curl -H "Content-Type: application/json" -X POST -d '{"username":"ttg","password":"password"}' http://localhost:5000/auth

{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE1MDc1ODYyNDksImV4cCI6MTUwNzU4NjU0OSwiaWRlbnRpdHkiOjEyMywiaWF0IjoxNTA3NTg2MjQ5fQ.R7IxmueUiQlEvSuFXnjemkSUP9UCvDuqqzwHGp5IoXA"
}
```

### Access Restricted Resource Using JWT Token
```
$ curl -X GET http://localhost:5000/api/v1/private -H "Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE1MDc1ODYyNDksImV4cCI6MTUwNzU4NjU0OSwiaWRlbnRpdHkiOjEyMywiaWF0IjoxNTA3NTg2MjQ5fQ.R7IxmueUiQlEvSuFXnjemkSUP9UCvDuqqzwHGp5IoXA"

{
    "meaning_of_life": 42
}
```

## Django Authentication Commands

### Access a secured endpoint without permission:
```
$ curl -H "Content-Type: application/json" http://localhost:8000/api/subscribers/

{"detail":"Authentication credentials were not provided."}%
```

### Get a token for a user:
```
$ curl --request POST --url http://localhost:8000/login --header 'content-type: application/json'   --data '{"username": "jgentle", "password": "P@$$WORD"}'
```
OR
```
$ curl -X POST -H 'content-type: application/json' -d '{"username":"jgentle", "password":"P@$$WORD"}' localhost:8000/login

{"token":"f52ad18f805d5296a59aaf5ada2361da711c1369"}%
```

### Access a secured endpoint with permissions:
```
$ curl -H "Content-Type: application/json" -H "Authorization: Token f52ad18f805d5296a59aaf5ada2361da711c1369" http://localhost:8000/api/subscribers/

[{"id":1,"name":"mungbean boy","age":43,"email":"sprout@legume.com"},{"id":2,"name":"treebeard","age":67,"email":"acorn@legume.com"},{"id":3,"name":"woodie","age":56,"email":"oak@legume.com"}]%
```

### Obtain a JWT Token:
```
$ curl -X POST http://localhost:8000/api/jwt-auth/ -H "content-type: application/json" -d '{"username":"jgentle", "password":"P@$$WORD"}'

{"token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1MDc3NDIwMTAsImVtYWlsIjoiamdlbnRsZUB0YWNjLnV0ZXhhcy5lZHUiLCJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImpnZW50bGUifQ.TK7Yg0bKMjomJNa9r7UtGsJkkCzcH3Bg9m6v7x2bsA8"}%
```

### Use JWT Token on secured endpoint:
```
$ curl -H "Content-Type: application/json" -H "Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1MDc3NDIwMTAsImVtYWlsIjoiamdlbnRsZUB0YWNjLnV0ZXhhcy5lZHUiLCJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImpnZW50bGUifQ.TK7Yg0bKMjomJNa9r7UtGsJkkCzcH3Bg9m6v7x2bsA8" -X GET  http://localhost:8000/api/subscribers/

[{"id":1,"name":"mungbean boy","age":43,"email":"sprout@legume.com"},{"id":2,"name":"treebeard","age":67,"email":"acorn@legume.com"},{"id":3,"name":"woodie","age":56,"email":"oak@legume.com"}]%
```
