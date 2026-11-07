import json
from http.server import BaseHTTPRequestHandler
from scipy.stats import poisson
import numpy as np

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        home_lambda = 1.85
        away_lambda = 1.15
        max_goals = 6
        
        home_probs = [poisson.pmf(i, home_lambda) for i in range(max_goals + 1)]
        away_probs = [poisson.pmf(j, away_lambda) for j in range(max_goals + 1)]
        matrix = np.outer(home_probs, away_probs)
        
        home_win = float(np.sum(np.tril(matrix, -1)))
        draw = float(np.sum(np.diag(matrix)))
        away_win = float(np.sum(np.triu(matrix, 1)))
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
        return
