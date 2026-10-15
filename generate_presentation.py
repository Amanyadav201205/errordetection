"""
Professional Presentation Generator for Computer Networks Lab Project
Title: Interactive Network Error Detection & Correction Simulator
Authors: AMAN KUMAR YADAV, PRATIK BHARADBHUNJE, DEVRISHI GADIA

Full Paragraph Edition: Detailed, comprehensive paragraph-by-paragraph academic explanations
across all 12 slides covering 1D Parity, 2D Parity Matrix, Hamming Code, Internet Checksum,
CRC Modulo-2, and Network Simulator 2 (NS-2) discrete-event channel simulation.
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
        bg.line.fill.background()
        return bg

    def add_header(slide, category_text, title_text, subtitle_text=None):
        set_slide_background(slide)
        
        # Category Badge
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(8), Inches(0.35))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = f"●  {category_text.upper()}"
        p_cat.font.name = FONT_HEADING
        p_cat.font.size = Pt(10.5)
        p_cat.font.bold = True
        p_cat.font.color.rgb = CYAN_ACCENT

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.65), Inches(11.73), Inches(0.65))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.name = FONT_HEADING
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_WHITE

        if subtitle_text:
            sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.22), Inches(11.73), Inches(0.4))
            tf_sub = sub_box.text_frame
            tf_sub.word_wrap = True
            p_sub = tf_sub.paragraphs[0]
            p_sub.text = subtitle_text
            p_sub.font.name = FONT_BODY
            p_sub.font.size = Pt(12)
            p_sub.font.color.rgb = TEXT_MUTED

    def add_card(slide, left, top, width, height, title=None, subtitle=None):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1.5)

        tx_box = slide.shapes.add_textbox(Inches(left + 0.25), Inches(top + 0.18), Inches(width - 0.5), Inches(height - 0.36))
        tf = tx_box.text_frame
        tf.word_wrap = True

        if title:
            p_title = tf.paragraphs[0]
            p_title.text = title
            p_title.font.name = FONT_HEADING
            p_title.font.size = Pt(15)
            p_title.font.bold = True
            p_title.font.color.rgb = CYAN_ACCENT

        if subtitle:
            p_sub = tf.add_paragraph()
            p_sub.text = subtitle
            p_sub.font.name = FONT_BODY
            p_sub.font.size = Pt(11)
            p_sub.font.color.rgb = TEXT_MUTED
            p_sub.space_before = Pt(2)

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
    pill = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(0.85), Inches(3.8), Inches(0.42))
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
    t_box = s1.shapes.add_textbox(Inches(1.0), Inches(1.4), Inches(11.33), Inches(1.5))
    tf1 = t_box.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "Interactive Network Error Detection & Correction Simulator"
    p1.font.name = FONT_HEADING
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE

    p1_sub = tf1.add_paragraph()
    p1_sub.text = "Comprehensive Mathematical Simulation of Data Link Layer Error Control Mechanisms Integrated with Network Simulator 2 (NS-2) Physical Channel Discrete-Event Modeling"
    p1_sub.font.name = FONT_BODY
    p1_sub.font.size = Pt(14)
    p1_sub.font.color.rgb = CYAN_ACCENT
    p1_sub.space_before = Pt(4)

    # Abstract Paragraph Card
    tf_abs = add_card(s1, 1.0, 3.1, 11.33, 2.1, "Project Overview & Engineering Scope")
    p_abs1 = tf_abs.add_paragraph()
    p_abs1.text = "This project presents an end-to-end interactive simulation platform designed to model Data Link Layer error control mechanisms, physical channel noise propagation, mathematical syndrome verification, and Network Simulator 2 (NS-2) discrete-event packet loss modeling. The platform unites five foundational error control algorithms—1D Parity, 2D Parity Matrix, Hamming Code (7, 4), Internet Checksum (RFC 1071), and Cyclic Redundancy Check (CRC)—with an interactive noise injection workbench, automated Forward Error Correction (FEC), and real-time trace file analytics."
    p_abs1.font.name = FONT_BODY
    p_abs1.font.size = Pt(11.5)
    p_abs1.font.color.rgb = TEXT_WHITE
    p_abs1.space_before = Pt(4)

    p_abs2 = tf_abs.add_paragraph()
    p_abs2.text = "By pairing rigorous mathematical encoding with discrete-event network channel simulation, students and researchers can dynamically inspect every stage of network transmission: codeword construction, bitwise noise injection, syndrome evaluation, and packet recovery across duplex links."
    p_abs2.font.name = FONT_BODY
    p_abs2.font.size = Pt(11)
    p_abs2.font.color.rgb = TEXT_MUTED
    p_abs2.space_before = Pt(4)

    # Team Members Container
    team_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(5.4), Inches(11.33), Inches(1.6))
    team_box.fill.solid()
    team_box.fill.fore_color.rgb = CARD_BG
    team_box.line.color.rgb = CARD_BORDER

    tb_header = s1.shapes.add_textbox(Inches(1.25), Inches(5.5), Inches(5.0), Inches(0.3))
    p_th = tb_header.text_frame.paragraphs[0]
    p_th.text = "PROJECT TEAM MEMBERS"
    p_th.font.name = FONT_HEADING
    p_th.font.size = Pt(11.5)
    p_th.font.bold = True
    p_th.font.color.rgb = CYAN_ACCENT

    members = [
        ("AMAN KUMAR YADAV", "1D/2D Parity & CRC Modulo-2 Division", "Full-Stack Web Engine & Project Architecture"),
        ("PRATIK BHARADBHUNJE", "Hamming Code Linear Block Equations", "Syndrome Evaluation & 1-Bit Error Correction"),
        ("DEVRISHI GADIA", "Internet Checksum 1's Complement Sum", "NS-2 Physical Channel Modeling & Trace Analytics")
    ]
    for idx, (m_name, r1, r2) in enumerate(members):
        col_x = 1.25 + (idx * 3.75)
        m_box = s1.shapes.add_textbox(Inches(col_x), Inches(5.85), Inches(3.6), Inches(1.05))
        tf_m = m_box.text_frame
        tf_m.word_wrap = True
        pm1 = tf_m.paragraphs[0]
        pm1.text = m_name
        pm1.font.name = FONT_HEADING
        pm1.font.size = Pt(14)
        pm1.font.bold = True
        pm1.font.color.rgb = TEXT_WHITE
        
        pm2 = tf_m.add_paragraph()
        pm2.text = f"• {r1}\n• {r2}"
        pm2.font.name = FONT_BODY
        pm2.font.size = Pt(10.5)
        pm2.font.color.rgb = TEXT_MUTED
        pm2.space_before = Pt(2)

    # =========================================================================
    # SLIDE 2: PROJECT OVERVIEW & OBJECTIVES
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Executive Summary", "Project Motivation, Problem Statement & Objectives", "Bridging theoretical Data Link Layer error control with realistic physical channel noise modeling")

    tf_c1 = add_card(s2, 0.8, 1.75, 5.7, 5.3, "1. The Physical Channel Problem Statement", "Transmission media impairments and silent data corruption:")
    p_c1_1 = tf_c1.add_paragraph()
    p_c1_1.text = "In modern data communications, physical transmission channels—such as copper twisted pairs, coaxial cables, optical fibers, and free-space wireless RF media—are inherently subject to ambient physical impairments. Thermal noise, electromagnetic interference (EMI), signal attenuation, cross-talk, and transient voltage spikes cause bit inversions (0 becoming 1 or 1 becoming 0) and multi-bit burst corruptions across transmission lines."
    p_c1_1.font.name = FONT_BODY
    p_c1_1.font.size = Pt(11)
    p_c1_1.font.color.rgb = TEXT_WHITE
    p_c1_1.space_before = Pt(6)

    p_c1_2 = tf_c1.add_paragraph()
    p_c1_2.text = "Without robust Data Link Layer error control, higher-layer protocols (such as TCP, IP, and application payloads) receive corrupted frames, resulting in catastrophic system crashes, corrupted database records, and critical security vulnerabilities. Furthermore, traditional academic instruction relies on static textbook formulas that fail to demonstrate how check bits interact with live channel noise, queueing delays, and packet drop events across active communication links."
    p_c1_2.font.name = FONT_BODY
    p_c1_2.font.size = Pt(10.5)
    p_c1_2.font.color.rgb = TEXT_MUTED
    p_c1_2.space_before = Pt(6)

    tf_c2 = add_card(s2, 6.8, 1.75, 5.7, 5.3, "2. Project Engineering Objectives", "Comprehensive interactive simulation suite and goals:")
    p_c2_1 = tf_c2.add_paragraph()
    p_c2_1.text = "The primary objective of this project is to bridge mathematical error detection theory with practical network engineering. We developed an interactive dual-mode simulation environment that implements five classical error control algorithms from first mathematical principles while linking each algorithm to a real-world Network Simulator 2 (NS-2) discrete-event transmission engine."
    p_c2_1.font.name = FONT_BODY
    p_c2_1.font.size = Pt(11)
    p_c2_1.font.color.rgb = TEXT_WHITE
    p_c2_1.space_before = Pt(6)

    p_c2_2 = tf_c2.add_paragraph()
    p_c2_2.text = "The platform provides complete transparency into every phase of communication: binary data encoding, redundancy overhead calculation, physical channel noise injection, receiver syndrome computation, and Forward Error Correction (FEC). Available as a Python Tkinter desktop GUI, a local HTTP server, and a cloud-hosted web application, the system allows students and professors to interactively flip bits, configure NS-2 error rates, and observe real-time packet recovery."
    p_c2_2.font.name = FONT_BODY
    p_c2_2.font.size = Pt(10.5)
    p_c2_2.font.color.rgb = TEXT_MUTED
    p_c2_2.space_before = Pt(6)

    # =========================================================================
    # SLIDE 3: END-TO-END PIPELINE (6 STAGES)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "System Architecture", "End-to-End Network Transmission Pipeline", "The 6 architectural stages modeling sender encoding, channel transmission, noise, and receiver recovery")

    tf_s3_l = add_card(s3, 0.8, 1.75, 5.7, 5.3, "Transmitter & Channel Modeling (Stages 1–3)", "Message generation, mathematical encoding, and NS-2 link traversal:")
    p_s3_l1 = tf_s3_l.add_paragraph()
    p_s3_l1.text = "The simulator is organized around an end-to-end 6-stage transmission architecture that mirrors the actual lifecycle of a Data Link Layer frame traversing a noisy physical network. In STAGE 1 (Binary Message Input), arbitrary binary sequences or ASCII plaintext are validated, formatted, and converted into raw data vectors, with presets available for 4, 8, 12, and 16-bit word lengths."
    p_s3_l1.font.name = FONT_BODY
    p_s3_l1.font.size = Pt(11)
    p_s3_l1.font.color.rgb = TEXT_WHITE
    p_s3_l1.space_before = Pt(6)

    p_s3_l2 = tf_s3_l.add_paragraph()
    p_s3_l2.text = "In STAGE 2 (Redundancy Encoding & Framing), the selected mathematical algorithm computes redundant check bits—such as 1D parity bits, 2D matrix parities, power-of-two Hamming check bits, 1's complement checksums, or CRC remainder polynomials—and appends them to form the transmitted codeword. In STAGE 3 (Physical Channel & NS-2 Modeling), the codeword is transmitted across a point-to-point duplex link modeled in NS-2 (network_error_sim.tcl) with 2 Mbps bandwidth, 10 ms delay, and DropTail queue management, establishing an authentic discrete-event transmission environment."
    p_s3_l2.font.name = FONT_BODY
    p_s3_l2.font.size = Pt(10.5)
    p_s3_l2.font.color.rgb = TEXT_MUTED
    p_s3_l2.space_before = Pt(6)

    tf_s3_r = add_card(s3, 6.8, 1.75, 5.7, 5.3, "Noise Injection, Receiver & Recovery (Stages 4–6)", "Physical corruption, syndrome decoding, and autonomous error recovery:")
    p_s3_r1 = tf_s3_r.add_paragraph()
    p_s3_r1.text = "In STAGE 4 (Channel Noise & Error Injection), transmission noise is introduced either stochastically via the NS-2 ErrorModel or interactively by allowing the user to click any bit on the canvas to invert it (0 <-> 1), inject random single-bit noise, or simulate multi-bit burst corruptions affecting consecutive bits across the wire."
    p_s3_r1.font.name = FONT_BODY
    p_s3_r1.font.size = Pt(11)
    p_s3_r1.font.color.rgb = TEXT_WHITE
    p_s3_r1.space_before = Pt(6)

    p_s3_r2 = tf_s3_r.add_paragraph()
    p_s3_r2.text = "In STAGE 5 (Receiver Verification & Syndrome Computation), the receiving node recalculates parity equations, executes 1's complement addition, or carries out Modulo-2 polynomial long division on the incoming frame. Finally, in STAGE 6 (Diagnosis, Recovery & FEC), the system localizes bit errors, applies automatic Forward Error Correction where algebraically possible (as in 2D Parity and Hamming Codes), or triggers packet discard flags, displaying complete step-by-step diagnostic feedback."
    p_s3_r2.font.name = FONT_BODY
    p_s3_r2.font.size = Pt(10.5)
    p_s3_r2.font.color.rgb = TEXT_MUTED
    p_s3_r2.space_before = Pt(6)

    # =========================================================================
    # SLIDE 4: TECHNIQUE 1 — 1D PARITY CHECK
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Algorithm 1 of 5", "1D Parity Check (Vertical Redundancy Check)", "Minimal bandwidth redundancy mechanism for single-bit error detection")

    tf_p1 = add_card(s4, 0.8, 1.75, 5.7, 5.3, "Mathematical Formulation & Working Mechanism", "Parity generation, decision boundary, and algebraic limitations:")
    p_p1_1 = tf_p1.add_paragraph()
    p_p1_1.text = "One-Dimensional (1D) Parity Check, traditionally referred to as Vertical Redundancy Check (VRC), represents the simplest and most lightweight error-detection mechanism in digital telecommunications. The algorithm appends a single redundant parity bit (P) to an n-bit binary data stream so that the total count of 1-bits conforms to a pre-defined parity convention. Under Even Parity, the check bit is generated as the Exclusive-OR (XOR) sum of all message bits: P = b1 ^ b2 ^ ... ^ bn, ensuring that the total count of 1s in the transmitted codeword is always even. Under Odd Parity, P is inverted so the total count of 1s is always odd."
    p_p1_1.font.name = FONT_BODY
    p_p1_1.font.size = Pt(11)
    p_p1_1.font.color.rgb = TEXT_WHITE
    p_p1_1.space_before = Pt(6)

    p_p1_2 = tf_p1.add_paragraph()
    p_p1_2.text = "At the receiving destination, the entire received codeword is XOR-summed. If the parity sum matches the expected scheme, the frame is accepted as valid. While 1D Parity requires minimal bandwidth overhead (a single bit per frame), its detection capability is strictly limited: it reliably detects all single-bit errors and any odd number of simultaneous bit flips (1, 3, 5 bits), but is completely blind to even numbers of bit flips (2, 4, 6 bits), because two inverted bits cancel each other out during binary XOR summation."
    p_p1_2.font.name = FONT_BODY
    p_p1_2.font.size = Pt(10.5)
    p_p1_2.font.color.rgb = TEXT_MUTED
    p_p1_2.space_before = Pt(6)

    tf_p2 = add_card(s4, 6.8, 1.75, 5.7, 5.3, "NS-2 Channel Integration & Trace Analytics", "Duplex link simulation and ErrorModel packet drop verification:")
    p_p2_1 = tf_p2.add_paragraph()
    p_p2_1.text = "In our simulation platform, the 1D Parity module is integrated with Network Simulator 2 via the network_error_sim.tcl simulation script. The transmitter node (Node 0) encapsulates the parity-encoded codeword (for example, data '11010010' with even parity bit '0' yielding codeword '110100100') into Constant Bit Rate (CBR) UDP packets and transmits them across a 2 Mbps duplex link with a 10 ms delay toward the receiver sink (Node 1)."
    p_p2_1.font.name = FONT_BODY
    p_p2_1.font.size = Pt(11)
    p_p2_1.font.color.rgb = TEXT_WHITE
    p_p2_1.space_before = Pt(6)

    p_p2_2 = tf_p2.add_paragraph()
    p_p2_2.text = "Physical channel noise is introduced using the NS-2 ErrorModel/Uniform module, which injects packet loss and bit corruption according to a statistical packet error rate. The entire discrete-event sequence is logged into ns2/ns2_parity.tr. When NS-2 corrupts a single bit in transit, the receiver parity check fails immediately, generating an 'Error Detected' alert and discarding the packet. This confirms that 1D Parity provides 100% detection reliability for isolated single-bit transmission noise across simulated links."
    p_p2_2.font.name = FONT_BODY
    p_p2_2.font.size = Pt(10.5)
    p_p2_2.font.color.rgb = TEXT_MUTED
    p_p2_2.space_before = Pt(6)

    # =========================================================================
    # SLIDE 5: TECHNIQUE 2 — 2D PARITY CHECK (MATRIX GRID)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Algorithm 2 of 5", "2D Parity Check (Matrix Grid Localization)", "Combining Longitudinal (LRC) & Vertical (VRC) Redundancy Checks for bit error correction")

    tf_2d1 = add_card(s5, 0.8, 1.75, 5.7, 5.3, "Matrix Structuring & Error Localization", "Two-dimensional parity calculations and geometric intersection:")
    p_2d1_1 = tf_2d1.add_paragraph()
    p_2d1_1.text = "Two-Dimensional (2D) Parity Check significantly enhances error detection capability by organizing the raw binary message into a two-dimensional matrix of M rows and N columns. Each individual row is assigned a Longitudinal Redundancy Check (LRC) parity bit, while each column is assigned a Vertical Redundancy Check (VRC) parity bit. In addition, an overall corner parity bit is computed across all row parity bits, producing a total check bit overhead of M + N + 1 bits. This orthogonal grid structure establishes two independent parity constraints for every single data bit in the matrix."
    p_2d1_1.font.name = FONT_BODY
    p_2d1_1.font.size = Pt(11)
    p_2d1_1.font.color.rgb = TEXT_WHITE
    p_2d1_1.space_before = Pt(6)

    p_2d1_2 = tf_2d1.add_paragraph()
    p_2d1_2.text = "When the frame arrives at the receiving node, parities are recalculated along both dimensions, generating a row syndrome vector and a column syndrome vector. If a single bit flip occurs at row coordinate i and column coordinate j, both the row i parity check and column j parity check fail simultaneously. The receiver determines the exact geometric intersection (i, j) of the failed parity lines, precisely localizing the corrupted bit without ambiguity."
    p_2d1_2.font.name = FONT_BODY
    p_2d1_2.font.size = Pt(10.5)
    p_2d1_2.font.color.rgb = TEXT_MUTED
    p_2d1_2.space_before = Pt(6)

    tf_2d2 = add_card(s5, 6.8, 1.75, 5.7, 5.3, "Forward Error Correction & NS-2 Trace Integration", "Autonomous 1-bit repair and multi-packet channel modeling:")
    p_2d2_1 = tf_2d2.add_paragraph()
    p_2d2_1.text = "The defining breakthrough of 2D Parity over 1D Parity is its capability for autonomous Forward Error Correction (FEC). Once the corrupted bit coordinate (i, j) is localized, the receiver inverts that specific bit (b[i][j] = ~b[i][j]), fully restoring the original data vector without requiring a costly packet retransmission. Additionally, 2D Parity detects up to 3 simultaneous bit errors and 100% of all burst corruptions whose length does not exceed N bits."
    p_2d2_1.font.name = FONT_BODY
    p_2d2_1.font.size = Pt(11)
    p_2d2_1.font.color.rgb = TEXT_WHITE
    p_2d2_1.space_before = Pt(6)

    p_2d2_2 = tf_2d2.add_paragraph()
    p_2d2_2.text = "In our NS-2 simulation environment, the serialized 2D Parity matrix is transmitted across the duplex link between Node 0 and Node 1. The resulting trace events logged in ns2/ns2_parity2d.tr capture packet enqueue, link propagation, and receiver queueing. When channel noise corrupts a bit in transit, the receiver reconstructs the matrix grid, pinpoints the faulty row and column, and visually restores the corrupted bit in real time, demonstrating complete physical-to-link-layer error recovery."
    p_2d2_2.font.name = FONT_BODY
    p_2d2_2.font.size = Pt(10.5)
    p_2d2_2.font.color.rgb = TEXT_MUTED
    p_2d2_2.space_before = Pt(6)

    # =========================================================================
    # SLIDE 6: TECHNIQUE 3 — HAMMING CODE (n, k)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Algorithm 3 of 5", "Hamming Code (n, k) & Forward Error Correction", "Power-of-two parity placement with mathematical syndrome calculation for automatic bit recovery")

    tf_h1 = add_card(s6, 0.8, 1.75, 5.7, 5.3, "Mathematical Foundation & Linear Block Theory", "Richard Hamming (1950) coding theory and power-of-two bit placement:")
    p_h1_1 = tf_h1.add_paragraph()
    p_h1_1.text = "Formulated by Richard W. Hamming in 1950, Hamming Codes are a distinguished family of linear block codes that achieve single-error correction (SEC) and double-error detection (DED). In the standard Hamming (7, 4) scheme, 4 information data bits (d1, d2, d3, d4) are combined with 3 redundant check bits (p1, p2, p4) to form a 7-bit codeword. Parity bits are strictly assigned to bit positions that are powers of two (1, 2, 4, 8, ...), while data bits occupy the remaining non-power-of-two indices (3, 5, 6, 7). The required number of parity bits r for k data bits is governed by Hamming's rule: 2^r >= k + r + 1."
    p_h1_1.font.name = FONT_BODY
    p_h1_1.font.size = Pt(11)
    p_h1_1.font.color.rgb = TEXT_WHITE
    p_h1_1.space_before = Pt(6)

    p_h1_2 = tf_h1.add_paragraph()
    p_h1_2.text = "Each parity bit covers a specific subset of codeword bits whose binary index representation contains a 1 at that parity bit's power-of-two position. Specifically, p1 covers bits {1, 3, 5, 7}, p2 covers bits {2, 3, 6, 7}, and p4 covers bits {4, 5, 6, 7}. This orthogonal assignment ensures that every bit position in the codeword is represented by a unique binary combination of parity bits, establishing a linear system of parity-check equations over GF(2)."
    p_h1_2.font.name = FONT_BODY
    p_h1_2.font.size = Pt(10.5)
    p_h1_2.font.color.rgb = TEXT_MUTED
    p_h1_2.space_before = Pt(6)

    tf_h2 = add_card(s6, 6.8, 1.75, 5.7, 5.3, "Syndrome Decoding, FEC & NS-2 Trace Integration", "Automatic single-bit correction and server memory applications:")
    p_h2_1 = tf_h2.add_paragraph()
    p_h2_1.text = "At the destination receiver, each parity-check equation is re-evaluated to construct a 3-bit syndrome vector: S = (s3, s2, s1) in binary. If S = 000, the transmission is perfectly clean. If a single bit flip occurs during transit, the decimal value of the syndrome vector S directly corresponds to the exact 1-indexed position of the corrupted bit (for example, syndrome S = 101_2 = 5 indicates that bit 5 is inverted). The receiver automatically flips bit 5 back to its original state, achieving instantaneous forward error correction without retransmission."
    p_h2_1.font.name = FONT_BODY
    p_h2_1.font.size = Pt(11)
    p_h2_1.font.color.rgb = TEXT_WHITE
    p_h2_1.space_before = Pt(6)

    p_h2_2 = tf_h2.add_paragraph()
    p_h2_2.text = "Because Hamming codes execute in O(1) hardware cycle latency, they are ubiquitously deployed in server ECC RAM, processor caches, satellite telemetries, and RAID-2 storage systems. In our simulator, the Hamming module is bridged to NS-2 (ns2/ns2_hamming.tr). Packets subjected to simulated channel noise are captured at the receiver sink, where the 3-bit syndrome decoder identifies and repairs the inverted bit, proving empirical forward error correction across discrete-event network channels."
    p_h2_2.font.name = FONT_BODY
    p_h2_2.font.size = Pt(10.5)
    p_h2_2.font.color.rgb = TEXT_MUTED
    p_h2_2.space_before = Pt(6)

    # =========================================================================
    # SLIDE 7: TECHNIQUE 4 — INTERNET CHECKSUM
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Algorithm 4 of 5", "Internet Checksum (1's Complement Summation)", "The foundational error detection mechanism powering IPv4, TCP, and UDP packet headers")

    tf_ck1 = add_card(s7, 0.8, 1.75, 5.7, 5.3, "Mathematical Mechanism & 1's Complement", "RFC 1071 standard protocol mechanism and end-around carry addition:")
    p_ck1_1 = tf_ck1.add_paragraph()
    p_ck1_1.text = "The Internet Checksum is the foundational error-detection algorithm standardized in RFC 1071 and ubiquitously deployed across the core protocols of the TCP/IP suite, including IPv4 header validation, TCP segment integrity, and UDP datagram checking. The algorithm operates by segmenting the binary input stream into uniform k-bit words (typically 16-bit integers in network implementations). These words are summed together sequentially using One's Complement Arithmetic, which differs fundamentally from standard two's complement addition."
    p_ck1_1.font.name = FONT_BODY
    p_ck1_1.font.size = Pt(11)
    p_ck1_1.font.color.rgb = TEXT_WHITE
    p_ck1_1.space_before = Pt(6)

    p_ck1_2 = tf_ck1.add_paragraph()
    p_ck1_2.text = "Whenever an addition produces a carry bit exceeding the k-bit boundary (an overflow), the carry bit is not discarded; instead, it is wrapped around and added back into the least significant bit (LSB), a process known as end-around carry. Once all words have been accumulated into the running sum, the bitwise one's complement (NOT operation) of the final sum is calculated, and this resulting k-bit value is transmitted as the checksum field alongside the original data payload."
    p_ck1_2.font.name = FONT_BODY
    p_ck1_2.font.size = Pt(10.5)
    p_ck1_2.font.color.rgb = TEXT_MUTED
    p_ck1_2.space_before = Pt(6)

    tf_ck2 = add_card(s7, 6.8, 1.75, 5.7, 5.3, "Receiver Zero-Check, Limits & NS-2 Modeling", "Fast router computation, protocol context, and channel loss verification:")
    p_ck2_1 = tf_ck2.add_paragraph()
    p_ck2_1.text = "At the destination receiver, the verification process is computationally elegant and highly optimized for router processing: the receiver sums all incoming k-bit data words plus the received checksum using one's complement addition. If no bits were corrupted during transit, the resulting sum must evaluate to all 1-bits (0xFFFF in hexadecimal), which inverts to 0x0000 (zero). Any non-zero result indicates that transmission corruption occurred, prompting the transport layer to discard the corrupted segment immediately."
    p_ck2_1.font.name = FONT_BODY
    p_ck2_1.font.size = Pt(11)
    p_ck2_1.font.color.rgb = TEXT_WHITE
    p_ck2_1.space_before = Pt(6)

    p_ck2_2 = tf_ck2.add_paragraph()
    p_ck2_2.text = "Although the Internet Checksum is exceptionally fast to compute in software, it possesses recognized algorithmic limitations: it cannot detect transposed words (swapping the order of two 16-bit blocks) or compensating bit errors (where an increment in one word is mathematically cancelled by a decrement in another). In our NS-2 simulation bridge, checksum-protected packets are transmitted across the simulated link (ns2/ns2_checksum.tr). Corrupted frames trigger receiver checksum validation failures and record packet drop events at intermediate router queues."
    p_ck2_2.font.name = FONT_BODY
    p_ck2_2.font.size = Pt(10.5)
    p_ck2_2.font.color.rgb = TEXT_MUTED
    p_ck2_2.space_before = Pt(6)

    # =========================================================================
    # SLIDE 8: TECHNIQUE 5 — CYCLIC REDUNDANCY CHECK (CRC)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Algorithm 5 of 5", "Cyclic Redundancy Check (CRC Modulo-2 Division)", "High-performance polynomial division over GF(2) utilized in Ethernet, Wi-Fi, and USB")

    tf_crc1 = add_card(s8, 0.8, 1.75, 5.7, 5.3, "Galois Field GF(2) Polynomial Long Division", "Algebraic foundation, generator polynomials, and frame check sequence:")
    p_crc1_1 = tf_crc1.add_paragraph()
    p_crc1_1.text = "Cyclic Redundancy Check (CRC) is the most powerful, mathematically sophisticated, and widely deployed error-detection mechanism in modern computer networking, serving as the mandatory standard for Ethernet (IEEE 802.3), Wi-Fi (IEEE 802.11), USB, SATA, and cellular wireless links. CRC treats binary data sequences as algebraic polynomials whose coefficients belong to the Galois Field of two elements, GF(2). In GF(2) arithmetic, addition and subtraction are identical and equivalent to the bitwise Exclusive-OR (XOR) operation performed without carries or borrows."
    p_crc1_1.font.name = FONT_BODY
    p_crc1_1.font.size = Pt(11)
    p_crc1_1.font.color.rgb = TEXT_WHITE
    p_crc1_1.space_before = Pt(6)

    p_crc1_2 = tf_crc1.add_paragraph()
    p_crc1_2.text = "Given an n-bit data polynomial D(x) and a predetermined (r+1)-bit generator polynomial G(x), the sender first appends r zeros to the data polynomial, shifting it by x^r: D(x) * x^r. The sender then executes binary long division of D(x) * x^r by G(x) using Modulo-2 XOR operations. The resulting r-bit remainder polynomial, R(x), constitutes the Frame Check Sequence (FCS) and is appended to the message: T(x) = D(x) * x^r ^ R(x). The transmitted codeword polynomial T(x) is mathematically guaranteed to be exactly divisible by G(x)."
    p_crc1_2.font.name = FONT_BODY
    p_crc1_2.font.size = Pt(10.5)
    p_crc1_2.font.color.rgb = TEXT_MUTED
    p_crc1_2.space_before = Pt(6)

    tf_crc2 = add_card(s8, 6.8, 1.75, 5.7, 5.3, "Detection Superiority, Presets & NS-2 Trace Integration", "Comprehensive burst-error detection and industry standards:")
    p_crc2_1 = tf_crc2.add_paragraph()
    p_crc2_1.text = "The mathematical properties of CRC provide extraordinary detection power: a CRC with an r-bit generator polynomial detects 100% of all single-bit errors, 100% of all double-bit errors, 100% of all odd numbers of errors (provided G(x) contains (x+1) as a factor), and 100% of all burst error corruptions of length up to r bits. Our simulator supports key industry generator polynomials, including CRC-4 (x^4 + x + 1), CRC-8 (x^8 + x^2 + x + 1), CRC-16-IBM (x^16 + x^15 + x^2 + 1), CRC-CCITT (x^16 + x^12 + x^5 + 1), and CRC-32 (Ethernet standard)."
    p_crc2_1.font.name = FONT_BODY
    p_crc2_1.font.size = Pt(11)
    p_crc2_1.font.color.rgb = TEXT_WHITE
    p_crc2_1.space_before = Pt(6)

    p_crc2_2 = tf_crc2.add_paragraph()
    p_crc2_2.text = "At the receiving node, the entire incoming codeword is divided by G(x). A remainder of zero confirms an uncorrupted frame, whereas any non-zero remainder alerts the Data Link Layer to discard the frame. In our NS-2 simulation (ns2/ns2_crc.tr), CRC-encoded frames traverse the simulated duplex link under varying ErrorModel loss rates. Corrupted frames reliably trigger non-zero syndrome remainders and register drop events in the NS-2 trace, modeling realistic Ethernet frame discards."
    p_crc2_2.font.name = FONT_BODY
    p_crc2_2.font.size = Pt(10.5)
    p_crc2_2.font.color.rgb = TEXT_MUTED
    p_crc2_2.space_before = Pt(6)

    # =========================================================================
    # SLIDE 9: NETWORK SIMULATOR 2 (NS-2) ARCHITECTURE
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Channel Simulation Engine", "Network Simulator 2 (NS-2) Integration Architecture", "Coupling physical link discrete-event simulation with Data Link Layer error control")

    tf_ns1 = add_card(s9, 0.8, 1.75, 5.7, 5.3, "OTcl Network Topology Configuration", "Physical channel modeling in network_error_sim.tcl:")
    p_ns1_1 = tf_ns1.add_paragraph()
    p_ns1_1.text = "Network Simulator 2 (NS-2) is an industry-standard, object-oriented discrete-event network simulator widely utilized in telecommunication research to model network protocol dynamics, routing algorithms, and physical channel transmission impairments. NS-2 operates on a dual-language architecture: the core simulation engine and packet scheduler are written in C++ for maximum computational throughput, while simulation topology scripts, agent configurations, and event schedules are authored in Object Tcl (OTcl)."
    p_ns1_1.font.name = FONT_BODY
    p_ns1_1.font.size = Pt(11)
    p_ns1_1.font.color.rgb = TEXT_WHITE
    p_ns1_1.space_before = Pt(6)

    p_ns1_2 = tf_ns1.add_paragraph()
    p_ns1_2.text = "In our project, the physical channel is configured in ns2/network_error_sim.tcl. The simulation creates a point-to-point network topology consisting of a source node (Node 0) and a destination sink node (Node 1). Node 0 is configured with a UDP agent connected to a Constant Bit Rate (CBR) traffic generator transmitting 64-byte packets. Node 1 is equipped with an Agent/Null sink. The two nodes are connected via a full-duplex link configured with a bandwidth of 2.0 Mbps, a propagation delay of 10 ms, and a DropTail queue discipline."
    p_ns1_2.font.name = FONT_BODY
    p_ns1_2.font.size = Pt(10.5)
    p_ns1_2.font.color.rgb = TEXT_MUTED
    p_ns1_2.space_before = Pt(6)

    tf_ns2 = add_card(s9, 6.8, 1.75, 5.7, 5.3, "Trace File (.tr) Parsing & Python-to-NS-2 Bridge", "Real-time event analytics and WSL execution bridge:")
    p_ns2_1 = tf_ns2.add_paragraph()
    p_ns2_1.text = "To authentically simulate noisy physical transmission channels, the NS-2 ErrorModel/Uniform module is inserted directly into the duplex link between Node 0 and Node 1. The ErrorModel applies a configurable statistical packet loss rate, causing packets to be dropped or corrupted during transit. Dropped packets are redirected to an Agent/Null drop-target, capturing realistic channel packet drop behavior."
    p_ns2_1.font.name = FONT_BODY
    p_ns2_1.font.size = Pt(11)
    p_ns2_1.font.color.rgb = TEXT_WHITE
    p_ns2_1.space_before = Pt(6)

    p_ns2_2 = tf_ns2.add_paragraph()
    p_ns2_2.text = "As packets traverse the simulated link, NS-2 outputs granular event records to standard trace files (.tr). Our Python simulation bridge (modules/ns2_bridge.py) automates the execution of NS-2 inside Windows Subsystem for Linux (WSL) and parses the 12-column event records: '+' indicates packet enqueue at Node 0, '-' indicates packet transmission onto the physical wire, 'r' represents successful packet arrival at Node 1, and 'd' denotes a packet dropped due to queue congestion or simulated channel noise. The parser computes the Packet Error Rate (PER) in real time and streams trace analytics directly to the user interface."
    p_ns2_2.font.name = FONT_BODY
    p_ns2_2.font.size = Pt(10.5)
    p_ns2_2.font.color.rgb = TEXT_MUTED
    p_ns2_2.space_before = Pt(6)

    # =========================================================================
    # SLIDE 10: MULTI-TECHNIQUE NS-2 VERIFICATION MATRIX
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Empirical Validation", "Multi-Technique NS-2 Verification Matrix", "Empirical benchmark proving that all 5 error detection techniques are 100% verified across NS-2")

    rows_data = [
        ("1D Parity Check", "110100100", "Node 0 ➔ Node 1 (2 Mbps)", "20.0% ErrorModel", "✓ Parity Bit Verified", "✅ VERIFIED IN NS-2"),
        ("2D Parity Matrix", "11011101001111...", "Node 0 ➔ Node 1 (2 Mbps)", "20.0% ErrorModel", "✓ Row/Col Corrected", "✅ VERIFIED IN NS-2"),
        ("Hamming Code (n,k)", "0110011 (7, 4)", "Node 0 ➔ Node 1 (2 Mbps)", "20.0% ErrorModel", "✓ Syndrome Auto-Flip", "✅ VERIFIED IN NS-2"),
        ("Internet Checksum", "1010100100111001...", "Node 0 ➔ Node 1 (2 Mbps)", "20.0% ErrorModel", "✓ 1's Complement Inverted", "✅ VERIFIED IN NS-2"),
        ("CRC Modulo-2", "11010110111110", "Node 0 ➔ Node 1 (2 Mbps)", "20.0% ErrorModel", "✓ Remainder == 0 Checked", "✅ VERIFIED IN NS-2")
    ]

    table_shape = s10.shapes.add_table(6, 6, Inches(0.8), Inches(1.75), Inches(11.73), Inches(2.7))
    table = table_shape.table

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
        cell.fill.fore_color.rgb = RGBColor(30, 58, 138)
        p = cell.text_frame.paragraphs[0]
        p.font.name = FONT_HEADING
        p.font.size = Pt(11)
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
            p.font.size = Pt(10)
            if c_idx == 5:
                p.font.bold = True
                p.font.color.rgb = GREEN_ACCENT
            elif c_idx == 0:
                p.font.bold = True
                p.font.color.rgb = TEXT_WHITE
            else:
                p.font.color.rgb = TEXT_MUTED

    c_box = add_card(s10, 0.8, 4.65, 11.73, 2.4, "Empirical NS-2 Verification & Batch Runner Analysis (/api/run-ns2-all)")
    p_cb1 = c_box.add_paragraph()
    p_cb1.text = "To provide rigorous empirical evidence to the academic examination panel, our simulation platform links each of the five error control algorithms directly to its own dedicated NS-2 trace file. In the project directory, five distinct trace files—ns2_parity.tr, ns2_parity2d.tr, ns2_hamming.tr, ns2_checksum.tr, and ns2_crc.tr—record the exact packet transmission, queue latency, and drop events generated during live simulation runs."
    p_cb1.font.name = FONT_BODY
    p_cb1.font.size = Pt(11)
    p_cb1.font.color.rgb = TEXT_WHITE
    p_cb1.space_before = Pt(4)

    p_cb2 = c_box.add_paragraph()
    p_cb2.text = "Our platform features a dedicated multi-technique batch runner accessible via the REST API endpoint /api/run-ns2-all. When triggered, the engine serializes codewords for each algorithm, executes the NS-2 simulation inside WSL, and parses the resulting trace logs in parallel. The benchmark confirms that across all five techniques, packets subjected to simulated channel noise are either mathematically corrected at the receiver (for 2D Parity and Hamming Codes) or accurately flagged as corrupted and discarded (for 1D Parity, Checksum, and CRC), proving 100% empirical validation in NS-2."
    p_cb2.font.name = FONT_BODY
    p_cb2.font.size = Pt(10.5)
    p_cb2.font.color.rgb = TEXT_MUTED
    p_cb2.space_before = Pt(4)

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

    t_comp = s11.shapes.add_table(6, 6, Inches(0.8), Inches(1.75), Inches(11.73), Inches(2.7)).table
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
        cell.fill.fore_color.rgb = RGBColor(14, 116, 144)
        p = cell.text_frame.paragraphs[0]
        p.font.name = FONT_HEADING
        p.font.size = Pt(11)
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
            p.font.size = Pt(10)
            if c_idx == 0:
                p.font.bold = True
                p.font.color.rgb = CYAN_ACCENT
            elif c_idx == 3 and "correction" in val.lower():
                p.font.bold = True
                p.font.color.rgb = GREEN_ACCENT
            else:
                p.font.color.rgb = TEXT_MUTED

    c_comp_box = add_card(s11, 0.8, 4.65, 11.73, 2.4, "Multi-Dimensional Technical Trade-Off Analysis")
    p_cc1 = c_comp_box.add_paragraph()
    p_cc1.text = "A comprehensive engineering evaluation of error control mechanisms requires balancing four competing design constraints: transmission bandwidth overhead, computational complexity, error detection strength, and forward error correction capability. 1D Parity offers the absolute lowest bandwidth overhead (1 bit per codeword) and simplest hardware implementation (O(n) XOR gates), but provides no error correction and fails to detect even numbers of bit flips. 2D Parity introduces moderate overhead (M + N + 1 bits) but achieves single-bit forward error correction through orthogonal grid localization. Hamming Code provides optimal single-error correction (SEC) with logarithmic parity overhead (ceil(log2(n+k+1))), making it ideal for hardware-accelerated memory architectures."
    p_cc1.font.name = FONT_BODY
    p_cc1.font.size = Pt(11)
    p_cc1.font.color.rgb = TEXT_WHITE
    p_cc1.space_before = Pt(4)

    p_cc2 = c_comp_box.add_paragraph()
    p_cc2.text = "The Internet Checksum requires a constant 16-bit overhead per packet and operates via simple 1's complement arithmetic (O(n) time), making it exceptionally lightweight for software execution in operating system IP stacks, though it is vulnerable to transposed and compensating bit errors. Cyclic Redundancy Check (CRC) represents the pinnacle of error detection power, guaranteeing 100% detection of all single-bit, double-bit, odd-bit, and burst errors up to r bits. Although software CRC division requires O(n * r) operations, hardware implementations execute at wire speed (O(1) cycle latency) using Linear Feedback Shift Registers (LFSR). In industry, these techniques are deployed across standard protocol layers: 1D Parity in asynchronous RS-232 serial links, 2D Parity in magnetic tape storage, Hamming Code in ECC RAM and RAID-2, Checksum in IPv4/TCP/UDP, and CRC in Ethernet IEEE 802.3 and Wi-Fi."
    p_cc2.font.name = FONT_BODY
    p_cc2.font.size = Pt(10.5)
    p_cc2.font.color.rgb = TEXT_MUTED
    p_cc2.space_before = Pt(4)

    # =========================================================================
    # SLIDE 12: IMPLEMENTATION & CONCLUSION
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Summary & Conclusion", "Implementation Highlights & Project Conclusion", "Fully functional multi-platform simulator ready for live classroom and lab demonstrations")

    tf_c12_l = add_card(s12, 0.8, 1.75, 5.7, 5.3, "1. Key Implementation Accomplishments", "Engineering architecture and deliverables:")
    p_c12_l1 = tf_c12_l.add_paragraph()
    p_c12_l1.text = "The Interactive Network Error Detection & Correction Simulator was developed using an enterprise-grade multi-platform architecture designed for accessibility, academic demonstrations, and research experimentation. The computational core is powered by Python 3.14, implementing custom algorithmic modules for Parity, 2D Matrix, Hamming Code, RFC 1071 Checksum, and CRC polynomial division without external dependencies. The user interface is provided in two complementary forms: a high-performance native desktop GUI developed using Python Tkinter, and a modern, responsive web application built with Vanilla HTML5, CSS3 glassmorphism design tokens, and modular asynchronous JavaScript."
    p_c12_l1.font.name = FONT_BODY
    p_c12_l1.font.size = Pt(11)
    p_c12_l1.font.color.rgb = TEXT_WHITE
    p_c12_l1.space_before = Pt(6)

    p_c12_l2 = tf_c12_l.add_paragraph()
    p_c12_l2.text = "Network Simulator 2 (NS-2) runs natively or via Windows Subsystem for Linux (WSL), bridged via real-time subprocess execution. The platform delivers an unprecedented level of interactive control: users can toggle bits at will, inject burst noise, configure NS-2 link parameters, and observe mathematical syndrome calculations updating instantaneously. The software architecture is cleanly separated into modular components, ensuring zero external dependencies for desktop execution and providing full REST API endpoints for web-based experimentation."
    p_c12_l2.font.name = FONT_BODY
    p_c12_l2.font.size = Pt(10.5)
    p_c12_l2.font.color.rgb = TEXT_MUTED
    p_c12_l2.space_before = Pt(6)

    tf_c12_r = add_card(s12, 6.8, 1.75, 5.7, 5.3, "2. Project Summary & Live Demonstration", "Developed and presented by:")
    p_team_lead = tf_c12_r.add_paragraph()
    p_team_lead.text = "AMAN KUMAR YADAV\nPRATIK BHARADBHUNJE\nDEVRISHI GADIA"
    p_team_lead.font.name = FONT_HEADING
    p_team_lead.font.size = Pt(16)
    p_team_lead.font.bold = True
    p_team_lead.font.color.rgb = TEXT_WHITE
    p_team_lead.space_before = Pt(4)

    p_proj = tf_c12_r.add_paragraph()
    p_proj.text = "Computer Networks Lab Project"
    p_proj.font.name = FONT_BODY
    p_proj.font.size = Pt(12)
    p_proj.font.color.rgb = CYAN_ACCENT
    p_proj.space_before = Pt(4)

    p_c12_r1 = tf_c12_r.add_paragraph()
    p_c12_r1.text = "In conclusion, this project provides a unified, interactive platform that seamlessly bridges abstract discrete mathematics with practical network engineering. By modeling every stage from bit encoding through noisy channel propagation to receiver syndrome decoding, it demystifies how modern communication networks maintain data integrity across flawed physical media."
    p_c12_r1.font.name = FONT_BODY
    p_c12_r1.font.size = Pt(10.5)
    p_c12_r1.font.color.rgb = TEXT_WHITE
    p_c12_r1.space_before = Pt(6)

    p_c12_r2 = tf_c12_r.add_paragraph()
    p_c12_r2.text = "The project is fully open-source, deployed live on Vercel at https://error-detection-simulator.vercel.app/, and maintained on GitHub at https://github.com/Amanyadav201205/errordetection. We invite questions, technical discussions, and live experimentation from the evaluation panel."
    p_c12_r2.font.name = FONT_BODY
    p_c12_r2.font.size = Pt(10.5)
    p_c12_r2.font.color.rgb = TEXT_MUTED
    p_c12_r2.space_before = Pt(6)

    # Save presentation
    output_path = os.path.join(r"D:\CNLFINAL", "Error_Detection_and_Correction_Presentation.pptx")
    prs.save(output_path)
    print(f"Presentation successfully created at: {output_path}")
    return output_path

if __name__ == "__main__":
    create_slide_deck()
