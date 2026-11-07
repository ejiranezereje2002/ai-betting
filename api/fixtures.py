import json
import urllib.request
from http.server import BaseHTTPRequestHandler
from datetime import datetime

API_KEY = "f5cf6a914875b1d4b4976214103dfe0c"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        today = datetime.utcnow().strftime('%Y-%m-%d')
        url = f"https://v3.football.api-sports.io/fixtures?date={today}"

        req = urllib.request.Request(url)
        req.add_header("x-apisports-key", API_KEY)

        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                raw_data = json.loads(response.read().decode('utf-8'))
                fixtures = []

                for item in raw_data.get("response", [])[:12]:
                    fixtures.append({
                        "id": item["fixture"]["id"],
                        "league": item["league"]["name"],
                        "date": item["fixture"]["date"],
                        "status": item["fixture"]["status"]["short"],
                        "home": item["teams"]["home"]["name"],
                        "away": item["teams"]["away"]["name"]
                    })

                self.wfile.write(json.dumps({"status": "success", "fixtures": fixtures}).encode('utf-8'))
        except Exception as e:
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
