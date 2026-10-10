"""
Web Server for Interactive Network Error Detection & Correction Simulator
Serves the web application and provides REST APIs for algorithm execution and NS-2 simulation.
Runs on http://localhost:5000
"""

import sys
import os
import json
import mimetypes
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import webbrowser

# Add workspace directory to path
WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, WORKSPACE_DIR)

from modules.parity import encode_parity, verify_parity
from modules.parity2d import encode_2d_parity, verify_2d_parity
from modules.hamming import encode_hamming, verify_and_correct_hamming
from modules.checksum import encode_checksum, verify_checksum
from modules.crc import encode_crc, verify_crc, PRESET_POLYNOMIALS
from modules.error_injection import (
    inject_error_at_indices,
    inject_single_random_error,
    inject_burst_error
)
from modules.ns2_bridge import is_ns2_available, run_ns2_simulation, run_ns2_for_technique, run_all_techniques_in_ns2

PORT = 5000
WEB_DIR = os.path.join(WORKSPACE_DIR, "web")

class SimulatorRequestHandler(BaseHTTPRequestHandler):
    def send_json_response(self, data: dict, status_code: int = 200):
        response_bytes = json.dumps(data).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response_bytes)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(response_bytes)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        # Serve static web files
        req_path = self.path.split("?")[0]
        if req_path == "/" or req_path == "":
            req_path = "/index.html"
            
        if req_path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
            return
            
        if req_path == "/api/status":
            ns2_stat = is_ns2_available()
            self.send_json_response({
                "status": "online",
                "ns2": ns2_stat,
                "team": [
                    {"name": "AMAN KUMAR YADAV"},
                    {"name": "PRATIK BHARADBHUNJE"},
                    {"name": "DEVRISHI GADIA"}
                ]
            })
            return
            
        if req_path == "/api/presets":
            self.send_json_response({
                "crc_presets": PRESET_POLYNOMIALS
            })
            return

        file_path = os.path.join(WEB_DIR, req_path.lstrip("/"))
        if not (os.path.exists(file_path) and os.path.isfile(file_path)):
            file_path = os.path.join(WORKSPACE_DIR, req_path.lstrip("/"))
        if os.path.exists(file_path) and os.path.isfile(file_path):
            mime_type, _ = mimetypes.guess_type(file_path)
            if not mime_type:
                mime_type = "application/octet-stream"
            try:
                with open(file_path, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", mime_type)
                self.send_header("Content-Length", str(len(content)))
                self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
                self.send_header("Pragma", "no-cache")
                self.send_header("Expires", "0")
                self.end_headers()
                self.wfile.write(content)
            except Exception as e:
                self.send_error(500, f"Error reading file: {str(e)}")
        else:
            self.send_error(404, f"File not found: {req_path}")

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)
        try:
            body = json.loads(post_data.decode("utf-8")) if post_data else {}
        except Exception:
            body = {}
            
        req_path = self.path.split("?")[0]
        
        # 1. API: /api/encode
        if req_path == "/api/encode":
            tech = body.get("technique", "parity")
            data = body.get("data", "11010010")
            
            try:
                if tech == "parity":
                    ptype = body.get("parity_type", "even")
                    res = encode_parity(data, ptype)
                elif tech == "parity2d":
                    rows = int(body.get("rows", 3))
                    cols = int(body.get("cols", 4))
                    ptype = body.get("parity_type", "even")
                    res = encode_2d_parity(data, rows, cols, ptype)
                elif tech == "hamming":
                    res = encode_hamming(data)
                elif tech == "checksum":
                    block_sz = int(body.get("block_size", 8))
                    res = encode_checksum(data, block_sz)
                elif tech == "crc":
                    gen = body.get("generator", "10011")
                    res = encode_crc(data, gen)
                else:
                    return self.send_json_response({"error": f"Unknown technique: {tech}"}, 400)
                    
                self.send_json_response({"success": True, "result": res})
            except Exception as e:
                self.send_json_response({"success": False, "error": str(e)}, 500)
            return

        # 2. API: /api/verify
        if req_path == "/api/verify":
            tech = body.get("technique", "parity")
            received_frame = body.get("frame", "")
            orig_data = body.get("original_data", "")
            
            try:
                if tech == "parity":
                    ptype = body.get("parity_type", "even")
                    res = verify_parity(received_frame, ptype, len(orig_data))
                elif tech == "parity2d":
                    rows = int(body.get("rows", 3))
                    cols = int(body.get("cols", 4))
                    ptype = body.get("parity_type", "even")
                    res = verify_2d_parity(received_frame, rows, cols, ptype)
                elif tech == "hamming":
                    res = verify_and_correct_hamming(received_frame)
                elif tech == "checksum":
                    block_sz = int(body.get("block_size", 8))
                    res = verify_checksum(received_frame, block_sz)
                elif tech == "crc":
                    gen = body.get("generator", "10011")
                    res = verify_crc(received_frame, gen)
                else:
                    return self.send_json_response({"error": f"Unknown technique: {tech}"}, 400)
                    
                self.send_json_response({"success": True, "result": res})
            except Exception as e:
                self.send_json_response({"success": False, "error": str(e)}, 500)
            return

        # 3. API: /api/run-ns2
        if req_path == "/api/run-ns2":
            frame = body.get("frame", "11010010")
            err_rate = float(body.get("error_rate", 0.2))
            num_pkts = int(body.get("num_packets", 15))
            technique = body.get("technique", "general")
            
            try:
                sim_res = run_ns2_simulation(
                    encoded_bits=frame,
                    error_rate=err_rate,
                    num_packets=num_pkts,
                    technique=technique,
                    workspace_dir=WORKSPACE_DIR
                )
                self.send_json_response({"success": True, "result": sim_res})
            except Exception as e:
                self.send_json_response({"success": False, "error": str(e)}, 500)
            return

        # 4. API: /api/run-ns2-all (Multi-Technique NS-2 Verification)
        if req_path == "/api/run-ns2-all":
            data = body.get("data", "11010010")
            err_rate = float(body.get("error_rate", 0.2))
            
            try:
                all_res = run_all_techniques_in_ns2(data=data, error_rate=err_rate)
                self.send_json_response({"success": True, "result": all_res})
            except Exception as e:
                self.send_json_response({"success": False, "error": str(e)}, 500)
            return

        self.send_error(404, "Endpoint not found")

    def log_message(self, format, *args):
        # Clean terminal output
        sys.stdout.write(f"[Server] {self.address_string()} - {format % args}\n")
        sys.stdout.flush()

def start_server():
    server = ThreadingHTTPServer(("0.0.0.0", PORT), SimulatorRequestHandler)
    print("=" * 65)
    print(f">> Interactive Network Simulator running at: http://localhost:{PORT}")
    print(f">> Serving static files from: {WEB_DIR}")
    print("=" * 65)
    server.serve_forever()

if __name__ == "__main__":
    start_server()
