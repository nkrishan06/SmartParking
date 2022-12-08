# 

Created and tested with Python version 3.10

## To launch

### PC
- Download the project.

In a terminal
- Move to the project's root.
- It's recommended to create a virtual environment inside the project's root directory
    ```
    python -m venv .venv
    ```
- Activate the virtual env
    ```
    source .venv/bin/activate
    ```
- Then
    ```
    pip install -r requirements.txt
    cd src/station
    uvicorn server:app --reload
    ```
- Open a browser using the address indicated by the server's output.

- To manually test, you can we use the following public broker: https://www.emqx.com/en/mqtt/public-mqtt5-broker
- Subscribe to the topic `pk_ps/uds/sciences/#`
- The messages must be of type JSON with the following structure:
    ```js
    {
        "id": "id_number",
        "status": "[1|0]",
        "date": "yyyy-mm-dd"
        "time": "HH:MM:ss"
    }
    ```


### Raspberry Pi
In a terminal, execute
```
pip install paho-mqtt
```

Just copy the files from the directory `src/rpi` and place them in a directory in the Raspberry Pi

Launch the script:
```
python3 rpi_client.py
```

