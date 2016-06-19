#/bin/bash

docker stop flask
docker rm flask
docker run \
  -it \
  --rm \
  --link postgres:postgres \
  --name='test' \
  -e "GILLARD_SETTINGS=gillard.cfg" \
  flask \
  run_tests.py
