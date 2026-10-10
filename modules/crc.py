"""
Module 6: Cyclic Redundancy Check (CRC)
Implements XOR-based polynomial binary division, remainder generation,
codeword creation, step-by-step division trace, and receiver-side integrity verification.
"""
from typing import Dict, Any, List, Tuple

PRESET_POLYNOMIALS = {
    "CRC-4 (ITU)": "10011",                       # x^4 + x + 1
    "CRC-8 (Standard)": "100000111",              # x^8 + x^2 + x + 1
    "CRC-8 (ATM)": "100000111",                   # x^8 + x^2 + x + 1
    "CRC-12": "1100000001111",                    # x^12 + x^11 + x^3 + x^2 + x + 1
    "CRC-16 (IBM)": "11000000000000101",          # x^16 + x^15 + x^2 + 1
    "CRC-16 (CCITT)": "10001000000100001",        # x^16 + x^12 + x^5 + 1
    "CRC-32 (IEEE 802.3)": "100000100110000010001110110110111"
}

def xor_strings(a: str, b: str) -> str:
    """Performs bitwise XOR between two binary strings of equal length."""
    return "".join('0' if bit_a == bit_b else '1' for bit_a, bit_b in zip(a, b))

def mod2_division(dividend: str, divisor: str) -> Tuple[str, List[Dict[str, str]]]:
    """
    Performs Modulo-2 (XOR) binary long division.
    Returns: (remainder, trace_steps)
    """
    div_len = len(divisor)
    current = list(dividend[:div_len])
    cursor = div_len
    steps = []
    
    while True:
        curr_str = "".join(current)
        if current[0] == '1':
            applied_divisor = divisor
            res = xor_strings(curr_str, divisor)
        else:
            applied_divisor = '0' * div_len
            res = xor_strings(curr_str, applied_divisor)
            
        # The first bit becomes 0 after XOR with MSB, discard MSB
        next_val = list(res[1:])
        
        step_info = {
            "window": curr_str,
            "divisor_applied": applied_divisor,
            "xor_result": res,
            "remainder_before_pull": "".join(next_val)
        }
        
        if cursor < len(dividend):
            brought_down = dividend[cursor]
            next_val.append(brought_down)
            step_info["brought_down"] = brought_down
            cursor += 1
            current = next_val
            steps.append(step_info)
        else:
            step_info["brought_down"] = "None (End of Dividend)"
            steps.append(step_info)
            remainder = "".join(next_val)
            break
            
    return remainder, steps

def encode_crc(data_bits: str, generator: str) -> Dict[str, Any]:
    """
    Encodes data bits using CRC generator polynomial:
    1. Appends (len(generator) - 1) zeros to data
    2. Performs Modulo-2 division
    3. Remainder is the CRC checksum
    4. Codeword = data_bits + remainder
    """
    k = len(generator) - 1
    augmented_data = data_bits + ('0' * k)
    
    remainder, steps = mod2_division(augmented_data, generator)
    transmitted_frame = data_bits + remainder
    
    explanation = [
        f"Original Data (M): {data_bits} (Length: {len(data_bits)})",
        f"Generator Polynomial (G): {generator} (Degree: {k})",
        f"Augmented Data (M * 2^{k}): {augmented_data}",
        f"Calculated Remainder / CRC Checksum: {remainder} ({len(remainder)} bits)",
        f"Transmitted Frame (M + R): {data_bits} | {remainder} = {transmitted_frame}",
        f"Total division steps executed: {len(steps)}"
    ]
    
    return {
        "original_data": data_bits,
        "generator": generator,
        "degree": k,
        "augmented_data": augmented_data,
        "remainder": remainder,
        "encoded_frame": transmitted_frame,
        "steps": steps,
        "explanation": "\n".join(explanation)
    }

def verify_crc(received_frame: str, generator: str) -> Dict[str, Any]:
    """
    Verifies received CRC frame:
    Divides received frame by generator polynomial using Modulo-2 division.
    If remainder is all '0's, no error detected.
    Otherwise, transmission error detected.
    """
    k = len(generator) - 1
    if len(received_frame) <= k:
        return {
            "error_detected": True,
            "can_correct": False,
            "status": "Frame too short",
            "explanation": f"Received frame length ({len(received_frame)}) must be greater than generator degree ({k}).",
            "received_frame": received_frame,
            "received_data": received_frame,
            "received_crc": "",
            "generator": generator,
            "remainder": "",
            "steps": []
        }
        
    remainder, steps = mod2_division(received_frame, generator)
    error_detected = any(b == '1' for b in remainder)
    
    rx_data = received_frame[:-k]
    rx_crc = received_frame[-k:]
    
    explanation = [
        f"Received Codeword: {received_frame}",
        f"Extracted Data: {rx_data}, Extracted CRC: {rx_crc}",
        f"Generator Polynomial: {generator}",
        f"Receiver Division Remainder (Syndrome): {remainder}",
        f"Check: Remainder is {'ALL ZEROS (Valid)' if not error_detected else 'NON-ZERO (Error)'}",
        f"Status: {'ERROR DETECTED! Data corrupted during transmission.' if error_detected else 'DATA IS CORRECT! (No Error)'}"
    ]
    
    return {
        "received_frame": received_frame,
        "received_data": rx_data,
        "received_crc": rx_crc,
        "generator": generator,
        "remainder": remainder,
        "error_detected": error_detected,
        "status": "Error Detected" if error_detected else "Data is Correct (No Error)",
        "can_correct": False,
        "steps": steps,
        "explanation": "\n".join(explanation)
    }
