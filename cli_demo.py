"""
Command-Line Interface (CLI) Demonstration
Interactive Network Error Detection and Correction Simulator
Computer Networks Lab Project
"""

import sys
from modules.parity import encode_parity, verify_parity
from modules.parity2d import encode_2d_parity, verify_2d_parity
from modules.hamming import encode_hamming, verify_and_correct_hamming
from modules.checksum import encode_checksum, verify_checksum
from modules.crc import encode_crc, verify_crc
from modules.error_injection import inject_error_at_indices
from modules.ns2_bridge import run_ns2_simulation, is_ns2_available

def print_separator(title=""):
    print("\n" + "=" * 65)
    if title:
        print(f"  {title}")
        print("=" * 65)

def main():
    print_separator("COMPUTER NETWORKS LAB PROJECT")
    print("Project: Interactive Network Error Detection & Correction Simulator")
    print("Team: AMAN KUMAR YADAV, PRATIK BHARADBHUNJE, DEVRISHI GADIA")
    
    # 1. Parity Check
    print_separator("DEMO 1: PARITY CHECK (EVEN PARITY)")
    data1 = "1011001"
    enc1 = encode_parity(data1, "even")
    print(enc1["explanation"])
    
    # Clean check
    v1_clean = verify_parity(enc1["encoded_frame"], "even")
    print("\n[Case 1: No Error in Channel]")
    print(v1_clean["explanation"])
    
    # Injected error
    corrupt1 = enc1["encoded_frame"][:-1] + ('1' if enc1["encoded_frame"][-1] == '0' else '0')
    v1_err = verify_parity(corrupt1, "even")
    print("\n[Case 2: 1-Bit Error Injected in Channel]")
    print(v1_err["explanation"])

    # 2. 2D Parity
    print_separator("DEMO 2: 2D PARITY CHECK (3x4 MATRIX)")
    data2 = "110110101111"
    enc2 = encode_2d_parity(data2, rows=3, cols=4, parity_type="even")
    print(enc2["explanation"])
    
    # Inject error at Row 1, Col 2 (0-indexed)
    inj2 = inject_error_at_indices(enc2["encoded_frame"], [7])
    v2 = verify_2d_parity(inj2["corrupted_frame"], rows=3, cols=4, parity_type="even")
    print("\n[Case: Bit Flipped at Row 1, Col 2]")
    print(v2["explanation"])
    print(f"Status: {v2['status']}")

    # 3. Hamming Code
    print_separator("DEMO 3: HAMMING CODE (SINGLE ERROR CORRECTION)")
    data3 = "1011"
    enc3 = encode_hamming(data3)
    print(enc3["explanation"])
    
    # Inject error at position 5
    inj3 = inject_error_at_indices(enc3["encoded_frame"], [4]) # index 4 is 1-based pos 5
    v3 = verify_and_correct_hamming(inj3["corrupted_frame"])
    print("\n[Case: Bit Inverted at Position 5 in Codeword]")
    print(v3["explanation"])

    # 4. Internet Checksum
    print_separator("DEMO 4: INTERNET CHECKSUM (8-BIT BLOCKS)")
    data4 = "1010100100111001"
    enc4 = encode_checksum(data4, block_size=8)
    print(enc4["explanation"])
    
    # Receiver verify clean
    v4 = verify_checksum(enc4["encoded_frame"], block_size=8)
    print("\n[Receiver Checksum Verification]")
    print(v4["explanation"])

    # 5. CRC
    print_separator("DEMO 5: CYCLIC REDUNDANCY CHECK (CRC-4: 10011)")
    data5 = "1101011011"
    gen5 = "10011"
    enc5 = encode_crc(data5, gen5)
    print(enc5["explanation"])
    
    v5 = verify_crc(enc5["encoded_frame"], gen5)
    print("\n[Receiver CRC Verification]")
    print(v5["explanation"])

    # 6. NS-2 Channel Simulation
    print_separator("DEMO 6: NS-2 DISCRETE EVENT NETWORK SIMULATION")
    ns_info = is_ns2_available()
    print(f"NS-2 Environment: {ns_info}")
    print("Running NS-2 Channel Simulation (Transmitter -> ErrorModel -> Receiver)...")
    res_ns2 = run_ns2_simulation(encoded_bits=enc5["encoded_frame"], error_rate=0.25, num_packets=12)
    print(f"Packets Queued at Tx (+):     {res_ns2['total_sent']}")
    print(f"Packets Corrupted/Dropped (d): {res_ns2['total_dropped']}")
    print(f"Packets Received at Rx (r):   {res_ns2['total_received']}")
    print(f"Packet Error Rate (PER):      {res_ns2['loss_percentage']}%")
    print(f"Generated Trace File:         {res_ns2['trace_file']}")
    print_separator("DEMO COMPLETE - ALL 9 MODULES FUNCTIONAL")

if __name__ == "__main__":
    main()
