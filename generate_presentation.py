"""
Professional Presentation Generator for Computer Networks Lab Project
Title: Interactive Network Error Detection & Correction Simulator
Authors: AMAN KUMAR YADAV, PRATIK BHARADBHUNJE, DEVRISHI GADIA
"""

import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# -------------------------------------------------------------
# Color Palette & Styling Tokens
# -------------------------------------------------------------
BG_COLOR = RGBColor(15, 23, 42)          # Slate-900 / Deep Navy
CARD_BG = RGBColor(30, 41, 59)           # Slate-800
CARD_BORDER = RGBColor(51, 65, 85)       # Slate-700
CYAN_ACCENT = RGBColor(56, 189, 248)     # Sky-400
INDIGO_ACCENT = RGBColor(99, 102, 241)   # Indigo-500
GREEN_ACCENT = RGBColor(52, 211, 153)    # Emerald-400
AMBER_ACCENT = RGBColor(251, 191, 36)    # Amber-400
TEXT_WHITE = RGBColor(248, 250, 252)     # Slate-50
TEXT_MUTED = RGBColor(148, 163, 184)     # Slate-400
TEXT_CYAN = RGBColor(56, 189, 248)
CODE_BG = RGBColor(11, 15, 25)

FONT_HEADING = "Segoe UI"
FONT_BODY = "Segoe UI"
FONT_CODE = "Consolas"

