from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class FlagHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        if self.path in ("/secret", "/flag", "/secret/", "/flag/"):
            resp = {
                "flag": "FLAG{55rf_4ll0w5_1nt3rn4l_4cc355}",
                "message": "You exploited SSRF to reach this internal service!",
                "service": "internal-flag",
                "note": "This service is not accessible from outside. You used SSRF!"
            }
        else:
            resp = {"status": "InnovateTech Internal Service", "endpoints": ["/flag", "/secret"]}
        self.wfile.write(json.dumps(resp).encode())

    def log_message(self, *args):
        pass

if __name__ == "__main__":
    print("Internal flag service listening on :9999")
    HTTPServer(("0.0.0.0", 9999), FlagHandler).serve_forever()
