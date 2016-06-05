docker stop flask
docker rm flask
docker run \
  -d \
  -p 5000:5000 \
  --name flask \
  --link postgres:postgres \
  flask
