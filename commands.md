

## Station's MQTT client
cd projects/uds/ift713/project/
source .ift713-venv/bin/activate
python -m station_client.py


## Server
cd projects/uds/ift713/project/
source .ift713-venv/bin/activate
uvicorn server:app --reload