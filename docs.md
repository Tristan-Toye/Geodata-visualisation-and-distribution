# Geodata Visualization and Distribution - Technical Documentation

## Table of Contents

1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [API Reference](#api-reference)
4. [Data Models](#data-models)
5. [Configuration](#configuration)
6. [Deployment Guide](#deployment-guide)
7. [Development Guide](#development-guide)
8. [Troubleshooting](#troubleshooting)

## Overview

The Geodata Visualization and Distribution system is a real-time geospatial data processing and visualization platform designed for tracking and monitoring GPS-enabled vehicles. The system provides a scalable architecture for collecting, processing, and visualizing location-based data through a web-based dashboard.

### Key Features

- **Real-time GPS Data Collection**: Serial communication with Arduino Mega devices
- **Streaming Data Processing**: Apache Kafka-based message distribution
- **Interactive Visualization**: Real-time maps and charts using Leaflet and Plotly
- **Scalable Architecture**: Microservices-based design for horizontal scaling
- **Web Dashboard**: Modern responsive interface built with Flask and Bulma CSS

### Technology Stack

- **Backend**: Python 3.7+, Flask 2.x
- **Data Streaming**: Apache Kafka 2.x
- **Serial Communication**: PySerial
- **Geospatial Processing**: GeoPy
- **Frontend**: HTML5, JavaScript, Leaflet.js, Plotly.js
- **Styling**: Bulma CSS Framework
- **Hardware**: Arduino Mega with GPS module

## System Architecture

### High-Level Architecture

```
┌─────────────┐    ┌─────────────────┐    ┌─────────────┐    ┌─────────────┐
│   Arduino   │───▶│  Data Collector │───▶│   Kafka     │───▶│ Web Server  │
│    Mega     │    │  (obtaining_    │    │   Broker    │    │   (app.py)  │
│   (GPS)     │    │   data.py)      │    │             │    │             │
└─────────────┘    └─────────────────┘    └─────────────┘    └─────────────┘
                                                                    │
                                                                    ▼
                                                           ┌─────────────┐
                                                           │   Web       │
                                                           │ Dashboard   │
                                                           │ (index.html)│
                                                           └─────────────┘
```

### Component Details

#### 1. Data Collection Layer (`obtaining_data.py`)

**Purpose**: Collects raw GPS data from Arduino Mega via USB serial connection.

**Key Functions**:
- `opkuis(L)`: Cleans and processes raw GPS data
- `schrijf(L)`: Calculates distance and velocity, publishes to Kafka

**Data Processing Flow**:
1. Read raw serial data from Arduino
2. Clean and convert GPS coordinates
3. Calculate distance between consecutive points
4. Compute velocity (distance/time)
5. Publish structured data to Kafka topic

#### 2. Message Broker Layer (Apache Kafka)

**Purpose**: Provides scalable, fault-tolerant message distribution.

**Configuration**:
- **Host**: localhost:9092
- **Topic**: geo_spatial_data
- **Partitions**: 1 (default)
- **Replication Factor**: 1 (single broker)

**Consumer Groups**:
- `geo_data`: For map visualization
- `grafiek`: For chart visualization

#### 3. Web Application Layer (`app.py`)

**Purpose**: Flask-based web server providing real-time data streaming endpoints.

**Key Endpoints**:
- `/DataMonitoring_Elektrische_Wagen`: Main dashboard
- `/DataMonitoring_Elektrische_Wagen/geo_spatial_data`: SSE endpoint for map data
- `/DataMonitoring_Elektrische_Wagen/grafiek`: SSE endpoint for chart data

#### 4. Frontend Layer (`templates/index.html`)

**Purpose**: Interactive web dashboard with real-time visualizations.

**Components**:
- **Map Visualization**: Leaflet.js with Mapbox tiles
- **Chart Visualization**: Plotly.js for velocity graphs
- **Real-time Updates**: Server-Sent Events (SSE) for live data

## API Reference

### Web Application Endpoints

#### GET `/DataMonitoring_Elektrische_Wagen`

**Description**: Main dashboard page

**Response**: HTML page with interactive map and charts

**Content-Type**: `text/html`

#### GET `/DataMonitoring_Elektrische_Wagen/geo_spatial_data`

**Description**: Server-Sent Events endpoint for real-time map data

**Response**: Stream of JSON data in SSE format

**Content-Type**: `text/event-stream`

**Data Format**:
```json
{
  "auto": "Tiny_car",
  "tijd": "2024-01-01T12:00:00Z",
  "key": "Tiny_car_2024-01-01T12:00:00Z",
  "breedtegraad": 51.032489,
  "lengtegraad": 2.866134,
  "afgelegde_weg": 150.5,
  "snelheid": 2.3
}
```

#### GET `/DataMonitoring_Elektrische_Wagen/grafiek`

**Description**: Server-Sent Events endpoint for real-time chart data

**Response**: Stream of Plotly chart configurations in SSE format

**Content-Type**: `text/event-stream`

**Data Format**:
```json
{
  "data": "[Plotly chart data array]",
  "layout": "[Plotly layout configuration]"
}
```

### Kafka API

#### Producer Configuration

```python
client = KafkaClient(hosts="localhost:9092")
topic = client.topics['geo_spatial_data']
producer = topic.get_sync_producer()
```

#### Consumer Configuration

```python
consumer = client.topics['geo_spatial_data'].get_simple_consumer(
    consumer_group="geo_data",
    auto_commit_enable=True,
    auto_commit_interval_ms=1000,
    auto_offset_reset=OffsetType.LATEST,
    reset_offset_on_start=False
)
```

## Data Models

### GPS Data Schema

```json
{
  "auto": "string",           // Vehicle identifier
  "tijd": "string",           // UTC timestamp (ISO 8601)
  "key": "string",            // Unique message identifier
  "breedtegraad": "float",    // Latitude (decimal degrees)
  "lengtegraad": "float",     // Longitude (decimal degrees)
  "afgelegde_weg": "float",   // Total distance traveled (meters)
  "snelheid": "float"         // Current velocity (meters/second)
}
```

### Chart Data Schema

```json
{
  "data": "string",           // JSON-encoded Plotly data array
  "layout": "string"          // JSON-encoded Plotly layout object
}
```

### Raw Arduino Data Format

```
$GPGGA,123456.789,5101.9494,N,00251.9680,E,1,08,1.0,3.0,M,50.0,M,,*6A
$GPRMC,123456.789,A,5101.9494,N,00251.9680,E,2.3,45.0,010124,1.2,E,A*2C
```

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `KAFKA_HOST` | Kafka broker host | localhost:9092 | Yes |
| `KAFKA_TOPIC` | Kafka topic name | geo_spatial_data | Yes |
| `ARDUINO_PORT` | Arduino serial port | COM4 | Yes |
| `ARDUINO_BAUDRATE` | Serial baud rate | 9600 | No |
| `FLASK_PORT` | Web server port | 5001 | No |
| `FLASK_DEBUG` | Debug mode | True | No |

### Hardware Configuration

#### Arduino Mega Setup

1. **GPS Module Connection**:
   - Connect GPS module to Arduino Mega
   - Ensure proper power supply (3.3V or 5V as per module specs)
   - Connect TX/RX pins correctly

2. **Serial Communication**:
   - Baud rate: 9600
   - Data format: 8N1 (8 data bits, no parity, 1 stop bit)
   - Flow control: None

3. **Arduino Code Requirements**:
   ```cpp
   // Example Arduino code structure
   void setup() {
     Serial.begin(9600);
     // GPS module initialization
   }
   
   void loop() {
     // Read GPS data
     // Output in NMEA format
     Serial.println(gpsData);
   }
   ```

### Kafka Configuration

#### Single Broker Setup

```properties
# server.properties
broker.id=0
listeners=PLAINTEXT://localhost:9092
log.dirs=/tmp/kafka-logs
num.partitions=1
default.replication.factor=1
```

#### Topic Creation

```bash
kafka-topics.sh --create --topic geo_spatial_data \
  --bootstrap-server localhost:9092 \
  --partitions 1 \
  --replication-factor 1
```

## Deployment Guide

### Prerequisites

1. **Python Environment**:
   ```bash
   python --version  # Python 3.7+
   pip --version     # pip 19.0+
   ```

2. **Apache Kafka**:
   - Download Kafka 2.x or later
   - Extract to desired directory
   - Start Zookeeper and Kafka servers

3. **Hardware Setup**:
   - Arduino Mega with GPS module
   - USB cable for serial communication
   - Stable power supply

### Installation Steps

1. **Clone Repository**:
   ```bash
   git clone https://github.com/yourusername/Geodata-visualisation-and-distribution.git
   cd Geodata-visualisation-and-distribution
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Kafka**:
   ```bash
   # Start Zookeeper
   bin/zookeeper-server-start.sh config/zookeeper.properties
   
   # Start Kafka
   bin/kafka-server-start.sh config/server.properties
   
   # Create topic
   bin/kafka-topics.sh --create --topic geo_spatial_data \
     --bootstrap-server localhost:9092
   ```

4. **Configure Arduino**:
   - Upload GPS reading code to Arduino Mega
   - Connect via USB
   - Note COM port (Windows) or device path (Linux/Mac)

5. **Update Configuration**:
   - Edit `obtaining_data.py` to set correct COM port
   - Verify Kafka host settings

### Production Deployment

#### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5001

CMD ["python", "app.py"]
```

#### Systemd Service (Linux)

```ini
[Unit]
Description=Geodata Visualization Service
After=network.target

[Service]
Type=simple
User=geodata
WorkingDirectory=/opt/geodata
ExecStart=/usr/bin/python3 app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

## Development Guide

### Development Environment Setup

1. **Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

2. **Install Development Dependencies**:
   ```bash
   pip install -r requirements-dev.txt
   ```

3. **Code Style**:
   - Follow PEP 8 for Python code
   - Use 4 spaces for indentation
   - Maximum line length: 120 characters

### Testing

#### Unit Tests

```bash
python -m pytest tests/
```

#### Integration Tests

```bash
python -m pytest tests/integration/
```

#### Manual Testing

1. Start Kafka and Zookeeper
2. Run `python obtaining_data.py`
3. Run `python app.py`
4. Access dashboard at `http://localhost:5001/DataMonitoring_Elektrische_Wagen`

### Code Structure

```
Geodata-visualisation-and-distribution/
├── app.py                 # Flask web application
├── obtaining_data.py      # Data collection and processing
├── templates/
│   └── index.html        # Web dashboard
├── tests/                # Test suite
│   ├── unit/
│   └── integration/
├── docs/                 # Documentation
├── requirements.txt      # Production dependencies
├── requirements-dev.txt  # Development dependencies
└── README.md            # Project overview
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Arduino Connection Issues

**Problem**: `SerialException: [Errno 2] No such file or directory`

**Solution**:
- Check if Arduino is connected
- Verify COM port in Device Manager (Windows)
- Update port configuration in `obtaining_data.py`

**Problem**: `SerialException: [Errno 13] Permission denied`

**Solution**:
- Close Arduino IDE or other serial monitors
- Check user permissions for serial port access
- Restart the application

#### 2. Kafka Connection Issues

**Problem**: `KafkaException: NoBrokersAvailable`

**Solution**:
- Verify Kafka server is running: `netstat -an | grep 9092`
- Check Kafka logs for errors
- Ensure topic exists: `kafka-topics.sh --list --bootstrap-server localhost:9092`

**Problem**: `TopicDoesNotExistError`

**Solution**:
```bash
kafka-topics.sh --create --topic geo_spatial_data \
  --bootstrap-server localhost:9092
```

#### 3. Web Application Issues

**Problem**: Dashboard not loading

**Solution**:
- Check Flask server logs
- Verify port 5001 is not in use
- Check browser console for JavaScript errors

**Problem**: Real-time updates not working

**Solution**:
- Verify SSE endpoints are accessible
- Check Kafka consumer groups
- Monitor network connectivity

#### 4. Data Processing Issues

**Problem**: GPS coordinates are invalid

**Solution**:
- Check GPS module signal strength
- Verify NMEA data format
- Test with known good coordinates

**Problem**: Distance calculations are incorrect

**Solution**:
- Verify coordinate system (WGS-84)
- Check geopy installation
- Validate coordinate precision

### Performance Optimization

#### Kafka Optimization

```properties
# Optimize for high-throughput scenarios
num.network.threads=3
num.io.threads=8
socket.send.buffer.bytes=102400
socket.receive.buffer.bytes=102400
socket.request.max.bytes=104857600
```

#### Flask Optimization

```python
# Enable production mode
app.run(debug=False, host='0.0.0.0', port=5001)

# Use production WSGI server
# gunicorn -w 4 -b 0.0.0.0:5001 app:app
```

### Monitoring and Logging

#### Application Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

#### Kafka Monitoring

```bash
# Monitor consumer lag
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --describe --group geo_data

# Monitor topic metrics
kafka-run-class.sh kafka.tools.ConsumerPerformance \
  --topic geo_spatial_data --broker-list localhost:9092
```

### Security Considerations

1. **Network Security**:
   - Use HTTPS in production
   - Implement proper authentication
   - Restrict network access

2. **Data Security**:
   - Encrypt sensitive data
   - Implement data retention policies
   - Regular security audits

3. **Hardware Security**:
   - Secure physical access to Arduino
   - Implement tamper detection
   - Regular firmware updates

## References

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [Leaflet.js Documentation](https://leafletjs.com/reference.html)
- [Plotly.js Documentation](https://plotly.com/javascript/)
- [GeoPy Documentation](https://geopy.readthedocs.io/)
- [PySerial Documentation](https://pyserial.readthedocs.io/) 