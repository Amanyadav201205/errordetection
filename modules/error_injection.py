"""
Module 7: Error Injection Module
Simulates transmission channel noise and errors by allowing:
- Manual single/multiple bit flipping
- Random bit corruption
- Burst error injection
- Bit Error Rate (BER) probabilistic noise simulation
"""
import random
from typing import Dict, Any, List

def flip_bit(b: str) -> str:
    return '1' if b == '0' else '0'

def inject_error_at_indices(frame: str, indices: List[int]) -> Dict[str, Any]:
    """
    Flips bits at specified 0-based indices.
    """
    chars = list(frame)
    flipped = []
    for idx in indices:
        if 0 <= idx < len(chars):
            orig = chars[idx]
            chars[idx] = flip_bit(orig)
            flipped.append((idx, orig, chars[idx]))
            
    corrupted_frame = "".join(chars)
    return {
        "original_frame": frame,
        "corrupted_frame": corrupted_frame,
        "flipped_indices": [f[0] for f in flipped],
        "flipped_details": flipped,
        "num_errors": len(flipped),
        "has_error": len(flipped) > 0
    }

def inject_single_random_error(frame: str) -> Dict[str, Any]:
    """Flips one random bit in the frame."""
    if not frame:
        return inject_error_at_indices(frame, [])
    idx = random.randint(0, len(frame) - 1)
    return inject_error_at_indices(frame, [idx])

def inject_burst_error(frame: str, burst_length: int = 3, start_idx: int = None) -> Dict[str, Any]:
    """
    Flips a sequence of consecutive bits to simulate a burst noise spike.
    """
    n = len(frame)
    if n == 0 or burst_length <= 0:
        return inject_error_at_indices(frame, [])
        
    burst_length = min(burst_length, n)
    if start_idx is None or start_idx < 0 or start_idx + burst_length > n:
        max_start = max(0, n - burst_length)
        start_idx = random.randint(0, max_start)
        
    indices = list(range(start_idx, start_idx + burst_length))
    return inject_error_at_indices(frame, indices)

def inject_ber_noise(frame: str, ber: float = 0.1) -> Dict[str, Any]:
    """
    Simulates Bit Error Rate (BER) probability per bit.
    """
    indices = [i for i in range(len(frame)) if random.random() < ber]
    return inject_error_at_indices(frame, indices)
