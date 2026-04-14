from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Store logs in memory
logs_data = []

# =========================
# HOME ROUTE
# =========================
@app.route('/')
def home():
    return "Backend Running"


# =========================
# UPLOAD LOG FILE
# =========================
@app.route('/upload-log', methods=['POST'])
def upload_log():
    file = request.files.get('file')

    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    content = file.read().decode('utf-8')
    lines = content.split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            continue

        log_type = "INFO"

        if "error" in line.lower():
            log_type = "ERROR"
        elif "warning" in line.lower():
            log_type = "WARNING"

        logs_data.append({
            "type": log_type,
            "message": line
        })

    return jsonify({"message": "Logs uploaded successfully"})


# =========================
# STATS ROUTE
# =========================
@app.route('/stats')
def get_stats():
    total = len(logs_data)
    error = sum(1 for log in logs_data if log['type'] == 'ERROR')
    warning = sum(1 for log in logs_data if log['type'] == 'WARNING')
    info = sum(1 for log in logs_data if log['type'] == 'INFO')

    return jsonify({
        "total": total,
        "error": error,
        "warning": warning,
        "info": info
    })


# =========================
# GET ALL LOGS
# =========================
@app.route('/logs')
def get_logs():
    return jsonify(logs_data)


# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(debug=True)