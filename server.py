import http.server
import socketserver
import webbrowser
import os

PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    print("Press Ctrl+C to stop the server")
    webbrowser.open(f'http://localhost:{PORT}/index.html')
    httpd.serve_forever() 