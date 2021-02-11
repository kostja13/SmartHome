FROM python:3

RUN pip install --upgrade pip && \
    pip install --no-cache-dir thrift &&\
    pip install --no-cache-dir paho-mqtt

WORKDIR /srv


ADD ./zentrale .

ENTRYPOINT [ "python", "./zentraleio.py" ]
