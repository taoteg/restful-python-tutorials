# Django REST Framework: JSON Web Tokens (JWT)

_Written by MASNUNon MAY 28, 2017_

**(This post is a part of a tutorial series on [Building REST APIs in Django](http://polyglot.ninja/django-building-rest-apis/))**

Our last post was about Authentication and Permissions and we covered the available methods of authentication in Django REST Framework. In that post, we learned how to use the built in Token based authentication in DRF. In this post, we will learn more about JSON Web Tokens aka JWT and we will see if JWT can be a better authentication mechanism for securing our REST APIs.

## Understanding JSON Web Tokens (JWTs)

We have actually written a detailed blog post about JSON Web Tokens earlier. In case you have missed it, you probably should read it first. We have also described how to use JWT with Flask – reading that one might also help better understand how things work. And of course, we will briefly cover the idea of JWT in this post as well.

If we want to put it simply – you take some data in JSON format, you hash it with a secret and you get a string that you use as a token. You (your web app actually) pass this token to the user when s/he logs in. The user takes the token and on subsequent requests, passes it back in the “Authorization” header. The web app now takes this token back, “decodes” it back to the original JSON payload. It can now read the stored data (identity of the user, token expiry and other data which was embedded in the JSON). While decoding, the same secret is used, so third party attackers can’t just forge a JWT. We would want our token to be small in size, so the JSON payload is usually intentionally kept small. And of course, it should not contain any sensitive information like user password.

## JWT vs DRF’s Token Based Authentication

So in our last blog post, we saw Django REST Framework includes a token based authentication system which can generate a token for the user. That works fine, right? Why would we want to switch to JSON Web Tokens instead of that?

Let’s first see how DRF generates the tokens:

```
def generate_key(self):
    return binascii.hexlify(os.urandom(20)).decode()
```

It’s just random. The token generated can not be anyway related to the user that it belongs to. So how does it associate a token with an user? It stores the token and a reference to the user in a table in database. Here comes the first point – while using DRF’s token based auth, we need to query database on every request (unless of course we have cached that token which). But what if we have multiple application servers? Now we need all our application servers to connect to the same database or same cache server. How will that scale when the project gets really really big? What if we want to provide single sign on across multiple services? We will need to maintain a central auth service where other services request to verify a token. Can JWT simplify these for us?

JWT is just an encoded (read – hashed / signed) JSON data. As long as any webservice has access to the secret used in signing the data, it can also decode and read the embedded data. It doesn’t need any database calls. You can generate the token from one service and other services can read and verify it just fine. It’s more efficient and simply scales better.

## JWT in Django REST Framework

DRF does not directly support JWTs out of the box. But there’s an [excellent package](https://getblimp.github.io/django-rest-framework-jwt/) that adds support for it. Let’s see how easily we can integrate JWT in our REST APIs.

### Install and Configure

Let’s first install the package using `pip`:

```
pip install djangorestframework-jwt
```

That should install the package. Now we need to add `rest_framework_jwt.authentication.JSONWebTokenAuthentication` to the default authentication classes in REST Framework settings.

```
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    )
}
```

We added it to the top of the list. Next, we just have to add it’s built in view to our urlpatterns.

```
from rest_framework_jwt.views import obtain_jwt_token
urlpatterns = router.urls + [
    url(r'^jwt-auth/', obtain_jwt_token),
]
```

### Obtain a Token

The `obtain_jwt_token` view will check the user credentials and provide a JWT if everything goes alright. Let’s try it.

```
$ curl --request POST \
  --url http://localhost:8000/api/jwt-auth/ \
  --header 'content-type: application/json' \
  --data '{"username": "test_user", "password": "awesomepwd"}'

{"token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJlbWFpbCI6IiIsInVzZXJuYW1lIjoidGVzdF91c2VyIiwiZXhwIjoxNDk1OTkyOTg2fQ.sWSzdiBNNcXDqhcdcjWKjwpPsVV7tCIie-uit_Yz7W0"}
```

Awesome, everything worked just fine. We have got our token too. What do we do next? We use this token to access a secured resource.

### Using the obtained JWT

We need to pass the token in the form of `JWT <token>` as the value of the `Authorization` header. Here’s a sample curl request:

```
$ curl -H "Content-Type: application/json" -H "Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJlbWFpbCI6IiIsInVzZXJuYW1lIjoidGVzdF91c2VyIiwiZXhwIjoxNDk1OTkyOTg2fQ.sWSzdiBNNcXDqhcdcjWKjwpPsVV7tCIie-uit_Yz7W0" -X GET  http://localhost:8000/api/subscribers/

[{"id":1,"name":"Abu Ashraf Masnun","age":29,"email":"masnun@polyglot.ninja"},{"id":2,"name":"Abu Ashraf Masnun","age":29,"email":"masnun@polyglot.ninja"},{"id":3,"name":"Abu Ashraf Masnun","age":29,"email":"masnun@polyglot.ninja"},{"id":4,"name":"Abu Ashraf Masnun","age":29,"email":"masnun@polyglot.ninja"}]
```

So our token worked fine! Cool!

## Where to go next?

Now that you have seen how simple and easy it is to add JSON Web Token based authentication to Django REST Framework, you probably should dive deeper into the package documentation. Specially these topics might be interesting:

* [Refresh Tokens](https://getblimp.github.io/django-rest-framework-jwt/#refresh-token): If you enable JWT token refreshing, you can exchange your current token with a new, fresh one before the existing one expires. The new token will of course have a renewed expiry time set.
* [Verify Token](Verify Token): If you just share the secret, all services can verify the user on their own. However, in modern micro service based architecture, you may want to provide an API end point that other services can use to verify a JWT they received from the user. This can be useful for those scenarios.
* And of course look at the [settings options available](settings options available) and see how you can [customize the token generation process](https://getblimp.github.io/django-rest-framework-jwt/#creating-a-new-token-manually).

In the future, we shall try to cover more about Django, Django REST Framework and Python in general. If you liked the content, please subscribe to the mailing list so we can notify you when we post new contents.
