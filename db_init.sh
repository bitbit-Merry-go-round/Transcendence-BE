#!/bin/bash

curl -X POST http://localhost:8000/users/create/ \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_access_token' \
  -d '{
        "uid": "yham",
        "status": "ON",
  	    "message": "message",
		    "wins": 2,
		    "loses": 1
		    }'

curl -X POST \
  http://localhost:8000/users/create/ \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_access_token' \
  -d '{
		    "uid": "hyecheon",
		    "status": "ON",
		    "message": "message",
		    "wins": 3,
		    "loses": 2
		    }'

curl -X POST \
  http://localhost:8000/users/create/ \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_access_token' \
  -d '{
		    "uid": "jeseo",
		    "avatar": "base64_encoded_image_data",
		    "status": "ON",
		    "message": "message",
		    "wins": 4,
		    "loses": 3
		    }'

curl -X POST \
  http://localhost:8000/users/create/ \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_access_token' \
  -d '{
		    "uid": "eunjiko",
		    "avatar": "base64_encoded_image_data",
		    "status": "ON",
		    "message": "message",
		    "wins": 2,
		    "loses": 1
		    }'


curl -X POST \
  http://localhost:8000/users/create/ \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_access_token' \
  -d '{
		    "uid": "heshin",
		    "avatar": "base64_encoded_image_data",
		    "status": "ON",
		    "message": "message",
		    "wins": 5,
		    "loses": 1
		    }'

curl -X POST \
  http://localhost:8000/users/yham/friends/ \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_access_token' \
  -d '{
		    "from_user": "yham",
		    "to_user": "hyecheon"
		    }'

curl -X POST \
  http://localhost:8000/users/hyecheon/friends/ \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_access_token' \
  -d '{
		    "from_user": "hyecheon",
		    "to_user": "yham"
		    }'


curl -X POST \
  http://localhost:8000/users/jeseo/friends/ \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_access_token' \
  -d '{
		    "from_user": "jeseo",
		    "to_user": "heshin"
		    }'


curl -X POST \
  http://localhost:8000/users/jeseo/friends/ \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_access_token' \
  -d '{
		    "from_user": "jeseo",
		    "to_user": "eunjiko"
		    }'

curl -X POST \
  http://localhost:8000/users/eunjiko/friends/ \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_access_token' \
  -d '{
		    "from_user": "eunjiko",
		    "to_user": "jeseo"
		    }'

curl -X POST \
  http://localhost:8000/users/eunjiko/friends/ \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_access_token' \
  -d '{
		    "from_user": "eunjiko",
		    "to_user": "heshin"
		    }'

curl -X POST \
  http://localhost:8000/users/heshin/friends/ \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_access_token' \
  -d '{
		    "from_user": "heshin",
		    "to_user": "jeseo"
		    }'

curl -X POST \
  http://localhost:8000/users/heshin/friends/ \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_access_token' \
  -d '{
		    "from_user": "heshin",
		    "to_user": "eunjiko"
		    }'
