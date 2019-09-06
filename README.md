# Sensor Data Service

## Usage

All responses will have the form

```json
{
    "data": "Mixed type holding the content of the response",
    "message": "Description of what happened"
}
```

Subsequent response definitions will only detail the expected value of the `data field`

### List all devices

**Definition**

`GET /devices`

**Response**

- `200 OK` on success

```json
[
    {
    "gyroscope_id": 1,
    "trip_id": 3,
    "x_value": 1.11304,
    "y_value": 1.66957,
    "z_value": -0.83478,
    "timestamp": "2017-01-19 16:19:03.051205"
    },
    {
    "gyroscope_id": 2,
    "trip_id": 3,
    "x_value": 1.46087,
    "y_value": 1.94783,
    "z_value": -0.69565,
    "timestamp": "2017-01-19 16:19:03.093157"
    },
]
```

### Add new sensor data

**Definition**

`POST /devices`

**Arguments**

- `"gyroscope_id":string` a globally unique identifier for this gyroscope sensor
- `"trip_id":string` Trip ID
- `"x_value":string` X Value
- `"y_value":string` Y Value
- `"z_value":string` Z Value
- `"timestamp":string` Time Stamp

  
If the gyroscope with the given gyrscope_id already exists, the existing device will be overwritten.

**Response**

- `201 Created` on success

```json
{
    "gyroscope_id": 2,
    "trip_id": 3,
    "x_value": 1.46087,
    "y_value": 1.94783,
    "z_value": -0.69565,
    "timestamp": "2017-01-19 16:19:03.093157"
}
```

## Lookup device details

`GET /sensor/<identifier>`

**Response**

- `404 Not Found` if the sensor data not exist
- `200 OK` on success

```json
{
   "gyroscope_id": 2,
    "trip_id": 3,
    "x_value": 1.46087,
    "y_value": 1.94783,
    "z_value": -0.69565,
    "timestamp": "2017-01-19 16:19:03.093157"
}
```

## Delete a device

**Definition**

`DELETE /sensor/<identifier>`

**Response**

- `404 Not Found` if the device does not exist
- `204 No Content` on success