"""
Automated Unit Tests for All Error Detection and Correction Modules
"""
from modules.parity import encode_parity, verify_parity
from modules.parity2d import encode_2d_parity, verify_2d_parity
from modules.hamming import encode_hamming, verify_and_correct_hamming
from modules.checksum import encode_checksum, verify_checksum
from modules.crc import encode_crc, verify_crc
from modules.error_injection import inject_error_at_indices

def run_tests():
    print("=== Testing Module 2: Parity Check ===")
    res1 = encode_parity("1011001", "even")
    print("Encoded Even:", res1["encoded_frame"])
    v1 = verify_parity(res1["encoded_frame"], "even")
    assert not v1["error_detected"], "Failed even parity check"
    
    # Inject error
    corrupted = res1["encoded_frame"][:-1] + ('1' if res1["encoded_frame"][-1] == '0' else '0')
    v1_err = verify_parity(corrupted, "even")
    assert v1_err["error_detected"], "Failed to detect parity error"
    print("Parity: PASSED")

    print("\n=== Testing Module 3: 2D Parity Check ===")
    res2d = encode_2d_parity("110110101111", rows=3, cols=4, parity_type="even")
    frame2d = res2d["encoded_frame"]
    v2d_clean = verify_2d_parity(frame2d, rows=3, cols=4, parity_type="even")
    assert not v2d_clean["error_detected"], "Failed 2D clean verification"
    
    # Flip bit at row 1, col 2 (stride = cols + 1 = 5, pos = 1*5 + 2 = 7)
    inj = inject_error_at_indices(frame2d, [7])
    v2d_err = verify_2d_parity(inj["corrupted_frame"], rows=3, cols=4, parity_type="even")
    assert v2d_err["can_correct"], "Failed to correct 2D single error"
    print("2D Parity: PASSED (Corrected bit at Row", v2d_err["failed_rows"], "Col", v2d_err["failed_cols"], ")")

    print("\n=== Testing Module 4: Hamming Code ===")
    data_h = "1011"
    h_enc = encode_hamming(data_h)
    print("Hamming (7,4) Encoded:", h_enc["encoded_frame"])
    h_v_clean = verify_and_correct_hamming(h_enc["encoded_frame"])
    assert not h_v_clean["error_detected"], "Hamming clean failed"
    
    # Flip bit at pos 5 (0-indexed pos 4)
    h_corrupted = inject_error_at_indices(h_enc["encoded_frame"], [4])["corrupted_frame"]
    h_v_err = verify_and_correct_hamming(h_corrupted)
    assert h_v_err["error_detected"] and h_v_err["can_correct"], "Hamming failed to detect/correct"
    assert h_v_err["error_pos"] == 5, f"Expected error pos 5, got {h_v_err['error_pos']}"
    assert h_v_err["recovered_data"] == data_h, "Recovered data does not match original"
    print("Hamming Code: PASSED (Detected error at pos 5 and corrected to original data)")

    print("\n=== Testing Module 5: Checksum ===")
    chk_enc = encode_checksum("1010100100111001", block_size=8)
    chk_v_clean = verify_checksum(chk_enc["encoded_frame"], block_size=8)
    assert not chk_v_clean["error_detected"], "Checksum clean failed"
    
    # Corrupt a bit
    chk_corrupted = inject_error_at_indices(chk_enc["encoded_frame"], [3])["corrupted_frame"]
    chk_v_err = verify_checksum(chk_corrupted, block_size=8)
    assert chk_v_err["error_detected"], "Checksum error detection failed"
    print("Checksum: PASSED")

    print("\n=== Testing Module 6: CRC ===")
    data_crc = "1101011011"
    gen = "10011" # CRC-4
    crc_enc = encode_crc(data_crc, gen)
    crc_v_clean = verify_crc(crc_enc["encoded_frame"], gen)
    assert not crc_v_clean["error_detected"], "CRC clean failed"
    
    # Corrupt a bit
    crc_corrupted = inject_error_at_indices(crc_enc["encoded_frame"], [2])["corrupted_frame"]
    crc_v_err = verify_crc(crc_corrupted, gen)
    assert crc_v_err["error_detected"], "CRC error detection failed"
    print("CRC: PASSED")

    print("\n=== Testing NS-2 Channel Integration (All 5 Techniques) ===")
    from modules.ns2_bridge import run_all_techniques_in_ns2
    ns2_suite = run_all_techniques_in_ns2("11010010", error_rate=0.2)
    assert len(ns2_suite) == 5, f"Expected 5 techniques, got {len(ns2_suite)}"
    for r in ns2_suite:
        assert r["verified_with_ns2"], f"Technique {r['display_name']} failed NS-2 verification"
        print(f"  [NS-2 INTEGRATED] {r['display_name']:<30} => Codeword: {r['encoded_frame']:<16} Link: Node 0 -> 1 | Loss: {r['ns2_loss_percentage']}% | Status: {r['status']}")

    print("\nALL MODULE AND NS-2 INTEGRATION TESTS PASSED WITH 100% SUCCESS!")

if __name__ == "__main__":
    run_tests()
