# kafka_perf_producer.py
# This is our "load generator" — it pumps airline JSON into the "raw" Kafka topic
# Think of it like Locust, but for Kafka instead of HTTP
#
# INSTALL FIRST:
#   pip install kafka-python
#
# RUN:
#   python kafka_perf_producer.py

import time
import json
from kafka import KafkaProducer          # The Kafka client library
from airline_payload import generate_flight_record  # Our fake data generator

# ─── CONFIG ───────────────────────────────────────────────────────────────────

KAFKA_BROKER = "localhost:9092"          # Where your Kafka is running
RAW_TOPIC    = "raw"                     # The first topic in your pipeline
TOTAL_RECORDS = 100                      # NFR: we want to send 100 records
TARGET_SECONDS = 60                      # NFR: within 60 seconds (1 minute)

# ─── SETUP PRODUCER ───────────────────────────────────────────────────────────

# KafkaProducer is the object that connects to Kafka and sends messages
# value_serializer converts our Python string into bytes (Kafka needs bytes)
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: v.encode("utf-8"),  # string → bytes

    # How long to wait for Kafka to confirm message was received (ms)
    request_timeout_ms=5000,

    # Number of retry attempts if a send fails
    retries=3
)

# ─── INJECT RECORDS ───────────────────────────────────────────────────────────

print(f"Starting load test: sending {TOTAL_RECORDS} records to '{RAW_TOPIC}'...")
print(f"NFR target: all {TOTAL_RECORDS} must be PROCESSED within {TARGET_SECONDS} seconds\n")

# Record when we started — we need this to measure total time
test_start_time = time.time()

# Track each message we send: {message_id: time_sent}
# We'll use this later to calculate end-to-end latency
sent_messages = {}

for i in range(TOTAL_RECORDS):

    # Generate one airline JSON record
    record_str = generate_flight_record()

    # Parse it back to get the message_id out (we need it for tracking)
    record_dict = json.loads(record_str)
    message_id = record_dict["message_id"]

    # Note the exact time we're sending this specific message
    send_time = time.time()
    sent_messages[message_id] = send_time

    # Send to the "raw" Kafka topic
    # .send() is non-blocking — it queues the message and returns immediately
    producer.send(RAW_TOPIC, value=record_str)

    # Print progress every 10 records
    if (i + 1) % 10 == 0:
        elapsed = time.time() - test_start_time
        rate = (i + 1) / elapsed
        print(f"  Sent {i+1}/{TOTAL_RECORDS} records | Rate: {rate:.1f} records/sec | Elapsed: {elapsed:.1f}s")

# flush() waits until ALL queued messages are actually sent to Kafka
# Without this, the program might exit before all messages are delivered
producer.flush()

total_send_time = time.time() - test_start_time

print(f"\n✓ All {TOTAL_RECORDS} records sent to '{RAW_TOPIC}'")
print(f"  Send time: {total_send_time:.2f} seconds")
print(f"  Send rate: {TOTAL_RECORDS / total_send_time:.1f} records/second")

# Save sent_messages to a file so the consumer script can use them for latency calc
import pickle
with open("sent_messages.pkl", "wb") as f:
    pickle.dump(sent_messages, f)

print(f"\nNow run: python kafka_perf_consumer.py")
print(f"That will consume from 'curated' and verify the NFR.\n")

producer.close()
