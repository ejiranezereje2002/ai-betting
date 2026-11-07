import json
import math
from http.server import BaseHTTPRequestHandler

def poisson_pmf(k, lam):
    return (lam**k) * math.exp(-lam) / math.factorial(k)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            home_lambda = 1.85
            away_lambda = 1.15
            max_goals = 6
            
            home_probs = [poisson_pmf(i, home_lambda) for i in range(max_goals + 1)]
            away_probs = [poisson_pmf(j, away_lambda) for j in range(max_goals + 1)]
            
            home_win = 0.0
            draw = 0.0
            away_win = 0.0
            
            for h in range(max_goals + 1):
                for a in range(max_goals + 1):
                    prob = home_probs[h] * away_probs[a]
                    if h > a:
                        home_win += prob
                    elif h == a:
                        draw += prob
                    else:
                        away_win += prob
                        
            total = home_win + draw + away_win
            
            response_data = {
                "status": "success",
                "probabilities": {
                    "home_win": home_win / total,
                    "draw": draw / total,
                    "away_win": away_win / total
                }
            }
            
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
        return
