FROM python:3

RUN pip install --upgrade pip && \
    pip install --no-cache-dir paho-mqtt

WORKDIR /srv


ADD sensor.py .

ENTRYPOINT [ "python", "./sensor.py" ]
