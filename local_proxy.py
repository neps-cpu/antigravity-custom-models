# ==========================================
# OpenAI/OpenRouter Local Request Proxy
# Created by Neps
# ==========================================

import http.server
import socketserver
import urllib.request
import json

# =====================================================================
# CONFIGURATION: Set your OpenRouter API details here
# =====================================================================
PORT = 8000
TARGET_URL = "https://openrouter.ai/api/v1"  # OpenRouter base API
API_KEY = "sk-or-v1-YOUR_OPENROUTER_API_KEY"  # Replace with your actual OpenRouter key

# The proxy will rewrite the IDE's internal model ID to this OpenRouter model ID
REWRITE_MODEL = "anthropic/claude-3.5-sonnet"
# =====================================================================

class ProxyHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            body = json.loads(post_data.decode('utf-8'))
            if body and "model" in body:
                # Rewrite the model identifier to OpenRouter format
                body["model"] = REWRITE_MODEL
                post_data = json.dumps(body).encode('utf-8')
                print(f"Forwarding to OpenRouter model: {REWRITE_MODEL}")
        except Exception:
            body = None

        # Build request to target endpoint
        target_endpoint = TARGET_URL + self.path
        
        # Generic OpenAI-compatible forwarding
        req = urllib.request.Request(target_endpoint, data=post_data, method="POST")
        req.add_header("Content-Type", "application/json")
        
        # Inject OpenRouter Authorization headers
        if API_KEY:
            req.add_header("Authorization", f"Bearer {API_KEY}")
            
        # OpenRouter requirements: HTTP-Referer and X-Title
        req.add_header("HTTP-Referer", "http://localhost:8000")
        req.add_header("X-Title", "Antigravity IDE")
        
        try:
            with urllib.request.urlopen(req) as response:
                res_data = response.read()
                self.send_response(response.status)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(res_data)
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))

    def do_GET(self):
        target_endpoint = TARGET_URL + self.path
        req = urllib.request.Request(target_endpoint, method="GET")
        if API_KEY:
            req.add_header("Authorization", f"Bearer {API_KEY}")
        try:
            with urllib.request.urlopen(req) as response:
                res_data = response.read()
                self.send_response(response.status)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(res_data)
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))

if __name__ == '__main__':
    # Allow socket address reuse immediately
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), ProxyHandler) as httpd:
        print(f"OpenRouter Proxy running on http://localhost:{PORT}")
        print(f"Forwarding requests to: {TARGET_URL}")
        print(f"Targeting model: {REWRITE_MODEL}")
        httpd.serve_forever()
