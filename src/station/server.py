from typing import Union
from fastapi import FastAPI
import logging
import paho.mqtt.client as mqtt

from bd_fake import parking_lot_states
from station_client import on_connect, on_message



### Configure logging
# from https://www.codeschat.com/article/145.html
logger = logging.getLogger()
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
fh = logging.FileHandler(filename='./server.log')
formatter = logging.Formatter(
    "%(asctime)s - %(module)s - %(funcName)s - line:%(lineno)d - %(levelname)s - %(message)s"
)

ch.setFormatter(formatter)
fh.setFormatter(formatter)
logger.addHandler(ch) #Exporting logs to the screen
logger.addHandler(fh) #Exporting logs to a file

logger = logging.getLogger(__name__)

logger.info(f"id(parking_lot_states): {id(parking_lot_states):x}")
###



### Setup station's MQTT client
# https://github.com/eclipse/paho.mqtt.python#loop_start--loop_stop

# Create client and register the callbacks
client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

# client.connect("broker.emqx.io", port=1883, keepalive=60)
client.connect_async("broker.emqx.io", port=1883, keepalive=60)

# Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a manual interface.
# _ = client.loop_forever()
_ = client.loop_start()   # Non-blocking
###



### FastAPI stuff
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/uds/{lot_id}")
def read_item(lot_id: str):
    return [{"slot_id": slot_id, "status": status} for slot_id, status in parking_lot_states[lot_id].items()]


@app.get("/uds/{lot_id}/slot/{slot_id}")
def read_lot_slot_status(lot_id: str, slot_id: int):
    return {"slot_id": slot_id, "status": parking_lot_states[lot_id][slot_id]}
###