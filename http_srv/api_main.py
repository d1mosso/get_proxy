import random
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import threading

lock = threading.Lock()

def get_proxy_from_file():
    with lock:
        with open('proxy_list.txt') as f:
            return [line.rstrip('\n') for line in f]

def get_proxy_ip():
    random_proxy = random.choice(get_proxy_from_file())
    if random_proxy:
        return {'proxy_ip': random_proxy}
    else:
        return {'proxy_ip': "Proxy_list.txt empty"}

def health():
    if get_proxy_from_file():
        return {"status": "OK"}
    else:
        return {"status": "DOWN"}


class Server(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    # GET sends back a Hello world message
    def do_GET(self):
        if self.path == "/get_proxy":
            self._set_headers()
            response = json.dumps(get_proxy_ip())
            response = bytes(response, 'utf-8')
            self.wfile.write(response)
        if self.path == "/health":
            self._set_headers()
            response = json.dumps(health())
            response = bytes(response, 'utf-8')
            self.wfile.write(response)


def run_http_srv(server_class=HTTPServer, handler_class=Server, port=8008):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)

    print('Starting httpd on port %d...' % port)
    try:
        httpd.serve_forever()
    except Exception:
        httpd.shutdown()


def run_thread_http_srv():
    http_srv_thread = threading.Thread(target=run_http_srv, name='Thread HTTP server')
    http_srv_thread.start()

