"""Public-facing server on port 3000.
Serves built frontend static files and proxies /api to backend on port 8000.
"""
import http.server
import urllib.request
import os
import sys
import json

FRONTEND_DIST = os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "dist")
BACKEND_URL = "http://127.0.0.1:8000"

class PublicHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/api/") or self.path == "/health":
            self.proxy_to_backend()
        else:
            # Serve static files from frontend dist
            self.directory = FRONTEND_DIST
            if self.path == "/":
                self.path = "/index.html"
            # Check if file exists, otherwise serve index.html (SPA routing)
            file_path = os.path.join(FRONTEND_DIST, self.path.lstrip("/"))
            if not os.path.exists(file_path):
                self.path = "/index.html"
            super().do_GET()

    def do_POST(self):
        if self.path.startswith("/api/"):
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length) if content_length > 0 else b""
            self.proxy_to_backend(body=body, method="POST")
        else:
            self.send_error(404)

    def do_PUT(self):
        if self.path.startswith("/api/"):
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length) if content_length > 0 else b""
            self.proxy_to_backend(body=body, method="PUT")
        else:
            self.send_error(404)

    def do_PATCH(self):
        if self.path.startswith("/api/"):
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length) if content_length > 0 else b""
            self.proxy_to_backend(body=body, method="PATCH")
        else:
            self.send_error(404)

    def proxy_to_backend(self, body=None, method="GET"):
        url = f"{BACKEND_URL}{self.path}"
        req = urllib.request.Request(url, data=body, method=method)
        for header, value in self.headers.items():
            if header.lower() not in ("host", "content-length", "connection"):
                req.add_header(header, value)
        try:
            response = urllib.request.urlopen(req)
            data = response.read()
            self.send_response(response.status)
            for header, value in response.headers.items():
                if header.lower() not in ("transfer-encoding", "connection", "content-encoding"):
                    self.send_header(header, value)
            self.end_headers()
            self.wfile.write(data)
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            self.end_headers()
            self.wfile.write(e.read())
        except Exception as e:
            self.send_error(502, f"Backend unavailable: {e}")

    def log_message(self, format, *args):
        print(f"[public:3000] {args[0]} {args[1]} {args[2]}", flush=True)


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    server = http.server.HTTPServer(("0.0.0.0", port), PublicHandler)
    print(f"🚀 Public server running on http://0.0.0.0:{port}")
    print(f"   Serving frontend from: {FRONTEND_DIST}")
    print(f"   Proxying /api -> {BACKEND_URL}")
    server.serve_forever()