# kafka_perf_consumer.py
# This reads from the "curated" topic and checks if the NFR was met:
# "100 records processed within 60 seconds"
# It also measures per-message latency (time from raw → curated)
#
# RUN (after kafka_perf_producer.py):
#   python kafka_perf_consumer.py

import time
import json
import pickle
from kafka import KafkaConsumer          # The Kafka client library for reading

# ─── CONFIG ───────────────────────────────────────────────────────────────────

KAFKA_BROKER   = "localhost:9092"
CURATED_TOPIC  = "curated"             # We read from the FINAL topic
TOTAL_RECORDS  = 100                   # How many we expect to see
NFR_SECONDS    = 60                    # Must all arrive within this time
TIMEOUT_WAIT   = 120                   # Stop waiting after 2 minutes regardless

# ─── LOAD SEND TIMESTAMPS ─────────────────────────────────────────────────────

# Load the send times saved by the producer script
# sent_messages = {message_id: time_when_it_was_sent_to_raw}
try:
    with open("sent_messages.pkl", "rb") as f:
        sent_messages = pickle.load(f)
    print(f"Loaded {len(sent_messages)} sent message timestamps")
except FileNotFoundError:
    print("ERROR: Run kafka_perf_producer.py first!")
    exit(1)

# ─── SETUP CONSUMER ───────────────────────────────────────────────────────────

# KafkaConsumer connects to Kafka and reads messages from a topic
# auto_offset_reset="earliest" means: start reading from the beginning of the topic
# value_deserializer converts bytes back to a Python string
consumer = KafkaConsumer(
    CURATED_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    auto_offset_reset="earliest",       # Read from beginning of topic
    consumer_timeout_ms=5000,           # Stop polling if no new messages for 5 seconds
    value_deserializer=lambda v: v.decode("utf-8"),  # bytes → string
    group_id="perf-test-consumer"       # Consumer group ID — Kafka uses this for tracking
)

# ─── CONSUME AND MEASURE ──────────────────────────────────────────────────────

print(f"\nListening on '{CURATED_TOPIC}' topic...")
print(f"NFR: {TOTAL_RECORDS} records must arrive within {NFR_SECONDS} seconds\n")

# Track results
received_count  = 0          # How many curated messages we've seen
latencies       = []         # List of per-message latencies in seconds
first_msg_time  = None       # When the first curated message arrived
last_msg_time   = None       # When the last curated message arrived
nfr_passed      = False      # Did we meet the NFR?

consume_start = time.time()

# Loop through messages as they arrive in the curated topic
for message in consumer:

    # message.value is our JSON string — parse it back to a dict
    try:
        record = json.loads(message.value)
    except json.JSONDecodeError:
        print(f"  WARNING: Could not parse message: {message.value[:80]}")
        continue

    received_count += 1
    now = time.time()

    # Track timing of first and last message
    if first_msg_time is None:
        first_msg_time = now

    last_msg_time = now

    # ── Latency calculation ──
    # If the curated record still has message_id, we can calculate
    # how long it took to go from raw → curated
    message_id = record.get("message_id")
    if message_id and message_id in sent_messages:
        latency = now - sent_messages[message_id]  # seconds
        latencies.append(latency)

    # Print progress every 10 messages
    if received_count % 10 == 0:
        elapsed = now - consume_start
        print(f"  Received {received_count}/{TOTAL_RECORDS} | Elapsed: {elapsed:.1f}s")

    # Stop if we've received everything we expected
    if received_count >= TOTAL_RECORDS:
        break

    # Stop if we've been waiting too long (safety exit)
    if (now - consume_start) > TIMEOUT_WAIT:
        print(f"\nTIMEOUT: waited {TIMEOUT_WAIT}s, only received {received_count} records")
        break

consumer.close()

# ─── NFR REPORT ───────────────────────────────────────────────────────────────

total_pipeline_time = (last_msg_time - first_msg_time) if (first_msg_time and last_msg_time) else 0
throughput = received_count / total_pipeline_time if total_pipeline_time > 0 else 0

# Check if NFR passed: did all 100 records arrive within 60 seconds?
nfr_passed = (received_count >= TOTAL_RECORDS) and (total_pipeline_time <= NFR_SECONDS)

print("\n" + "="*55)
print("  PERFORMANCE TEST RESULTS")
print("="*55)

print(f"\n  Records sent:          {TOTAL_RECORDS}")
print(f"  Records received:      {received_count}")
print(f"  Records missed:        {TOTAL_RECORDS - received_count}")

print(f"\n  Total pipeline time:   {total_pipeline_time:.2f} seconds")
print(f"  Throughput:            {throughput:.1f} records/second")
print(f"  Throughput/min:        {throughput * 60:.0f} records/minute")

if latencies:
    avg_latency = sum(latencies) / len(latencies)
    min_latency = min(latencies)
    max_latency = max(latencies)
    # p95: sort latencies, take the value at the 95th percentile position
    sorted_lat = sorted(latencies)
    p95_index = int(len(sorted_lat) * 0.95)
    p95_latency = sorted_lat[p95_index]

    print(f"\n  End-to-end latency (raw → curated):")
    print(f"    Average:  {avg_latency:.3f}s")
    print(f"    Min:      {min_latency:.3f}s")
    print(f"    Max:      {max_latency:.3f}s")
    print(f"    P95:      {p95_latency:.3f}s   ← 95% of records processed faster than this")

print(f"\n  NFR: 100 records processed in 60 seconds")
print(f"  NFR STATUS: {'✓ PASSED' if nfr_passed else '✗ FAILED'}")

if not nfr_passed:
    if received_count < TOTAL_RECORDS:
        print(f"  REASON: Only {received_count}/{TOTAL_RECORDS} records made it to curated")
    else:
        print(f"  REASON: Took {total_pipeline_time:.1f}s, limit is {NFR_SECONDS}s")

print("="*55)
