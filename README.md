# Appointment Scheduling API

This is a RESTful API for managing appointment scheduling, including provider availability, appointment slot retrieval, reservation, and confirmation. It is built using Flask.

## Requirements

- Python 3.x
- Flask

# Notes


If time allowed, I would have stored and updated the providers availability and the reservations in a database.



## Test Cases using Postman


http://127.0.0.1:5000/providers/1/availability

{
    "criteria": [
        {
            "provider_id": 1,
            "date": "2024-08-13",
            "start_time": "11:00",
            "end_time": "15:00"
        }
     ]
}


http://127.0.0.1:5000/appointments/reserve

{
    "criteria": [
        {
            "provider_id": 1,
            "client_id": 123,
            "date": "2024-08-13",
            "start_time": "13:15",
            "end_time": "13:30"
        }
     ]
}

http://127.0.0.1:5000/appointments/confirm

{
    "criteria": [
        {
            "appointment_id": 1
        }
     ]
}
