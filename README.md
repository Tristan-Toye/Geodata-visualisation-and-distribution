# Geodata Visualization and Distribution

A real-time geospatial data visualization and distribution system that collects GPS data from an Arduino Mega device and displays it through an interactive web interface using Flask, Kafka, Plotly, and Leaflet.

## 🚀 Features

- **Real-time GPS Tracking**: Collects GPS coordinates from Arduino Mega via USB serial connection
- **Live Map Visualization**: Interactive map using Leaflet.js with real-time marker updates
- **Real-time Charts**: Dynamic velocity graphs using Plotly.js with live data streaming
- **Scalable Data Distribution**: Apache Kafka broker for efficient data distribution
- **Web Dashboard**: Modern web interface built with Flask and Bulma CSS

## 🏗️ Architecture

```
Arduino Mega → USB Serial → obtaining_data.py → Kafka Broker → app.py → Web Dashboard
```

### Components

- **Data Collection** (`obtaining_data.py`): Serial communication with Arduino, GPS data processing
- **Data Distribution** (Kafka): Message broker for scalable data streaming
- **Web Application** (`app.py`): Flask server with real-time data endpoints
- **Frontend** (`templates/index.html`): Interactive dashboard with map and charts

## 📋 Prerequisites

- Python 3.7+
- Apache Kafka (running on localhost:9092)
- Arduino Mega with GPS module
- USB connection to Arduino

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Geodata-visualisation-and-distribution.git
   cd Geodata-visualisation-and-distribution
   ```

2. **Install Python dependencies**
   ```bash
   pip install flask pykafka plotly geopy pyserial
   ```

3. **Set up Apache Kafka**
   - Download and start Kafka server
   - Create topic: `geo_spatial_data`
   - Ensure Kafka is running on `localhost:9092`

4. **Configure Arduino connection**
   - Connect Arduino Mega via USB
   - Update COM port in `obtaining_data.py` (currently set to COM4)

## 🚀 Usage

1. **Start the data collection**
   ```bash
   python obtaining_data.py
   ```

2. **Start the web application**
   ```bash
   python app.py
   ```

3. **Access the dashboard**
   - Open browser and navigate to `http://localhost:5001/DataMonitoring_Elektrische_Wagen`
   - View real-time map and velocity charts

## 📊 Data Flow

1. **Data Collection**: Arduino sends GPS coordinates via serial communication
2. **Data Processing**: Python script cleans and processes raw GPS data
3. **Distance Calculation**: Uses geopy to calculate distance between consecutive points
4. **Kafka Publishing**: Processed data is published to Kafka topic
5. **Web Streaming**: Flask endpoints stream data to frontend via Server-Sent Events
6. **Visualization**: Real-time updates on map and charts

## 🗂️ Project Structure

```
Geodata-visualisation-and-distribution/
├── app.py                 # Flask web application
├── obtaining_data.py      # Arduino data collection and processing
├── templates/
│   └── index.html        # Web dashboard interface
└── README.md             # Project documentation
```

## 🔧 Configuration

### Arduino Setup
- Baud rate: 9600
- GPS module connected to Arduino Mega
- Serial output format: GPS coordinates

### Kafka Configuration
- Host: localhost:9092
- Topic: geo_spatial_data
- Consumer groups: geo_data, grafiek

### Web Application
- Port: 5001
- Debug mode: enabled
- Map center: [51.032489, 2.866134] (Belgium)

## 📈 Data Schema

```json
{
  "auto": "Tiny_car",
  "tijd": "UTC timestamp",
  "key": "unique_identifier",
  "breedtegraad": "latitude",
  "lengtegraad": "longitude",
  "afgelegde_weg": "total_distance_meters",
  "snelheid": "velocity_mps"
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Troubleshooting

### Common Issues

1. **Arduino Connection Error**
   - Check USB port configuration in `obtaining_data.py`
   - Ensure Arduino is properly connected and recognized

2. **Kafka Connection Error**
   - Verify Kafka server is running on localhost:9092
   - Check if topic `geo_spatial_data` exists

3. **Map Not Loading**
   - Verify internet connection (required for Mapbox tiles)
   - Check browser console for JavaScript errors

## 📞 Support

For support and questions, please open an issue in the GitHub repository.
