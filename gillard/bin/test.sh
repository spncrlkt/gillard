#/bin/bash

docker stop flask
docker rm flask
docker run \
  -it \
  --rm \
  --link postgres:postgres \
  --name='test' \
  flask \
  run_tests.py
