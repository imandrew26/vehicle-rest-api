# Vehicle API

A simple REST API for managing vehicle records.

## Routes

- GET /vehicle - Retrieve a list of all vehicles.
- POST /vehicle - Create a new vehicle record.
- GET /vehicle/<vin> - Retrieve details of a specific vehicle by its VIN.
- PUT /vehicle/<vin> - Update an existing vehicle's details by its VIN.
- DELETE /vehicle/<vin> - Delete a specific vehicle record by its VIN.

## Example Request Body

{
  "VIN": "abcdefg",
  "ManufacturerName": "Honda",
  "Description": "Small, efficient sedan",
  "HorsePower": 158,
  "ModelName": "Civic",
  "ModelYear": 2017,
  "PurchasePrice": 20000.00,
  "FuelType": "Gasoline"
}

## Requirements

- Python 3.x
- Flask