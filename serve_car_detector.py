#!/usr/bin/env python3
"""
Simple server to deploy the car detector on your local network.
Run: python serve_car_detector.py
Then open http://localhost:8080 from your phone, or use your computer/other device
on the same WiFi with http://<your-phone-ip>:8080
"""

import http.server
import socketserver
import os
import socket

PORT = 8080

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.path = '/car_detector_deploy.html'
        return super().do_GET()

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return '127.0.0.1'

if __name__ == '__main__':
    os.chdir('/data/data/com.termux/files/home')
    ip = get_local_ip()
    print('\n' + '='*50)
    print('🚗 Car Detector - Deployed!')
    print('='*50)
    print(f'📱 On this phone:  http://localhost:{PORT}')
    print(f'🌐 On same WiFi:   http://{ip}:{PORT}')
    print('='*50)
    print('Press Ctrl+C to stop\n')
    
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('\nServer stopped.')
