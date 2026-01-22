# import necessary modules and initialize Flask app
from models import *
from flask import Flask, jsonify, request
from hashlib import sha256

app = Flask(__name__)

@app.route('/add_employee', methods=['POST'])
def api_add_employee():
    """
    Add a new employee to the database.
    Needs 'name', 'email', 'password', and optional 'role' in JSON body.
    """
    # extart data from the request
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    # hash the password
    password_hash = sha256(password.encode()).hexdigest()
    role = data.get('role', 'employee')
    # add employee to the database
    success = add_employee(name, email, password_hash, role)
    if success:
        return jsonify({'message': 'Employee added successfully.'}), 201
    else:
        return jsonify({'message': 'Error adding employee.'}), 500

@app.route('/login', methods=['POST'])
def api_login_user():
    """
    Login a user.
    Needs 'email' and 'password' in JSON body.
    """
    # extract data from the request
    data = request.json
    email = data.get('email')
    password = data.get('password')
    # hash the password
    password_hash = sha256(password.encode()).hexdigest()
    # attempt to login the user
    user = login_user(email, password_hash)
    if user:
        return jsonify({'message': 'Login successful.', 'user': user}), 200
    else:
        return jsonify({'message': 'Invalid credentials.'}), 401
    
@app.route('/record_attendance', methods=['POST'])
def api_record_attendance():
    """
    Record attendance for an employee.
    Needs 'employee_id', 'date', and optional 'check_in' and 'check_out' in JSON body.
    """
    # extract data from the request
    data = request.json
    employee_id = data.get('employee_id')
    # convert the date string to a date object
    date = data.get('date')
    # convert the time into datetime objects if they exist also in HH:MM:SS format
    check_in = data.get('check_in', None)
    check_out = data.get('check_out', None)
    # convert time into HH:MM:SS format
    print("API Check-in:", check_in)
    print("API Check-out:", check_out)
    print("API Date:", date)
    # attempt to record attendance
    success = record_attendance(employee_id, date, check_in, check_out)
    if success:
        return jsonify({'message': 'Attendance recorded successfully.'}), 200
    else:
        return jsonify({'message': 'Error recording attendance.'}), 500
    
@app.route('/adjust_attendance', methods=['POST'])
def api_adjust_attendance():
    """
    Adjust attendance for an employee.
    Needs 'employee_id', 'date', 'adjustment_type', and optional
    'reason' in JSON body.
    """
    data = request.json
    employee_id = data.get('employee_id')
    date = data.get('date')
    date = datetime.date.fromisoformat(date)
    adjustment_type = data.get('adjustment_type')
    if adjustment_type == "Overtime":
        success = add_overtime_adjustment(employee_id, date)
        if success:
            return jsonify({'message': 'Overtime adjustment added successfully.'}), 200
        else:
            return jsonify({'message': 'Error adding overtime adjustment.'}), 500
    assert adjustment_type in ["late", "early_exit", "Both"], "Invalid adjustment type."
    success = add_adjustment(employee_id, date, adjustment_type)
    if success:
        return jsonify({'message': 'Attendance adjusted successfully.'}), 200
    else:
        return jsonify({'message': 'Error adjusting attendance.'}), 500

@app.route('/get_attendance/<int:employee_id>', methods=['GET'])
def api_get_attendance(employee_id):
    """
    get the attendance for an employee.
    Needs 'employee_id' as URL parameter. Start and end date as optional query parameters.
    """
    data = request.json
    start_date = data.get('start_date', None)
    end_date = data.get('end_date', None)
    attendance = get_employee_attendance(employee_id=employee_id, start_date=datetime.datetime.fromisoformat(start_date), end_date=datetime.datetime.fromisoformat(end_date))
    if attendance is not None:
        return jsonify({'attendance': attendance}), 200
    else:
        return jsonify({'message': 'Error retrieving attendance.'}), 500
    
@app.route('/get_adjustment/<int:employee_id>', methods=['GET'])
def api_get_adjustment(employee_id):
    """
    get the adjustments for an employee.
    Needs 'employee_id' as URL parameter.
    """
    adjustment = get_employee_adjustments(employee_id)
    if adjustment is not None:
        return jsonify({'adjustment': adjustment}), 200
    else:
        return jsonify({'message': 'Error retrieving adjustment.'}), 500

if __name__ == "__main__":
    if init_db():
        app.run(debug=True)
    else:
        print("Error initializing the database.")
