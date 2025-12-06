#!/usr/bin/env python3
import http.server
import socketserver
import os
import json
import urllib.parse
import requests
from dotenv import load_dotenv

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"

PORT = 8000

if not ELEVENLABS_API_KEY:
    print("WARNING: ELEVENLABS_API_KEY not found in environment variables!")
    print("Please set ELEVENLABS_API_KEY in your .env file or as an environment variable.")
else:
    print("✓ ELEVENLABS_API_KEY loaded")

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()
    
    def do_POST(self):
        if self.path == '/tts':
            self.handle_tts()
        else:
            self.send_response(404)
            self.end_headers()
    
    def handle_tts(self):
        if not ELEVENLABS_API_KEY:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            error_msg = {
                'error': 'ELEVENLABS_API not configured',
                'message': 'Please set ELEVENLABS_API in your .env file or as an environment variable'
            }
            self.wfile.write(json.dumps(error_msg).encode())
            return
        
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            text = data.get('text', '')
            
            if not text:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'No text provided'}).encode())
                return
            
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": ELEVENLABS_API_KEY
            }
            payload = {
                "text": text,
                "model_id": "eleven_turbo_v2",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.5
                }
            }
            
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            self.send_response(200)
            self.send_header('Content-Type', 'audio/mpeg')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(response.content)
            
        except requests.exceptions.RequestException as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            error_msg = {
                'error': 'ElevenLabs API request failed',
                'message': str(e),
                'details': f'Status: {e.response.status_code if hasattr(e, "response") and e.response else "N/A"}'
            }
            self.wfile.write(json.dumps(error_msg).encode())
        except Exception as e:
            import traceback
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            error_msg = {
                'error': 'Internal server error',
                'message': str(e),
                'type': type(e).__name__
            }
            print(f"TTS Error: {traceback.format_exc()}")
            self.wfile.write(json.dumps(error_msg).encode())
    
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        super().do_GET()
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"Server running at http://localhost:{PORT}/")
        print("Press Ctrl+C to stop")
        httpd.serve_forever()


