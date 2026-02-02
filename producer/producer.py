import json
import time
import random
from datetime import datetime
from kafka import KafkaProducer

# Kafka connection
producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)




# Simulation parameters
USERS = ["user_1", "user_2", "user_3", "user_4", "user_5"]
ITEMS = ["item_A", "item_B", "item_C"]
TYPES = ["click", "view", "purchase"]

# Data distribution weights
U_WEIGHTS = [40, 10, 10, 30, 10] 
I_WEIGHTS = [65, 25, 10]

INTERVAL = 0.1
# 10 events / second
# 120 per min

print("Producer initialized. Generating traffic simulation...")

try:
    while True:
        # Generate weighted random sample
        record = {
            "user_id": random.choices(USERS, weights=U_WEIGHTS)[0],
            "item_id": random.choices(ITEMS, weights=I_WEIGHTS)[0],
            "interaction_type": random.choice(TYPES),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        producer.send('user_interactions', value =record,key = USERS[id]) # topic , record   , NO key
        print(f"Dispatching event: {record['user_id']} -> {record['item_id']}")
        time.sleep(INTERVAL)
        
except KeyboardInterrupt:
    print("Producer stopped by user.")
except Exception as e:
    print(f"Producer failed: {e}")