#!/usr/bin/env python3
"""Static file server for course-site. Reads port from PORT env var."""
import os
import socketserver
import http.server

os.chdir(os.path.join(os.path.dirname(__file__), '..', 'course-site'))
port = int(os.environ.get('PORT', '8770'))

with socketserver.TCPServer(('', port), http.server.SimpleHTTPRequestHandler) as httpd:
    print(f'Serving course-site on port {port}')
    httpd.serve_forever()
