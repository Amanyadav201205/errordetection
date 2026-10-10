"""
Module 2: Parity Check (1D Parity)
Supports Even Parity and Odd Parity encoding, verification, and step-by-step calculation.
"""
from typing import Dict, Any, Tuple

def calculate_parity_bit(data_bits: str, parity_type: str = "even") -> str:
    """
    Calculates single parity bit for given binary string.
    Even Parity: total number of 1s (including parity bit) is even.
    Odd Parity: total number of 1s (including parity bit) is odd.
    """
    ones_count = data_bits.count('1')
    if parity_type.lower() == "even":
        return '0' if (ones_count % 2 == 0) else '1'
    else:  # odd parity
        return '1' if (ones_count % 2 == 0) else '0'

def encode_parity(data_bits: str, parity_type: str = "even") -> Dict[str, Any]:
    """
    Encodes binary data with 1D parity bit.
    """
    parity_bit = calculate_parity_bit(data_bits, parity_type)
    transmitted_frame = data_bits + parity_bit
    ones_count = data_bits.count('1')
    
    explanation = [
        f"Original Data: {data_bits} (Length: {len(data_bits)} bits)",
        f"Number of 1s in data: {ones_count}",
        f"Parity Scheme: {parity_type.capitalize()} Parity",
        f"Parity Bit calculated: '{parity_bit}' (makes total 1s count {ones_count + int(parity_bit)} -> {'even' if (ones_count + int(parity_bit)) % 2 == 0 else 'odd'})",
        f"Transmitted Frame (Data + Parity): {data_bits} | {parity_bit} = {transmitted_frame}"
    ]
    
    return {
        "original_data": data_bits,
        "parity_type": parity_type.lower(),
        "parity_bit": parity_bit,
        "encoded_frame": transmitted_frame,
        "explanation": "\n".join(explanation)
    }

def verify_parity(received_frame: str, parity_type: str = "even", original_data_len: int = None) -> Dict[str, Any]:
    """
    Verifies received frame for parity errors.
    """
    if len(received_frame) < 2:
        return {
            "is_valid": False,
            "error_detected": True,
            "can_correct": False,
            "status": "Frame too short",
            "received_data": received_frame,
            "received_parity": "",
            "expected_parity": "",
            "explanation": "Frame too short (must be at least 2 bits)."
        }
    
    if original_data_len is not None and original_data_len < len(received_frame):
        received_data = received_frame[:original_data_len]
        received_parity = received_frame[original_data_len:]
    else:
        received_data = received_frame[:-1]
        received_parity = received_frame[-1]
        
    total_ones = received_frame.count('1')
    data_ones = received_data.count('1')
    
    expected_parity = calculate_parity_bit(received_data, parity_type)
    
    if parity_type.lower() == "even":
        error_detected = (total_ones % 2 != 0)
    else:
        error_detected = (total_ones % 2 == 0)
        
    explanation = [
        f"Received Frame: {received_frame}",
        f"Extracted Data: {received_data}, Received Parity Bit: {received_parity}",
        f"Total 1s in Received Frame: {total_ones}",
        f"Expected Parity for {received_data}: '{expected_parity}'",
        f"Parity Condition Check ({parity_type.capitalize()}): Total 1s is {'EVEN' if total_ones % 2 == 0 else 'ODD'}",
        f"Result: {'ERROR DETECTED! Frame corrupted.' if error_detected else 'NO ERROR DETECTED. Frame is valid.'}"
    ]
    
    return {
        "received_data": received_data,
        "received_parity": received_parity,
        "expected_parity": expected_parity,
        "error_detected": error_detected,
        "status": "Error Detected" if error_detected else "Data is Correct (No Error)",
        "can_correct": False,
        "explanation": "\n".join(explanation)
    }
