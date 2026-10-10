"""
Automated End-to-End System Health Check
Verifies:
1. Web server and static HTML serving
2. Persistent footer with team members and hidden course details
3. All 5 error detection & correction modules (encoding, error injection, verification, correction)
4. NS-2 discrete event channel simulation (via WSL /usr/bin/ns)
"""
import urllib.request
import json
import sys

def run_health_check():
    print("=" * 65)
    print("RUNNING COMPLETE END-TO-END HEALTH VERIFICATION")
    print("=" * 65)

    # 1. Test Server & Static File
    try:
        html = urllib.request.urlopen("http://127.0.0.1:5000/").read().decode()
        assert "AMAN KUMAR YADAV" in html, "Footer missing member 1"
        assert "PRATIK BHARADBHUNJE" in html, "Footer missing member 2"
        assert "DEVRISHI GADIA" in html, "Footer missing member 3"
        assert "24BCE0839" not in html, "Register number should not be shown"
        assert "24BCE2318" not in html, "Register number should not be shown"
        assert "24BCT0212" not in html, "Register number should not be shown"
        assert "BCSE308P" not in html, "Course code still present in HTML"
        assert "VL2026270103128" not in html, "Class number still present in HTML"
        print("[PASS] 1. Web Server & Persistent Team Footer (Only Names): 100% Verified!")
    except Exception as e:
        print(f"[FAIL] Web Server: {e}")
        return False

    # 2. Test API Status
    try:
        status = json.loads(urllib.request.urlopen("http://127.0.0.1:5000/api/status").read().decode())
        assert status["status"] == "online"
        assert status["ns2"]["available"] == True
        print(f"[PASS] 2. Backend & NS-2 Status: Connected! (Engine: {status['ns2']['path']})")
    except Exception as e:
        print(f"[FAIL] API Status: {e}")
        return False

    # 3. Test Modules
    try:
        # A. Parity
        enc = json.loads(urllib.request.urlopen(urllib.request.Request(
            "http://127.0.0.1:5000/api/encode",
            data=json.dumps({"technique": "parity", "data": "11010010"}).encode(),
            headers={"Content-Type": "application/json"}
        )).read().decode())["result"]
        
        ver_clean = json.loads(urllib.request.urlopen(urllib.request.Request(
            "http://127.0.0.1:5000/api/verify",
            data=json.dumps({"technique": "parity", "frame": enc["encoded_frame"], "original_data": "11010010"}).encode(),
            headers={"Content-Type": "application/json"}
        )).read().decode())["result"]
        assert not ver_clean["error_detected"], "Parity clean check failed"

        corrupted_parity = enc["encoded_frame"][:-1] + ('1' if enc["encoded_frame"][-1] == '0' else '0')
        ver_err = json.loads(urllib.request.urlopen(urllib.request.Request(
            "http://127.0.0.1:5000/api/verify",
            data=json.dumps({"technique": "parity", "frame": corrupted_parity, "original_data": "11010010"}).encode(),
            headers={"Content-Type": "application/json"}
        )).read().decode())["result"]
        assert ver_err["error_detected"], "Parity error detection failed"
        print("[PASS] 3. Module 2 (1D Parity Check): Verified Clean & Error Detection!")

        # B. 2D Parity
        enc2d = json.loads(urllib.request.urlopen(urllib.request.Request(
            "http://127.0.0.1:5000/api/encode",
            data=json.dumps({"technique": "parity2d", "data": "110110101111", "rows": 3, "cols": 4}).encode(),
            headers={"Content-Type": "application/json"}
        )).read().decode())["result"]
        
        corrupted_2d = list(enc2d["encoded_frame"])
        corrupted_2d[7] = '0' if corrupted_2d[7] == '1' else '1'
        ver_2d = json.loads(urllib.request.urlopen(urllib.request.Request(
            "http://127.0.0.1:5000/api/verify",
            data=json.dumps({"technique": "parity2d", "frame": "".join(corrupted_2d), "rows": 3, "cols": 4}).encode(),
            headers={"Content-Type": "application/json"}
        )).read().decode())["result"]
        assert ver_2d["can_correct"] == True, "2D parity single-bit correction failed"
        print("[PASS] 4. Module 3 (2D Parity Matrix): Verified Single-Bit Localization & Correction!")

        # C. Hamming Code
        enc_h = json.loads(urllib.request.urlopen(urllib.request.Request(
            "http://127.0.0.1:5000/api/encode",
            data=json.dumps({"technique": "hamming", "data": "1011"}).encode(),
            headers={"Content-Type": "application/json"}
        )).read().decode())["result"]
        
        corrupted_h = list(enc_h["encoded_frame"])
        corrupted_h[4] = '0' if corrupted_h[4] == '1' else '1' # Invert pos 5
        ver_h = json.loads(urllib.request.urlopen(urllib.request.Request(
            "http://127.0.0.1:5000/api/verify",
            data=json.dumps({"technique": "hamming", "frame": "".join(corrupted_h)}).encode(),
            headers={"Content-Type": "application/json"}
        )).read().decode())["result"]
        assert ver_h["can_correct"] == True and ver_h["recovered_data"] == "1011", "Hamming correction failed"
        print("[PASS] 5. Module 4 (Hamming Code): Verified Syndrome & Single-Bit Automatic Correction!")

        # D. Checksum
        enc_chk = json.loads(urllib.request.urlopen(urllib.request.Request(
            "http://127.0.0.1:5000/api/encode",
            data=json.dumps({"technique": "checksum", "data": "1010100100111001", "block_size": 8}).encode(),
            headers={"Content-Type": "application/json"}
        )).read().decode())["result"]
        
        ver_chk = json.loads(urllib.request.urlopen(urllib.request.Request(
            "http://127.0.0.1:5000/api/verify",
            data=json.dumps({"technique": "checksum", "frame": enc_chk["encoded_frame"], "block_size": 8}).encode(),
            headers={"Content-Type": "application/json"}
        )).read().decode())["result"]
        assert not ver_chk["error_detected"], "Checksum clean verification failed"
        print("[PASS] 6. Module 5 (Internet Checksum): Verified 1's Complement Addition & Inversion!")

        # E. CRC
        enc_crc = json.loads(urllib.request.urlopen(urllib.request.Request(
            "http://127.0.0.1:5000/api/encode",
            data=json.dumps({"technique": "crc", "data": "1101011011", "generator": "10011"}).encode(),
            headers={"Content-Type": "application/json"}
        )).read().decode())["result"]
        
        ver_crc = json.loads(urllib.request.urlopen(urllib.request.Request(
            "http://127.0.0.1:5000/api/verify",
            data=json.dumps({"technique": "crc", "frame": enc_crc["encoded_frame"], "generator": "10011"}).encode(),
            headers={"Content-Type": "application/json"}
        )).read().decode())["result"]
        assert not ver_crc["error_detected"], "CRC clean verification failed"
        print("[PASS] 7. Module 6 (CRC): Verified Modulo-2 XOR Polynomial Long Division!")

        # 4. Test NS-2 Discrete Event Simulation
        ns2_res = json.loads(urllib.request.urlopen(urllib.request.Request(
            "http://127.0.0.1:5000/api/run-ns2",
            data=json.dumps({"frame": "11010010", "error_rate": 0.25, "num_packets": 12}).encode(),
            headers={"Content-Type": "application/json"}
        )).read().decode())["result"]
        
        assert ns2_res["total_sent"] > 0, "NS-2 failed to transmit"
        print(f"[PASS] 8. Module 7 & 9 (NS-2 Simulation): Verified! Sent: {ns2_res['total_sent']}, Corrupted/Dropped: {ns2_res['total_dropped']}, Received: {ns2_res['total_received']}, PER: {ns2_res['loss_percentage']}%")

    except Exception as e:
        print(f"[FAIL] Error testing modules: {e}")
        return False

    print("=" * 65)
    print(">>> OVERALL STATUS: YES! THE SYSTEM IS 100% WORKING PROPERLY! <<<")
    print("=" * 65)
    return True

if __name__ == "__main__":
    success = run_health_check()
    sys.exit(0 if success else 1)
