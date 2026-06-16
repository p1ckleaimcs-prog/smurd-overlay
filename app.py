import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

BASE_IP = '81.181.113.133'
PORTS_TO_TRY = ['30120', '30110', '30130', '30100']
WORKING_PORT = '30120'

# Găsim portul corect o singură dată, la pornirea serverului pe Render
for port in PORTS_TO_TRY:
    test_url = f'http://{BASE_IP}:{port}/players.json'
    try:
        response = requests.get(test_url, timeout=2)
        if response.status_code == 200:
            WORKING_PORT = port
            print(f"[OK] Server gasit pe portul: {port}")
            break
    except Exception:
        continue

URL = f'http://{BASE_IP}:{WORKING_PORT}/players.json'

@app.route('/')
def index():
    # Trimite fișierul HTML către browser/OBS
    try:
        with open("overlay.html", "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Eroare la incarcarea overlay.html: {str(e)}", 500

@app.route('/players')
def get_players():
    # Returnează numărul de jucători sub formă de JSON în timp real
    try:
        response = requests.get(URL, timeout=1.5)
        if response.status_code == 200:
            data = response.json()
            return jsonify({"players": str(len(data))})
    except Exception:
        pass
    return jsonify({"players": "--"})

if __name__ == '__main__':
    # Render folosește o variabilă de mediu numită PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)