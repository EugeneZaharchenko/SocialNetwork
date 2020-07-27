# SocialNetwork

Simple REST API implemented by Flask framework. Token authentication is implemented (JWT is used).

To start working with service, run command:
_python runserver.py_

##Basic Features:
####1. user signup
    
May be executed by endpoint:
_http://127.0.0.1:5000/signup_ or _localhost:5000/signup_

with such **parameters in request body**:

{
    "name": "Eugene",
    "email": "Eugene@e.ua",
    "password": "1401"
}

**As a result:**

{
  "message": "New user named Eugene, id: e88aadbe-ac82-4994-946f-ef18e6098042 was created!"
}

####2. user login
    
May executed by endpoint:
_http://127.0.0.1:5000/login_ or _localhost:5000/login_

with such **parameters in request authorization header**:

    Username: Eugene
    Password: 1401

**As a result:**

{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiJlODhhYWRiZS1hYzgyLTQ5OTQtOTQ2Zi1lZjE4ZTYwOTgwNDIiLCJleHAiOjE1OTU4NDU2Mjh9.GPDBNysEfOI2yU35gI2HJe8mJZT0LYadXMwFBqKP_3c"
}

####3. post creation
    
May be executed by endpoint:
_http://127.0.0.1:5000/user/add_post_ or _localhost:5000/user/add_post_

with such **parameters in request headers**:

    x-access-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiJlODhhYWRiZS1hYzgyLTQ5OTQtOTQ2Zi1lZjE4ZTYwOTgwNDIiLCJleHAiOjE1OTU4NDU2Mjh9.GPDBNysEfOI2yU35gI2HJe8mJZT0LYadXMwFBqKP_3c

and such **parameters in request body**:

{"body":"new post made to test functionality"}

**As a result:**

{
  "message": "New post of user Eugene created!"
}

####4.  post like
    
May be executed by endpoint:
_http://127.0.0.1:5000/user/post/2/like_ or _localhost:5000/user/post/2/like_

with such **parameters in request headers**:

    x-access-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiJlODhhYWRiZS1hYzgyLTQ5OTQtOTQ2Zi1lZjE4ZTYwOTgwNDIiLCJleHAiOjE1OTU4NDU2Mjh9.GPDBNysEfOI2yU35gI2HJe8mJZT0LYadXMwFBqKP_3c

where /post/**2** - number of post.

**As a result:**

{
  "message": "New like of user 3 to post_id 2 created!"
}

####5.  post unlike
    
May be executed by endpoint:
_http://127.0.0.1:5000/user/post/2/unlike_ or _localhost:5000/user/post/2/unlike_

with such **parameters in request headers**:

    x-access-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiJlODhhYWRiZS1hYzgyLTQ5OTQtOTQ2Zi1lZjE4ZTYwOTgwNDIiLCJleHAiOjE1OTU4NDU2Mjh9.GPDBNysEfOI2yU35gI2HJe8mJZT0LYadXMwFBqKP_3c

where /post/**2** - number of post.

**As a result:**

{
  "message": "New unlike of user 3 to post_id 2 created!"
}

####6.  analytics about how many likes was made
    
May be executed by endpoint:
_http://127.0.0.1:5000/analitics/?date_from=2020-07-22&date_to=2020-07-27_ or _localhost:/analitics/?date_from=2020-07-22&date_to=2020-07-27_

with such **parameters in request headers**:

    x-access-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiJlODhhYWRiZS1hYzgyLTQ5OTQtOTQ2Zi1lZjE4ZTYwOTgwNDIiLCJleHAiOjE1OTU4NDU2Mjh9.GPDBNysEfOI2yU35gI2HJe8mJZT0LYadXMwFBqKP_3c

where: **date_from=2020-07-22** - start date, **date_to=2020-07-27** - end date of analytics (exclusive).

**As a result:**

{
  "message": "Likes quantity aggregated by dates are: {25: 1, 26: 2}"
}

(likes on 25th, 26th days were previously stored in db).

####7.  user activity - an endpoint which will show when user was login last time and when he mades a last request to the service
    
May be executed by endpoint:
_http://127.0.0.1:5000/user_ or _localhost:/user_

with such **parameters in request headers**:

    x-access-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiJlODhhYWRiZS1hYzgyLTQ5OTQtOTQ2Zi1lZjE4ZTYwOTgwNDIiLCJleHAiOjE1OTU4NDU2Mjh9.GPDBNysEfOI2yU35gI2HJe8mJZT0LYadXMwFBqKP_3c

**As a result:**

{
  "user": {
    "created": "Mon, 27 Jul 2020 08:23:22 GMT",
    "last_actions": "Mon, 27 Jul 2020 09:16:18 GMT",
    "last_login": "Mon, 27 Jul 2020 08:27:08 GMT",
    "name": "Eugene",
    "password": "sha256$ayWvFbgh$cfa5ce854be17ec0f040792e32214eb3ed904d5163337be4da9fae23d4d3311d",
    "public_id": "e88aadbe-ac82-4994-946f-ef18e6098042"
  }
}

where: **"created"** - user creation date;
       **"last_actions"** - last request to the service, made by the user;
       **"last_login"** - last time when login to the service was made by the user;
       **"name"** - user's name;
       **"password"** - user's password (hashed);
       **"public_id"** - hashed user id, by which user may be identified to perform queries.

###Some additional
####8.   users - an endpoint which will show information about users registered in the service
    
May be executed by endpoint:
_http://127.0.0.1:5000/users_ or _localhost:/users_

with such **parameters in request headers**:

    x-access-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiJlODhhYWRiZS1hYzgyLTQ5OTQtOTQ2Zi1lZjE4ZTYwOTgwNDIiLCJleHAiOjE1OTU4NDU2Mjh9.GPDBNysEfOI2yU35gI2HJe8mJZT0LYadXMwFBqKP_3c

**As a result:**

{
  "1": "d3270d3a-1e99-4442-a20f-d21bced5a514",
  "2": "b668bb4d-44f0-4e34-9640-a9afb9baf105",
  "3": "e88aadbe-ac82-4994-946f-ef18e6098042"
}

where: **"1"** - user id, **"d3270d3a-1e99-4442-a20f-d21bced5a514"** - hashed user id, by which user may be identified to perform queries (public user id).