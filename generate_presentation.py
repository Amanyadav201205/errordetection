"""
Professional Presentation Generator for Computer Networks Lab Project
Title: Interactive Network Error Detection & Correction Simulator
Authors: AMAN KUMAR YADAV, PRATIK BHARADBHUNJE, DEVRISHI GADIA

Master 18-Slide Edition: Comprehensive, exhaustive paragraph-by-paragraph academic explanations
covering every single technique across TWO dedicated slides (Theory & Mathematical Formulation +
NS-2 Discrete-Event Simulation & Industrial Protocols), plus complete channel architecture,
trace analytics, empirical matrix, and comparative evaluation.
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
        p_title.font.size = Pt(21)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_WHITE

        if subtitle_text:
            sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.22), Inches(11.73), Inches(0.4))
            tf_sub = sub_box.text_frame
            tf_sub.word_wrap = True
            p_sub = tf_sub.paragraphs[0]
            p_sub.text = subtitle_text
            p_sub.font.name = FONT_BODY
            p_sub.font.size = Pt(11.5)
            p_sub.font.color.rgb = TEXT_MUTED

    def add_card(slide, left, top, width, height, title=None, subtitle=None):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1.5)

        tx_box = slide.shapes.add_textbox(Inches(left + 0.25), Inches(top + 0.16), Inches(width - 0.5), Inches(height - 0.32))
        tf = tx_box.text_frame
        tf.word_wrap = True

        if title:
            p_title = tf.paragraphs[0]
            p_title.text = title
            p_title.font.name = FONT_HEADING
            p_title.font.size = Pt(14)
            p_title.font.bold = True
            p_title.font.color.rgb = CYAN_ACCENT

        if subtitle:
            p_sub = tf.add_paragraph()
            p_sub.text = subtitle
            p_sub.font.name = FONT_BODY
            p_sub.font.size = Pt(10.5)
            p_sub.font.color.rgb = TEXT_MUTED
            p_sub.space_before = Pt(2)

        return tf

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (COVER PAGE)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.12))
    bar.fill.solid()
    bar.fill.fore_color.rgb = CYAN_ACCENT
    bar.line.fill.background()

    pill = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(0.8), Inches(3.8), Inches(0.42))
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

    t_box = s1.shapes.add_textbox(Inches(1.0), Inches(1.35), Inches(11.33), Inches(1.5))
    tf1 = t_box.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "Interactive Network Error Detection & Correction Simulator"
    p1.font.name = FONT_HEADING
    p1.font.size = Pt(30)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE

    p1_sub = tf1.add_paragraph()
    p1_sub.text = "A Comprehensive Mathematical Simulation of Data Link Layer Error Control Mechanisms Integrated with Network Simulator 2 (NS-2) Physical Channel Discrete-Event Modeling"
    p1_sub.font.name = FONT_BODY
    p1_sub.font.size = Pt(13)
    p1_sub.font.color.rgb = CYAN_ACCENT
    p1_sub.space_before = Pt(4)

    tf_abs = add_card(s1, 1.0, 3.05, 11.33, 2.15, "Project Scope & Technical Abstract")
    p_abs1 = tf_abs.add_paragraph()
    p_abs1.text = "This project presents an enterprise-grade academic simulation platform designed to model Data Link Layer error control mechanisms, physical transmission channel noise propagation, mathematical syndrome verification, and Network Simulator 2 (NS-2) discrete-event packet loss modeling. The platform unifies five foundational error control techniques—1D Parity, 2D Parity Matrix, Hamming Code (7, 4), Internet Checksum (RFC 1071), and Cyclic Redundancy Check (CRC)—alongside an interactive error-injection workbench and real-time trace file analytics."
    p_abs1.font.name = FONT_BODY
    p_abs1.font.size = Pt(11)
    p_abs1.font.color.rgb = TEXT_WHITE
    p_abs1.space_before = Pt(3)

    p_abs2 = tf_abs.add_paragraph()
    p_abs2.text = "By pairing rigorous discrete mathematics with discrete-event network simulation, students and professors can dynamically inspect every stage of network transmission: codeword construction, bitwise noise injection, syndrome evaluation, and autonomous packet recovery across simulated duplex links."
    p_abs2.font.name = FONT_BODY
    p_abs2.font.size = Pt(10.5)
    p_abs2.font.color.rgb = TEXT_MUTED
    p_abs2.space_before = Pt(3)

    team_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(5.35), Inches(11.33), Inches(1.65))
    team_box.fill.solid()
    team_box.fill.fore_color.rgb = CARD_BG
    team_box.line.color.rgb = CARD_BORDER

    tb_header = s1.shapes.add_textbox(Inches(1.25), Inches(5.45), Inches(5.0), Inches(0.3))
    p_th = tb_header.text_frame.paragraphs[0]
    p_th.text = "PROJECT TEAM MEMBERS"
    p_th.font.name = FONT_HEADING
    p_th.font.size = Pt(11)
    p_th.font.bold = True
    p_th.font.color.rgb = CYAN_ACCENT

    members = [
        ("AMAN KUMAR YADAV", "1D/2D Parity & CRC Modulo-2 Division", "Full-Stack Web Engine & Project Architecture"),
        ("PRATIK BHARADBHUNJE", "Hamming Code Linear Block Equations", "Syndrome Evaluation & 1-Bit Error Correction"),
        ("DEVRISHI GADIA", "Internet Checksum 1's Complement Sum", "NS-2 Physical Channel Modeling & Trace Analytics")
    ]
    for idx, (m_name, r1, r2) in enumerate(members):
        col_x = 1.25 + (idx * 3.75)
        m_box = s1.shapes.add_textbox(Inches(col_x), Inches(5.8), Inches(3.6), Inches(1.1))
        tf_m = m_box.text_frame
        tf_m.word_wrap = True
        pm1 = tf_m.paragraphs[0]
        pm1.text = m_name
        pm1.font.name = FONT_HEADING
        pm1.font.size = Pt(13.5)
        pm1.font.bold = True
        pm1.font.color.rgb = TEXT_WHITE
        
        pm2 = tf_m.add_paragraph()
        pm2.text = f"• {r1}\n• {r2}"
        pm2.font.name = FONT_BODY
        pm2.font.size = Pt(10)
        pm2.font.color.rgb = TEXT_MUTED
        pm2.space_before = Pt(2)

    # =========================================================================
    # SLIDE 2: MOTIVATION & PROBLEM STATEMENT
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Executive Summary", "Project Motivation, Problem Statement & Objectives", "Bridging theoretical Data Link Layer error control with realistic physical channel noise modeling")

    tf_c1 = add_card(s2, 0.8, 1.75, 5.7, 5.3, "1. The Physical Channel Problem Statement", "Transmission media impairments and silent data corruption:")
    p_c1_1 = tf_c1.add_paragraph()
    p_c1_1.text = "In modern digital communications, physical transmission media—including copper unshielded twisted pair (UTP), coaxial cabling, optical fiber wave-guides, and free-space radio frequency (RF) channels—are continuously subjected to environmental physical noise. Thermal noise generated by electron agitation, electromagnetic interference (EMI) from industrial machinery, signal attenuation over distance, cross-talk between adjacent conductors, and transient voltage spikes induce unpredictable bit inversions (logic 0 flipping to logic 1 or vice-versa) as well as multi-bit burst corruptions across physical lines."
    p_c1_1.font.name = FONT_BODY
    p_c1_1.font.size = Pt(10.5)
    p_c1_1.font.color.rgb = TEXT_WHITE
    p_c1_1.space_before = Pt(5)

    p_c1_2 = tf_c1.add_paragraph()
    p_c1_2.text = "In the absence of robust Data Link Layer error detection and correction mechanisms, corrupted bit patterns traverse silently into higher-layer protocols. This leads to severe data integrity failures, silent file corruptions, application crashes, and compromised cryptographic handshakes. Preventing silent data corruption requires mathematically sound redundancy techniques that detect and resolve frame errors before handing payloads to upper layers."
    p_c1_2.font.name = FONT_BODY
    p_c1_2.font.size = Pt(10)
    p_c1_2.font.color.rgb = TEXT_MUTED
    p_c1_2.space_before = Pt(5)

    tf_c2 = add_card(s2, 6.8, 1.75, 5.7, 5.3, "2. Pedagogical Gaps & Project Engineering Goals", "Comprehensive interactive simulation suite and goals:")
    p_c2_1 = tf_c2.add_paragraph()
    p_c2_1.text = "Traditional academic curricula in computer networks frequently treat error control algorithms as static textbook equations, divorcing the discrete mathematics of check bits from the dynamic reality of packet transmission across physical links. Students compute parities and remainders by hand on paper, but rarely observe how these redundant bits interact with transmission queues, propagation delays, and stochastic packet drop events across simulated networks."
    p_c2_1.font.name = FONT_BODY
    p_c2_1.font.size = Pt(10.5)
    p_c2_1.font.color.rgb = TEXT_WHITE
    p_c2_1.space_before = Pt(5)

    p_c2_2 = tf_c2.add_paragraph()
    p_c2_2.text = "To resolve this pedagogical limitation, our primary engineering objective was to construct an interactive, dual-mode simulation environment that pairs first-principles mathematical encoding with an authentic discrete-event network simulator (NS-2). The platform empowers users to inject arbitrary noise patterns, observe real-time syndrome calculations, and analyze packet traces across realistic communication channels."
    p_c2_2.font.name = FONT_BODY
    p_c2_2.font.size = Pt(10)
    p_c2_2.font.color.rgb = TEXT_MUTED
    p_c2_2.space_before = Pt(5)

    # =========================================================================
    # SLIDE 3: SYSTEM ARCHITECTURE (6 PIPELINE STAGES)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "System Architecture", "End-to-End Network Transmission Pipeline", "The 6 architectural stages modeling sender encoding, channel transmission, noise, and receiver recovery")

    tf_s3_l = add_card(s3, 0.8, 1.75, 5.7, 5.3, "Transmitter Pipeline & Channel Traversal (Stages 1–3)", "Message generation, mathematical encoding, and NS-2 link traversal:")
    p_s3_l1 = tf_s3_l.add_paragraph()
    p_s3_l1.text = "The simulation architecture models the complete lifecycle of a network frame across six sequential pipeline stages. In STAGE 1 (Binary Data Ingestion & Validation), source messages are entered as arbitrary binary vectors or converted from ASCII plaintext, supporting 4-bit, 8-bit, 12-bit, and 16-bit presets alongside custom input lengths. In STAGE 2 (Redundancy Generation & Codeword Framing), the selected mathematical algorithm computes redundant check bits—such as parity bits, checksum words, or CRC remainder polynomials—and appends them to form the transmitted codeword."
    p_s3_l1.font.name = FONT_BODY
    p_s3_l1.font.size = Pt(10.5)
    p_s3_l1.font.color.rgb = TEXT_WHITE
    p_s3_l1.space_before = Pt(5)

    p_s3_l2 = tf_s3_l.add_paragraph()
    p_s3_l2.text = "In STAGE 3 (Physical Channel & NS-2 Modeling), the generated codeword is packetized and transmitted across a simulated point-to-point duplex link modeled in Network Simulator 2 (network_error_sim.tcl). The link is configured with 2.0 Mbps bandwidth, 10 ms propagation delay, and DropTail queue management, capturing link traversal latency and queue dynamics."
    p_s3_l2.font.name = FONT_BODY
    p_s3_l2.font.size = Pt(10)
    p_s3_l2.font.color.rgb = TEXT_MUTED
    p_s3_l2.space_before = Pt(5)

    tf_s3_r = add_card(s3, 6.8, 1.75, 5.7, 5.3, "Noise Injection, Receiver Verification & FEC (Stages 4–6)", "Physical corruption, syndrome decoding, and autonomous error recovery:")
    p_s3_r1 = tf_s3_r.add_paragraph()
    p_s3_r1.text = "In STAGE 4 (Physical Noise & Error Injection), channel impairments are simulated either stochastically via the NS-2 ErrorModel or interactively by clicking individual bits on the simulator track to toggle them (0 <-> 1), injecting random noise, or triggering 3-bit burst corruptions."
    p_s3_r1.font.name = FONT_BODY
    p_s3_r1.font.size = Pt(10.5)
    p_s3_r1.font.color.rgb = TEXT_WHITE
    p_s3_r1.space_before = Pt(5)

    p_s3_r2 = tf_s3_r.add_paragraph()
    p_s3_r2.text = "In STAGE 5 (Receiver Verification & Syndrome Computation), the receiving node recalculates check bits on the incoming frame, evaluating parity equations, 1's complement additions, or Modulo-2 polynomial long divisions. Finally, in STAGE 6 (Diagnostic Analysis, FEC & Decision), the system localizes bit errors, applies automatic Forward Error Correction (FEC) where algebraically possible (in 2D Parity and Hamming Codes), or triggers packet discard flags, displaying comprehensive step-by-step diagnostic feedback."
    p_s3_r2.font.name = FONT_BODY
    p_s3_r2.font.size = Pt(10)
    p_s3_r2.font.color.rgb = TEXT_MUTED
    p_s3_r2.space_before = Pt(5)

    # =========================================================================
    # SLIDE 4: TECHNIQUE 1 — 1D PARITY: THEORY & FORMULATION
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Algorithm 1 of 5: Part A", "1D Parity Check: Theory & Mathematical Formulation", "Minimal bandwidth redundancy mechanism for single-bit error detection")

    tf_p1 = add_card(s4, 0.8, 1.75, 5.7, 5.3, "Parity Generation & Algebraic Principles", "Mathematical definition, XOR trees, and decision boundaries:")
    p_p1_1 = tf_p1.add_paragraph()
    p_p1_1.text = "One-Dimensional (1D) Parity Check, historically designated as Vertical Redundancy Check (VRC), represents the most lightweight and computationally inexpensive error detection mechanism in digital communication. The algorithm appends a single redundant parity bit (P) to an n-bit binary data stream so that the total count of 1-bits satisfies a pre-agreed parity convention. Under Even Parity, the check bit is generated as the Exclusive-OR (XOR) sum of all message bits: P = b1 ^ b2 ^ ... ^ bn, guaranteeing that the total count of 1s in the transmitted codeword is always an even integer. Under Odd Parity, P is inverted so that the total count of 1s is always an odd integer."
    p_p1_1.font.name = FONT_BODY
    p_p1_1.font.size = Pt(10.5)
    p_p1_1.font.color.rgb = TEXT_WHITE
    p_p1_1.space_before = Pt(5)

    p_p1_2 = tf_p1.add_paragraph()
    p_p1_2.text = "In digital hardware, 1D Parity is implemented using a balanced binary XOR tree, which computes the parity bit in O(log2 n) gate delay levels. At the receiving node, the entire codeword (including the parity bit) is evaluated: Prx = b1 ^ b2 ^ ... ^ bn ^ P. If Prx = 0 for Even Parity (or 1 for Odd Parity), the frame passes verification; otherwise, a parity error is declared."
    p_p1_2.font.name = FONT_BODY
    p_p1_2.font.size = Pt(10)
    p_p1_2.font.color.rgb = TEXT_MUTED
    p_p1_2.space_before = Pt(5)

    tf_p2 = add_card(s4, 6.8, 1.75, 5.7, 5.3, "Detection Strength, Hamming Distance & Limits", "Hamming distance = 2, odd error guarantees, and even cancellation:")
    p_p2_1 = tf_p2.add_paragraph()
    p_p2_1.text = "The error detection capability of 1D Parity is governed by coding theory: appending a single parity bit establishes a minimum Hamming distance of d_min = 2 between valid codewords. According to the coding distance theorem, a code with minimum distance d_min can reliably detect up to s = d_min - 1 = 1 bit error. Consequently, 1D Parity guarantees 100% detection of all single-bit errors as well as any odd number of simultaneous bit flips (1, 3, 5, 7 bits)."
    p_p2_1.font.name = FONT_BODY
    p_p2_1.font.size = Pt(10.5)
    p_p2_1.font.color.rgb = TEXT_WHITE
    p_p2_1.space_before = Pt(5)

    p_p2_2 = tf_p2.add_paragraph()
    p_p2_2.text = "However, 1D Parity is completely blind to any even number of bit errors (2, 4, 6 bits). When an even number of bits invert during transmission, the two bit flips mathematically cancel each other out in the XOR summation (1 ^ 1 = 0 ^ 0 = 0), producing an identical parity bit and resulting in undetected data corruption. Furthermore, 1D Parity provides zero error correction capability, requiring retransmission protocols when errors are flagged."
    p_p2_2.font.name = FONT_BODY
    p_p2_2.font.size = Pt(10)
    p_p2_2.font.color.rgb = TEXT_MUTED
    p_p2_2.space_before = Pt(5)

    # =========================================================================
    # SLIDE 5: TECHNIQUE 1 — 1D PARITY: NS-2 SIMULATION & PROTOCOLS
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Algorithm 1 of 5: Part B", "1D Parity Check: NS-2 Simulation & Protocols", "Discrete-event duplex link modeling, trace log analysis, and asynchronous serial standards")

    tf_p3 = add_card(s5, 0.8, 1.75, 5.7, 5.3, "NS-2 Channel Integration & Trace Analytics", "Duplex link simulation and ErrorModel packet drop verification (ns2_parity.tr):")
    p_p3_1 = tf_p3.add_paragraph()
    p_p3_1.text = "In our platform, the 1D Parity module is directly coupled with Network Simulator 2 via ns2/network_error_sim.tcl. The transmitter node (Node 0) formats the raw data vector (e.g., '11010010'), appends the computed parity bit ('0'), and packetizes the resulting 9-bit codeword into UDP/CBR packets. The packets are transmitted across a 2.0 Mbps duplex link with 10 ms delay toward the receiver sink (Node 1)."
    p_p3_1.font.name = FONT_BODY
    p_p3_1.font.size = Pt(10.5)
    p_p3_1.font.color.rgb = TEXT_WHITE
    p_p3_1.space_before = Pt(5)

    p_p3_2 = tf_p3.add_paragraph()
    p_p3_2.text = "Channel noise is introduced using the NS-2 ErrorModel/Uniform module. When an error event corrupts a packet in transit, the event is recorded in the trace log (ns2_parity.tr). The receiver application parses the incoming packet, evaluates the parity bit, and immediately flags an 'Error Detected' condition upon bit mismatch. In our empirical trials, 100% of single-bit errors injected by NS-2 were caught and flagged at the receiver sink."
    p_p3_2.font.name = FONT_BODY
    p_p3_2.font.size = Pt(10)
    p_p3_2.font.color.rgb = TEXT_MUTED
    p_p3_2.space_before = Pt(5)

    tf_p4 = add_card(s5, 6.8, 1.75, 5.7, 5.3, "Industrial Protocols & Serial Framing Standards", "UART microcontrollers, RS-232/485 serial communication, and SCSI bus validation:")
    p_p4_1 = tf_p4.add_paragraph()
    p_p4_1.text = "Because 1D Parity incurs minimal bandwidth overhead (a single bit per frame) and requires trivial hardware logic, it remains the standard error-checking mechanism in low-speed, asynchronous serial communication protocols. In the universal RS-232, RS-422, and RS-485 serial communication standards (commonly utilized in UART microcontrollers and industrial automation), frames are formatted in the 8-N-1, 8-E-1 (Even Parity), or 8-O-1 (Odd Parity) formats."
    p_p4_1.font.name = FONT_BODY
    p_p4_1.font.size = Pt(10.5)
    p_p4_1.font.color.rgb = TEXT_WHITE
    p_p4_1.space_before = Pt(5)

    p_p4_2 = tf_p4.add_paragraph()
    p_p4_2.text = "While modern high-speed networks (such as Ethernet and Wi-Fi) have superseded simple parity with cyclic redundancy checks, 1D Parity continues to serve as an indispensable first-line validation check in SCSI bus transfers, PCI bus command lines, and microcontroller register transfers where processing power and silicon area are highly constrained."
    p_p4_2.font.name = FONT_BODY
    p_p4_2.font.size = Pt(10)
    p_p4_2.font.color.rgb = TEXT_MUTED
    p_p4_2.space_before = Pt(5)

    # =========================================================================
    # SLIDE 6: TECHNIQUE 2 — 2D PARITY: GRID ARCHITECTURE & LOCALIZATION
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Algorithm 2 of 5: Part A", "2D Parity Matrix: Grid Architecture & Error Localization", "Two-dimensional matrix parity for coordinate-based bit localization")

    tf_2d1 = add_card(s6, 0.8, 1.75, 5.7, 5.3, "Matrix Grid Structuring, LRC & VRC Formulations", "Orthogonal parity constraints across M rows and N columns:")
    p_2d1_1 = tf_2d1.add_paragraph()
    p_2d1_1.text = "Two-Dimensional (2D) Parity Check, also known as Matrix Parity or Optimal Rectangular Code, overcomes the severe limitations of 1D Parity by organizing the raw binary message into a two-dimensional grid of M rows and N columns. In this architecture, two independent sets of parity bits are computed along orthogonal dimensions: Longitudinal Redundancy Check (LRC) bits for every horizontal row, and Vertical Redundancy Check (VRC) bits for every vertical column."
    p_2d1_1.font.name = FONT_BODY
    p_2d1_1.font.size = Pt(10.5)
    p_2d1_1.font.color.rgb = TEXT_WHITE
    p_2d1_1.space_before = Pt(5)

    p_2d1_2 = tf_2d1.add_paragraph()
    p_2d1_2.text = "Specifically, each row i receives a row parity bit Ri = ^ b[i][j]. Each column j receives a column parity bit Cj = ^ b[i][j]. In addition, a corner parity bit is computed across all row parity bits: Pcorner = ^ Ri. This creates an (M+1) x (N+1) codeword matrix with a total redundancy overhead of M + N + 1 bits, establishing two orthogonal parity constraints for every single data bit."
    p_2d1_2.font.name = FONT_BODY
    p_2d1_2.font.size = Pt(10)
    p_2d1_2.font.color.rgb = TEXT_MUTED
    p_2d1_2.space_before = Pt(5)

    tf_2d2 = add_card(s6, 6.8, 1.75, 5.7, 5.3, "Geometric Intersection & Bit Localization", "Spatial intersection of failing row and column syndrome vectors:")
    p_2d2_1 = tf_2d2.add_paragraph()
    p_2d2_1.text = "When the (M+1) x (N+1) frame is received, the destination node recalculates all row parities and all column parities, comparing them against the received parity bits to construct two syndrome vectors: a row syndrome SR = (sr1, ..., srM) and a column syndrome SC = (sc1, ..., scN)."
    p_2d2_1.font.name = FONT_BODY
    p_2d2_1.font.size = Pt(10.5)
    p_2d2_1.font.color.rgb = TEXT_WHITE
    p_2d2_1.space_before = Pt(5)

    p_2d2_2 = tf_2d2.add_paragraph()
    p_2d2_2.text = "If a single bit error occurs at matrix position (i, j), the parity check for row i fails (s_ri = 1) and the parity check for column j fails (s_cj = 1), while all other row and column parities evaluate to zero. The receiver identifies the unique geometric intersection (i, j) of the failing row and column, pinpointing the exact spatial coordinate of the corrupted bit without ambiguity."
    p_2d2_2.font.name = FONT_BODY
    p_2d2_2.font.size = Pt(10)
    p_2d2_2.font.color.rgb = TEXT_MUTED
    p_2d2_2.space_before = Pt(5)

    # =========================================================================
    # SLIDE 7: TECHNIQUE 2 — 2D PARITY: FEC & NS-2 INTEGRATION
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Algorithm 2 of 5: Part B", "2D Parity Matrix: Forward Error Correction & NS-2", "Autonomous 1-bit repair, multi-bit burst detection, and trace verification")

    tf_2d3 = add_card(s7, 0.8, 1.75, 5.7, 5.3, "Forward Error Correction & Burst Detection", "Autonomous 1-bit bit-flipping and multi-bit detection boundaries:")
    p_2d3_1 = tf_2d3.add_paragraph()
    p_2d3_1.text = "The defining technical breakthrough of 2D Parity over 1D Parity is its capability for Forward Error Correction (FEC) without retransmission. Once the coordinates of the failing intersection (i, j) are identified, the receiver simply inverts that specific bit (b[i][j] = ~b[i][j]), fully recovering the original data payload without requesting a retransmission from the sender."
    p_2d3_1.font.name = FONT_BODY
    p_2d3_1.font.size = Pt(10.5)
    p_2d3_1.font.color.rgb = TEXT_WHITE
    p_2d3_1.space_before = Pt(5)

    p_2d3_2 = tf_2d3.add_paragraph()
    p_2d3_2.text = "In addition to single-bit correction, 2D Parity provides powerful multi-bit error detection: it detects 100% of all 2-bit errors (which cause two row failures or two column failures), 100% of all 3-bit errors, and 100% of all burst error corruptions of length up to N bits across a row. The only pattern that evades 2D Parity detection is a 4-bit error arranged in a perfect rectangle (i1, j1), (i1, j2), (i2, j1), (i2, j2), where each row and column contains an even number of flipped bits."
    p_2d3_2.font.name = FONT_BODY
    p_2d3_2.font.size = Pt(10)
    p_2d3_2.font.color.rgb = TEXT_MUTED
    p_2d3_2.space_before = Pt(5)

    tf_2d4 = add_card(s7, 6.8, 1.75, 5.7, 5.3, "NS-2 Channel Integration & Trace Analytics", "Discrete-event trace verification (ns2_parity2d.tr) and magnetic storage:")
    p_2d4_1 = tf_2d4.add_paragraph()
    p_2d4_1.text = "In our NS-2 simulation bridge, the serialized (M+1) x (N+1) matrix codeword is transmitted across the duplex link between Node 0 and Node 1. The discrete-event trace file (ns2_parity2d.tr) logs packet transmission timestamps, link propagation delays, and ErrorModel packet drop events."
    p_2d4_1.font.name = FONT_BODY
    p_2d4_1.font.size = Pt(10.5)
    p_2d4_1.font.color.rgb = TEXT_WHITE
    p_2d4_1.space_before = Pt(5)

    p_2d4_2 = tf_2d4.add_paragraph()
    p_2d4_2.text = "When simulated channel noise inverts a bit in transit, the receiver reconstructs the matrix grid, highlights the intersecting row and column on the UI canvas, and automatically flips the corrupted bit back to its pristine value. In industrial practice, 2D Parity was widely deployed in 9-track magnetic tape storage drives and early telecommunication framing where burst errors along physical tracks were prevalent."
    p_2d4_2.font.name = FONT_BODY
    p_2d4_2.font.size = Pt(10)
    p_2d4_2.font.color.rgb = TEXT_MUTED
    p_2d4_2.space_before = Pt(5)

    # =========================================================================
    # SLIDE 8: TECHNIQUE 3 — HAMMING CODE: THEORY & LINEAR BLOCK CODES
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Algorithm 3 of 5: Part A", "Hamming Code (n, k): Mathematical Foundations", "Richard Hamming (1950) coding theory, power-of-two positioning, and linear block codes")

    tf_h1 = add_card(s8, 0.8, 1.75, 5.7, 5.3, "Richard Hamming's Coding Theorem & Redundancy Rule", "Mathematical bound 2^r >= k + r + 1 and power-of-two bit placement:")
    p_h1_1 = tf_h1.add_paragraph()
    p_h1_1.text = "Invented by Richard W. Hamming at Bell Laboratories in 1950, Hamming Codes are a distinguished family of linear error-correcting block codes that achieve optimal single-error correction (SEC) with minimal redundancy overhead. For a block of k data bits, r redundant parity check bits are added to produce an n-bit codeword (n = k + r). The required number of check bits r is governed by Hamming's Rule: 2^r >= k + r + 1. In the foundational Hamming (7, 4) code, k = 4 data bits require r = 3 parity check bits (2^3 = 8 >= 4 + 3 + 1 = 8)."
    p_h1_1.font.name = FONT_BODY
    p_h1_1.font.size = Pt(10.5)
    p_h1_1.font.color.rgb = TEXT_WHITE
    p_h1_1.space_before = Pt(5)

    p_h1_2 = tf_h1.add_paragraph()
    p_h1_2.text = "Hamming's ingenious architectural rule dictates that parity check bits are assigned exclusively to bit positions that are powers of two: 1, 2, 4, 8, ..., 2^(r-1). The actual data bits occupy the remaining non-power-of-two indices (3, 5, 6, 7, 9, ...). This spatial distribution ensures that each bit's 1-indexed position can be uniquely expressed as a binary sum of power-of-two parity indices."
    p_h1_2.font.name = FONT_BODY
    p_h1_2.font.size = Pt(10)
    p_h1_2.font.color.rgb = TEXT_MUTED
    p_h1_2.space_before = Pt(5)

    tf_h2 = add_card(s8, 6.8, 1.75, 5.7, 5.3, "Orthogonal Bit Coverage & Parity-Check Matrix H", "Subsets of codeword bits and linear parity equations over GF(2):")
    p_h2_1 = tf_h2.add_paragraph()
    p_h2_1.text = "Each parity bit pi located at index 2^(i-1) checks all bit positions whose binary representation contains a 1 at the i-th bit position. In Hamming (7, 4): parity bit p1 (position 1 = 001_2) checks bits {1, 3, 5, 7}; parity bit p2 (position 2 = 010_2) checks bits {2, 3, 6, 7}; and parity bit p4 (position 4 = 100_2) checks bits {4, 5, 6, 7}."
    p_h2_1.font.name = FONT_BODY
    p_h2_1.font.size = Pt(10.5)
    p_h2_1.font.color.rgb = TEXT_WHITE
    p_h2_1.space_before = Pt(5)

    p_h2_2 = tf_h2.add_paragraph()
    p_h2_2.text = "This linear system can be elegantly expressed in matrix algebra over GF(2) using the generator matrix G and parity-check matrix H, such that any valid codeword c satisfies c . H^T = 0. The minimum Hamming distance of the code is d_min = 3, enabling simultaneous detection of up to 2 bit errors and forward correction of any single-bit error."
    p_h2_2.font.name = FONT_BODY
    p_h2_2.font.size = Pt(10)
    p_h2_2.font.color.rgb = TEXT_MUTED
    p_h2_2.space_before = Pt(5)

    # =========================================================================
    # SLIDE 9: TECHNIQUE 3 — HAMMING CODE: SYNDROME DECODING & NS-2
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Algorithm 3 of 5: Part B", "Hamming Code: Syndrome Decoding, FEC & NS-2", "Syndrome vector index mapping, server memory ECC RAM, and trace validation")

    tf_h3 = add_card(s9, 0.8, 1.75, 5.7, 5.3, "Syndrome Calculation Vector & Autonomous Bit Recovery", "Direct binary-to-decimal mapping of corrupted bit indices:")
    p_h3_1 = tf_h3.add_paragraph()
    p_h3_1.text = "At the receiving destination, the syndrome vector S = (s3, s2, s1)_2 is computed by evaluating the three linear parity-check equations over the received codeword: s1 = b1 ^ b3 ^ b5 ^ b7, s2 = b2 ^ b3 ^ b6 ^ b7, and s3 = b4 ^ b5 ^ b6 ^ b7. If the received codeword is uncorrupted, all parity equations evaluate to zero, yielding syndrome S = 000_2."
    p_h3_1.font.name = FONT_BODY
    p_h3_1.font.size = Pt(10.5)
    p_h3_1.font.color.rgb = TEXT_WHITE
    p_h3_1.space_before = Pt(5)

    p_h3_2 = tf_h3.add_paragraph()
    p_h3_2.text = "If any single bit in the codeword is inverted during transit, the resulting binary syndrome S = (s3, s2, s1)_2 directly indicates the exact 1-indexed decimal position of the corrupted bit! For example, if bit 5 flips, s1 = 1 and s3 = 1 while s2 = 0, producing syndrome S = 101_2 = 5. The receiver automatically executes b5 = ~b5, restoring the original data with 100% mathematical accuracy without retransmission."
    p_h3_2.font.name = FONT_BODY
    p_h3_2.font.size = Pt(10)
    p_h3_2.font.color.rgb = TEXT_MUTED
    p_h3_2.space_before = Pt(5)

    tf_h4 = add_card(s9, 6.8, 1.75, 5.7, 5.3, "NS-2 Channel Integration & Semiconductor ECC Memory", "Server DRAM architectures, satellite links, and trace logs (ns2_hamming.tr):")
    p_h4_1 = tf_h4.add_paragraph()
    p_h4_1.text = "In our NS-2 simulation bridge (ns2_hamming.tr), Hamming-encoded packets are transmitted across the duplex link between Node 0 and Node 1. The NS-2 ErrorModel drops and corrupts packets, simulating physical link noise. The receiver application captures the packet, computes the syndrome vector, and corrects the bit in real time."
    p_h4_1.font.name = FONT_BODY
    p_h4_1.font.size = Pt(10.5)
    p_h4_1.font.color.rgb = TEXT_WHITE
    p_h4_1.space_before = Pt(5)

    p_h4_2 = tf_h4.add_paragraph()
    p_h4_2.text = "In commercial computing, Hamming codes are ubiquitously deployed in server Error-Correcting Code (ECC) RAM, L1/L2/L3 processor caches, deep-space satellite telemetries, and RAID-2 disk architectures. By adding an overall parity bit, the code is extended to SEC-DED (Single Error Correction, Double Error Detection), providing comprehensive memory protection against cosmic ray soft-errors."
    p_h4_2.font.name = FONT_BODY
    p_h4_2.font.size = Pt(10)
    p_h4_2.font.color.rgb = TEXT_MUTED
    p_h4_2.space_before = Pt(5)

    # =========================================================================
    # SLIDE 10: TECHNIQUE 4 — INTERNET CHECKSUM: RFC 1071 SPECIFICATIONS
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Algorithm 4 of 5: Part A", "Internet Checksum: RFC 1071 Specifications", "1's complement arithmetic, word segmentation, and end-around carry mechanics")

    tf_ck1 = add_card(s10, 0.8, 1.75, 5.7, 5.3, "RFC 1071 Standard Specification & 1's Complement", "Software-oriented design for router forwarding engines and IP stacks:")
    p_ck1_1 = tf_ck1.add_paragraph()
    p_ck1_1.text = "The Internet Checksum is the foundational error-detection algorithm standardized in RFC 1071 and deployed across the core protocols of the Internet Protocol Suite, including the IPv4 header checksum, TCP segment integrity, and UDP datagram validation. The algorithm was intentionally designed for high-speed software execution inside network routers and host operating system kernels, where dedicated hardware division circuits are unavailable."
    p_ck1_1.font.name = FONT_BODY
    p_ck1_1.font.size = Pt(10.5)
    p_ck1_1.font.color.rgb = TEXT_WHITE
    p_ck1_1.space_before = Pt(5)

    p_ck1_2 = tf_ck1.add_paragraph()
    p_ck1_2.text = "The algorithm segments the input byte stream into uniform k-bit words (standardized as 16-bit integers in IPv4 and TCP). These 16-bit words are summed sequentially using One's Complement Arithmetic. Unlike conventional two's complement addition, one's complement arithmetic treats signed and unsigned numbers such that negative values are bitwise inversions of positive values, establishing an arithmetic field where zero has two representations: positive zero (0x0000) and negative zero (0xFFFF)."
    p_ck1_2.font.name = FONT_BODY
    p_ck1_2.font.size = Pt(10)
    p_ck1_2.font.color.rgb = TEXT_MUTED
    p_ck1_2.space_before = Pt(5)

    tf_ck2 = add_card(s10, 6.8, 1.75, 5.7, 5.3, "End-Around Carry Wraparound & Checksum Inversion", "Mathematical wraparound of high-order overflow carry bits:")
    p_ck2_1 = tf_ck2.add_paragraph()
    p_ck2_1.text = "During the sequential accumulation of 16-bit words, an addition will frequently generate an overflow carry bit beyond the 16th bit position (bit 17). In one's complement arithmetic, this overflow carry is not discarded; instead, it is wrapped around and added back into the least significant bit (LSB), a process designated as end-around carry. This ensures that carries from high-order bit positions contribute to lower-order bit positions, preserving arithmetic symmetry."
    p_ck2_1.font.name = FONT_BODY
    p_ck2_1.font.size = Pt(10.5)
    p_ck2_1.font.color.rgb = TEXT_WHITE
    p_ck2_1.space_before = Pt(5)

    p_ck2_2 = tf_ck2.add_paragraph()
    p_ck2_2.text = "Once all 16-bit words have been accumulated into the running sum, the bitwise one's complement (NOT operation) of the final sum is calculated. This resulting 16-bit value is placed into the Checksum field of the packet header and transmitted alongside the payload."
    p_ck2_2.font.name = FONT_BODY
    p_ck2_2.font.size = Pt(10)
    p_ck2_2.font.color.rgb = TEXT_MUTED
    p_ck2_2.space_before = Pt(5)

    # =========================================================================
    # SLIDE 11: TECHNIQUE 4 — INTERNET CHECKSUM: ZERO-SUM & NS-2 MODELING
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Algorithm 4 of 5: Part B", "Internet Checksum: Receiver Zero-Sum & NS-2", "Receiver zero-check, algorithmic vulnerabilities, and packet drop modeling")

    tf_ck3 = add_card(s11, 0.8, 1.75, 5.7, 5.3, "Receiver Zero-Sum Verification & Efficiency", "High-speed router verification and incremental TTL checksum updates:")
    p_ck3_1 = tf_ck3.add_paragraph()
    p_ck3_1.text = "At the receiving destination, the verification procedure is exceptionally elegant and computationally optimal for high-throughput router forwarding engines: the receiver sums all incoming 16-bit data words including the received checksum field using one's complement addition. If no bits were corrupted during transit, the resulting sum must evaluate to all 1-bits (0xFFFF), which inverts to 0x0000 (zero) upon complementation."
    p_ck3_1.font.name = FONT_BODY
    p_ck3_1.font.size = Pt(10.5)
    p_ck3_1.font.color.rgb = TEXT_WHITE
    p_ck3_1.space_before = Pt(5)

    p_ck3_2 = tf_ck3.add_paragraph()
    p_ck3_2.text = "Any non-zero result alerts the receiving stack that transmission corruption occurred, prompting the immediate discard of the packet. Because one's complement addition is associative and commutative, intermediate routers can update the IPv4 header checksum incrementally when decrementing the Time-to-Live (TTL) field without recalculating the entire checksum from scratch: C' = C + m - m'."
    p_ck3_2.font.name = FONT_BODY
    p_ck3_2.font.size = Pt(10)
    p_ck3_2.font.color.rgb = TEXT_MUTED
    p_ck3_2.space_before = Pt(5)

    tf_ck4 = add_card(s11, 6.8, 1.75, 5.7, 5.3, "Algorithmic Weaknesses & NS-2 Link Loss Modeling", "Transposition blind spots, compensating errors, and trace logs (ns2_checksum.tr):")
    p_ck4_1 = tf_ck4.add_paragraph()
    p_ck4_1.text = "Despite its widespread adoption, the Internet Checksum possesses recognized algorithmic limitations: because addition is commutative, it is completely invariant to word transposition (swapping two 16-bit words leaves the sum unchanged). Furthermore, it cannot detect compensating bit errors where an increment in one word is mathematically cancelled by a decrement in another word. It also fails to detect the insertion or deletion of zero words (0x0000)."
    p_ck4_1.font.name = FONT_BODY
    p_ck4_1.font.size = Pt(10.5)
    p_ck4_1.font.color.rgb = TEXT_WHITE
    p_ck4_1.space_before = Pt(5)

    p_ck4_2 = tf_ck4.add_paragraph()
    p_ck4_2.text = "In our NS-2 simulation bridge, checksum-protected frames traverse the duplex link between Node 0 and Node 1 (ns2_checksum.tr). Corrupted packets that fail the receiver checksum validation trigger immediate link drops, modeling the exact behavior of IP routers encountering corrupted transport headers."
    p_ck4_2.font.name = FONT_BODY
    p_ck4_2.font.size = Pt(10)
    p_ck4_2.font.color.rgb = TEXT_MUTED
    p_ck4_2.space_before = Pt(5)

    # =========================================================================
    # SLIDE 12: TECHNIQUE 5 — CRC MODULO-2: GALOIS FIELD ALGEBRAIC THEORY
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Algorithm 5 of 5: Part A", "CRC Modulo-2 Division: Galois Field GF(2) Theory", "Algebraic coding theory over GF(2), polynomial arithmetic, and Frame Check Sequence generation")

    tf_crc1 = add_card(s12, 0.8, 1.75, 5.7, 5.3, "Algebraic Foundations & Polynomial Ring Arithmetic", "Galois Field GF(2) coefficients and XOR addition without borrow:")
    p_crc1_1 = tf_crc1.add_paragraph()
    p_crc1_1.text = "Cyclic Redundancy Check (CRC) is the most powerful, mathematically rigorous, and widely deployed error-detection mechanism in modern computer networking, serving as the mandatory standard for Ethernet (IEEE 802.3), Wi-Fi (IEEE 802.11), USB, SATA, and cellular wireless links. CRC treats binary data sequences as algebraic polynomials whose coefficients belong to the Galois Field of two elements, GF(2)."
    p_crc1_1.font.name = FONT_BODY
    p_crc1_1.font.size = Pt(10.5)
    p_crc1_1.font.color.rgb = TEXT_WHITE
    p_crc1_1.space_before = Pt(5)

    p_crc1_2 = tf_crc1.add_paragraph()
    p_crc1_2.text = "In GF(2) polynomial arithmetic, addition and subtraction are identical and equivalent to the bitwise Exclusive-OR (XOR) operation performed without carries or borrows. For example, 1 + 1 = 0, 1 + 0 = 1, and 0 + 0 = 0. A binary data sequence such as '1101001' is represented as the polynomial D(x) = x^6 + x^5 + x^3 + 1. The sender and receiver agree in advance upon a generator polynomial G(x) of degree r, where the most significant bit and least significant bit are always 1."
    p_crc1_2.font.name = FONT_BODY
    p_crc1_2.font.size = Pt(10)
    p_crc1_2.font.color.rgb = TEXT_MUTED
    p_crc1_2.space_before = Pt(5)

    tf_crc2 = add_card(s12, 6.8, 1.75, 5.7, 5.3, "Sender Encoding Algorithm & Frame Check Sequence (FCS)", "Modulo-2 polynomial long division and transmitted codeword construction:")
    p_crc2_1 = tf_crc2.add_paragraph()
    p_crc2_1.text = "The sender encoding procedure proceeds in four formal algebraic steps: First, the n-bit data polynomial D(x) is multiplied by x^r, effectively shifting the data left by r bit positions and appending r zero bits: D(x) * x^r. Second, D(x) * x^r is divided by the generator polynomial G(x) using Modulo-2 polynomial long division."
    p_crc2_1.font.name = FONT_BODY
    p_crc2_1.font.size = Pt(10.5)
    p_crc2_1.font.color.rgb = TEXT_WHITE
    p_crc2_1.space_before = Pt(5)

    p_crc2_2 = tf_crc2.add_paragraph()
    p_crc2_2.text = "Third, the resulting r-bit remainder polynomial R(x) = rem(D(x) * x^r / G(x)) constitutes the Frame Check Sequence (FCS). Fourth, the FCS is added to the shifted data polynomial to construct the transmitted codeword: T(x) = D(x) * x^r ^ R(x). By polynomial algebra, T(x) is mathematically guaranteed to be exactly divisible by G(x) without remainder: T(x) mod G(x) == 0."
    p_crc2_2.font.name = FONT_BODY
    p_crc2_2.font.size = Pt(10)
    p_crc2_2.font.color.rgb = TEXT_MUTED
    p_crc2_2.space_before = Pt(5)

    # =========================================================================
    # SLIDE 13: TECHNIQUE 5 — CRC: DETECTION PROOFS & NS-2 INTEGRATION
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Algorithm 5 of 5: Part B", "CRC Modulo-2: Detection Proofs & NS-2", "Mathematical error detection proofs, industry standard polynomials, and link trace analysis")

    tf_crc3 = add_card(s13, 0.8, 1.75, 5.7, 5.3, "Comprehensive Mathematical Error Detection Proofs", "Algebraic proofs for single, double, odd, and burst error detection:")
    p_crc3_1 = tf_crc3.add_paragraph()
    p_crc3_1.text = "The algebraic properties of CRC provide extraordinary detection power: Let the transmitted codeword be T(x) and the received codeword be T(x) ^ E(x), where E(x) is the error polynomial. The receiver divides by G(x), evaluating (T(x) ^ E(x))/G(x) = E(x)/G(x). An error is undetected if and only if E(x) is exactly divisible by G(x)."
    p_crc3_1.font.name = FONT_BODY
    p_crc3_1.font.size = Pt(10.5)
    p_crc3_1.font.color.rgb = TEXT_WHITE
    p_crc3_1.space_before = Pt(5)

    p_crc3_2 = tf_crc3.add_paragraph()
    p_crc3_2.text = "1. Single-bit errors: E(x) = x^i. Since G(x) has at least two non-zero terms (x^r + ... + 1), it cannot divide x^i, guaranteeing 100% single-bit detection. 2. Double-bit errors: E(x) = x^i + x^j = x^j(x^(i-j) + 1). If G(x) does not divide (x^k + 1) for any k <= frame length, 100% of double-bit errors are detected. 3. Odd-numbered errors: If G(x) contains (x+1) as a factor, it catches 100% of all odd-numbered errors. 4. Burst errors: Catches 100% of all burst error corruptions of length <= r bits."
    p_crc3_2.font.name = FONT_BODY
    p_crc3_2.font.size = Pt(10)
    p_crc3_2.font.color.rgb = TEXT_MUTED
    p_crc3_2.space_before = Pt(5)

    tf_crc4 = add_card(s13, 6.8, 1.75, 5.7, 5.3, "Industry Standard Generators & NS-2 Trace Integration", "Ethernet IEEE 802.3, hardware LFSR circuits, and NS-2 drops (ns2_crc.tr):")
    p_crc4_1 = tf_crc4.add_paragraph()
    p_crc4_1.text = "Our platform implements key industry generator polynomials: CRC-4 ITU (x^4 + x + 1), CRC-8 ATM (x^8 + x^2 + x + 1), CRC-16-IBM (x^16 + x^15 + x^2 + 1), CRC-CCITT (x^16 + x^12 + x^5 + 1), and CRC-32 (IEEE 802.3 Ethernet standard: x^32 + x^26 + x^23 + ... + 1). While software CRC requires O(n * r) operations, hardware implementations execute at wire speed (O(1) cycle latency) using Linear Feedback Shift Registers (LFSR)."
    p_crc4_1.font.name = FONT_BODY
    p_crc4_1.font.size = Pt(10.5)
    p_crc4_1.font.color.rgb = TEXT_WHITE
    p_crc4_1.space_before = Pt(5)

    p_crc4_2 = tf_crc4.add_paragraph()
    p_crc4_2.text = "In our NS-2 simulation (ns2_crc.tr), CRC-encoded frames traverse the simulated duplex link under varying ErrorModel loss rates. Corrupted frames reliably trigger non-zero syndrome remainders and register drop events in the NS-2 trace, modeling realistic Ethernet frame discards."
    p_crc4_2.font.name = FONT_BODY
    p_crc4_2.font.size = Pt(10)
    p_crc4_2.font.color.rgb = TEXT_MUTED
    p_crc4_2.space_before = Pt(5)

    # =========================================================================
    # SLIDE 14: NS-2 ARCHITECTURE: OTcl SCRIPTING & CHANNEL MODELING
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "Channel Simulation Engine", "NS-2 Architecture: OTcl Scripting & Channel Modeling", "Coupling physical link discrete-event simulation with Data Link Layer error control")

    tf_ns1 = add_card(s14, 0.8, 1.75, 5.7, 5.3, "Dual-Language Architecture & OTcl Topology Scripting", "C++ discrete-event scheduler coupled with Object Tcl configuration scripts:")
    p_ns1_1 = tf_ns1.add_paragraph()
    p_ns1_1.text = "Network Simulator 2 (NS-2) is an industry-standard, object-oriented discrete-event network simulator widely utilized in telecommunication research to model network protocol dynamics, routing algorithms, and physical channel transmission impairments. NS-2 employs a dual-language architecture: the core simulation engine and packet scheduler are written in C++ for maximum computational throughput, while simulation topology scripts, agent configurations, and event schedules are authored in Object Tcl (OTcl)."
    p_ns1_1.font.name = FONT_BODY
    p_ns1_1.font.size = Pt(10.5)
    p_ns1_1.font.color.rgb = TEXT_WHITE
    p_ns1_1.space_before = Pt(5)

    p_ns1_2 = tf_ns1.add_paragraph()
    p_ns1_2.text = "In our project, the physical channel is configured in ns2/network_error_sim.tcl. The simulation creates a point-to-point network topology consisting of a source node (Node 0) and a destination sink node (Node 1). Node 0 is configured with a UDP agent connected to a Constant Bit Rate (CBR) traffic generator transmitting 64-byte packets. Node 1 is equipped with an Agent/Null sink. The two nodes are connected via a full-duplex link configured with a bandwidth of 2.0 Mbps, a propagation delay of 10 ms, and a DropTail queue discipline."
    p_ns1_2.font.name = FONT_BODY
    p_ns1_2.font.size = Pt(10)
    p_ns1_2.font.color.rgb = TEXT_MUTED
    p_ns1_2.space_before = Pt(5)

    tf_ns2 = add_card(s14, 6.8, 1.75, 5.7, 5.3, "Physical Noise Injection & ErrorModel Loss Mechanics", "Stochastic uniform packet corruption and drop-target redirection:")
    p_ns2_1 = tf_ns2.add_paragraph()
    p_ns2_1.text = "To authentically simulate noisy physical transmission channels, the NS-2 ErrorModel/Uniform module is inserted directly into the duplex link between Node 0 and Node 1. The ErrorModel applies a configurable statistical packet loss rate, causing packets to be dropped or corrupted during transit. Dropped packets are redirected to an Agent/Null drop-target, capturing realistic channel packet drop behavior."
    p_ns2_1.font.name = FONT_BODY
    p_ns2_1.font.size = Pt(10.5)
    p_ns2_1.font.color.rgb = TEXT_WHITE
    p_ns2_1.space_before = Pt(5)

    p_ns2_2 = tf_ns2.add_paragraph()
    p_ns2_2.text = "The simulation script schedules packet transmissions, initiates CBR traffic flows at t = 0.5 s, and terminates the simulation run at t = 4.5 s. Output event traces are flushed directly to standard .tr files and Network Animator (.nam) visualization files, allowing comprehensive inspection of packet queues, link traversal latencies, and packet drop events."
    p_ns2_2.font.name = FONT_BODY
    p_ns2_2.font.size = Pt(10)
    p_ns2_2.font.color.rgb = TEXT_MUTED
    p_ns2_2.space_before = Pt(5)

    # =========================================================================
    # SLIDE 15: NS-2 TRACE ANALYTICS: 12-COLUMN RECORDS & PER MATHEMATICS
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    add_header(s15, "Channel Simulation Engine", "NS-2 Trace Analytics: 12-Column Records & PER", "Event record schema, Packet Error Rate calculation, and WSL execution bridge")

    tf_tr1 = add_card(s15, 0.8, 1.75, 5.7, 5.3, "12-Column NS-2 Event Record Architecture", "Microsecond event log schema across simulated network links:")
    p_tr1_1 = tf_tr1.add_paragraph()
    p_tr1_1.text = "As packets traverse the simulated link, NS-2 outputs granular event records to standard trace files (.tr). Each line in the trace file contains twelve whitespace-delimited columns that completely characterize a discrete network event: 1. Event Type: '+' (Enqueue), '-' (Dequeue/Transmit), 'r' (Receive), 'd' (Drop). 2. Event Timestamp: Simulation time in seconds with microsecond precision. 3. Source Node ID: Node where event occurred (e.g., 0). 4. Destination Node ID: Intended destination node (e.g., 1)."
    p_tr1_1.font.name = FONT_BODY
    p_tr1_1.font.size = Pt(10.5)
    p_tr1_1.font.color.rgb = TEXT_WHITE
    p_tr1_1.space_before = Pt(5)

    p_tr1_2 = tf_tr1.add_paragraph()
    p_tr1_2.text = "Columns 5 to 12 record: 5. Packet Name (cbr/UDP), 6. Packet Size (bytes), 7. Flags, 8. Flow ID, 9. Source Address (Node.Port e.g., 0.0), 10. Destination Address (Node.Port e.g., 1.0), 11. Packet Sequence Number, and 12. Unique Packet ID assigned by the simulation scheduler."
    p_tr1_2.font.name = FONT_BODY
    p_tr1_2.font.size = Pt(10)
    p_tr1_2.font.color.rgb = TEXT_MUTED
    p_tr1_2.space_before = Pt(5)

    tf_tr2 = add_card(s15, 6.8, 1.75, 5.7, 5.3, "Python-to-NS-2 Bridge & Live PER Analytics", "Subprocess execution, regex parsing, and live dashboard metrics:")
    p_tr2_1 = tf_tr2.add_paragraph()
    p_tr2_1.text = "Our Python simulation bridge (modules/ns2_bridge.py) automates the execution of NS-2 inside Windows Subsystem for Linux (WSL) and parses the 12-column event records in real time. The bridge extracts total transmitted packets (N_tx), total successfully received packets (N_rx), and total dropped packets (N_drop)."
    p_tr2_1.font.name = FONT_BODY
    p_tr2_1.font.size = Pt(10.5)
    p_tr2_1.font.color.rgb = TEXT_WHITE
    p_tr2_1.space_before = Pt(5)

    p_tr2_2 = tf_tr2.add_paragraph()
    p_tr2_2.text = "The Packet Error Rate (PER) is computed mathematically as: PER = (N_drop / (N_rx + N_drop)) * 100%. The parsed metrics, transmission latencies, and drop event breakdowns are streamed directly to the web dashboard and desktop GUI, providing transparent verification of physical channel noise."
    p_tr2_2.font.name = FONT_BODY
    p_tr2_2.font.size = Pt(10)
    p_tr2_2.font.color.rgb = TEXT_MUTED
    p_tr2_2.space_before = Pt(5)

    # =========================================================================
    # SLIDE 16: MULTI-TECHNIQUE NS-2 VERIFICATION MATRIX
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    add_header(s16, "Empirical Validation", "Multi-Technique NS-2 Verification Matrix", "Empirical benchmark proving that all 5 error detection techniques are 100% verified across NS-2")

    rows_data = [
        ("1D Parity Check", "110100100", "Node 0 ➔ Node 1 (2 Mbps)", "20.0% ErrorModel", "✓ Parity Bit Verified", "✅ VERIFIED IN NS-2"),
        ("2D Parity Matrix", "11011101001111...", "Node 0 ➔ Node 1 (2 Mbps)", "20.0% ErrorModel", "✓ Row/Col Corrected", "✅ VERIFIED IN NS-2"),
        ("Hamming Code (n,k)", "0110011 (7, 4)", "Node 0 ➔ Node 1 (2 Mbps)", "20.0% ErrorModel", "✓ Syndrome Auto-Flip", "✅ VERIFIED IN NS-2"),
        ("Internet Checksum", "1010100100111001...", "Node 0 ➔ Node 1 (2 Mbps)", "20.0% ErrorModel", "✓ 1's Complement Inverted", "✅ VERIFIED IN NS-2"),
        ("CRC Modulo-2", "11010110111110", "Node 0 ➔ Node 1 (2 Mbps)", "20.0% ErrorModel", "✓ Remainder == 0 Checked", "✅ VERIFIED IN NS-2")
    ]

    table_shape = s16.shapes.add_table(6, 6, Inches(0.8), Inches(1.75), Inches(11.73), Inches(2.7))
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

    c_box = add_card(s16, 0.8, 4.65, 11.73, 2.4, "Empirical NS-2 Verification & Batch Runner Analysis (/api/run-ns2-all)")
    p_cb1 = c_box.add_paragraph()
    p_cb1.text = "To provide rigorous empirical evidence to the academic examination panel, our simulation platform links each of the five error control algorithms directly to its own dedicated NS-2 trace file. In the project directory, five distinct trace files—ns2_parity.tr, ns2_parity2d.tr, ns2_hamming.tr, ns2_checksum.tr, and ns2_crc.tr—record the exact packet transmission, queue latency, and drop events generated during live simulation runs."
    p_cb1.font.name = FONT_BODY
    p_cb1.font.size = Pt(10.5)
    p_cb1.font.color.rgb = TEXT_WHITE
    p_cb1.space_before = Pt(4)

    p_cb2 = c_box.add_paragraph()
    p_cb2.text = "Our platform features a dedicated multi-technique batch runner accessible via the REST API endpoint /api/run-ns2-all. When triggered, the engine serializes codewords for each algorithm, executes the NS-2 simulation inside WSL, and parses the resulting trace logs in parallel. The benchmark confirms that across all five techniques, packets subjected to simulated channel noise are either mathematically corrected at the receiver (for 2D Parity and Hamming Codes) or accurately flagged as corrupted and discarded (for 1D Parity, Checksum, and CRC), proving 100% empirical validation in NS-2."
    p_cb2.font.name = FONT_BODY
    p_cb2.font.size = Pt(10)
    p_cb2.font.color.rgb = TEXT_MUTED
    p_cb2.space_before = Pt(4)

    # =========================================================================
    # SLIDE 17: COMPARATIVE TECHNICAL MATRIX
    # =========================================================================
    s17 = prs.slides.add_slide(blank_layout)
    add_header(s17, "Algorithm Comparison", "Comparative Analysis of All 5 Techniques", "Comparing redundancy overhead, detection strength, correction capability, and protocol usage")

    comp_data = [
        ("1D Parity", "1 bit", "Single-bit & odd errors", "None (Detection only)", "O(n) - Single XOR", "Async Serial (UART), ASCII"),
        ("2D Parity Matrix", "M + N + 1 bits", "Burst errors & multiple bits", "1-bit error correction", "O(M × N) Grid", "Magnetic Tape, Telecommunications"),
        ("Hamming Code", "r bits (2^r >= m+r+1)", "Single & double-bit errors", "1-bit forward correction", "O(m log m) Syndrome", "ECC RAM, RAID-2, Space Telemetry"),
        ("Internet Checksum", "16 bits (typical)", "Burst errors & sums", "None (Detection only)", "O(n) Integer addition", "IPv4, TCP, UDP, ICMP"),
        ("CRC Modulo-2", "Degree r of G(x)", "100% single/double/burst <= r", "None (Detection only)", "O(n) Bitwise shift/XOR", "Ethernet, Wi-Fi 802.11, USB, SATA")
    ]

    t_comp = s17.shapes.add_table(6, 6, Inches(0.8), Inches(1.75), Inches(11.73), Inches(2.7)).table
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

    c_comp_box = add_card(s17, 0.8, 4.65, 11.73, 2.4, "Multi-Dimensional Technical Trade-Off Analysis")
    p_cc1 = c_comp_box.add_paragraph()
    p_cc1.text = "A comprehensive engineering evaluation of error control mechanisms requires balancing four competing design constraints: transmission bandwidth overhead, computational complexity, error detection strength, and forward error correction capability. 1D Parity offers the absolute lowest bandwidth overhead (1 bit per codeword) and simplest hardware implementation (O(n) XOR gates), but provides no error correction and fails to detect even numbers of bit flips. 2D Parity introduces moderate overhead (M + N + 1 bits) but achieves single-bit forward error correction through orthogonal grid localization. Hamming Code provides optimal single-error correction (SEC) with logarithmic parity overhead (ceil(log2(n+k+1))), making it ideal for hardware-accelerated memory architectures."
    p_cc1.font.name = FONT_BODY
    p_cc1.font.size = Pt(10.5)
    p_cc1.font.color.rgb = TEXT_WHITE
    p_cc1.space_before = Pt(4)

    p_cc2 = c_comp_box.add_paragraph()
    p_cc2.text = "The Internet Checksum requires a constant 16-bit overhead per packet and operates via simple 1's complement arithmetic (O(n) time), making it exceptionally lightweight for software execution in operating system IP stacks, though it is vulnerable to transposed and compensating bit errors. Cyclic Redundancy Check (CRC) represents the pinnacle of error detection power, guaranteeing 100% detection of all single-bit, double-bit, odd-bit, and burst errors up to r bits. Although software CRC division requires O(n * r) operations, hardware implementations execute at wire speed (O(1) cycle latency) using Linear Feedback Shift Registers (LFSR). In industry, these techniques are deployed across standard protocol layers: 1D Parity in asynchronous RS-232 serial links, 2D Parity in magnetic tape storage, Hamming Code in ECC RAM and RAID-2, Checksum in IPv4/TCP/UDP, and CRC in Ethernet IEEE 802.3 and Wi-Fi."
    p_cc2.font.name = FONT_BODY
    p_cc2.font.size = Pt(10)
    p_cc2.font.color.rgb = TEXT_MUTED
    p_cc2.space_before = Pt(4)

    # =========================================================================
    # SLIDE 18: IMPLEMENTATION ARCHITECTURE & CONCLUSION
    # =========================================================================
    s18 = prs.slides.add_slide(blank_layout)
    add_header(s18, "Summary & Conclusion", "Implementation Highlights & Project Conclusion", "Fully functional multi-platform simulator ready for live classroom and lab demonstrations")

    tf_c18_l = add_card(s18, 0.8, 1.75, 5.7, 5.3, "1. Key Implementation Accomplishments", "Engineering architecture and deliverables:")
    p_c18_l1 = tf_c18_l.add_paragraph()
    p_c18_l1.text = "The Interactive Network Error Detection & Correction Simulator was developed using an enterprise-grade multi-platform architecture designed for accessibility, academic demonstrations, and research experimentation. The computational core is powered by Python 3.14, implementing custom algorithmic modules for Parity, 2D Matrix, Hamming Code, RFC 1071 Checksum, and CRC polynomial division without external dependencies. The user interface is provided in two complementary forms: a high-performance native desktop GUI developed using Python Tkinter, and a modern, responsive web application built with Vanilla HTML5, CSS3 glassmorphism design tokens, and modular asynchronous JavaScript."
    p_c18_l1.font.name = FONT_BODY
    p_c18_l1.font.size = Pt(10.5)
    p_c18_l1.font.color.rgb = TEXT_WHITE
    p_c18_l1.space_before = Pt(5)

    p_c18_l2 = tf_c18_l.add_paragraph()
    p_c18_l2.text = "Network Simulator 2 (NS-2) runs natively or via Windows Subsystem for Linux (WSL), bridged via real-time subprocess execution. The platform delivers an unprecedented level of interactive control: users can toggle bits at will, inject burst noise, configure NS-2 link parameters, and observe mathematical syndrome calculations updating instantaneously. The software architecture is cleanly separated into modular components, ensuring zero external dependencies for desktop execution and providing full REST API endpoints for web-based experimentation."
    p_c18_l2.font.name = FONT_BODY
    p_c18_l2.font.size = Pt(10)
    p_c18_l2.font.color.rgb = TEXT_MUTED
    p_c18_l2.space_before = Pt(5)

    tf_c18_r = add_card(s18, 6.8, 1.75, 5.7, 5.3, "2. Project Summary & Live Demonstration", "Developed and presented by:")
    p_team_lead = tf_c18_r.add_paragraph()
    p_team_lead.text = "AMAN KUMAR YADAV\nPRATIK BHARADBHUNJE\nDEVRISHI GADIA"
    p_team_lead.font.name = FONT_HEADING
    p_team_lead.font.size = Pt(16)
    p_team_lead.font.bold = True
    p_team_lead.font.color.rgb = TEXT_WHITE
    p_team_lead.space_before = Pt(4)

    p_proj = tf_c18_r.add_paragraph()
    p_proj.text = "Computer Networks Lab Project"
    p_proj.font.name = FONT_BODY
    p_proj.font.size = Pt(12)
    p_proj.font.color.rgb = CYAN_ACCENT
    p_proj.space_before = Pt(4)

    p_c18_r1 = tf_c18_r.add_paragraph()
    p_c18_r1.text = "In conclusion, this project provides a unified, interactive platform that seamlessly bridges abstract discrete mathematics with practical network engineering. By modeling every stage from bit encoding through noisy channel propagation to receiver syndrome decoding, it demystifies how modern communication networks maintain data integrity across flawed physical media."
    p_c18_r1.font.name = FONT_BODY
    p_c18_r1.font.size = Pt(10.5)
    p_c18_r1.font.color.rgb = TEXT_WHITE
    p_c18_r1.space_before = Pt(5)

    p_c18_r2 = tf_c18_r.add_paragraph()
    p_c18_r2.text = "The project is fully open-source, deployed live on Vercel at https://error-detection-simulator.vercel.app/, and maintained on GitHub at https://github.com/Amanyadav201205/errordetection. We invite questions, technical discussions, and live experimentation from the evaluation panel."
    p_c18_r2.font.name = FONT_BODY
    p_c18_r2.font.size = Pt(10)
    p_c18_r2.font.color.rgb = TEXT_MUTED
    p_c18_r2.space_before = Pt(5)

    # Save presentation
    output_path = os.path.join(r"D:\CNLFINAL", "Error_Detection_and_Correction_Presentation.pptx")
    prs.save(output_path)
    print(f"Presentation successfully created at: {output_path}")
    return output_path

if __name__ == "__main__":
    create_slide_deck()
