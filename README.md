# Running Services

### Zookeeper Service

hostname: zookeeper
port: 2181

### Kafka Service

hostname: kafka
port: 9092

### MySQL DB Service

hostname: db
port: 8090

### Audit Service

hostname: audit_log
port: 8110

### Receiver Service

hostname: receiver
port: 8080

### Storage Service

hostname: storage
port: 8090

### Service Service

hostname: service
port: 8100

```
curl -X POST -H "Content-Type: application/json" -d '{"gun_id": "d290f1ee-6c54-4b01-90e6-d701748f0851","game_id": "1c3b5a4e-b4d3-42f9-afaa-b3618924bbe2","user_id":"736bf87e-79e5-4d49-8e52-8e75d5e06f84","num_missed_shots": 300,"num_body_shots": 800,"num_head_shots": 2121,"num_bullets_shot": 300}' http://localhost:8080/new/gun_stat
```
