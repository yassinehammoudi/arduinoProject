from flask import Flask, request, jsonify
from flask_cors import CORS
import time, json, os

app = Flask(__name__)
CORS(app)

dataset_file = 'dataset.json'
if not os.path.exists(dataset_file):
    with open(dataset_file, 'w') as f:
        json.dump([], f)

# Thresholds
TEMP_THRESHOLD = 29  # °C
HUM_THRESHOLD = 50   # %

latest_data = {}

@app.route('/ingest', methods=['POST'])
def ingest():
    """
    Endpoint to receive sensor data (JSON payload).
    Example POST body:
    {
      "temperature": 25,
      "humidity": 60
    }
    """
    global latest_data
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No JSON received"}), 400

        # Add timestamp
        data['timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S")

        # Check for alerts
        alerts = []
        if data['temperature'] >= TEMP_THRESHOLD:
            alerts.append(f"⚠ High Temperature: {data['temperature']}°C")
        if data['humidity'] >= HUM_THRESHOLD:
            alerts.append(f"⚠ High Humidity: {data['humidity']}%")
        data['alerts'] = alerts

        latest_data = data

        # Save to dataset.json
        with open(dataset_file, 'r') as f:
            dataset = json.load(f)
        dataset.append(data)
        with open(dataset_file, 'w') as f:
            json.dump(dataset, f, indent=2)

        return jsonify({"status": "success", "data": data}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/data')
def get_data():
    """Return latest data with alerts"""
    return jsonify(latest_data)


@app.route('/dataset')
def get_dataset():
    with open(dataset_file, 'r') as f:
        dataset = json.load(f)
    return jsonify(dataset)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
