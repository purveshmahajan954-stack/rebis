#!/usr/bin/env python3
import http.server
import socketserver
import os

PORT = 5000

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # The exact user-uploaded SDI Technology snapshot is exposed at /technology;
        # the existing Rebis homepage remains available at "/".
        if self.path in ('/technology', '/technology/'):
            self.path = '/attached_assets/www_sdipresence_com_1784979776747.html'
        if self.path in ('/products', '/products/'):
            self.path = '/attached_assets/www_sdipresence_com_(1)_1784979797888.html'
        if self.path in ('/founder', '/founder/'):
            self.path = '/attached_assets/www_sdipresence_com_(2)_1784979828457.html'
        if self.path in ('/funding', '/funding/'):
            self.path = '/attached_assets/www_sdipresence_com_(3)_1784979859871.html'
        # Webflow makes XHR calls to /navigation-items/* for dynamic nav content.
        # Return empty JSON so the scripts don't throw uncaught exceptions.
        if self.path.startswith('/navigation-items'):
            body = b'{"items":[]}'
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path == '/' or self.path == '':
            self.path = '/www_sdipresence_com_source.html'
        return super().do_GET()

    def log_message(self, format, *args):
        print(f"[{self.address_string()}] {format % args}")

os.chdir(os.path.dirname(os.path.abspath(__file__)))

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()
