import json
import sys
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch


# Connection settings
es = Elasticsearch("http://elasticsearch:9200")
INDEX_NAME = "realtime_analytics"

# Consumer configuration
consumer = KafkaConsumer(
    'user_interactions', # topic 
    bootstrap_servers='kafka:9092',# kafka container
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    auto_offset_reset='latest', # as no offset commit
    group_id='analytics_engine' # cosumer group
)
#700
# Global state for stream processing
user_hits = {}
item_hits = {}
event_counter = 0
THRESHOLD = 50

for msg in consumer:
    data = msg.value
    u_id = data['user_id']
    i_id = data['item_id']
    
    event_counter += 1
    
    # Calculate user averages
    user_hits[u_id] = user_hits.get(u_id, 0) + 1
    avg_per_user = event_counter / len(user_hits)
    
    # Calculate item statistics
    item_hits[i_id] = item_hits.get(i_id, 0) + 1
    counts = item_hits.values()
    max_count = max(counts)
    min_count = min(counts)

    # Simple alerting logic
    alert_flag = "NORMAL"
    if item_hits[i_id] >= THRESHOLD:
        alert_flag = "CRITICAL"
        print(f"Threshold exceeded: {i_id} reached {item_hits[i_id]} hits")

    # Document schema for Elasticsearch
    payload = {
        "user_id": u_id,
        "item_id": i_id,
        "type": data['interaction_type'],
        "timestamp": data['timestamp'],
        "avg_user_activity": round(avg_per_user, 2),
        "item_total": item_hits[i_id],
        "global_max": max_count,
        "global_min": min_count,
        "status": alert_flag
    }

    try:
        es.index(index=INDEX_NAME, document=payload)
        # Log progress for monitoring
        print(f"Processed event {event_counter}: {u_id} | Avg: {round(avg_per_user, 2)}")
        sys.stdout.flush()
    except Exception as err:
        print(f"Indexing error: {err}")
        sys.stdout.flush()