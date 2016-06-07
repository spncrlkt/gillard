#/bin/bash

docker run \
  -it \
  --link postgres:postgres \
  --rm \
  postgres:9.5.3 \
  sh -c \
  'exec psql -h "$POSTGRES_PORT_5432_TCP_ADDR" -p "$POSTGRES_PORT_5432_TCP_PORT" -U postgres'
