#!/usr/bin/env python3
import http.server
import socketserver
import os
import re

PORT = 5000

# Load the navbar snippet once at startup
_BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(_BASE, 'navbar_inject.html'), encoding='utf-8') as f:
    NAVBAR_HTML = f.read().encode('utf-8')

# Pages that get the Rebis navbar injected (maps URL path → file path)
SUBPAGES = {
    '/technology': 'attached_assets/www_sdipresence_com_1784979776747.html',
    '/products':   'attached_assets/www_sdipresence_com_(1)_1784979797888.html',
    '/founder':    'attached_assets/www_sdipresence_com_(2)_1784979828457.html',
    '/funding':    'attached_assets/www_sdipresence_com_(3)_1784979859871.html',
}


def strip_original_navbar(html: bytes) -> bytes:
    """Remove the original site's <div role="banner" ...> navbar completely."""
    marker = b'role="banner"'
    idx = html.find(marker)
    if idx == -1:
        return html

    # Walk backward to the opening < of this tag
    start = html.rfind(b'<', 0, idx)
    if start == -1:
        return html

    # Count div depth to find the matching closing </div>
    depth = 0
    pos = start
    length = len(html)
    while pos < length:
        next_open  = html.find(b'<', pos)
        if next_open == -1:
            break
        if html[next_open:next_open+2] == b'</':
            # closing tag
            close_end = html.find(b'>', next_open)
            if close_end == -1:
                break
            tag = html[next_open+2:close_end].strip().split()[0].lower() if html[next_open+2:close_end].strip() else b''
            if tag == b'div':
                depth -= 1
                if depth == 0:
                    # Found the matching closing </div>
                    end = close_end + 1
                    return html[:start] + html[end:]
            pos = close_end + 1
        else:
            # opening or self-closing tag
            close_end = html.find(b'>', next_open)
            if close_end == -1:
                break
            tag_content = html[next_open+1:close_end]
            tag_name = tag_content.strip().split()[0].lower() if tag_content.strip() else b''
            tag_name = re.sub(rb'[^a-z]', b'', tag_name)
            is_self_closing = tag_content.rstrip().endswith(b'/')
            if tag_name == b'div' and not is_self_closing:
                depth += 1
            pos = close_end + 1

    return html


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split('?')[0].rstrip('/')

        # Webflow XHR calls — return empty JSON
        if self.path.startswith('/navigation-items'):
            body = b'{"items":[]}'
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        # Sub-pages: serve with old navbar stripped and Rebis navbar injected
        if path in SUBPAGES:
            file_path = os.path.join(_BASE, SUBPAGES[path])
            try:
                with open(file_path, 'rb') as f:
                    content = f.read()

                # 1. Strip the original site navbar
                content = strip_original_navbar(content)

                # 2. Inject Rebis navbar right after <body ...>
                idx = content.lower().find(b'<body')
                if idx != -1:
                    close = content.find(b'>', idx)
                    if close != -1:
                        content = content[:close+1] + b'\n' + NAVBAR_HTML + content[close+1:]

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


os.chdir(_BASE)

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()
