docker stop flask
docker rm flask
docker run \
  -d \
  -p 5000:5000 \
  --name flask \
  --link postgres:postgres \
  -e "GILLARD_SETTINGS=gillard.cfg" \
  flask