def create_slide_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.fill.background() # no border
        return bg

    def add_header(slide, category_text, title_text, subtitle_text=None):
        set_slide_background(slide)
        
        # Category Badge
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(8), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = f"●  {category_text.upper()}"
        p_cat.font.name = FONT_HEADING
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = CYAN_ACCENT

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.5), Inches(0.7))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.name = FONT_HEADING
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_WHITE

        if subtitle_text:
            sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.5), Inches(0.4))
            tf_sub = sub_box.text_frame
            tf_sub.word_wrap = True
            p_sub = tf_sub.paragraphs[0]
            p_sub.text = subtitle_text
            p_sub.font.name = FONT_BODY
            p_sub.font.size = Pt(13)
            p_sub.font.color.rgb = TEXT_MUTED

    def add_card(slide, left, top, width, height, title=None, subtitle=None):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1.5)

        tx_box = slide.shapes.add_textbox(Inches(left + 0.25), Inches(top + 0.2), Inches(width - 0.5), Inches(height - 0.4))
        tf = tx_box.text_frame
        tf.word_wrap = True

        if title:
            p_title = tf.paragraphs[0]
            p_title.text = title
            p_title.font.name = FONT_HEADING
            p_title.font.size = Pt(16)
            p_title.font.bold = True
            p_title.font.color.rgb = CYAN_ACCENT

        if subtitle:
            p_sub = tf.add_paragraph()
            p_sub.text = subtitle
            p_sub.font.name = FONT_BODY
            p_sub.font.size = Pt(12)
            p_sub.font.color.rgb = TEXT_MUTED

        return tf

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (COVER PAGE)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    # Decorative top bar
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.12))
    bar.fill.solid()
    bar.fill.fore_color.rgb = CYAN_ACCENT
    bar.line.fill.background()

    # Category Pill
    pill = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.2), Inches(3.6), Inches(0.45))
    pill.fill.solid()
    pill.fill.fore_color.rgb = RGBColor(14, 116, 144)
    pill.line.color.rgb = CYAN_ACCENT
    p_pill = pill.text_frame.paragraphs[0]
    p_pill.text = "COMPUTER NETWORKS LAB PROJECT"
    p_pill.font.name = FONT_HEADING
    p_pill.font.size = Pt(11)
    p_pill.font.bold = True
    p_pill.font.color.rgb = TEXT_WHITE
    p_pill.alignment = PP_ALIGN.CENTER

    # Title
    t_box = s1.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(11.3), Inches(1.8))
    tf1 = t_box.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "Interactive Network Error Detection\n& Correction Simulator"
    p1.font.name = FONT_HEADING
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE

    # Subtitle
    sub_box = s1.shapes.add_textbox(Inches(1.0), Inches(3.8), Inches(11.3), Inches(0.9))
    tf_sub = sub_box.text_frame
    tf_sub.word_wrap = True
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = "A Comprehensive Mathematical Simulation of Data Link Layer Error Control Mechanisms Integrated with Network Simulator 2 (NS-2) Physical Channel Discrete-Event Modeling"
    p_sub.font.name = FONT_BODY
    p_sub.font.size = Pt(15)
    p_sub.font.color.rgb = TEXT_MUTED

    # Team Members Container
    team_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(5.0), Inches(11.33), Inches(1.8))
    team_box.fill.solid()
    team_box.fill.fore_color.rgb = CARD_BG
    team_box.line.color.rgb = CARD_BORDER

    tb_header = s1.shapes.add_textbox(Inches(1.3), Inches(5.15), Inches(5.0), Inches(0.4))
    p_th = tb_header.text_frame.paragraphs[0]
    p_th.text = "PROJECT TEAM MEMBERS"
    p_th.font.name = FONT_HEADING
    p_th.font.size = Pt(12)
    p_th.font.bold = True
    p_th.font.color.rgb = CYAN_ACCENT

    # 3 Member Cards
    members = [
        ("AMAN KUMAR YADAV", "Parity & CRC Modulo-2 Division", "Web Engine & Architecture"),
        ("PRATIK BHARADBHUNJE", "Hamming Code Syndrome Calculation", "Forward Error Correction"),
        ("DEVRISHI GADIA", "Internet Checksum 1's Complement", "NS-2 Channel Integration")
    ]
    for idx, (m_name, r1, r2) in enumerate(members):
        col_x = 1.3 + (idx * 3.7)
        m_box = s1.shapes.add_textbox(Inches(col_x), Inches(5.6), Inches(3.4), Inches(1.1))
        tf_m = m_box.text_frame
        tf_m.word_wrap = True
        pm1 = tf_m.paragraphs[0]
        pm1.text = m_name
        pm1.font.name = FONT_HEADING
        pm1.font.size = Pt(15)
        pm1.font.bold = True
        pm1.font.color.rgb = TEXT_WHITE
        
        pm2 = tf_m.add_paragraph()
        pm2.text = f"• {r1}\n• {r2}"
        pm2.font.name = FONT_BODY
        pm2.font.size = Pt(11)
        pm2.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 2: PROJECT OVERVIEW & OBJECTIVES
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Executive Summary", "Project Motivation & Architectural Objectives", "Bridging theoretical Data Link Layer error control with realistic physical channel noise modeling")

    # Card 1: Problem Statement
    tf_c1 = add_card(s2, 0.8, 1.9, 5.7, 4.9, "1. The Problem in Physical Transmission", "Real-world network transmission challenges:")
    items_c1 = [
        ("Physical Noise & Attenuation: ", "Thermal noise, cross-talk, and fading corrupt binary bits (0 -> 1 or 1 -> 0) across copper and wireless media."),
        ("Silent Data Corruption: ", "Without Data Link Layer error detection, corrupted packets compromise application layer payloads, files, and protocols."),
        ("Limitations of Textbook Theory: ", "Traditional static exercises fail to show how check bits interact with live channel noise, loss rates, and syndrome recovery.")
    ]
    for prefix, body in items_c1:
        p = tf_c1.add_paragraph()
        p.space_before = Pt(12)
        r1 = p.add_run()
        r1.text = f"• {prefix}"
        r1.font.bold = True
        r1.font.color.rgb = TEXT_WHITE
        r2 = p.add_run()
        r2.text = body
        r2.font.color.rgb = TEXT_MUTED
        p.font.size = Pt(12)

    # Card 2: Implemented Solution
    tf_c2 = add_card(s2, 6.8, 1.9, 5.7, 4.9, "2. Our Integrated Solution", "Complete interactive simulation suite:")
    items_c2 = [
        ("5 Core Algorithms: ", "Full implementation of 1D Parity, 2D Parity Matrix, Hamming Code (n,k), Internet Checksum, and Cyclic Redundancy Check (CRC)."),
        ("Network Simulator 2 (NS-2): ", "Real discrete-event simulation via WSL with Node 0 (Tx), Node 1 (Rx), 2 Mbps link, and ErrorModel packet loss."),
        ("Bit-Level Error Injection: ", "Interactive bit-flipping, single-bit random noise, and 3-bit burst error corruption simulations."),
        ("Multi-Platform Availability: ", "Runs as high-performance Desktop GUI (Tkinter), Local Web Server (Python 3.14), and Cloud Web Application.")
    ]
    for prefix, body in items_c2:
        p = tf_c2.add_paragraph()
        p.space_before = Pt(10)
        r1 = p.add_run()
        r1.text = f"• {prefix}"
        r1.font.bold = True
        r1.font.color.rgb = GREEN_ACCENT
        r2 = p.add_run()
        r2.text = body
        r2.font.color.rgb = TEXT_MUTED
        p.font.size = Pt(12)

    # =========================================================================
    # SLIDE 3: END-TO-END PIPELINE (6 STAGES)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "System Architecture", "End-to-End Network Transmission Pipeline", "The 6 architectural stages modeling sender encoding, channel transmission, noise, and receiver recovery")

    stages = [
        ("01", "Input Binary", "Validation of binary stream (4, 8, 12, 16-bit presets or ASCII text converter)."),
        ("02", "Encode & Redundancy", "Generation of check bits, syndrome matrices, and transmitted codeword."),
        ("03", "Channel & NS-2", "Physical transmission across duplex link with optional NS-2 ErrorModel loss."),
        ("04", "Error Injection", "Interactive single-bit flip, random channel noise, or 3-bit burst corruption."),
        ("05", "Receiver Verify", "Syndrome evaluation, 1's complement check, or Modulo-2 XOR division."),
        ("06", "Recovery & Result", "Automated bit correction, diagnostic breakdown, and step-by-step visualizer.")
    ]

    for idx, (num, st_name, st_desc) in enumerate(stages):
        col = idx % 3
        row = idx // 3
        cx = 0.8 + (col * 3.95)
        cy = 1.9 + (row * 2.55)
        
        tf_st = add_card(s3, cx, cy, 3.75, 2.3)
        p_num = tf_st.paragraphs[0]
        p_num.text = f"STAGE {num}"
        p_num.font.name = FONT_CODE
        p_num.font.size = Pt(11)
        p_num.font.bold = True
        p_num.font.color.rgb = CYAN_ACCENT

        p_name = tf_st.add_paragraph()
        p_name.text = st_name
        p_name.font.name = FONT_HEADING
        p_name.font.size = Pt(16)
        p_name.font.bold = True
        p_name.font.color.rgb = TEXT_WHITE

        p_desc = tf_st.add_paragraph()
        p_desc.text = st_desc
        p_desc.font.name = FONT_BODY
        p_desc.font.size = Pt(11.5)
        p_desc.font.color.rgb = TEXT_MUTED
        p_desc.space_before = Pt(4)

    # =========================================================================
    # SLIDE 4: TECHNIQUE 1 — 1D PARITY CHECK
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Algorithm 1 of 5", "1D Parity Check (Even & Odd Schemes)", "Minimal bandwidth redundancy mechanism for single-bit error detection")

    tf_p1 = add_card(s4, 0.8, 1.9, 5.7, 5.0, "Mathematical Formulation & Working", "Parity Bit Generation:")
    points_p1 = [
        ("Concept: ", "Appends a single check bit (P) to the data stream such that the total count of binary 1s satisfies the chosen parity rule."),
        ("Even Parity: ", "P = 0 if sum of data bits is even; P = 1 if sum of data bits is odd.\nFormula: P = b1 ⊕ b2 ⊕ ... ⊕ bn"),
        ("Odd Parity: ", "P = 1 if sum of data bits is even; P = 0 if sum of data bits is odd."),
        ("Receiver Decision: ", "Computes parity over received frame. If parity matches scheme -> Accepted; else -> Discarded (Error Detected)."),
        ("Detection Strength: ", "Detects all odd numbers of bit errors (1, 3, 5...). Cannot detect even numbers of bit flips (2, 4...) because they cancel out parity.")
    ]
    for pfx, txt in points_p1:
        p = tf_p1.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = f"• {pfx}"
        r1.font.bold = True
        r1.font.color.rgb = TEXT_WHITE
        r2 = p.add_run()
        r2.text = txt
        r2.font.color.rgb = TEXT_MUTED
        p.font.size = Pt(11.5)

    tf_p2 = add_card(s4, 6.8, 1.9, 5.7, 5.0, "NS-2 Physical Channel Simulation", "Transmission across NS-2 Duplex Link:")
    points_p2 = [
        ("Codeword Transmission: ", "Transmitter (Node 0) formats the frame (e.g. 11010010 + '0' = 110100100) and packetizes it into CBR UDP packets."),
        ("NS-2 ErrorModel Loss: ", "The duplex link applies a uniform loss probability. When an ErrorModel drop event occurs, a bit corruption event is registered."),
        ("NS-2 Trace Output (.tr): ", "Generated events record packet enqueue (+), drop (d), and receive (r) at Node 1 (Sink)."),
        ("Live Result: ", "When NS-2 flips a single bit, the receiver parity check fails instantly, triggering 'Error Detected' with 100% reliability for 1-bit noise.")
    ]
    for pfx, txt in points_p2:
        p = tf_p2.add_paragraph()
        p.space_before = Pt(10)
        r1 = p.add_run()
        r1.text = f"• {pfx}"
        r1.font.bold = True
        r1.font.color.rgb = CYAN_ACCENT
        r2 = p.add_run()
        r2.text = txt
        r2.font.color.rgb = TEXT_MUTED
        p.font.size = Pt(11.5)

    # =========================================================================
    # SLIDE 5: TECHNIQUE 2 — 2D PARITY CHECK (MATRIX GRID)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Algorithm 2 of 5", "2D Parity Check (Matrix Grid Localization)", "Combining Longitudinal (LRC) & Vertical (VRC) Redundancy Checks for bit error correction")

    tf_2d1 = add_card(s5, 0.8, 1.9, 5.7, 5.0, "Matrix Organization & Error Pinpointing", "Grid Coordinates and Parity Intersection:")
    points_2d1 = [
        ("Matrix Structuring: ", "Data stream of length M × N is organized into an M-row by N-column rectangular matrix grid."),
        ("Row Parity (LRC): ", "Computes horizontal parity for each row i (adds 1 bit per row)."),
        ("Column Parity (VRC): ", "Computes vertical parity for each column j (adds 1 bit per column)."),
        ("Corner Parity: ", "Calculates overall matrix parity bit at the bottom-right intersection."),
        ("Intersection Localization: ", "If bit at Row i, Column j is flipped, Row i parity FAILS and Column j parity FAILS. Their intersection (i, j) uniquely pinpoints the corrupted bit!"),
        ("Forward Error Correction: ", "The receiver automatically inverts bit (i, j) back to its original state, achieving complete 1-bit recovery!")
    ]
    for pfx, txt in points_2d1:
        p = tf_2d1.add_paragraph()
        p.space_before = Pt(7)
        r1 = p.add_run()
        r1.text = f"• {pfx}"
        r1.font.bold = True
        r1.font.color.rgb = TEXT_WHITE
        r2 = p.add_run()
        r2.text = txt
        r2.font.color.rgb = TEXT_MUTED
        p.font.size = Pt(11.5)

    tf_2d2 = add_card(s5, 6.8, 1.9, 5.7, 5.0, "NS-2 Simulation & Recovery Demonstration", "Channel Noise Modeling:")
    points_2d2 = [
        ("Packet Serialization: ", "The entire (M+1) × (N+1) codeword matrix is serialized and sent across NS-2 link from Node 0 to Node 1."),
        ("NS-2 Trace Validation: ", "Trace log ns2_parity2d.tr confirms packet transmission across the link with ErrorModel packet drops."),
        ("Observed Behavior: ", "When NS-2 corrupts a packet in transit, the receiver reconstructs the grid, detects the failed row and column, and corrects the bit seamlessly."),
        ("Limitation Handled: ", "If multiple bits flip across different rows/columns, the system flags 'Multiple Errors Detected (Uncorrectable)' accurately.")
    ]
    for pfx, txt in points_2d2:
        p = tf_2d2.add_paragraph()
        p.space_before = Pt(10)
        r1 = p.add_run()
        r1.text = f"• {pfx}"
        r1.font.bold = True
        r1.font.color.rgb = GREEN_ACCENT
        r2 = p.add_run()
        r2.text = txt
        r2.font.color.rgb = TEXT_MUTED
        p.font.size = Pt(11.5)

    # =========================================================================
    # SLIDE 6: TECHNIQUE 3 — HAMMING CODE (n, k)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Algorithm 3 of 5", "Hamming Code (n, k) & Forward Error Correction", "Power-of-two parity placement with mathematical syndrome calculation for automatic bit recovery")

    tf_h1 = add_card(s6, 0.8, 1.9, 5.7, 5.0, "Mathematical Foundation & Syndrome Theory", "Richard Hamming (1950) Coding Theory:")
    points_h1 = [
        ("Check Bit Placement: ", "For k data bits, r parity bits are inserted at power-of-two bit indices (1, 2, 4, 8, ...) where 2^r >= k + r + 1."),
        ("Bit Coverage: ", "Parity bit at position 2^i checks all bit positions whose binary index has a 1 in the i-th bit position:\n• P1 checks [1, 3, 5, 7, 9, 11...]\n• P2 checks [2, 3, 6, 7, 10, 11...]\n• P4 checks [4, 5, 6, 7, 12, 13...]"),
        ("Syndrome Calculation: ", "Receiver recalculates parity checks: Syndrome S = (s_r ... s_2 s_1)_2.\n• S = 0 => No error (Frame is clean)\n• S = Decimal value D => EXACT bit at position D is corrupted!"),
        ("Automatic Bit Flipping: ", "Codeword[D] = ~Codeword[D]. The corrupted bit is inverted and original data is extracted with 100% accuracy.")
    ]
    for pfx, txt in points_h1:
        p = tf_h1.add_paragraph()
        p.space_before = Pt(7)
        r1 = p.add_run()
        r1.text = f"• {pfx}"
        r1.font.bold = True
        r1.font.color.rgb = TEXT_WHITE
        r2 = p.add_run()
        r2.text = txt
        r2.font.color.rgb = TEXT_MUTED
        p.font.size = Pt(11)

    tf_h2 = add_card(s6, 6.8, 1.9, 5.7, 5.0, "NS-2 Simulation & Syndrome Execution", "Discrete-Event Link Validation:")
    points_h2 = [
        ("NS-2 Trace Engine: ", "Hamming codeword (e.g. 7-bit codeword for 4-bit data) transmitted across Node 0 -> Node 1 link."),
        ("Trace Events in ns2_hamming.tr: ", "Logs packets undergoing transmission (+) and ErrorModel drops (d)."),
        ("Syndrome Localization Demo: ", "When NS-2 injects channel corruption, the simulator calculates the exact syndrome index (e.g. Syndrome = 5), highlights position 5 in yellow, and flips it back to original value."),
        ("Industrial Relevance: ", "Core algorithm used in ECC RAM (Server Memory), RAID-2 disk arrays, and satellite communication links.")
    ]
    for pfx, txt in points_h2:
        p = tf_h2.add_paragraph()
        p.space_before = Pt(10)
        r1 = p.add_run()
        r1.text = f"• {pfx}"
        r1.font.bold = True
        r1.font.color.rgb = CYAN_ACCENT
        r2 = p.add_run()
        r2.text = txt
        r2.font.color.rgb = TEXT_MUTED
        p.font.size = Pt(11.5)

    # =========================================================================
    # SLIDE 7: TECHNIQUE 4 — INTERNET CHECKSUM
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Algorithm 4 of 5", "Internet Checksum (1's Complement Summation)", "The foundational error detection mechanism powering IPv4, TCP, and UDP packet headers")

    tf_ck1 = add_card(s7, 0.8, 1.9, 5.7, 5.0, "Mathematical Mechanism & 1's Complement", "RFC 1071 Standard Protocol Mechanism:")
    points_ck1 = [
        ("Block Segmentation: ", "The binary message stream is divided into k-bit blocks (typically 4, 8, or 16 bits)."),
        ("1's Complement Addition: ", "Sender adds all k-bit words together using standard binary addition."),
        ("End-Around Carry: ", "Whenever an overflow carry bit exceeds k bits, it is wrapped around and added to the least significant bit (LSB)."),
        ("Checksum Inversion: ", "The final running sum is inverted (1's complement: 0 -> 1, 1 -> 0) and appended to the payload."),
        ("Receiver Verification: ", "Receiver sums all message blocks PLUS the checksum. If all bits in the sum equal 1 (i.e. complemented result is 0), the packet is VALID; otherwise CORRUPTED!")
    ]
    for pfx, txt in points_ck1:
        p = tf_ck1.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = f"• {pfx}"
        r1.font.bold = True
        r1.font.color.rgb = TEXT_WHITE
        r2 = p.add_run()
        r2.text = txt
        r2.font.color.rgb = TEXT_MUTED
        p.font.size = Pt(11.5)

    tf_ck2 = add_card(s7, 6.8, 1.9, 5.7, 5.0, "NS-2 Channel Integration & Protocol Context", "Evaluating Link Transmission:")
    points_ck2 = [
        ("NS-2 Trace Modeling: ", "The Checksum-protected frame is transmitted across the NS-2 channel from Node 0 to Node 1."),
        ("Trace Events in ns2_checksum.tr: ", "Demonstrates packet drops and transmissions over 2 Mbps channel with 10 ms delay."),
        ("Why Internet Protocols Use It: ", "1's complement summation is extremely fast to compute in software with simple integer additions, requiring minimal CPU cycles in routers."),
        ("Observed Detection: ", "Detects any burst error that alters the arithmetic sum. Clean frames yield complemented sum = 0x0000; corrupted frames yield non-zero sum.")
    ]
    for pfx, txt in points_ck2:
        p = tf_ck2.add_paragraph()
        p.space_before = Pt(10)
        r1 = p.add_run()
        r1.text = f"• {pfx}"
        r1.font.bold = True
        r1.font.color.rgb = AMBER_ACCENT
        r2 = p.add_run()
        r2.text = txt
        r2.font.color.rgb = TEXT_MUTED
        p.font.size = Pt(11.5)

    # =========================================================================
    # SLIDE 8: TECHNIQUE 5 — CYCLIC REDUNDANCY CHECK (CRC)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Algorithm 5 of 5", "Cyclic Redundancy Check (CRC Modulo-2 Division)", "High-performance polynomial division over GF(2) utilized in Ethernet, Wi-Fi, and USB")

    tf_crc1 = add_card(s8, 0.8, 1.9, 5.7, 5.0, "Polynomial Division over GF(2)", "Binary Modulo-2 XOR Mathematics:")
    points_crc1 = [
        ("Polynomial Representation: ", "Binary data treated as coefficients of a polynomial M(x). Generator polynomial G(x) of degree r defines divisor."),
        ("Sender Encoding: ", "1. Multiply M(x) by 2^r (append r zero bits to data).\n2. Divide by G(x) using Modulo-2 division (XOR subtraction without borrow).\n3. Remainder R(x) of r bits is the CRC Checksum.\n4. Transmitted Codeword = M(x)*2^r + R(x)."),
        ("Receiver Verification: ", "Receiver divides received frame by G(x). If Remainder == 0 => Clean (Accepted); If Remainder != 0 => Corrupted!"),
        ("Preset Polynomials Supported: ", "• CRC-4 (ITU): 10011 (x^4 + x + 1)\n• CRC-8 (ATM): 100000111\n• CRC-16 (IBM): 11000000000000101\n• CRC-32 (IEEE 802.3 Ethernet): 33-bit polynomial")
    ]
    for pfx, txt in points_crc1:
        p = tf_crc1.add_paragraph()
        p.space_before = Pt(7)
        r1 = p.add_run()
        r1.text = f"• {pfx}"
        r1.font.bold = True
        r1.font.color.rgb = TEXT_WHITE
        r2 = p.add_run()
        r2.text = txt
        r2.font.color.rgb = TEXT_MUTED
        p.font.size = Pt(11)

    tf_crc2 = add_card(s8, 6.8, 1.9, 5.7, 5.0, "Detection Superiority & NS-2 Trace Integration", "Industry-Standard Error Detection Power:")
    points_crc2 = [
        ("100% Single-Bit Errors: ", "Any single-bit error is not divisible by G(x) (provided G(x) has at least 2 non-zero terms)."),
        ("100% Double-Bit Errors: ", "Detects all double-bit errors provided G(x) does not divide (x^k + 1)."),
        ("100% Odd-Numbered Errors: ", "If G(x) contains factor (x + 1), it catches ALL odd numbers of flipped bits."),
        ("Burst Errors <= r Bits: ", "Detects 100% of all burst error corruptions of length <= degree of G(x)."),
        ("NS-2 Integration (ns2_crc.tr): ", "Transmits CRC codeword over NS-2 link. Channel packet drops trigger non-zero syndrome remainder at receiver sink.")
    ]
    for pfx, txt in points_crc2:
        p = tf_crc2.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = f"• {pfx}"
        r1.font.bold = True
        r1.font.color.rgb = GREEN_ACCENT
        r2 = p.add_run()
        r2.text = txt
        r2.font.color.rgb = TEXT_MUTED
        p.font.size = Pt(11)

    # =========================================================================
    # SLIDE 9: NETWORK SIMULATOR 2 (NS-2) ARCHITECTURE
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Channel Simulation Engine", "Network Simulator 2 (NS-2) Integration Architecture", "Coupling physical link discrete-event simulation with Data Link Layer error control")

    tf_ns1 = add_card(s9, 0.8, 1.9, 5.7, 5.0, "OTcl Network Topology Configuration", "Physical Channel Modeling in network_error_sim.tcl:")
    points_ns1 = [
        ("Simulator Engine: ", "NS-2 discrete-event network simulator executed natively in WSL (/usr/bin/ns)."),
        ("Transmitter Node (n0): ", "Agent/UDP attached to Node 0 with Constant Bit Rate (CBR) traffic generator sending 64-byte packets."),
        ("Receiver Node (n1): ", "Agent/Null sink attached to Node 1 acting as the destination receiver."),
        ("Duplex Link: ", "Bandwidth: 2.0 Mbps, Propagation Delay: 10 ms, Queueing: DropTail."),
        ("ErrorModel Loss Module: ", "Inserted directly on link n0 -> n1 with uniform random loss variable ($loss_module set rate_ $err_rate). Dropped packets routed to Agent/Null drop-target.")
    ]
    for pfx, txt in points_ns1:
        p = tf_ns1.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = f"• {pfx}"
        r1.font.bold = True
        r1.font.color.rgb = TEXT_WHITE
        r2 = p.add_run()
        r2.text = txt
        r2.font.color.rgb = TEXT_MUTED
        p.font.size = Pt(11.5)

    tf_ns2 = add_card(s9, 6.8, 1.9, 5.7, 5.0, "Trace Parsing & Python-to-NS-2 Bridge", "Real-Time Trace File Analytics (.tr):")
    points_ns2 = [
        ("Subprocess Bridge (ns2_bridge.py): ", "Automates execution via 'wsl bash -c ns network_error_sim.tcl [params]', streaming stdout and return codes."),
        ("Trace Event Parser: ", "Parses 12-column NS-2 event records:\n• '+' : Packet queued at Transmitter (Node 0)\n• '-' : Packet transmitted onto physical link\n• 'd' : Packet DROPPED / CORRUPTED by ErrorModel\n• 'r' : Packet successfully received at Node 1 (Sink)"),
        ("Packet Error Rate (PER): ", "Calculates PER = (Dropped / (Received + Dropped)) * 100%."),
        ("NAM Visualizer Support: ", "Generates network animation (.nam) files for visual packet flow inspection.")
    ]
    for pfx, txt in points_ns2:
        p = tf_ns2.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = f"• {pfx}"
        r1.font.bold = True
        r1.font.color.rgb = CYAN_ACCENT
        r2 = p.add_run()
        r2.text = txt
        r2.font.color.rgb = TEXT_MUTED
        p.font.size = Pt(11.5)

    # =========================================================================
    # SLIDE 10: MULTI-TECHNIQUE NS-2 VERIFICATION MATRIX
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Empirical Validation", "Multi-Technique NS-2 Verification Matrix", "Empirical benchmark proving that all 5 error detection techniques are 100% verified across NS-2")

    # Table of Verification
    rows_data = [
        ("1D Parity Check", "110100100", "Node 0 ➔ Node 1 (2 Mbps)", "20.0% ErrorModel", "✓ Parity Bit Verified", "✅ VERIFIED IN NS-2"),
        ("2D Parity Matrix", "11011101001111...", "Node 0 ➔ Node 1 (2 Mbps)", "20.0% ErrorModel", "✓ Row/Col Corrected", "✅ VERIFIED IN NS-2"),
        ("Hamming Code (n,k)", "0110011 (7, 4)", "Node 0 ➔ Node 1 (2 Mbps)", "20.0% ErrorModel", "✓ Syndrome Auto-Flip", "✅ VERIFIED IN NS-2"),
        ("Internet Checksum", "1010100100111001...", "Node 0 ➔ Node 1 (2 Mbps)", "20.0% ErrorModel", "✓ 1's Complement Inverted", "✅ VERIFIED IN NS-2"),
        ("CRC Modulo-2", "11010110111110", "Node 0 ➔ Node 1 (2 Mbps)", "20.0% ErrorModel", "✓ Remainder == 0 Checked", "✅ VERIFIED IN NS-2")
    ]

    table_shape = s10.shapes.add_table(6, 6, Inches(0.8), Inches(1.9), Inches(11.73), Inches(3.2))
    table = table_shape.table

    # Column widths
    table.columns[0].width = Inches(2.2)
    table.columns[1].width = Inches(2.3)
    table.columns[2].width = Inches(2.3)
    table.columns[3].width = Inches(1.7)
    table.columns[4].width = Inches(1.8)
    table.columns[5].width = Inches(1.43)

    headers = ["Technique", "Transmitted Codeword", "NS-2 Channel Link", "ErrorModel PER", "Receiver Status", "NS-2 Status"]
    for c_idx, h_text in enumerate(headers):
        cell = table.cell(0, c_idx)
        cell.text = h_text
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(30, 58, 138) # Dark blue
        p = cell.text_frame.paragraphs[0]
        p.font.name = FONT_HEADING
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

    for r_idx, row in enumerate(rows_data):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx + 1, c_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = CARD_BG if r_idx % 2 == 0 else RGBColor(24, 32, 47)
            p = cell.text_frame.paragraphs[0]
            p.font.name = FONT_BODY
            p.font.size = Pt(11)
            if c_idx == 5:
                p.font.bold = True
                p.font.color.rgb = GREEN_ACCENT
            elif c_idx == 0:
                p.font.bold = True
                p.font.color.rgb = TEXT_WHITE
            else:
                p.font.color.rgb = TEXT_MUTED

    # Bottom Callout Box
    c_box = add_card(s10, 0.8, 5.35, 11.73, 1.55, "Live Benchmark Execution via REST API (/api/run-ns2-all)")
    p_cb = c_box.add_paragraph()
    p_cb.text = "Our platform features a dedicated multi-technique batch runner that encodes data across all 5 algorithms, transmits each through NS-2 in WSL, logs separate trace files (ns2_parity.tr, ns2_parity2d.tr, ns2_hamming.tr, ns2_checksum.tr, ns2_crc.tr), and verifies error detection and bit correction live!"
    p_cb.font.name = FONT_BODY
    p_cb.font.size = Pt(12)
    p_cb.font.color.rgb = TEXT_WHITE
    p_cb.space_before = Pt(4)

    # =========================================================================
    # SLIDE 11: COMPARATIVE ANALYSIS TABLE
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Algorithm Comparison", "Comparative Analysis of All 5 Techniques", "Comparing redundancy overhead, detection strength, correction capability, and protocol usage")

    comp_data = [
        ("1D Parity", "1 bit", "Single-bit & odd errors", "None (Detection only)", "O(n) - Single XOR", "Async Serial (UART), ASCII"),
        ("2D Parity Matrix", "M + N + 1 bits", "Burst errors & multiple bits", "1-bit error correction", "O(M × N) Grid", "Magnetic Tape, Telecommunications"),
        ("Hamming Code", "r bits (2^r >= m+r+1)", "Single & double-bit errors", "1-bit forward correction", "O(m log m) Syndrome", "ECC RAM, RAID-2, Space Telemetry"),
        ("Internet Checksum", "16 bits (typical)", "Burst errors & sums", "None (Detection only)", "O(n) Integer addition", "IPv4, TCP, UDP, ICMP"),
        ("CRC Modulo-2", "Degree r of G(x)", "100% single/double/burst <= r", "None (Detection only)", "O(n) Bitwise shift/XOR", "Ethernet, Wi-Fi 802.11, USB, SATA")
    ]

    t_comp = s11.shapes.add_table(6, 6, Inches(0.8), Inches(1.9), Inches(11.73), Inches(4.9)).table
    t_comp.columns[0].width = Inches(2.0)
    t_comp.columns[1].width = Inches(1.8)
    t_comp.columns[2].width = Inches(2.3)
    t_comp.columns[3].width = Inches(2.1)
    t_comp.columns[4].width = Inches(1.8)
    t_comp.columns[5].width = Inches(1.73)

    c_headers = ["Technique", "Redundancy Overhead", "Error Detection Power", "Error Correction", "Computational Cost", "Standard Protocols"]
    for c_idx, h_text in enumerate(c_headers):
        cell = t_comp.cell(0, c_idx)
        cell.text = h_text
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(14, 116, 144) # Cyan-700
        p = cell.text_frame.paragraphs[0]
        p.font.name = FONT_HEADING
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

    for r_idx, row in enumerate(comp_data):
        for c_idx, val in enumerate(row):
            cell = t_comp.cell(r_idx + 1, c_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = CARD_BG if r_idx % 2 == 0 else RGBColor(24, 32, 47)
            p = cell.text_frame.paragraphs[0]
            p.font.name = FONT_BODY
            p.font.size = Pt(11)
            if c_idx == 0:
                p.font.bold = True
                p.font.color.rgb = CYAN_ACCENT
            elif c_idx == 3 and "correction" in val.lower():
                p.font.bold = True
                p.font.color.rgb = GREEN_ACCENT
            else:
                p.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 12: IMPLEMENTATION & CONCLUSION
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Summary & Conclusion", "Implementation Highlights & Project Conclusion", "Fully functional multi-platform simulator ready for live classroom and lab demonstrations")

    tf_c1 = add_card(s12, 0.8, 1.9, 5.7, 4.9, "1. Key Implementation Accomplishments", "Engineering Deliverables:")
    pts_c1 = [
        ("Multi-Platform Architecture: ", "Available as Tkinter desktop GUI (main.py) and modern responsive web application (localhost:5000 & Vercel cloud)."),
        ("Genuine NS-2 Integration: ", "Automated OTcl script execution in WSL, live PER calculation, and 12-column event trace parsing."),
        ("Interactive Learning Experience: ", "Real-time bit clicking to inject channel noise, animated glowing ring feedback, and step-by-step mathematical visualizers."),
        ("Zero Pip Dependencies for Core GUI: ", "Desktop simulator runs cleanly using Python Standard Library alone.")
    ]
    for pfx, txt in pts_c1:
        p = tf_c1.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = f"• {pfx}"
        r1.font.bold = True
        r1.font.color.rgb = GREEN_ACCENT
        r2 = p.add_run()
        r2.text = txt
        r2.font.color.rgb = TEXT_MUTED
        p.font.size = Pt(11.5)

    tf_c2 = add_card(s12, 6.8, 1.9, 5.7, 4.9, "2. Project Team & Demonstration Access", "Developed by:")
    p_team_lead = tf_c2.add_paragraph()
    p_team_lead.text = "AMAN KUMAR YADAV\nPRATIK BHARADBHUNJE\nDEVRISHI GADIA"
    p_team_lead.font.name = FONT_HEADING
    p_team_lead.font.size = Pt(17)
    p_team_lead.font.bold = True
    p_team_lead.font.color.rgb = TEXT_WHITE
    p_team_lead.space_before = Pt(8)

    p_proj = tf_c2.add_paragraph()
    p_proj.text = "Computer Networks Lab Project"
    p_proj.font.name = FONT_BODY
    p_proj.font.size = Pt(13)
    p_proj.font.color.rgb = CYAN_ACCENT
    p_proj.space_before = Pt(6)

    pts_c2 = [
        ("Web Simulator URL: ", "http://localhost:5000"),
        ("Local Wi-Fi Network Access: ", "http://10.240.51.97:5000"),
        ("Source Code Repository: ", "https://github.com/Amanyadav201205/errordetection"),
        ("Desktop Application: ", "Run 'python main.py' or double-click 'run_app.bat'")
    ]
    for pfx, txt in pts_c2:
        p = tf_c2.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = f"• {pfx}"
        r1.font.bold = True
        r1.font.color.rgb = TEXT_WHITE
        r2 = p.add_run()
        r2.text = txt
        r2.font.color.rgb = TEXT_MUTED
        p.font.size = Pt(11)

    # Save presentation
    output_path = os.path.join(r"D:\CNLFINAL", "Error_Detection_and_Correction_Presentation.pptx")
    prs.save(output_path)
    print(f"Presentation successfully created at: {output_path}")
    return output_path

if __name__ == "__main__":
    create_slide_deck()
