FROM python:3.9.0-slim-buster

WORKDIR /usr/src/postmetheus

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN apt-get update ; \
    apt-get install -y --no-install-recommends curl=7.64.0-4+deb10u1 ; \
    curl -sL https://deb.nodesource.com/setup_15.x | bash - ; \
    apt-get install -y --no-install-recommends nodejs=15.5.0-1nodesource1 ; \
    npm install -g newman@5.2.1; \
    apt-get -y autoremove ; \
    apt-get -y clean ; \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .
COPY data ./data

EXPOSE 8080

CMD [ "python", "./postmetheus.py" ]
