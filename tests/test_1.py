import pytest
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from main import app, get_db_connection

@pytest.fixture
def client():

    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            conn = get_db_connection()
            conn.execute("DROP TABLE IF EXISTS Vehicles;")
            conn.executescript(open("schema.sql", "r").read())
            conn.close()
        yield client

# Tests

def test_get_empty_vehicles(client):
    """Test retrieving vehicles when no records exist."""
    response = client.get('/vehicle')
    assert response.status_code == 200
    assert response.json == []

def test_add_vehicle_success(client):
    """Test adding a vehicle."""
    vehicle_data = {
        "VIN": "abcdefg",
        "ManufacturerName": "Honda",
        "Description": "Small, efficient sedan",
        "HorsePower": 158,
        "ModelName": "Civic",
        "ModelYear": 2017,
        "PurchasePrice": 20000.00,
        "FuelType": "Gasoline"
    }
    response = client.post('/vehicle', json=vehicle_data)
    assert response.status_code == 201
    assert response.json['id'] > 0

def test_get_vehicle_by_vin_success(client):
    """Test retrieving a specific vehicle by VIN."""
    vehicle_data = {
        "VIN": "abcdefg",
        "ManufacturerName": "Honda",
        "Description": "Small, efficient sedan",
        "HorsePower": 158,
        "ModelName": "Civic",
        "ModelYear": 2017,
        "PurchasePrice": 20000.00,
        "FuelType": "Gasoline"
    }
    client.post('/vehicle', json=vehicle_data)
    response = client.get('/vehicle/abcdefg')
    assert response.status_code == 200
    assert response.json['VIN'] == "abcdefg"

def test_update_vehicle_success(client):
    """Test updating an existing vehicle."""
    vehicle_data = {
        "VIN": "abcdefg",
        "ManufacturerName": "Honda",
        "Description": "Small, efficient sedan",
        "HorsePower": 158,
        "ModelName": "Civic",
        "ModelYear": 2017,
        "PurchasePrice": 20000.00,
        "FuelType": "Gasoline"
    }

    client.post('/vehicle', json=vehicle_data)

    updated_data = {
    "VIN": "abcdefg",
    "ManufacturerName": "Honda",
    "Description": "Updated description",
    "HorsePower": 160,
    "ModelName": "Civic",
    "ModelYear": 2018,
    "PurchasePrice": 21000.00,
    "FuelType": "Gasoline"
    }

    response = client.put('/vehicle/abcdefg', json=updated_data)
    assert response.status_code == 200
    assert response.json['Description'] == "Updated description"

def test_delete_vehicle_success(client):
    """Test deleting an existing vehicle."""
    vehicle_data = {
        "VIN": "abcdefg",
        "ManufacturerName": "Honda",
        "Description": "Small, efficient sedan",
        "HorsePower": 158,
        "ModelName": "Civic",
        "ModelYear": 2017,
        "PurchasePrice": 20000.00,
        "FuelType": "Gasoline"
    }
    client.post('/vehicle', json=vehicle_data)

    response = client.delete('/vehicle/abcdefg')
    assert response.status_code == 204

def test_add_vehicle_with_missing_fields(client):
    """Test adding a vehicle with missing required fields."""
    vehicle_data = {
        "VIN": "xyz123",
        "ManufacturerName": "Toyota",
        "HorsePower": 120,
        "FuelType": "Gasoline"
    }
    response = client.post('/vehicle', json=vehicle_data)
    assert response.status_code == 422
    assert "errors" in response.json

def test_add_duplicate_vehicle(client):
    """Test adding a vehicle with a duplicate VIN."""
    vehicle_data = {
        "VIN": "duplicate123",
        "ManufacturerName": "Ford",
        "Description": "Compact SUV",
        "HorsePower": 180,
        "ModelName": "Escape",
        "ModelYear": 2020,
        "PurchasePrice": 25000.00,
        "FuelType": "Gasoline"
    }
    client.post('/vehicle', json=vehicle_data)
    response = client.post('/vehicle', json=vehicle_data)
    assert response.status_code == 400
    assert "error" in response.json

def test_get_nonexistent_vehicle(client):
    """Test retrieving a vehicle that does not exist."""
    response = client.get('/vehicle/nonexistentVIN')
    assert response.status_code == 404
    assert "error" in response.json

def test_update_nonexistent_vehicle(client):
    """Test updating a vehicle that does not exist."""
    updated_data = {
        "VIN": "nonexistent123",
        "ManufacturerName": "Mazda",
        "Description": "Updated description",
        "HorsePower": 200,
        "ModelName": "CX-5",
        "ModelYear": 2021,
        "PurchasePrice": 28000.00,
        "FuelType": "Gasoline"
    }
    response = client.put('/vehicle/nonexistent123', json=updated_data)
    assert response.status_code == 404
    assert "error" in response.json

def test_delete_nonexistent_vehicle(client):
    """Test deleting a vehicle that does not exist."""
    response = client.delete('/vehicle/nonexistentVIN')
    assert response.status_code == 404
    assert "error" in response.json
