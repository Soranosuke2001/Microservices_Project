# ACIT 3855 Microservices Project

### Description
This project is to demonstrate the microservices architecture. This application will receive 2 different types of events (Receiver Service) and will store the events to the database (Storage Service). There is a periodic processing service (Processing Service) that will calculate some statistics based on the data received. The Audit Service will allow users to fetch a specific event that was received previously. There is also a website (Dashboard Service) that will allow the user to view the statistics and is regularly updated.

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

### Processing Service

hostname: processing
port: 8100

### Dashboard Service

hostname: dashboard
port: 3000

# SQL Commands

### Getting a specific index

`SELECT * FROM gun_stats WHERE id=1;`

`SELECT * FROM purchase_history WHERE id=1;`

