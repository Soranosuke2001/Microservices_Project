"""
This script generates random data for transactions, users, and dates, and writes them to CSV files.
It creates 'transactions.csv' with transaction IDs, user IDs, and item IDs,
'users.csv' with game IDs, user IDs, and gun IDs, and 'dates.csv' with unique IDs and dates.
"""

import csv
import uuid
import random
from datetime import datetime, timedelta

# Generate transactions.csv with transaction data
with open("transactions.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["transaction_id", "user_id", "item_id"])
    writer.writeheader()

    for _ in range(1500):
        writer.writerow({
            "transaction_id": str(uuid.uuid4()),
            "user_id": str(uuid.uuid4()),
            "item_id": str(uuid.uuid4()),
        })

# Generate users.csv with user data
with open("users.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["game_id", "user_id", "gun_id"])
    writer.writeheader()

    for _ in range(1500):
        writer.writerow({
            "game_id": str(uuid.uuid4()),
            "user_id": str(uuid.uuid4()),
            "gun_id": str(uuid.uuid4()),
        })

# Generate a list of random datetimes with microseconds
datetimes = []
start_date = datetime(2020, 1, 1)
end_date = datetime(2024, 12, 31)

for _ in range(1000):
    random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    random_time = timedelta(hours=random.randint(0, 23),
                            minutes=random.randint(0, 59),
                            seconds=random.randint(0, 59),
                            microseconds=random.randint(0, 999999))  # Include random microseconds
    random_datetime = random_date + random_time

    datetimes.append(random_datetime)

# Generate dates.csv with datetime data including microseconds
with open("dates.csv", mode='w', newline='', encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["id", "date"])
    writer.writeheader()

    for date in datetimes:
        # Adjusted format to include microseconds with a decimal separator
        writer.writerow({
            "id": str(uuid.uuid4()),
            "date": date.strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"  # Truncate to milliseconds and append 'Z'
        })
