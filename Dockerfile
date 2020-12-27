FROM python:3.9.0-slim-buster

WORKDIR /usr/src/postmetheus

RUN apt-get update; \
    apt-get install curl -y; \
    curl -sL https://deb.nodesource.com/setup_15.x | bash - ; \
    apt-get install -y nodejs; \
    npm install -g newman;

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .
COPY data ./data

EXPOSE 8080

CMD [ "python", "./postmetheus.py" ]
