# syntax=docker/dockerfile:1

FROM tecktron/python-waitress:latest

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install -r requirements.txt

COPY . /app

CMD ["waitress-serve", "--port=5000", "--call", "app:create_app"]
