FROM python:3

RUN pip install --upgrade pip && \
    pip install --no-cache-dir thrift

WORKDIR /srv


ADD ./client .

ENTRYPOINT [ "python", "./client.py" ]
