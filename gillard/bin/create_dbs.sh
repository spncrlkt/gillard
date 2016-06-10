#/bin/bash

docker stop flask
docker rm flask
docker run \
  -it \
  --rm \
  --link postgres:postgres \
  flask \
  create_dbs.py
