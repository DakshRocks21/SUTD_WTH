# LORA Server

This is the server for the LORA project. It represents the backend of the project and is responsible for handling the data from the sensors and saving it to the database.


```json
    {
        "nodeId": int, // The id of the node that sent the data
        "status": int, // The status of the node (0: inactive, 1: SOS, 2: sensor data)
        "sos" : string, // UID used to identify the SOS, and the user that sent it (this is only present if the status is 1)
        "data" : { // The sensor data, see below (this is only present if the status is 2)
            "temperature": float, // The temperature value
            "humidity": float, // The humidity value
            "pressure": float, // The pressure value
        }
    }
```

```json
// SOS Data to be written to the database
// The location is calculated from the node's location (previously stored in the database)
"sos": [
    {
        "latitude": float, // The latitude of the SOS
        "longitude": float, // The longitude of the SOS
        "time": string, // The time of the SOS
        "message": string, // The message of the SOS
    }
]
```
