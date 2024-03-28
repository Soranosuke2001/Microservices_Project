#!/bin/sh
# Exit script on any error
set -e

# Initialize the database
echo "Initializing database..."
python create_database.py

# Start the main application
echo "Starting the application..."
exec python app.py
