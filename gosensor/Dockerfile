FROM golang:alpine
RUN apk update && \
    apk add git && \
    go get github.com/eclipse/paho.mqtt.golang
WORKDIR /svr
ADD sensor.go .
RUN go build -o sensor .
CMD ["./sensor"]
