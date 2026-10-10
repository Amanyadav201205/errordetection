"""
Module 5: Internet Checksum Module
Divides binary data into k-bit blocks, performs 1's complement addition with end-around carry,
generates checksum, and verifies data integrity at the receiver side.
"""
from typing import Dict, Any, List

def ones_complement_add(a: int, b: int, block_size: int) -> int:
    """Adds two integers using 1's complement addition with end-around carry."""
    max_val = (1 << block_size) - 1
    total = a + b
    # While there are overflow bits above block_size, wrap them around to LSB
    while total > max_val:
        carry = total >> block_size
        total = (total & max_val) + carry
    return total

def encode_checksum(data_bits: str, block_size: int = 8) -> Dict[str, Any]:
    """
    Pads data bits to multiple of block_size, splits into blocks,
    calculates 1's complement sum and inverts to produce Checksum.
    """
    # Pad to multiple of block_size
    remainder = len(data_bits) % block_size
    padded_data = data_bits
    if remainder != 0:
        pad_len = block_size - remainder
        padded_data = data_bits + ('0' * pad_len)
        
    blocks_str = [padded_data[i : i + block_size] for i in range(0, len(padded_data), block_size)]
    blocks_int = [int(b, 2) for b in blocks_str]
    
    current_sum = 0
    addition_steps = []
    for idx, b_int in enumerate(blocks_int):
        old_sum = current_sum
        current_sum = ones_complement_add(current_sum, b_int, block_size)
        addition_steps.append({
            "block_num": idx + 1,
            "block_str": blocks_str[idx],
            "block_int": b_int,
            "running_sum_bin": bin(current_sum)[2:].zfill(block_size),
            "step_desc": f"Block {idx+1} ({blocks_str[idx]} = {b_int}): Sum so far = {bin(current_sum)[2:].zfill(block_size)} ({current_sum})"
        })
        
    max_val = (1 << block_size) - 1
    # Checksum is 1's complement (bitwise NOT within block_size)
    checksum_int = max_val ^ current_sum
    checksum_bin = bin(checksum_int)[2:].zfill(block_size)
    
    transmitted_frame = padded_data + checksum_bin
    
    explanation = [
        f"Original Data: {data_bits} (Block Size: {block_size} bits)",
        f"Padded Data: {padded_data} (Divided into {len(blocks_str)} blocks)",
        "Blocks: " + " | ".join(blocks_str),
        "1's Complement Addition Steps:"
    ]
    for step in addition_steps:
        explanation.append("  " + step["step_desc"])
    explanation.append(f"Final 1's Complement Sum: {bin(current_sum)[2:].zfill(block_size)} ({current_sum})")
    explanation.append(f"Checksum (Bitwise Inversion): {checksum_bin} ({checksum_int})")
    explanation.append(f"Transmitted Frame (Data + Checksum): {padded_data} | {checksum_bin} = {transmitted_frame}")
    
    return {
        "original_data": data_bits,
        "padded_data": padded_data,
        "block_size": block_size,
        "blocks": blocks_str,
        "addition_steps": addition_steps,
        "final_sum_bin": bin(current_sum)[2:].zfill(block_size),
        "checksum_bin": checksum_bin,
        "checksum_int": checksum_int,
        "encoded_frame": transmitted_frame,
        "explanation": "\n".join(explanation)
    }

def verify_checksum(received_frame: str, block_size: int = 8) -> Dict[str, Any]:
    """
    Verifies received frame by adding all blocks (including received checksum).
    If result is all 1s (complemented sum == 0), no error.
    """
    if len(received_frame) < block_size * 2:
        return {
            "error_detected": True,
            "can_correct": False,
            "status": "Frame too short",
            "explanation": f"Frame must have at least {block_size*2} bits (at least 1 data block + 1 checksum).",
            "data_blocks": [],
            "rx_checksum": "",
            "final_sum_bin": "",
            "complemented_bin": ""
        }
        
    # Split received frame into blocks of block_size
    remainder = len(received_frame) % block_size
    frame = received_frame
    if remainder != 0:
        pad_len = block_size - remainder
        frame = received_frame + ('0' * pad_len)
        
    blocks_str = [frame[i : i + block_size] for i in range(0, len(frame), block_size)]
    data_blocks = blocks_str[:-1]
    rx_checksum_str = blocks_str[-1]
    
    blocks_int = [int(b, 2) for b in blocks_str]
    current_sum = 0
    addition_steps = []
    
    for idx, b_int in enumerate(blocks_int):
        current_sum = ones_complement_add(current_sum, b_int, block_size)
        is_chk = (idx == len(blocks_int) - 1)
        label = f"Checksum ({blocks_str[idx]})" if is_chk else f"Data Block {idx+1} ({blocks_str[idx]})"
        addition_steps.append(f"Add {label} -> Running Sum: {bin(current_sum)[2:].zfill(block_size)}")
        
    max_val = (1 << block_size) - 1
    # Check if sum is all 1s (i.e. complement is 0)
    complemented_sum = max_val ^ current_sum
    error_detected = (complemented_sum != 0)
    
    explanation = [
        f"Received Frame: {received_frame}",
        f"Data Blocks: {' | '.join(data_blocks)}",
        f"Received Checksum: {rx_checksum_str}",
        "Receiver Addition Steps:",
        "  " + "\n  ".join(addition_steps),
        f"Receiver Total Sum: {bin(current_sum)[2:].zfill(block_size)} ({current_sum})",
        f"Complemented Result: {bin(complemented_sum)[2:].zfill(block_size)} ({complemented_sum})",
        f"Status: {'ERROR DETECTED! Non-zero complemented sum.' if error_detected else 'DATA IS CORRECT! Complemented sum is all 0s (sum was all 1s).'}"
    ]
    
    return {
        "received_frame": received_frame,
        "block_size": block_size,
        "data_blocks": data_blocks,
        "rx_checksum": rx_checksum_str,
        "final_sum_bin": bin(current_sum)[2:].zfill(block_size),
        "complemented_bin": bin(complemented_sum)[2:].zfill(block_size),
        "error_detected": error_detected,
        "status": "Error Detected" if error_detected else "Data is Correct (No Error)",
        "can_correct": False,
        "explanation": "\n".join(explanation)
    }
