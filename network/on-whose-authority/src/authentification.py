#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import ssl

HOST_NAME = 'A MODIFIER'
PORT = 443

class MyHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text")
        self.end_headers()
    def do_GET(self):
        key = "k7SBjJ2qoKmqQUc5"
        if self.headers.get('Authorization') == 'Basic ' + key:
            self.send_response(200)
            self.send_header("Content-type", "text")
            self.end_headers()
            self.wfile.write(bytes("Flag: INSA{gotta_verify_the_certs}", "utf-8"));
        else:
            self.send_response(401)
            self.send_header("Content-type", "text")
            self.end_headers()
            self.wfile.write(bytes("You don't seem worthy of my trust...", "utf-8"));

if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME,PORT), MyHandler)
    httpd.socket = ssl.wrap_socket(httpd.socket, certfile='/etc/letsencrypt/live/zoug.top/fullchain.pem', keyfile='/etc/letsencrypt/live/zoug.top/privkey.pem', server_side=True)
    print("Launching server")
    httpd.serve_forever()
