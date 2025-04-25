from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# DB connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tusya123",
    database="smartcitydb"
)
cursor = db.cursor(dictionary=True)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add-citizen')
def add_citizen_form():
    return render_template('add_citizen.html')

@app.route('/add-address')
def add_address_form():
    return render_template('add_address.html')

@app.route('/add-device')
def add_device_form():
    return render_template('add_device.html')

@app.route('/add-health')
def add_health_form():
    return render_template('add_health.html')

@app.route('/add-vehicle')
def add_vehicle_form():
    return render_template('add_vehicle.html')

@app.route('/add-emergency')
def add_emergency_form():
    return render_template('add_emergency.html')

@app.route('/api/add-citizen', methods=['POST'])
def api_add_citizen():
    data = request.get_json()
    try:
        cursor.execute("SELECT IFNULL(MAX(CitizenID), 0) + 1 AS next_id FROM citizens")
        next_id = cursor.fetchone()['next_id']

        cursor.execute("""
            INSERT INTO citizens (CitizenID, Name, Email, PhoneNumber, DateOfBirth)
            VALUES (%s, %s, %s, %s, %s)
        """, (next_id, data['name'], data['email'], data['phone'], data['dob']))
        db.commit()

        return jsonify({"message": "Citizen added successfully!", "citizen_id": next_id})
    except mysql.connector.Error as err:
        return jsonify({"message": f"Error: {err}"}), 500

@app.route('/api/add-address', methods=['POST'])
def api_add_address():
    data = request.get_json()
    try:
        cursor.execute("SELECT IFNULL(MAX(AddressID), 0) + 1 AS next_id FROM addresses")
        next_id = cursor.fetchone()['next_id']

        cursor.execute("""
            INSERT INTO addresses (AddressID, CitizenID, Street, City, State, ZipCode)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (next_id, data['citizen_id'], data['street'], data['city'], data['state'], data['zipcode']))
        db.commit()

        return jsonify({"message": "Address added successfully!", "address_id": next_id})
    except mysql.connector.Error as err:
        return jsonify({"message": f"Error: {err}"}), 500
@app.route("/form")
def form_selector():
    form_type = request.args.get("type")
    return render_template(f"add_{form_type}.html")


@app.route("/api/add-vehicle", methods=["POST"])
def add_vehicle():
    data = request.form
    cursor = mysql.connection.cursor()
    cursor.execute("""
        INSERT INTO vehicles (CitizenID, LicensePlate, VehicleType, Model, Year, AddressID)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (data["citizen_id"], data["license_plate"], data["vehicle_type"], data["model"], data["year"], data["address_id"]))
    mysql.connection.commit()
    cursor.close()
    return "Vehicle Added!"


@app.route("/api/add-health", methods=["POST"])
def add_health():
    data = request.form
    cursor = mysql.connection.cursor()
    cursor.execute("""
        INSERT INTO citizen_health_data (CitizenID, BloodType, Allergies, MedicalConditions, LastCheckupDate)
        VALUES (%s, %s, %s, %s, %s)
    """, (data["citizen_id"], data["blood_type"], data["allergies"], data["conditions"], data["checkup_date"]))
    mysql.connection.commit()
    cursor.close()
    return "Health Record Added!"


@app.route('/api/add-device', methods=['POST'])
def api_add_device():
    data = request.get_json()
    try:
        cursor.execute("SELECT IFNULL(MAX(DeviceID), 0) + 1 AS next_id FROM smart_devices")
        next_id = cursor.fetchone()['next_id']

        cursor.execute("""
            INSERT INTO smart_devices (DeviceID, CitizenID, DeviceType, DeviceName, InstallationDate)
            VALUES (%s, %s, %s, %s, %s)
        """, (next_id, data['citizen_id'], data['device_type'], data['device_name'], data['install_date']))
        db.commit()

        return jsonify({"message": "Device added successfully!", "device_id": next_id})
    except mysql.connector.Error as err:
        return jsonify({"message": f"Error: {err}"}), 500

@app.route('/api/add-emergency', methods=['POST'])
def api_add_emergency():
    data = request.get_json()
    try:
        cursor.execute("SELECT IFNULL(MAX(EmergencyContactID), 0) + 1 AS next_id FROM emergency_contact")
        next_id = cursor.fetchone()['next_id']

        cursor.execute("""
            INSERT INTO emergency_contact (EmergencyContactID, CitizenID, ContactName, Relationship, PhoneNumber, Address)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (next_id, data['citizen_id'], data['contact_name'], data['relationship'], data['phone_number'], data['address']))
        db.commit()

        return jsonify({"message": "Contact added successfully!", "address_id": next_id})
    except mysql.connector.Error as err:
        return jsonify({"message": f"Error: {err}"}), 500

def api_add_employee():
    data = request.get_json()
    try:
        # Auto-generate the next EmpID
        cursor.execute("SELECT IFNULL(MAX(EmpID), 0) + 1 AS next_emp_id FROM employee")
        next_emp_id = cursor.fetchone()['next_emp_id']

        # Auto-generate CitizenID and Name (dummy for this case)
        cursor.execute("SELECT IFNULL(MAX(CitizenID), 0) + 1 AS next_citizen_id FROM employee")
        next_citizen_id = cursor.fetchone()['next_citizen_id']
        name = f"Employee{next_emp_id}"  # Auto-generated name, you can modify this logic

        cursor.execute("""
            INSERT INTO employee (EmpID, CitizenID, Name, Skills, Projects, Department, ManagerName, Certifications, HireDate)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            next_emp_id,
            data[],
            name,
            data['skills'],
            data['projects'],
            data['department'],
            data['manager_name'],
            data['certifications'],
            data['hire_date']
        ))
        db.commit()

        return jsonify({"message": "Employee data added successfully!", "emp_id": next_emp_id})
    except Error as err:
        return jsonify({"message": f"Error: {err}"}), 500
if __name__ == '__main__':
    app.run(debug=True)
