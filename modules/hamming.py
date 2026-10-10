"""
Module 4: Hamming Code (Error Detection and Correction)
Implements standard (n, k) Hamming Code:
- Parity bit calculation at powers of 2 (1-indexed: 1, 2, 4, 8, ...)
- Full syndrome calculation at the receiver side
- Single-bit error detection and automatic bit correction
"""
from typing import Dict, Any, List

def calculate_parity_count(m: int) -> int:
    """Finds minimum number of parity bits r such that 2^r >= m + r + 1"""
    r = 1
    while (2 ** r) < (m + r + 1):
        r += 1
    return r

def encode_hamming(data_bits: str) -> Dict[str, Any]:
    """
    Encodes binary string into Hamming Code with parity bits at positions 1, 2, 4, 8...
    """
    m = len(data_bits)
    r = calculate_parity_count(m)
    n = m + r
    
    # 1-indexed array representation (index 0 unused)
    code = ['_'] * (n + 1)
    
    # Place data bits in positions that are NOT powers of 2
    j = 0
    data_positions = []
    parity_positions = [2**i for i in range(r)]
    
    for i in range(1, n + 1):
        if i in parity_positions:
            continue
        code[i] = data_bits[j]
        data_positions.append((i, data_bits[j]))
        j += 1
        
    parity_details = []
    # Calculate each parity bit (Even parity)
    for p_idx in range(r):
        pos = 2 ** p_idx
        covered_positions = []
        ones_count = 0
        for i in range(1, n + 1):
            if i != pos and (i & pos) != 0:
                covered_positions.append(i)
                if code[i] == '1':
                    ones_count += 1
        # Even parity: make total 1s even
        p_val = '0' if (ones_count % 2 == 0) else '1'
        code[pos] = p_val
        parity_details.append({
            "parity_bit": f"P{pos}",
            "position": pos,
            "covered_positions": covered_positions,
            "value": p_val,
            "equation": f"P{pos} = XOR({', '.join(f'pos {cp}' for cp in covered_positions)}) = {p_val}"
        })
        
    encoded_str = "".join(code[1:])
    
    explanation = [
        f"Data Bits (m = {m}): {data_bits}",
        f"Parity Bits needed (r = {r}) such that 2^r >= m + r + 1 (2^{r} >= {m + r + 1})",
        f"Total Codeword Length (n = {n}): {n} bits",
        f"Parity Bit Positions: {', '.join(str(p) for p in parity_positions)}",
        "Calculated Parity Values:"
    ]
    for pd in parity_details:
        explanation.append(f"  {pd['parity_bit']} at pos {pd['position']}: {pd['value']} (covers positions {pd['covered_positions']})")
    explanation.append(f"Encoded Hamming Code: {encoded_str}")
    
    return {
        "original_data": data_bits,
        "m": m,
        "r": r,
        "n": n,
        "parity_positions": parity_positions,
        "parity_details": parity_details,
        "encoded_frame": encoded_str,
        "explanation": "\n".join(explanation)
    }

def verify_and_correct_hamming(received_frame: str) -> Dict[str, Any]:
    """
    Verifies received Hamming codeword.
    Calculates syndrome bits S_r ... S_1.
    If syndrome > 0, pinpoints exact error position and flips the bit to correct it!
    """
    n = len(received_frame)
    if n < 3:
        return {
            "error_detected": True,
            "can_correct": False,
            "status": "Frame too short",
            "explanation": "Hamming code must be at least 3 bits.",
            "syndrome_bits": [],
            "error_pos": 0,
            "corrected_frame": received_frame,
            "recovered_data": ""
        }
        
    r = 0
    while (2 ** r) <= n:
        r += 1
        
    code = ['_'] + list(received_frame) # 1-indexed
    
    syndrome_bits = []
    syndrome_details = []
    error_pos = 0
    
    for p_idx in range(r):
        pos = 2 ** p_idx
        ones_count = 0
        covered = []
        for i in range(1, n + 1):
            if (i & pos) != 0:
                covered.append(i)
                if code[i] == '1':
                    ones_count += 1
        # Syndrome bit is 0 if parity matches, 1 if mismatch
        s_val = 1 if (ones_count % 2 != 0) else 0
        syndrome_bits.append(s_val)
        if s_val == 1:
            error_pos += pos
        syndrome_details.append(f"S{pos} (covers {covered}) = {'1 (Parity Error)' if s_val else '0 (OK)'}")
        
    corrected_code = list(code)
    error_detected = (error_pos != 0)
    can_correct = False
    original_extracted_data = ""
    corrected_frame = received_frame
    
    parity_positions = [2**i for i in range(r)]
    
    if error_detected:
        if 1 <= error_pos <= n:
            can_correct = True
            old_val = corrected_code[error_pos]
            corrected_code[error_pos] = '1' if old_val == '0' else '0'
            corrected_frame = "".join(corrected_code[1:])
            status = "Error Detected & Corrected"
        else:
            status = "Multiple Errors Detected (Uncorrectable)"
    else:
        status = "Data is Correct (No Error)"
        
    # Extract data bits (non-parity positions) from corrected frame
    extracted_data_bits = [corrected_code[i] for i in range(1, n + 1) if i not in parity_positions]
    original_extracted_data = "".join(extracted_data_bits)
    
    explanation = [
        f"Received Codeword: {received_frame} (Length: {n})",
        f"Syndrome Evaluation:",
        "  " + "\n  ".join(syndrome_details),
        f"Syndrome Decimal Value (Error Position): {error_pos}",
    ]
    if error_detected and can_correct:
        explanation.append(f"==> Single-Bit Error Detected at Position {error_pos}!")
        explanation.append(f"==> Bit at Position {error_pos} flipped from '{code[error_pos]}' to '{corrected_code[error_pos]}'.")
        explanation.append(f"Corrected Codeword: {corrected_frame}")
        explanation.append(f"Recovered Message Bits: {original_extracted_data}")
    elif error_detected:
        explanation.append("==> Multiple errors detected. Unable to correct.")
    else:
        explanation.append("==> Syndrome = 0. All parity checks passed. Data received correctly!")
        explanation.append(f"Recovered Message Bits: {original_extracted_data}")
        
    return {
        "received_frame": received_frame,
        "n": n,
        "r": r,
        "syndrome_bits": syndrome_bits,
        "error_pos": error_pos,
        "error_detected": error_detected,
        "can_correct": can_correct,
        "corrected_frame": corrected_frame,
        "recovered_data": original_extracted_data,
        "status": status,
        "explanation": "\n".join(explanation)
    }
