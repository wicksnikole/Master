from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import random

app = Flask(__name__)

availabilities = []
appointments = []
reservations = []


#Allows providers to submit times they are available for appointments
@app.route('/providers/<provider_id>/availability', methods=['POST'])
def add_availability(provider_id):
    data = request.get_json()
    availability = {
        "id": len(availabilities) + 1,
        "provider_id": provider_id,
        "date": data['criteria'][0]['date'],
        "start_time": data['criteria'][0]['start_time'],
        "end_time": data['criteria'][0]['end_time']
    }
    availabilities.append(data)
    return jsonify({"message": "Availability added successfully", "availability": availability}), 201

#Allows a client to retrieve a list of available appointment slots
@app.route('/providers/<provider_id>/appointments', methods=['GET'])
def get_appointments(provider_id):
    slots = []
    for availability in availabilities:
        provider_id = availability['criteria'][0]['provider_id']
        start_time = availability['criteria'][0]['start_time']
        end_time = availability['criteria'][0]['end_time']
        date = availability['criteria'][0]['date']
        start_hours, start_minutes = map(int, start_time.split(":"))
        end_hours, end_minutes = map(int, end_time.split(":"))
        while (start_hours < end_hours) or (start_hours == end_hours and start_minutes < end_minutes):
            end_slot_minutes = start_minutes + 15 
            end_slot_hours = start_hours
            if end_slot_minutes >= 60:
                end_slot_minutes -= 60
                end_slot_hours += 1
            slots.append({
                "provider_id": provider_id,
                "date": date,
                "start_time": f"{start_hours:02}:{start_minutes:02}",
                "end_time": f"{end_slot_hours:02}:{end_slot_minutes:02}"
            })
            start_hours, start_minutes = end_slot_hours, end_slot_minutes
    return jsonify(slots)


#Allows clients to reserve an available appointment slot
@app.route('/appointments/reserve', methods=['POST'])
def reserve_appointment():
    data = request.get_json()
    appointment = {
        "id": random.randrange(100, 900, 3),
        "provider_id": data['criteria'][0]["provider_id"],
        "client_id": data['criteria'][0]["client_id"],
        "date": data['criteria'][0]["date"],
        "start_time": data['criteria'][0]["start_time"],
        "end_time": data['criteria'][0]["end_time"],
        "status": "reserved",
        'reserved_at': datetime.now()
    }
    provider_data = data['criteria'][0]["provider_id"]
    start_data = data['criteria'][0]["date"] + " " + data['criteria'][0]["start_time"]
    if datetime.strptime(start_data, '%Y-%m-%d %H:%M') <= datetime.now() + timedelta(hours=24):
        return jsonify({'error': 'Reservations must be made at least 24 hours in advance'}), 400
    
    
    isAvailable = False    #check if the appointment is available
    for availability in availabilities:
        start_availability = availability['criteria'][0]['date'] + " " + availability['criteria'][0]['start_time']
        provider_id = availability['criteria'][0]['provider_id']

        if start_data == start_availability and provider_id == provider_data: #if start date/time exists for the specific provider
            isAvailable = True
        else:
            isAvailable = False

    if isAvailable == True:
      appointments.append(appointment)
      return jsonify({"message": "Appointment reserved successfully", "appointment": appointment}), 201
    
    else:
        return jsonify({"message": "ERROR: Availability not found for the specified provider"}), 400


#Allows clients to confirm their reservation
@app.route('/appointments/confirm', methods=['POST'])
def confirm_appointment():
    data = request.get_json()
    appointment_id = data['criteria'][0]["appointment_id"]
    for appointment in appointments:
        if datetime.now() > appointment['reserved_at'] + timedelta(minutes=30):
          del appointment
          return jsonify({'error': 'Reservation expired'}), 400

        if appointment['id'] == appointment_id:
            appointment["status"] = "confirmed"
            return jsonify({"message": "Appointment confirmed successfully", "appointment": appointment})
    return jsonify({"message": "Appointment not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
