FROM python:3

RUN pip install --upgrade pip && \
    pip install --no-cache-dir thrift

WORKDIR /srv


ADD ./server .

ENTRYPOINT [ "python", "./server.py" ]
