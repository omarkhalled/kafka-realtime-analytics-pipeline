# Real-Time Interaction Analytics Pipeline

## Overview
This project implements a real-time data pipeline that generates application interaction events (e.g., click/view/purchase), streams them through Kafka, performs continuous aggregations in near real-time, stores the processed results in a NoSQL database (Elasticsearch), and visualizes the metrics in Kibana.

The solution is fully containerized using Docker Compose to provide a reproducible, portable environment that mirrors real-world deployment patterns.

---

## High-Level Architecture

**Event Generator / Producer → Kafka Topic → Consumer / Aggregator → Elasticsearch (NoSQL) → Kibana Dashboard**

- **Producer** continuously generates interaction events and publishes them to Kafka.
- **Kafka** buffers events durably and enables scalable, decoupled streaming between services.
- **Consumer** processes events in real-time, maintains lightweight state for aggregations, and indexes results into Elasticsearch.
- **Elasticsearch** stores the processed analytics documents and supports fast queries/filters for dashboarding.
- **Kibana** provides near real-time visualization and monitoring dashboards.

---

## Why These Tools?

### Kafka (Streaming Backbone)
Kafka is used as the streaming platform because it provides:
- **High-throughput ingestion** for continuous event streams
- **Durability** (messages are persisted on disk)
- **Decoupling** between producers and consumers
- **Horizontal scalability** using **partitions + consumer groups**

### Elasticsearch (NoSQL Storage)
Elasticsearch is used as the NoSQL datastore because it offers:
- **Document-oriented storage** for semi-structured events and computed metrics
- **Fast indexing and query performance** for real-time analytics use cases
- **Native integration with Kibana**, making dashboarding straightforward

### Kibana (Visualization & Monitoring)
Kibana is used to build dashboards that:
- Display near real-time streaming metrics (e.g., averages, min/max, totals)
- Provide filters by user/item/type and time-based drilldowns
- Support monitoring/alert-style views using indexed fields (e.g., `status`)

### Docker & Docker Compose (Containerized Microservices)
Everything runs as Docker containers because it provides:
- **Reproducibility** (consistent environment on any machine)
- **Service isolation** (Kafka, Elasticsearch, consumer, producer are decoupled)
- **Microservice-style architecture** (producer/consumer as independent services)
- **Easy orchestration** (single command to bring up/down the full stack)

This approach closely matches production patterns where event generation, ingestion, processing, storage, and visualization are typically deployed as separate services.

---
## Limitations (Summary) & How to Scale Next

### Current Limitations (in this implementation)
- **In-memory aggregation state**: Aggregations are stored in Python dictionaries inside the consumer, so if the consumer restarts, the state resets.
- **Scaling consumers affects correctness**: If multiple consumer instances run in the same consumer group, each one processes only a subset of Kafka partitions, which can lead to **partial aggregates** when state is kept locally per consumer.
- **High write volume to Elasticsearch**: Writing a document per processed event is simple for the case study, but at higher throughput it can increase index size and indexing load.
- **At-least-once behavior / potential duplicates**: Without strict idempotent writes + controlled offset commits, crashes can cause reprocessing and duplicate indexing.

### How I would scale this later (production direction)
- **Key-based partitioning**: Produce messages with a key (`user_id` or `item_id`) so all events for the same key land in the same partition → correct per-key aggregation when scaling consumers.
- **Externalize state**: Move aggregation state to Kafka Streams/Flink (stateful processing) or Redis/state store to survive restarts and support distributed correctness.
- **Upsert “current state” documents in Elasticsearch**: Instead of indexing per event, maintain one document per `user_id` and one per `item_id` using deterministic document IDs and atomic upserts.


## Repository Structure

```text
.
├── docker-compose.yml
├── producer/
│   ├── Dockerfile
│   └── producer.py
└── consumer/
    ├── Dockerfile
    └── consumer.py
