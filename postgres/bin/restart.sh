docker stop postgres
docker rm postgres
docker run \
  --name postgres \
  -d \
  --volumes-from postgres-data \
  postgres:9.5.3

