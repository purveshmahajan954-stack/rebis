#!/usr/bin/env python3
import http.server
import socketserver
import os

PORT = 5000

# Load the navbar snippet once at startup
_NAVBAR_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'navbar_inject.html')
with open(_NAVBAR_PATH, encoding='utf-8') as f:
    NAVBAR_HTML = f.read().encode('utf-8')

# Pages that get the Rebis navbar injected (maps URL path → file path)
SUBPAGES = {
    '/technology':  'attached_assets/www_sdipresence_com_1784979776747.html',
    '/products':    'attached_assets/www_sdipresence_com_(1)_1784979797888.html',
    '/founder':     'attached_assets/www_sdipresence_com_(2)_1784979828457.html',
    '/funding':     'attached_assets/www_sdipresence_com_(3)_1784979859871.html',
}


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        path = self.path.rstrip('/')

        # Webflow XHR calls — return empty JSON
        if self.path.startswith('/navigation-items'):
            body = b'{"items":[]}'
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        # Sub-pages: serve file with Rebis navbar injected
        if path in SUBPAGES:
            file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), SUBPAGES[path])
            try:
                with open(file_path, 'rb') as f:
                    content = f.read()
                # Inject navbar right after <body ...>
                insert_after = b'<body'
                idx = content.lower().find(insert_after)
                if idx != -1:
                    # find end of opening <body ...> tag
                    close = content.find(b'>', idx)
                    if close != -1:
                        content = content[:close + 1] + b'\n' + NAVBAR_HTML + content[close + 1:]
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            except FileNotFoundError:
                self.send_error(404, 'File not found')
            return

        # Homepage
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
