# airline_payload.py
# This file just holds a sample airline JSON record
# This is the data we will pump into the "raw" Kafka topic

import json
import uuid
import random
from datetime import datetime

# List of sample airlines to rotate through
AIRLINES = ["IndiGo", "Air India", "SpiceJet", "Vistara", "GoFirst"]
AIRPORTS = ["BOM", "DEL", "BLR", "HYD", "MAA", "CCU"]
STATUSES = ["ON_TIME", "DELAYED", "CANCELLED", "BOARDING"]


def generate_flight_record():
    """
    Creates one fake airline JSON record.
    Each call returns a slightly different record (random flight number, times, etc.)
    This simulates real data coming in.
    """

    record = {
        # Unique ID for this specific message — helps us track it end to end
        "message_id": str(uuid.uuid4()),

        # Timestamp of when this record was created — we use this to measure latency later
        "produced_at": datetime.utcnow().isoformat(),

        # Airline flight data
        "flight_number": f"{random.choice(['6E','AI','SG','UK','G8'])}{random.randint(100, 999)}",
        "airline": random.choice(AIRLINES),
        "origin": random.choice(AIRPORTS),
        "destination": random.choice(AIRPORTS),
        "scheduled_departure": "2024-06-01T08:00:00",
        "actual_departure": "2024-06-01T08:15:00",
        "delay_minutes": random.randint(0, 120),
        "status": random.choice(STATUSES),
        "passengers_boarded": random.randint(50, 180),
        "aircraft_type": random.choice(["A320", "B737", "ATR72"])
    }

    # Return it as a JSON string — Kafka messages are bytes/strings, not Python dicts
    return json.dumps(record)
