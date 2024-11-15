#!/bin/bash

# Virtual environment
source .venv/bin/activate

# Initialize database
if ! sqlite3 vehicles.db "SELECT name FROM sqlite_master WHERE type='table' AND name='Vehicles';" | grep -q 'Vehicles'; then
    echo "Initializing database."
    sqlite3 vehicles.db < schema.sql
else
    echo "Database previously initialized."
fi

# Run the Flask server
flask --app main.py run