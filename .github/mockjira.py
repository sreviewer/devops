"""Tiny mock Jira / ServiceNow for manual end-to-end checks. Usage: python mockjira.py <port> <log-file>"""
import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

port = int(sys.argv[1])
log = sys.argv[2]


class H(BaseHTTPRequestHandler):
    def do_POST(self):
        body = self.rfile.read(int(self.headers.get('Content-Length', 0))).decode('utf-8')
        with open(log, 'a', encoding='utf-8') as f:
            f.write(json.dumps({'path': self.path, 'auth': self.headers.get('Authorization'), 'body': json.loads(body) if body else None}) + '\n')
        if self.path == '/rest/api/2/issue':
            reply = {'id': '10001', 'key': 'SEC-42'}
        elif self.path == '/api/now/table/incident':
            reply = {'result': {'number': 'INC0010001', 'sys_id': 'abc123'}}
        else:
            reply = {'result': {'sys_id': 'v1'}}
        data = json.dumps(reply).encode()
        self.send_response(201)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *a):
        pass


HTTPServer((sys.argv[3] if len(sys.argv) > 3 else '127.0.0.1', port), H).serve_forever()
