import os
import time
import requests
from flask import Flask, jsonify

app = Flask(__name__)

BASE_IP = '81.181.113.133'
PORTS_TO_TRY = ['30120', '30110', '30130', '30100']
WORKING_PORT = '30120'

# Variabile pentru Cache
last_fetch_time = 0
cached_players = "--"
CACHE_COOLDOWN = 5  # Cere date de la FiveM doar din 5 in 5 secunde

# Găsim portul la pornire
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
    try:
        with open("overlay.html", "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Eroare la incarcarea overlay.html: {str(e)}", 500

@app.route('/players')
def get_players():
    global last_fetch_time, cached_players
    current_time = time.time()
    
    # Verificăm dacă au trecut 5 secunde de la ultima interogare către FiveM
    if current_time - last_fetch_time > CACHE_COOLDOWN:
        try:
            # Marim puțin timeout-ul ca să dăm timp serverului FiveM să răspundă
            response = requests.get(URL, timeout=2.5)
            if response.status_code == 200:
                data = response.json()
                cached_players = str(len(data))
                last_fetch_time = current_time # Resetăm cronometrul
        except Exception:
            # Dacă pică un request, pur și simplu păstrăm ultima valoare bună (nu dăm eroare)
            pass 
            
    # Returnăm instant ce avem în memorie
    return jsonify({"players": cached_players})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
