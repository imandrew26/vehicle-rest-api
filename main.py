from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = 'vehicles.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def validate_vehicle_data(data):
    required_fields = {
        'VIN': str,
        'ManufacturerName': str,
        'Description': str,
        'HorsePower': int,
        'ModelName': str,
        'ModelYear': int,
        'PurchasePrice': float,
        'FuelType': str
    }
    errors = {}

    for field, field_type in required_fields.items():
        if field not in data:
            errors[field] = "This field is required."
        elif not isinstance(data[field], field_type):
            errors[field] = f"Expected {field_type.__name__}, got {type(data[field]).__name__}."

    return errors

# GET - retrieve all vehicles
@app.route('/vehicle', methods=['GET'])
def get_all_vehicles():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Vehicles")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows]), 200

# GET - retrieve a specific vehicle
@app.route('/vehicle/<vin>', methods=['GET'])
def get_vehicle(vin):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Vehicles WHERE LOWER(VIN) = LOWER(?)", (vin,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return jsonify({"error": "Vehicle not found"}), 404
    return jsonify(dict(row)), 200

# POST - add a new vehicle
@app.route('/vehicle', methods=['POST'])
def add_vehicle():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Request must be JSON formatted"}), 400
    except Exception:
        return jsonify({"error": "Invalid JSON format"}), 400
    
    errors = validate_vehicle_data(data)
    if errors:
        return jsonify({"errors": errors}), 422
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            '''
            INSERT INTO Vehicles (VIN, ManufacturerName, Description, HorsePower, ModelName, ModelYear, PurchasePrice, FuelType)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            (
                data['VIN'], data['ManufacturerName'], data['Description'], 
                data['HorsePower'], data['ModelName'], data['ModelYear'], 
                data['PurchasePrice'], data['FuelType']
            )
        )
        conn.commit()
        response = dict(data)
        response['id'] = cursor.lastrowid
        status_code = 201
    except sqlite3.IntegrityError as e:
        response = {'error': str(e)}
        status_code = 400
    finally:
        conn.close()
    return jsonify(response), status_code

# PUT - update a specific vehicle
@app.route('/vehicle/<vin>', methods=['PUT'])
def update_vehicle(vin):
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Request must be JSON formatted"}), 400
    except Exception:
        return jsonify({"error": "Invalid JSON format"}), 400
    
    errors = validate_vehicle_data(data)
    if errors:
        return jsonify({"errors": errors}), 422

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''
        UPDATE Vehicles SET ManufacturerName = ?, Description = ?, HorsePower = ?, 
        ModelName = ?, ModelYear = ?, PurchasePrice = ?, FuelType = ?
        WHERE LOWER(VIN) = LOWER(?)
        ''',
        (
            data['ManufacturerName'], data['Description'], data['HorsePower'],
            data['ModelName'], data['ModelYear'], data['PurchasePrice'],
            data['FuelType'], vin
        )
    )
    conn.commit()
    updated_rows = cursor.rowcount
    conn.close()
    if updated_rows == 0:
        return jsonify({"error": "Vehicle not found"}), 404
    return jsonify(data), 200

# DELETE - delete a specific vehicle
@app.route('/vehicle/<vin>', methods=['DELETE'])
def delete_vehicle(vin):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Vehicles WHERE LOWER(VIN) = LOWER(?)", (vin,))
    conn.commit()
    deleted_rows = cursor.rowcount
    conn.close()
    if deleted_rows == 0:
        return jsonify({"error": "Vehicle not found"}), 404
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)