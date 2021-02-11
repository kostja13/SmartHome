FROM python:3

WORKDIR /srv
RUN mkdir sqlite

ADD webserver.py .

ENTRYPOINT [ "python", "./webserver.py" ]