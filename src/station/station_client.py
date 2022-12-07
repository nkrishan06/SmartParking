# This module/script when executed listens to the proper MQTT topic and updates the
# "DB" (for simplicity the DB is just a Python dictionary)
# This "DB" is shared with server.py script.


# import paho.mqtt.client as mqtt
import json     # Maybe this module is just overhead, but it makes things simpler

from typing import Union
from fastapi import FastAPI
from bd_fake import parking_lot_states


print(f"id(parking_lot_states): {id(parking_lot_states):x}")

# NOTES:

# Topic structure:
#   parking_system_name/parking_id/section/
#
# Example
#   pk_ps/uds/sciences/
#     pk_ps:    It's the name of our parking system. It will not change. This is mainly to identify
#               our topic given that for this demo we are using a public broker.
#     uds:      An id assigned to the owner of the parking lot (or just the parking lot as is).
#               An owner/parking lot can have different sections/levels under their control.
#     sciences:  The specific section/level inside the parking lot we are interested in. For example,
#               the university has different sections: faculty of science, school of administration,
#               the stadium, the faculty of engineering, etc.

# In this project we assume that this program is running on the local system UdS, i.e., we
# manage the parking lots only for the UdS, specifically, the (possibly fictitious) science's parking lot.
# But we are going to subscribe to all parkings lots in the UdS, that's why we use the wildcard uds/#
#

PARKING_ID = "pk_ps/uds"
TOPIC = f"{PARKING_ID}/+"



# From https://github.com/eclipse/paho.mqtt.python#usage-and-api

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {str(rc)}")

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")
    client.subscribe(TOPIC)
    print(f"subscribed to {TOPIC}")


# TODO: what happens if several sensors send messages? Does paho implements something like a queue or we receive all the messages?
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(f"msg.topic: {msg.topic}")
    print(f"msg.payload: {str(msg.payload)}")

    # Process the message
    section_id = msg.topic[len(PARKING_ID)+1:]
    try:
        payload = json.loads(msg.payload)
    except Exception as error:
        print("Failed when parsing msg.payload.")
        print(error)
        return

    print(f"section_id:  {section_id}")
    print(f"payload:     {payload}")
    print(f"payload.id:  {payload['id']}, {type(payload['id'])}")
    print(f"payload.msg: {payload['msg']}, {type(payload['msg'])}")
    
    try:
        slot_id = int(payload['id'])
    except Exception as error:
        print(f"Failed to transform the slot id into integer: payload['id']={payload['id']}")
        print(error)
        return

    try:
        slot_status = int(payload['msg'])
    except Exception as error:
        print(f"Failed to transform the slot status into integer: payload['msg']={payload['msg']}")
        print(error)
        return

    try:
        # If the status changed then update the BD
        if parking_lot_states[section_id][slot_id] != slot_status:
            parking_lot_states[section_id][slot_id] = slot_status

        print(f"parking_lot_states[section_id]: {parking_lot_states[section_id]}")
        for key, val in parking_lot_states[section_id].items():
            print(f"  {key}: {val}")
            
    except KeyError as error:
        print(f"The key: slot_id={slot_id} does not exists in the DB.")
        print(error)
    except Exception as error:
        print("Unknown error.")
        print(error)




# # Create client and register the callbacks
# client = mqtt.Client()
# client.on_connect = on_connect
# client.on_message = on_message

# # client.connect("mqtt.eclipseprojects.io", 1883, 60)
# # client.connect("broker.hivemq.com", port=1883, keepalive=60)
# # client.connect("broker.emqx.io", port=1883, keepalive=60)
# client.connect_async("broker.emqx.io", port=1883, keepalive=60)

# # Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
# # Other loop*() functions are available that give a threaded interface and a manual interface.
# # _ = client.loop_forever()
# _ = client.loop_start()   # Non-blocking