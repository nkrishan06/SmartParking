#!/usr/bin/python

import RPi.GPIO as GPIO

import time
import datetime

import paho.mqtt.client as mqtt
from parking_slot import ParkingSlot



GPIO.setmode(GPIO.BOARD)    # Use physical pin numbering
GPIO.setwarnings(False)     # Ignore warnings


# slot1_sensor_pin = 29
# slot2_sensor_pin = 31
slots_sensor_pins = [29, 31]

# TODO: Add a RED and GREEN LEDs to indicate if there are slots available or not.
led_pin = 7
GPIO.setup(led_pin, GPIO.OUT, initial=GPIO.LOW)   # Set pin to be an output pin and set initial value to low (off)


#
# We keep the state of the sensors. We use it to compare if there was a change
# in any of them. If so, we publish a message to the MQTT broker.
#

# Initialize states
slots = dict()

for i in enumerate(range(slots_sensor_pins), start=1):
  slots[i] = ParkingSlot(slots_sensor_pins[i], i)
  GPIO.setup(slots_sensor_pins[i], GPIO.IN)     # Set pin to be an input pin




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
SECTION = "sciences"
TOPIC = f"{PARKING_ID}/{SECTION}"

## NOTE: this should be done by the server
# For this prototype, the number of sensors used is the total capacity of the parking lot
remaining_slots = len(slots_sensor_pins)
##

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

            today: datetime = datetime.datetime.today()
            date_str: str = today.date().strftime("%Y-%m-%d")
            time_str: str = today.time().strftime("%H:%M:%S")
            

            # Format of payload was defined as JSON:
            #   { "id": id, "status": status }
            payload = { "id": parking_slot.id, "status": parking_slot.state, "date": date_str, "time": time_str }
            client.publish(topic=TOPIC, payload=payload)
            time.sleep(0.2)

            ## NOTE: the station's client should send us the status of the remaining_slots
            # Increase by 1 if no car in the slot. Otherwise, decrease by 1
            remaining_slots += 1 if parking_slot.state == 0 else -1
            ##

    ## NOTE: the station's client should send us the status of the remaining_slots. This should be on
    # a MQTT callback on_message while subscribed to a specific topic
    # Turn on if no remaining slots. Turn off otherwise
    if remaining_slots == 0:
        GPIO.output(led_pin, GPIO.HIGH) # Turn on
    else:
        GPIO.output(led_pin, GPIO.LOW)  # Turn off
    ##
  
