FROM python:3.5

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN apt-get install -y python-psycopg2

RUN mkdir /app
WORKDIR /app

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD . ./

ENTRYPOINT ["python"]
CMD ["app.py"]
