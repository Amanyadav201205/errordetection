"""
Module 3: 2D Parity Check (Two-Dimensional / Matrix Parity)
Arranges binary data into a 2D grid (rows x cols), computes row and column parities,
transmits the extended matrix, verifies at the receiver, and pinpoints/corrects single-bit errors.
"""
from typing import Dict, Any, List, Tuple

def calculate_parity(bits: List[str], parity_type: str = "even") -> str:
    ones_count = sum(1 for b in bits if b == '1')
    if parity_type.lower() == "even":
        return '0' if (ones_count % 2 == 0) else '1'
    else:
        return '1' if (ones_count % 2 == 0) else '0'

def encode_2d_parity(data_bits: str, rows: int = 4, cols: int = 4, parity_type: str = "even") -> Dict[str, Any]:
    """
    Arranges data bits into rows x cols.
    Pads with '0' if len(data_bits) < rows * cols.
    Truncates or pads to fit rows * cols.
    Computes row parity for each row and column parity for each column.
    """
    total_cells = rows * cols
    padded_bits = data_bits.ljust(total_cells, '0')[:total_cells]
    
    matrix: List[List[str]] = []
    for r in range(rows):
        row = list(padded_bits[r * cols : (r + 1) * cols])
        matrix.append(row)
        
    row_parities: List[str] = []
    for r in range(rows):
        p = calculate_parity(matrix[r], parity_type)
        row_parities.append(p)
        
    col_parities: List[str] = []
    for c in range(cols):
        col_bits = [matrix[r][c] for r in range(rows)]
        p = calculate_parity(col_bits, parity_type)
        col_parities.append(p)
        
    # Corner parity bit (parity of row_parities or col_parities)
    corner_parity = calculate_parity(row_parities, parity_type)
    
    # Transmitted sequence: each row + its row parity, then column parities row + corner
    transmitted_bits = ""
    for r in range(rows):
        transmitted_bits += "".join(matrix[r]) + row_parities[r]
    transmitted_bits += "".join(col_parities) + corner_parity
    
    explanation = [
        f"Grid Size: {rows} rows x {cols} cols (Total data bits: {total_cells})",
        f"Padded Data: {padded_bits}",
        f"Parity Type: {parity_type.capitalize()} Parity",
        f"Calculated Row Parities: {', '.join(f'Row {i}: {p}' for i, p in enumerate(row_parities))}",
        f"Calculated Column Parities: {', '.join(f'Col {j}: {p}' for j, p in enumerate(col_parities))}",
        f"Corner Parity: {corner_parity}",
        f"Total Encoded Frame Length: {len(transmitted_bits)} bits"
    ]
    
    return {
        "original_data": data_bits,
        "rows": rows,
        "cols": cols,
        "matrix": matrix,
        "row_parities": row_parities,
        "col_parities": col_parities,
        "corner_parity": corner_parity,
        "encoded_frame": transmitted_bits,
        "explanation": "\n".join(explanation)
    }

def verify_2d_parity(received_frame: str, rows: int = 4, cols: int = 4, parity_type: str = "even") -> Dict[str, Any]:
    """
    Verifies received 2D frame.
    Detects row and column parity mismatches and pinpoints the error coordinates (row, col).
    Corrects the bit if exactly one row and one column failed!
    """
    expected_len = (rows + 1) * (cols + 1)
    if len(received_frame) != expected_len:
        return {
            "error_detected": True,
            "can_correct": False,
            "status": "Frame Length Mismatch",
            "explanation": f"Expected {expected_len} bits for {rows}x{cols} grid with parities, got {len(received_frame)} bits.",
            "matrix": [],
            "row_parities": [],
            "col_parities": [],
            "corner_parity": "",
            "failed_rows": [],
            "failed_cols": [],
            "received_data": received_frame,
            "corrected_data": received_frame
        }
        
    stride = cols + 1
    rx_matrix: List[List[str]] = []
    rx_row_parities: List[str] = []
    
    for r in range(rows):
        chunk = received_frame[r * stride : (r + 1) * stride]
        rx_matrix.append(list(chunk[:cols]))
        rx_row_parities.append(chunk[cols])
        
    last_row = received_frame[rows * stride :]
    rx_col_parities = list(last_row[:cols])
    rx_corner_parity = last_row[cols]
    
    # Check rows
    failed_rows: List[int] = []
    for r in range(rows):
        total_row_bits = rx_matrix[r] + [rx_row_parities[r]]
        ones = sum(1 for b in total_row_bits if b == '1')
        if (parity_type.lower() == "even" and ones % 2 != 0) or (parity_type.lower() == "odd" and ones % 2 == 0):
            failed_rows.append(r)
            
    # Check columns
    failed_cols: List[int] = []
    for c in range(cols):
        total_col_bits = [rx_matrix[r][c] for r in range(rows)] + [rx_col_parities[c]]
        ones = sum(1 for b in total_col_bits if b == '1')
        if (parity_type.lower() == "even" and ones % 2 != 0) or (parity_type.lower() == "odd" and ones % 2 == 0):
            failed_cols.append(c)
            
    corrected_matrix = [list(r) for r in rx_matrix]
    can_correct = False
    corrected_data = ""
    error_detected = len(failed_rows) > 0 or len(failed_cols) > 0
    correction_msg = ""
    
    if len(failed_rows) == 1 and len(failed_cols) == 1:
        err_r = failed_rows[0]
        err_c = failed_cols[0]
        flipped_bit = corrected_matrix[err_r][err_c]
        corrected_matrix[err_r][err_c] = '1' if flipped_bit == '0' else '0'
        can_correct = True
        corrected_data = "".join("".join(row) for row in corrected_matrix)
        correction_msg = f"Single-bit error isolated at Row {err_r + 1}, Col {err_c + 1}. Bit '{flipped_bit}' corrected to '{corrected_matrix[err_r][err_c]}'."
    elif error_detected:
        correction_msg = f"Multiple errors detected (Failed Rows: {failed_rows}, Failed Cols: {failed_cols}). Cannot uniquely pinpoint single bit."
    else:
        correction_msg = "All row and column parities verified successfully. No error."
        
    rx_data = "".join("".join(row) for row in rx_matrix)
    
    return {
        "received_data": rx_data,
        "matrix": rx_matrix,
        "row_parities": rx_row_parities,
        "col_parities": rx_col_parities,
        "corner_parity": rx_corner_parity,
        "failed_rows": failed_rows,
        "failed_cols": failed_cols,
        "error_detected": error_detected,
        "can_correct": can_correct,
        "corrected_data": corrected_data if can_correct else rx_data,
        "status": "Error Corrected" if can_correct else ("Error Detected" if error_detected else "Data is Correct (No Error)"),
        "explanation": correction_msg
    }
