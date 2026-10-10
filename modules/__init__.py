"""
Interactive Network Error Detection and Correction Simulator
Computer Networks Lab Project
Modules package initialization
"""
from .parity import encode_parity, verify_parity
from .parity2d import encode_2d_parity, verify_2d_parity
from .hamming import encode_hamming, verify_and_correct_hamming
from .checksum import encode_checksum, verify_checksum
from .crc import encode_crc, verify_crc, PRESET_POLYNOMIALS
from .error_injection import inject_error_at_indices, inject_single_random_error, inject_burst_error
from .ns2_bridge import is_ns2_available, run_ns2_simulation
