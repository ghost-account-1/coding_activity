[![Build Status](https://travis-ci.org/ghost-account-1/coding_activity.svg?branch=dev)](https://travis-ci.org/ghost-account-1/coding_activity)

### You need python version 3
- Requirements
    - pip install Django
    - pip install djangorestframework
    - pip install django-oauth-toolkit


### Register
```
curl -X POST \
  http://127.0.0.1:8000/api/users/ \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' \
  -d '{
    "email": "email@example.com",
    "password": "password",
    "first_name": "first name",
    "last_name": "last name"
}'
```

#### Activation 
**After Registering, you can check the token in your console, where you did the python manage.py runserver**
```
curl -X PATCH http://127.0.0.1:8000/api/activation/ -H 'Authorization: Token 6e0d67e9510e143f6988b603aa4e095c35e408f5'
```

#### Login 
**You need to register you app at http://127.0.0.1:8000/o/applications/register/ but first login as an admin at http://127.0.0.1:8000/admin/ *you need to create a superuser first**
```
curl -X POST \
  http://127.0.0.1:8000/api/login/ \
  -H 'Content-Type: application/json' \
  -d '{
    "email": "email@example.com",
    "password": "password",
    "first_name": "first name",
    "last_name": "last name"}'
```

#### User List
**You need to add the CLIENT_ID and CLIENT_SECRET you get (after registering your app) in project/project/settings.py***
```
curl -X GET http://127.0.0.1:8000/api/users/ -H 'Authorization: Bearer Qe2UDBzcVWeNZStAMlllZIQP6f0v6N'
```
or

```
curl -X GET http://127.0.0.1:8000/api/users/
```

#### Change Password
```
curl -X PUT \
  http://127.0.0.1:8000/api/password/ \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer BoDzdGAMruwhFEMHwvrmH6qheDigrJ' \
  -d '{
    "old_password": "your old password here",
    "new_password": "your new password here"}'
```
