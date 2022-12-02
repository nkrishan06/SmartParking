#!/usr/bin/python
import time
import RPi.GPIO as GPIO
import time
import os,sys
from urllib.parse import urlparse
import paho.mqtt.client as mqtt
from parking_slot import ParkingSlot


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


# slot1_sensor_pin = 29
# slot2_sensor_pin = 31
sensor_pins = [29, 31]

# TODO: Add a RED and GREEN LEDs to indicate if there are slots available or not.


#
# We keep the state of the sensors. We use it to compare if there was a change
# in any of them. If so, we publish a message to the MQTT broker.
#

# Initialize states
slots = dict()

for i in enumerate(range(sensor_pins), start=1):
  slots[i] = ParkingSlot(sensor_pins[i], i)
  GPIO.setup(sensor_pins[i], GPIO.IN)


# TODO: Maybe these are not required
# Paho's MQTT callbacks
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {str(rc)}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")
    # client.subscribe(TOPIC)
    # print(f"subscribed to {TOPIC}")
    
def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))


#
# Program
#
client = mqtt.Client()
# Assign event callbacks
client.on_connect = on_connect
client.on_publish = on_publish

client.connect("broker.emqx.io", port=1883, keepalive=60)



# This is the Topic we are going to use.
# We suppose this system administrated by the UdS, and is located specifically
# at the Faculty of Sciences parking lot.
PARKING_ID = "pk_ps/uds"
SECTION = "science"
TOPIC = f"{PARKING_ID}/{SECTION}"


while 1:
    # Print out results
    rc = client.loop()

    # Read sensors
    for id, parking_slot in slots.items():
        slot_current_state = GPIO.input(parking_slot.rpi_pin)

        # Check if there was a change in the saved state. If so, publish to the topic
        if slot_current_state != parking_slot.status:
            # Update the saved state and publish
            parking_slot.state = slot_current_state

            # Format of payload was defined as JSON:
            #   { "id": id, "msg": status }
            payload = {"id": parking_slot.id, "msg": parking_slot.state}
            client.publish(topic=TOPIC, payload=payload)
            time.sleep(0.2)

        # TODO: need to track if all slots are occupied. If so, turn an LED to RED
  
