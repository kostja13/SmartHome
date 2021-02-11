package main

import (
	"encoding/json"
	"fmt"
	"math/rand"
	"time"
	mqtt "github.com/eclipse/paho.mqtt.golang"
)

func main() {
	opts := mqtt.NewClientOptions()
	opts.AddBroker(fmt.Sprintf("tcp://mosquitto:1883"))
	opts.SetClientID("gosensor1")
	client := mqtt.NewClient(opts)
	token := client.Connect()
	for !token.WaitTimeout(3 * time.Second) {
	}
	if err := token.Error(); err != nil {
		fmt.Printf("Error")
	}

	sensordaten := map[string]interface{}{"name": "tempsensor1", "id": 11, "value": 0}
	var diff int = 0
	var value int = 50



	for {
		time.Sleep(2000 * time.Millisecond)
		diff = rand.Intn(5)
		value = value + diff - 2
		if value > 50 {
			value = value - 3
		}
		if value < 3 {
			value = value + 2
		}
		sensordaten["value"] = value
		sensordatenJson, _ := json.Marshal(sensordaten)
		client.Publish("smarthome/tempsensor",0,false,string(sensordatenJson))
		fmt.Printf("%v\n", sensordaten["value"])
	}
}
