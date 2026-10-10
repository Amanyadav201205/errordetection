"""
Interactive Network Error Detection and Correction Simulator
=============================================================
Computer Networks Lab Project
Team Members:
  - AMAN KUMAR YADAV
  - PRATIK BHARADBHUNJE
  - DEVRISHI GADIA

Features:
  1. Input Data Module (Binary validation, presets, ASCII text conversion)
  2. 1D Parity Check (Even / Odd)
  3. 2D Parity Check (Matrix Grid with Row & Column Parity, Single-bit Error Pinpointing)
  4. Hamming Code (Power-of-2 Parity, Syndrome Calculation, Single-bit Correction)
  5. Internet Checksum (1's complement block addition with wraparound carry)
  6. CRC - Cyclic Redundancy Check (XOR polynomial division with full trace)
  7. Channel & Error Injection Module (Clickable bit-flipping, burst errors, random errors)
  8. Receiver Verification & Correction Module (Detailed diagnosis & status)
  9. NS-2 Channel Simulator Integration (Executes real NS-2 via WSL, ErrorModel, Trace analysis)
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from typing import Dict, Any, List

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.parity import encode_parity, verify_parity
from modules.parity2d import encode_2d_parity, verify_2d_parity
from modules.hamming import encode_hamming, verify_and_correct_hamming
from modules.checksum import encode_checksum, verify_checksum
from modules.crc import encode_crc, verify_crc, PRESET_POLYNOMIALS
from modules.error_injection import (
    inject_error_at_indices,
    inject_single_random_error,
    inject_burst_error
)
from modules.ns2_bridge import is_ns2_available, run_ns2_simulation

# Color Theme Palette
THEME = {
    "bg": "#0f172a",          # Slate 900
    "panel": "#1e293b",       # Slate 800
    "card": "#334155",        # Slate 700
    "accent": "#0ea5e9",      # Sky 500
    "accent_hover": "#38bdf8",# Sky 400
    "text": "#f8fafc",        # Slate 50
    "text_muted": "#94a3b8",  # Slate 400
    "border": "#475569",      # Slate 600
    "success": "#10b981",     # Emerald 500
    "error": "#ef4444",       # Red 500
    "warning": "#f59e0b",     # Amber 500
    "info": "#6366f1",        # Indigo 500
    "bit_0": "#1e293b",
    "bit_1": "#0369a1",
    "bit_flipped": "#dc2626"
}

class NetworkSimulatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Interactive Network Error Detection & Correction Simulator")
        self.geometry("1280x880")
        self.minsize(1100, 750)
        self.configure(bg=THEME["bg"])
        
        # State variables
        self.current_encoded_frame = ""
        self.current_transmitted_frame = ""
        self.current_encoding_result: Dict[str, Any] = {}
        self.current_verification_result: Dict[str, Any] = {}
        self.bit_buttons: List[tk.Button] = []
        self.flipped_indices = set()
        
        # Check NS-2 availability
        self.ns2_status = is_ns2_available()
        
        self.init_styles()
        self.build_ui()
        self.load_preset("8bit")

    def init_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        
        # Notebook / Tabs
        style.configure("TNotebook", background=THEME["bg"], borderwidth=0)
        style.configure("TNotebook.Tab", background=THEME["panel"], foreground=THEME["text"],
                        padding=[14, 6], font=("Segoe UI", 10, "bold"), borderwidth=0)
        style.map("TNotebook.Tab",
                  background=[("selected", THEME["accent"]), ("active", THEME["card"])],
                  foreground=[("selected", "#ffffff")])
        
        # Scrollbars
        style.configure("Vertical.TScrollbar", background=THEME["card"], troughcolor=THEME["panel"],
                        borderwidth=0, arrowcolor=THEME["text"])

    def build_ui(self):
        # 1. Header Banner
        header = tk.Frame(self, bg=THEME["panel"], padx=16, pady=10, relief="flat", bd=1)
        header.pack(fill="x", side="top")
        
        title_box = tk.Frame(header, bg=THEME["panel"])
        title_box.pack(side="left", fill="both")
        
        lbl_title = tk.Label(
            title_box,
            text="Interactive Network Error Detection & Correction Simulator",
            font=("Segoe UI", 15, "bold"),
            bg=THEME["panel"],
            fg="#38bdf8"
        )
        lbl_title.pack(anchor="w")
        
        lbl_sub = tk.Label(
            title_box,
            text="Data Link Layer & Physical Channel Transmission Modeling",
            font=("Segoe UI", 9),
            bg=THEME["panel"],
            fg=THEME["text_muted"]
        )
        lbl_sub.pack(anchor="w")
        
        # NS-2 engine indicator badge
        ns_badge_text = "NS-2 Engine: Connected (WSL)" if self.ns2_status["available"] else "NS-2 Engine: Standby"
        ns_badge_color = THEME["success"] if self.ns2_status["available"] else THEME["warning"]
        lbl_ns2 = tk.Label(
            header,
            text=f"● {ns_badge_text}",
            font=("Segoe UI", 9, "bold"),
            bg=THEME["card"],
            fg=ns_badge_color,
            padx=10,
            pady=4
        )
        lbl_ns2.pack(side="right", padx=5)

        # 2. Persistent Bottom Footer with Team Names
        footer = tk.Frame(self, bg=THEME["panel"], padx=16, pady=7, relief="solid", bd=1)
        footer.pack(fill="x", side="bottom")
        
        lbl_foot_tag = tk.Label(
            footer,
            text="● PROJECT TEAM:",
            font=("Segoe UI", 8, "bold"),
            bg=THEME["panel"],
            fg="#38bdf8"
        )
        lbl_foot_tag.pack(side="left", padx=(0, 10))
        
        team_str = "AMAN KUMAR YADAV    |    PRATIK BHARADBHUNJE    |    DEVRISHI GADIA"
        lbl_foot_team = tk.Label(
            footer,
            text=team_str,
            font=("Segoe UI", 8, "bold"),
            bg=THEME["panel"],
            fg=THEME["text"]
        )
        lbl_foot_team.pack(side="left")

        # 3. Main Container with Left Controls and Right Visualization Notebook
        paned = tk.PanedWindow(self, orient="horizontal", bg=THEME["bg"], sashrelief="flat", sashwidth=4)
        paned.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left Panel (Step 1: Input & Technique, Step 2: Transmission & Error Injection)
        left_container = tk.Frame(paned, bg=THEME["bg"], width=460)
        paned.add(left_container, minsize=420)
        
        # Right Panel (Tabs: Step 3 Verification & Visualization, Algorithm Trace, NS-2 Channel Simulation)
        right_container = tk.Frame(paned, bg=THEME["bg"])
        paned.add(right_container, minsize=550)
        
        self.build_left_panel(left_container)
        self.build_right_panel(right_container)

    # -------------------------------------------------------------
    # LEFT PANEL: Controls, Input, Technique Selection, Error Injection
    # -------------------------------------------------------------
    def build_left_panel(self, parent):
        canvas = tk.Canvas(parent, bg=THEME["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview, style="Vertical.TScrollbar")
        scrollable_frame = tk.Frame(canvas, bg=THEME["bg"])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=440)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Card 1: Module 1 - Input Data Module
        card_input = tk.LabelFrame(
            scrollable_frame,
            text=" 1. Input Data Module (Transmitter Source) ",
            font=("Segoe UI", 10, "bold"),
            bg=THEME["panel"],
            fg=THEME["accent"],
            padx=12,
            pady=10,
            relief="solid",
            bd=1
        )
        card_input.pack(fill="x", pady=(0, 10))
        
        tk.Label(card_input, text="Binary Message Data (0s and 1s):", font=("Segoe UI", 9),
                 bg=THEME["panel"], fg=THEME["text"]).pack(anchor="w")
        
        self.ent_data = tk.Entry(
            card_input,
            font=("Consolas", 12, "bold"),
            bg=THEME["card"],
            fg=THEME["text"],
            insertbackground="#ffffff",
            relief="flat",
            bd=4
        )
        self.ent_data.pack(fill="x", pady=6)
        self.ent_data.bind("<KeyRelease>", lambda e: self.validate_binary_input())
        
        # Quick presets
        preset_frame = tk.Frame(card_input, bg=THEME["panel"])
        preset_frame.pack(fill="x", pady=2)
        
        tk.Label(preset_frame, text="Presets:", font=("Segoe UI", 8), bg=THEME["panel"], fg=THEME["text_muted"]).pack(side="left")
        self.preset_btns = {}
        for label, val in [("8-bit", "11010010"), ("4-bit", "1011"), ("12-bit", "101100101101"), ("16-bit", "1010110001011101")]:
            btn = tk.Button(
                preset_frame,
                text=label,
                font=("Segoe UI", 8),
                bg=THEME["accent"] if val == "11010010" else THEME["card"],
                fg="#ffffff" if val == "11010010" else THEME["text"],
                relief="flat",
                activebackground=THEME["accent"],
                command=lambda v=val: self.set_input_data(v)
            )
            btn.pack(side="left", padx=3)
            self.preset_btns[val] = btn
            
        # ASCII text conversion helper
        ascii_box = tk.Frame(card_input, bg=THEME["panel"])
        ascii_box.pack(fill="x", pady=6)
        tk.Label(ascii_box, text="Text to Binary:", font=("Segoe UI", 8), bg=THEME["panel"], fg=THEME["text_muted"]).pack(side="left")
        self.ent_ascii = tk.Entry(ascii_box, font=("Segoe UI", 8), width=8, bg=THEME["card"], fg=THEME["text"], relief="flat")
        self.ent_ascii.pack(side="left", padx=4)
        btn_conv = tk.Button(
            ascii_box,
            text="Convert",
            font=("Segoe UI", 8),
            bg=THEME["card"],
            fg=THEME["accent_hover"],
            relief="flat",
            command=self.convert_ascii_to_binary
        )
        btn_conv.pack(side="left")

        # Card 2: Select Technique
        card_tech = tk.LabelFrame(
            scrollable_frame,
            text=" 2. Error Detection & Correction Technique ",
            font=("Segoe UI", 10, "bold"),
            bg=THEME["panel"],
            fg=THEME["accent"],
            padx=12,
            pady=10,
            relief="solid",
            bd=1
        )
        card_tech.pack(fill="x", pady=(0, 10))
        
        self.tech_var = tk.StringVar(value="parity")
        techniques = [
            ("1D Parity Check (Even / Odd)", "parity"),
            ("2D Parity Check (Matrix Grid)", "parity2d"),
            ("Hamming Code (Error Detection & Correction)", "hamming"),
            ("Internet Checksum (1's Complement Sum)", "checksum"),
            ("Cyclic Redundancy Check (CRC)", "crc")
        ]
        
        for text, val in techniques:
            rb = tk.Radiobutton(
                card_tech,
                text=text,
                variable=self.tech_var,
                value=val,
                font=("Segoe UI", 9),
                bg=THEME["panel"],
                fg=THEME["text"],
                selectcolor=THEME["panel"],
                activebackground=THEME["panel"],
                command=self.on_technique_changed
            )
            rb.pack(anchor="w", pady=2)
            
        # Dynamic Technique Parameters Sub-frame
        self.param_frame = tk.Frame(card_tech, bg=THEME["card"], padx=8, pady=8)
        self.param_frame.pack(fill="x", pady=6)
        self.update_param_controls()

        # Action Button: Encode / Redundancy Generation
        self.btn_encode = tk.Button(
            scrollable_frame,
            text="⚡ Step 1 & 2: Encode & Generate Redundancy",
            font=("Segoe UI", 10, "bold"),
            bg=THEME["accent"],
            fg="#ffffff",
            activebackground=THEME["accent_hover"],
            relief="flat",
            pady=8,
            command=self.handle_encode
        )
        self.btn_encode.pack(fill="x", pady=(0, 10))

        # Card 3: Module 7 - Channel & Error Injection Module
        card_channel = tk.LabelFrame(
            scrollable_frame,
            text=" 3. Transmitter & Channel Error Injection ",
            font=("Segoe UI", 10, "bold"),
            bg=THEME["panel"],
            fg=THEME["accent"],
            padx=12,
            pady=10,
            relief="solid",
            bd=1
        )
        card_channel.pack(fill="x", pady=(0, 10))
        
        tk.Label(
            card_channel,
            text="Transmitted Bits (Click any bit to flip/inject error):",
            font=("Segoe UI", 9),
            bg=THEME["panel"],
            fg=THEME["text"]
        ).pack(anchor="w", pady=(0, 4))
        
        # Frame of clickable bit boxes
        self.bits_container = tk.Frame(card_channel, bg=THEME["card"], padx=6, pady=8)
        self.bits_container.pack(fill="x", pady=4)
        
        # Error injection shortcut buttons
        err_actions = tk.Frame(card_channel, bg=THEME["panel"])
        err_actions.pack(fill="x", pady=6)
        
        btn_flip_rand = tk.Button(
            err_actions,
            text="🎲 Flip 1 Random Bit",
            font=("Segoe UI", 8, "bold"),
            bg=THEME["card"],
            fg=THEME["warning"],
            relief="flat",
            command=self.inject_random_error
        )
        btn_flip_rand.pack(side="left", padx=2, expand=True, fill="x")
        
        btn_burst = tk.Button(
            err_actions,
            text="⚡ Inject Burst (2-3 bits)",
            font=("Segoe UI", 8, "bold"),
            bg=THEME["card"],
            fg=THEME["error"],
            relief="flat",
            command=self.inject_burst_error_action
        )
        btn_burst.pack(side="left", padx=2, expand=True, fill="x")
        
        btn_clean = tk.Button(
            err_actions,
            text="✓ Clean (No Error)",
            font=("Segoe UI", 8, "bold"),
            bg=THEME["card"],
            fg=THEME["success"],
            relief="flat",
            command=self.clear_channel_errors
        )
        btn_clean.pack(side="left", padx=2, expand=True, fill="x")
        
        # Channel Simulation Mode: Direct vs NS-2
        chan_mode_frame = tk.Frame(card_channel, bg=THEME["panel"])
        chan_mode_frame.pack(fill="x", pady=6)
        
        self.channel_sim_var = tk.StringVar(value="direct")
        tk.Label(chan_mode_frame, text="Channel Simulation Engine:", font=("Segoe UI", 8, "bold"),
                 bg=THEME["panel"], fg=THEME["text_muted"]).pack(anchor="w")
                 
        rb_direct = tk.Radiobutton(
            chan_mode_frame,
            text="Direct Software Channel",
            variable=self.channel_sim_var,
            value="direct",
            font=("Segoe UI", 8),
            bg=THEME["panel"],
            fg=THEME["text"],
            selectcolor=THEME["panel"]
        )
        rb_direct.pack(side="left", padx=4)
        
        rb_ns2 = tk.Radiobutton(
            chan_mode_frame,
            text="NS-2 Discrete Event Simulator",
            variable=self.channel_sim_var,
            value="ns2",
            font=("Segoe UI", 8, "bold"),
            bg=THEME["panel"],
            fg=THEME["accent_hover"],
            selectcolor=THEME["panel"]
        )
        rb_ns2.pack(side="left", padx=4)

        # Action Button: Receiver Verification & Result Display
        self.btn_verify = tk.Button(
            scrollable_frame,
            text="🔍 Step 4: Transmit & Verify at Receiver",
            font=("Segoe UI", 10, "bold"),
            bg=THEME["success"],
            fg="#ffffff",
            activebackground="#059669",
            relief="flat",
            pady=8,
            command=self.handle_verify
        )
        self.btn_verify.pack(fill="x", pady=(0, 15))

    def set_input_data(self, val: str):
        self.ent_data.delete(0, tk.END)
        self.ent_data.insert(0, val)
        for v, b in getattr(self, "preset_btns", {}).items():
            if v == val:
                b.config(bg=THEME["accent"], fg="#ffffff")
            else:
                b.config(bg=THEME["card"], fg=THEME["text"])
        self.validate_binary_input()
        self.handle_encode()

    def convert_ascii_to_binary(self):
        txt = self.ent_ascii.get().strip()
        if not txt:
            return
        binary = "".join(format(ord(c), '08b') for c in txt)
        self.set_input_data(binary)

    def validate_binary_input(self):
        val = self.ent_data.get()
        cleaned = "".join(c for c in val if c in "01")
        if cleaned != val:
            self.ent_data.delete(0, tk.END)
            self.ent_data.insert(0, cleaned)

    def update_param_controls(self):
        # Clear param frame
        for widget in self.param_frame.winfo_children():
            widget.destroy()
            
        tech = self.tech_var.get()
        if tech == "parity":
            tk.Label(self.param_frame, text="Parity Mode:", font=("Segoe UI", 9),
                     bg=THEME["card"], fg=THEME["text"]).pack(side="left", padx=4)
            self.parity_type_var = tk.StringVar(value="even")
            for t in ["Even Parity", "Odd Parity"]:
                tk.Radiobutton(
                    self.param_frame,
                    text=t,
                    variable=self.parity_type_var,
                    value=t.split()[0].lower(),
                    font=("Segoe UI", 9),
                    bg=THEME["card"],
                    fg=THEME["text"],
                    selectcolor=THEME["card"],
                    command=self.handle_encode
                ).pack(side="left", padx=4)
                
        elif tech == "parity2d":
            tk.Label(self.param_frame, text="Grid Size:", font=("Segoe UI", 9),
                     bg=THEME["card"], fg=THEME["text"]).pack(side="left", padx=2)
            self.p2d_rows_var = tk.IntVar(value=3)
            self.p2d_cols_var = tk.IntVar(value=4)
            
            tk.Label(self.param_frame, text="Rows:", font=("Segoe UI", 8), bg=THEME["card"], fg=THEME["text_muted"]).pack(side="left")
            sp_r = tk.Spinbox(self.param_frame, from_=2, to=8, width=3, textvariable=self.p2d_rows_var, command=self.handle_encode)
            sp_r.pack(side="left", padx=2)
            
            tk.Label(self.param_frame, text="Cols:", font=("Segoe UI", 8), bg=THEME["card"], fg=THEME["text_muted"]).pack(side="left")
            sp_c = tk.Spinbox(self.param_frame, from_=2, to=8, width=3, textvariable=self.p2d_cols_var, command=self.handle_encode)
            sp_c.pack(side="left", padx=2)
            
            self.p2d_type_var = tk.StringVar(value="even")
            tk.Radiobutton(self.param_frame, text="Even", variable=self.p2d_type_var, value="even", bg=THEME["card"], fg=THEME["text"], selectcolor=THEME["card"], command=self.handle_encode).pack(side="left", padx=4)
            tk.Radiobutton(self.param_frame, text="Odd", variable=self.p2d_type_var, value="odd", bg=THEME["card"], fg=THEME["text"], selectcolor=THEME["card"], command=self.handle_encode).pack(side="left", padx=2)
            
        elif tech == "hamming":
            tk.Label(self.param_frame, text="Standard: Hamming Code (n, k) with powers-of-2 parity",
                     font=("Segoe UI", 8), bg=THEME["card"], fg=THEME["text_muted"]).pack(anchor="w")
            tk.Label(self.param_frame, text="Automatically computes required parity bits (r) & detects/corrects single-bit error.",
                     font=("Segoe UI", 8, "italic"), bg=THEME["card"], fg=THEME["accent_hover"]).pack(anchor="w")
            
        elif tech == "checksum":
            tk.Label(self.param_frame, text="Block Size:", font=("Segoe UI", 9),
                     bg=THEME["card"], fg=THEME["text"]).pack(side="left", padx=4)
            self.chk_block_var = tk.IntVar(value=8)
            for sz in [4, 8, 16]:
                tk.Radiobutton(
                    self.param_frame,
                    text=f"{sz}-bit",
                    variable=self.chk_block_var,
                    value=sz,
                    font=("Segoe UI", 9),
                    bg=THEME["card"],
                    fg=THEME["text"],
                    selectcolor=THEME["card"],
                    command=self.handle_encode
                ).pack(side="left", padx=4)
                
        elif tech == "crc":
            tk.Label(self.param_frame, text="Generator Polynomial:", font=("Segoe UI", 8),
                     bg=THEME["card"], fg=THEME["text"]).pack(anchor="w")
            self.crc_gen_choice = tk.StringVar(value="CRC-4 (ITU)")
            combo = ttk.Combobox(
                self.param_frame,
                textvariable=self.crc_gen_choice,
                values=list(PRESET_POLYNOMIALS.keys()) + ["Custom"],
                state="readonly",
                width=22
            )
            combo.pack(side="left", padx=2, pady=2)
            combo.bind("<<ComboboxSelected>>", self.on_crc_combo_changed)
            
            self.crc_custom_ent = tk.Entry(self.param_frame, font=("Consolas", 9), width=10, bg=THEME["panel"], fg=THEME["text"], relief="flat")
            self.crc_custom_ent.insert(0, PRESET_POLYNOMIALS["CRC-4 (ITU)"])
            self.crc_custom_ent.pack(side="left", padx=4)
            self.crc_custom_ent.bind("<KeyRelease>", lambda e: self.handle_encode())

    def on_technique_changed(self):
        self.update_param_controls()
        self.handle_encode()

    def on_crc_combo_changed(self, event=None):
        choice = self.crc_gen_choice.get()
        if choice in PRESET_POLYNOMIALS:
            self.crc_custom_ent.delete(0, tk.END)
            self.crc_custom_ent.insert(0, PRESET_POLYNOMIALS[choice])
        self.handle_encode()

    # -------------------------------------------------------------
    # RIGHT PANEL: Results, Interactive Algorithm Visualizers, NS-2 Trace
    # -------------------------------------------------------------
    def build_right_panel(self, parent):
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill="both", expand=True)
        
        # Tab 1: Verification Result & Architecture Pipeline
        self.tab_result = tk.Frame(self.notebook, bg=THEME["bg"], padx=10, pady=10)
        self.notebook.add(self.tab_result, text="  📊 Transmission & Results  ")
        
        # Tab 2: Detailed Technique Visualizer (Matrix, Hamming Table, CRC Steps, Checksum Additions)
        self.tab_visualizer = tk.Frame(self.notebook, bg=THEME["bg"], padx=10, pady=10)
        self.notebook.add(self.tab_visualizer, text="  🔬 Detailed Algorithm Visualizer  ")
        
        # Tab 3: NS-2 Channel Simulator & Trace Analytics
        self.tab_ns2 = tk.Frame(self.notebook, bg=THEME["bg"], padx=10, pady=10)
        self.notebook.add(self.tab_ns2, text="  🌐 NS-2 Network Simulator 2  ")
        
        self.build_tab_result()
        self.build_tab_visualizer()
        self.build_tab_ns2()

    def build_tab_result(self):
        # 1. Big Status Banner (Green / Red / Blue)
        self.status_banner = tk.Frame(self.tab_result, bg=THEME["card"], pady=12, padx=16, relief="solid", bd=1)
        self.status_banner.pack(fill="x", pady=(0, 10))
        
        self.lbl_status_icon = tk.Label(self.status_banner, text="READY", font=("Segoe UI", 16, "bold"),
                                        bg=THEME["card"], fg=THEME["text"])
        self.lbl_status_icon.pack(side="left", padx=8)
        
        self.lbl_status_desc = tk.Label(self.status_banner, text="Enter binary data and click 'Encode' to start simulation.",
                                        font=("Segoe UI", 10), bg=THEME["card"], fg=THEME["text_muted"])
        self.lbl_status_desc.pack(side="left", padx=8)
        
        # 2. Pipeline Cards Grid (Original -> Transmitted -> Injected/Received -> Result)
        cards_grid = tk.Frame(self.tab_result, bg=THEME["bg"])
        cards_grid.pack(fill="x", pady=(0, 10))
        
        def make_metric_card(parent, title, default_val):
            card = tk.Frame(parent, bg=THEME["panel"], padx=10, pady=8, relief="solid", bd=1)
            card.pack(side="left", fill="both", expand=True, padx=4)
            tk.Label(card, text=title, font=("Segoe UI", 8, "bold"), bg=THEME["panel"], fg=THEME["text_muted"]).pack(anchor="w")
            lbl_val = tk.Label(card, text=default_val, font=("Consolas", 11, "bold"), bg=THEME["panel"], fg=THEME["text"], wraplength=180, justify="left")
            lbl_val.pack(anchor="w", pady=(4, 0))
            return lbl_val
            
        self.card_orig = make_metric_card(cards_grid, "Original Data", "-")
        self.card_tx = make_metric_card(cards_grid, "Transmitted Frame", "-")
        self.card_rx = make_metric_card(cards_grid, "Received Frame", "-")
        self.card_corrected = make_metric_card(cards_grid, "Corrected Data", "-")

        # 3. Step-by-Step Flowchart Execution Summary
        flow_frame = tk.LabelFrame(
            self.tab_result,
            text=" System Architecture Execution Flow (Matches Lab Flowchart) ",
            font=("Segoe UI", 10, "bold"),
            bg=THEME["panel"],
            fg=THEME["accent"],
            padx=10,
            pady=8,
            relief="solid",
            bd=1
        )
        flow_frame.pack(fill="both", expand=True)
        
        self.txt_flow_log = scrolledtext.ScrolledText(
            flow_frame,
            font=("Consolas", 10),
            bg=THEME["bg"],
            fg=THEME["text"],
            insertbackground="#ffffff",
            relief="flat",
            bd=0,
            padx=8,
            pady=8
        )
        self.txt_flow_log.pack(fill="both", expand=True)

    def build_tab_visualizer(self):
        # Technique-specific custom visual view (Matrix table for 2D, Hamming syndrome breakdown, CRC division table)
        header_vis = tk.Frame(self.tab_visualizer, bg=THEME["bg"])
        header_vis.pack(fill="x", pady=(0, 6))
        
        self.lbl_vis_title = tk.Label(
            header_vis,
            text="Mathematical & Structural Breakdown",
            font=("Segoe UI", 12, "bold"),
            bg=THEME["bg"],
            fg="#38bdf8"
        )
        self.lbl_vis_title.pack(side="left")
        
        self.vis_content = tk.Frame(self.tab_visualizer, bg=THEME["panel"], padx=10, pady=10, relief="solid", bd=1)
        self.vis_content.pack(fill="both", expand=True)
        
        self.txt_vis_math = scrolledtext.ScrolledText(
            self.vis_content,
            font=("Consolas", 10),
            bg=THEME["bg"],
            fg=THEME["text"],
            relief="flat",
            bd=0,
            padx=8,
            pady=8
        )
        self.txt_vis_math.pack(fill="both", expand=True)

    def build_tab_ns2(self):
        # NS-2 discrete event simulator panel
        ns2_header = tk.Frame(self.tab_ns2, bg=THEME["panel"], padx=12, pady=10, relief="solid", bd=1)
        ns2_header.pack(fill="x", pady=(0, 10))
        
        tk.Label(
            ns2_header,
            text="Network Simulator 2 (NS-2) - Physical & Data Link Channel Simulation",
            font=("Segoe UI", 11, "bold"),
            bg=THEME["panel"],
            fg="#38bdf8"
        ).pack(anchor="w")
        
        info_txt = (
            "NS-2 simulates discrete packet flows across network links with an ErrorModel. "
            "Here, Transmitter Node (n0) sends encoded packets to Receiver Node (n1) across a channel subject to noise. "
            "Corrupted/dropped packets in NS-2 demonstrate channel degradation, triggering Data Link Layer error detection."
        )
        tk.Label(
            ns2_header,
            text=info_txt,
            font=("Segoe UI", 9),
            bg=THEME["panel"],
            fg=THEME["text_muted"],
            wraplength=700,
            justify="left"
        ).pack(anchor="w", pady=(2, 8))
        
        # NS-2 control parameters
        ctrl_bar = tk.Frame(ns2_header, bg=THEME["panel"])
        ctrl_bar.pack(fill="x")
        
        tk.Label(ctrl_bar, text="Channel Error Rate:", font=("Segoe UI", 9), bg=THEME["panel"], fg=THEME["text"]).pack(side="left")
        self.ns2_err_slider = tk.Scale(
            ctrl_bar,
            from_=0.0,
            to=0.8,
            resolution=0.05,
            orient="horizontal",
            length=140,
            bg=THEME["panel"],
            fg=THEME["text"],
            troughcolor=THEME["card"],
            highlightthickness=0
        )
        self.ns2_err_slider.set(0.2)
        self.ns2_err_slider.pack(side="left", padx=8)
        
        tk.Label(ctrl_bar, text="Packets:", font=("Segoe UI", 9), bg=THEME["panel"], fg=THEME["text"]).pack(side="left", padx=(10, 2))
        self.ns2_pkts_var = tk.IntVar(value=15)
        sp_pkts = tk.Spinbox(ctrl_bar, from_=5, to=50, width=4, textvariable=self.ns2_pkts_var)
        sp_pkts.pack(side="left", padx=4)
        
        self.btn_run_ns2 = tk.Button(
            ctrl_bar,
            text="▶ Run Real NS-2 Simulation",
            font=("Segoe UI", 9, "bold"),
            bg=THEME["accent"],
            fg="#ffffff",
            relief="flat",
            padx=10,
            command=self.execute_ns2_simulation_thread
        )
        self.btn_run_ns2.pack(side="left", padx=12)

        # NS-2 Results Summary Cards
        stats_frame = tk.Frame(self.tab_ns2, bg=THEME["bg"])
        stats_frame.pack(fill="x", pady=(0, 10))
        
        def make_ns2_stat(parent, title):
            f = tk.Frame(parent, bg=THEME["panel"], padx=12, pady=8, relief="solid", bd=1)
            f.pack(side="left", fill="both", expand=True, padx=4)
            tk.Label(f, text=title, font=("Segoe UI", 8, "bold"), bg=THEME["panel"], fg=THEME["text_muted"]).pack(anchor="w")
            lbl = tk.Label(f, text="-", font=("Segoe UI", 12, "bold"), bg=THEME["panel"], fg=THEME["text"])
            lbl.pack(anchor="w", pady=(2, 0))
            return lbl
            
        self.ns2_stat_sent = make_ns2_stat(stats_frame, "Packets Queued (+)")
        self.ns2_stat_corrupted = make_ns2_stat(stats_frame, "Corrupted / Dropped (d)")
        self.ns2_stat_received = make_ns2_stat(stats_frame, "Received by Sink (r)")
        self.ns2_stat_loss = make_ns2_stat(stats_frame, "Packet Error Rate (PER)")

        # Trace Log Display
        log_frame = tk.LabelFrame(
            self.tab_ns2,
            text=" NS-2 Trace File Events (.tr) & Transmission Timeline ",
            font=("Segoe UI", 10, "bold"),
            bg=THEME["panel"],
            fg=THEME["accent"],
            padx=8,
            pady=8,
            relief="solid",
            bd=1
        )
        log_frame.pack(fill="both", expand=True)
        
        self.txt_ns2_trace = scrolledtext.ScrolledText(
            log_frame,
            font=("Consolas", 9),
            bg=THEME["bg"],
            fg=THEME["text"],
            relief="flat",
            bd=0,
            padx=8,
            pady=8
        )
        self.txt_ns2_trace.pack(fill="both", expand=True)

    # -------------------------------------------------------------
    # SIMULATION LOGIC: Step 1 (Input & Encoding)
    # -------------------------------------------------------------
    def handle_encode(self):
        data = self.ent_data.get().strip()
        if not data:
            return
            
        tech = self.tech_var.get()
        res = {}
        
        if tech == "parity":
            ptype = getattr(self, "parity_type_var", tk.StringVar(value="even")).get()
            res = encode_parity(data, ptype)
            
        elif tech == "parity2d":
            rows = getattr(self, "p2d_rows_var", tk.IntVar(value=3)).get()
            cols = getattr(self, "p2d_cols_var", tk.IntVar(value=4)).get()
            ptype = getattr(self, "p2d_type_var", tk.StringVar(value="even")).get()
            res = encode_2d_parity(data, rows, cols, ptype)
            
        elif tech == "hamming":
            res = encode_hamming(data)
            
        elif tech == "checksum":
            block_sz = getattr(self, "chk_block_var", tk.IntVar(value=8)).get()
            res = encode_checksum(data, block_sz)
            
        elif tech == "crc":
            gen = self.crc_custom_ent.get().strip()
            if not gen or any(c not in "01" for c in gen) or gen[0] != '1':
                gen = "10011"
            res = encode_crc(data, gen)
            
        self.current_encoding_result = res
        self.current_encoded_frame = res.get("encoded_frame", "")
        self.current_transmitted_frame = self.current_encoded_frame
        self.flipped_indices = set()
        
        # Update metrics cards
        self.card_orig.config(text=data)
        self.card_tx.config(text=self.current_encoded_frame)
        self.card_rx.config(text=self.current_transmitted_frame)
        self.card_corrected.config(text="Pending Verification")
        
        # Render interactive bit boxes
        self.render_bit_buttons()
        
        # Display Flow Log
        self.txt_flow_log.delete("1.0", tk.END)
        self.txt_flow_log.insert(tk.END, "=== MODULE 1: INPUT DATA MODULE ===\n")
        self.txt_flow_log.insert(tk.END, f"Input Data: {data} (Length: {len(data)} bits)\n")
        self.txt_flow_log.insert(tk.END, f"Selected Technique: {self.get_technique_display_name()}\n\n")
        self.txt_flow_log.insert(tk.END, "=== MODULE 2-6: ENCODING & REDUNDANCY GENERATION ===\n")
        self.txt_flow_log.insert(tk.END, res.get("explanation", "") + "\n\n")
        self.txt_flow_log.insert(tk.END, "=== MODULE 7: TRANSMITTER READY ===\n")
        self.txt_flow_log.insert(tk.END, f"Transmitted Frame ready on channel: {self.current_encoded_frame}\n")
        self.txt_flow_log.insert(tk.END, "Click any bit above to inject an error, or click 'Transmit & Verify'.\n")
        
        # Update Visualizer Tab
        self.update_visualizer_tab(res)
        
        # Set Ready status banner
        self.status_banner.config(bg=THEME["card"])
        self.lbl_status_icon.config(text="READY ON CHANNEL", fg=THEME["accent_hover"], bg=THEME["card"])
        self.lbl_status_desc.config(text=f"Frame '{self.current_encoded_frame}' encoded. Modify bits or proceed to verify.", bg=THEME["card"])
        
        # Animate button feedback
        self.btn_encode.config(
            text="✓ Step 1 & 2: Encoded & Redundancy Generated!",
            bg=THEME["success"]
        )
        self.after(2000, lambda: self.btn_encode.config(
            text="⚡ Step 1 & 2: Encode & Generate Redundancy",
            bg=THEME["accent"]
        ))

    def get_technique_display_name(self) -> str:
        names = {
            "parity": "1D Parity Check",
            "parity2d": "2D Parity Check",
            "hamming": "Hamming Code (Error Detection & Correction)",
            "checksum": "Internet Checksum",
            "crc": "Cyclic Redundancy Check (CRC)"
        }
        return names.get(self.tech_var.get(), self.tech_var.get())

    def render_bit_buttons(self):
        # Clear previous bit buttons
        for w in self.bits_container.winfo_children():
            w.destroy()
        self.bit_buttons.clear()
        
        frame = self.current_transmitted_frame
        if not frame:
            return
            
        row_frame = None
        for i, bit_val in enumerate(frame):
            if i % 16 == 0:
                row_frame = tk.Frame(self.bits_container, bg=THEME["card"])
                row_frame.pack(fill="x", pady=2)
                
            is_flipped = (i in self.flipped_indices)
            btn_color = THEME["bit_flipped"] if is_flipped else (THEME["bit_1"] if bit_val == '1' else THEME["panel"])
            fg_color = "#ffffff"
            
            btn = tk.Button(
                row_frame,
                text=bit_val,
                font=("Consolas", 10, "bold"),
                width=3,
                height=1,
                bg=btn_color,
                fg=fg_color,
                activebackground=THEME["accent"],
                relief="flat",
                bd=1,
                command=lambda idx=i: self.toggle_bit(idx)
            )
            btn.pack(side="left", padx=2, pady=1)
            self.bit_buttons.append(btn)

    def toggle_bit(self, idx: int):
        chars = list(self.current_transmitted_frame)
        chars[idx] = '1' if chars[idx] == '0' else '0'
        self.current_transmitted_frame = "".join(chars)
        
        if idx in self.flipped_indices:
            self.flipped_indices.remove(idx)
        else:
            self.flipped_indices.add(idx)
            
        self.card_rx.config(text=self.current_transmitted_frame)
        self.render_bit_buttons()
        self.handle_verify()

    def inject_random_error(self):
        if not self.current_transmitted_frame:
            return
        res = inject_single_random_error(self.current_encoded_frame)
        self.current_transmitted_frame = res["corrupted_frame"]
        self.flipped_indices = set(res["flipped_indices"])
        self.card_rx.config(text=self.current_transmitted_frame)
        self.render_bit_buttons()
        self.handle_verify()

    def inject_burst_error_action(self):
        if not self.current_transmitted_frame:
            return
        res = inject_burst_error(self.current_encoded_frame, burst_length=3)
        self.current_transmitted_frame = res["corrupted_frame"]
        self.flipped_indices = set(res["flipped_indices"])
        self.card_rx.config(text=self.current_transmitted_frame)
        self.render_bit_buttons()
        self.handle_verify()

    def clear_channel_errors(self):
        self.current_transmitted_frame = self.current_encoded_frame
        self.flipped_indices = set()
        self.card_rx.config(text=self.current_transmitted_frame)
        self.render_bit_buttons()
        self.handle_verify()

    # -------------------------------------------------------------
    # SIMULATION LOGIC: Step 4 (Receiver Verification & Correction)
    # -------------------------------------------------------------
    def handle_verify(self):
        rx_frame = self.current_transmitted_frame
        if not rx_frame:
            return
            
        # Check if NS-2 channel simulation mode is selected
        if self.channel_sim_var.get() == "ns2":
            self.execute_ns2_simulation_thread()
            
        tech = self.tech_var.get()
        orig_data = self.ent_data.get().strip()
        v_res = {}
        
        if tech == "parity":
            ptype = getattr(self, "parity_type_var", tk.StringVar(value="even")).get()
            v_res = verify_parity(rx_frame, ptype, len(orig_data))
            
        elif tech == "parity2d":
            rows = getattr(self, "p2d_rows_var", tk.IntVar(value=3)).get()
            cols = getattr(self, "p2d_cols_var", tk.IntVar(value=4)).get()
            ptype = getattr(self, "p2d_type_var", tk.StringVar(value="even")).get()
            v_res = verify_2d_parity(rx_frame, rows, cols, ptype)
            
        elif tech == "hamming":
            v_res = verify_and_correct_hamming(rx_frame)
            
        elif tech == "checksum":
            block_sz = getattr(self, "chk_block_var", tk.IntVar(value=8)).get()
            v_res = verify_checksum(rx_frame, block_sz)
            
        elif tech == "crc":
            gen = self.crc_custom_ent.get().strip()
            if not gen:
                gen = "10011"
            v_res = verify_crc(rx_frame, gen)
            
        self.current_verification_result = v_res
        
        # Determine status and color styling
        err_detected = v_res.get("error_detected", False)
        can_correct = v_res.get("can_correct", False)
        
        if not err_detected:
            # Green: Data is Correct (No Error)
            self.status_banner.config(bg="#064e3b")
            self.lbl_status_icon.config(text="✓ DATA IS CORRECT (NO ERROR)", fg="#6ee7b7", bg="#064e3b")
            self.lbl_status_desc.config(text="Receiver verification passed successfully. No transmission errors detected.", bg="#064e3b", fg="#ecfdf5")
            self.card_corrected.config(text="Not Needed (Data Clean)", fg=THEME["success"])
        elif can_correct:
            # Blue: Error Detected and Corrected!
            self.status_banner.config(bg="#1e3a8a")
            self.lbl_status_icon.config(text="★ ERROR DETECTED & CORRECTED!", fg="#93c5fd", bg="#1e3a8a")
            corrected_val = v_res.get("recovered_data") or v_res.get("corrected_data") or v_res.get("corrected_frame", "-")
            self.lbl_status_desc.config(text=f"Single-bit error isolated. Data recovered: {corrected_val}", bg="#1e3a8a", fg="#eff6ff")
            self.card_corrected.config(text=corrected_val, fg="#60a5fa")
        else:
            # Red: Error Detected
            self.status_banner.config(bg="#7f1d1d")
            self.lbl_status_icon.config(text="⚠ ERROR DETECTED!", fg="#fca5a5", bg="#7f1d1d")
            self.lbl_status_desc.config(text="Transmission corrupted! Receiver detected bit discrepancy.", bg="#7f1d1d", fg="#fef2f2")
            self.card_corrected.config(text="Uncorrectable / Parity only", fg=THEME["error"])
            
        # Update Flow Log
        self.txt_flow_log.delete("1.0", tk.END)
        self.txt_flow_log.insert(tk.END, "========================================================\n")
        self.txt_flow_log.insert(tk.END, "   PROPOSED SYSTEM ARCHITECTURE EXECUTION LOG\n")
        self.txt_flow_log.insert(tk.END, "========================================================\n\n")
        self.txt_flow_log.insert(tk.END, f"1. [Input Message Data]: {orig_data}\n")
        self.txt_flow_log.insert(tk.END, f"2. [Selected Technique]: {self.get_technique_display_name()}\n")
        self.txt_flow_log.insert(tk.END, f"3. [Encoding / Redundancy]: {self.current_encoded_frame}\n")
        self.txt_flow_log.insert(tk.END, f"4. [Transmitter (Channel)]: Sent over communication link\n")
        
        has_channel_err = len(self.flipped_indices) > 0
        err_msg = f"Injected bit flip at 0-based indices: {sorted(list(self.flipped_indices))}" if has_channel_err else "None (Clean Channel)"
        self.txt_flow_log.insert(tk.END, f"5. [Error Injection]: {err_msg}\n")
        self.txt_flow_log.insert(tk.END, f"   Received Frame at Sink: {rx_frame}\n\n")
        self.txt_flow_log.insert(tk.END, "6. [Receiver Side Verification]:\n")
        self.txt_flow_log.insert(tk.END, v_res.get("explanation", "") + "\n\n")
        self.txt_flow_log.insert(tk.END, f"7. [Decision: Error Detected?]: {'YES' if err_detected else 'NO'}\n")
        if can_correct:
            self.txt_flow_log.insert(tk.END, f"8. [Error Correction]: Successfully corrected bit! Recovered message: {self.card_corrected.cget('text')}\n")
        self.txt_flow_log.insert(tk.END, "9. [Display Result]: Final status delivered to application sink.\n")
        
        # Update Visualizer Tab
        self.update_visualizer_tab(self.current_encoding_result, v_res)
        
        # Animate Step 4 button feedback
        self.btn_verify.config(
            text="✓ Step 4: Transmitted & Verified at Receiver!",
            bg="#059669"
        )
        self.after(2000, lambda: self.btn_verify.config(
            text="🔍 Step 4: Transmit & Verify at Receiver",
            bg=THEME["success"]
        ))

    def update_visualizer_tab(self, enc_res: Dict[str, Any], v_res: Dict[str, Any] = None):
        tech = self.tech_var.get()
        self.txt_vis_math.delete("1.0", tk.END)
        
        if tech == "parity2d":
            self.lbl_vis_title.config(text="2D Matrix Parity Breakdown & Coordinate Grid")
            self.txt_vis_math.insert(tk.END, "=== 2D PARITY MATRIX VIEW ===\n\n")
            
            # Show original matrix with row parities
            matrix = enc_res.get("matrix", [])
            row_p = enc_res.get("row_parities", [])
            col_p = enc_res.get("col_parities", [])
            corner_p = enc_res.get("corner_parity", "")
            
            self.txt_vis_math.insert(tk.END, "Transmitter Side Encoded Matrix:\n")
            header_str = "       " + " ".join(f"C{c}" for c in range(len(col_p))) + " | RowParity\n"
            self.txt_vis_math.insert(tk.END, header_str)
            self.txt_vis_math.insert(tk.END, "       " + "-" * (len(col_p) * 3 + 12) + "\n")
            
            for r_idx, row in enumerate(matrix):
                row_str = f"Row {r_idx}: " + "  ".join(row) + f"  |     {row_p[r_idx]}\n"
                self.txt_vis_math.insert(tk.END, row_str)
                
            self.txt_vis_math.insert(tk.END, "       " + "-" * (len(col_p) * 3 + 12) + "\n")
            col_str = "Col P: " + "  ".join(col_p) + f"  |     {corner_p} (Corner)\n\n"
            self.txt_vis_math.insert(tk.END, col_str)
            
            if v_res and v_res.get("matrix"):
                self.txt_vis_math.insert(tk.END, "Receiver Side Verified Matrix:\n")
                rx_mat = v_res.get("matrix", [])
                rx_row_p = v_res.get("row_parities", [])
                rx_col_p = v_res.get("col_parities", [])
                failed_r = v_res.get("failed_rows", [])
                failed_c = v_res.get("failed_cols", [])
                
                for r_idx, row in enumerate(rx_mat):
                    flag = " <-- PARITY FAILED!" if r_idx in failed_r else " (OK)"
                    self.txt_vis_math.insert(tk.END, f"Row {r_idx}: " + "  ".join(row) + f"  | {rx_row_p[r_idx]}{flag}\n")
                self.txt_vis_math.insert(tk.END, "Col P: " + "  ".join(rx_col_p) + f"  | {v_res.get('corner_parity')}\n")
                if failed_c:
                    col_flags = "       " + " ".join(" ^" if c in failed_c else "  " for c in range(len(rx_col_p))) + "\n"
                    self.txt_vis_math.insert(tk.END, col_flags)
                    self.txt_vis_math.insert(tk.END, f"Failed Column(s): {failed_c}\n\n")
                self.txt_vis_math.insert(tk.END, v_res.get("explanation", "") + "\n")
                
        elif tech == "hamming":
            self.lbl_vis_title.config(text="Hamming Code Codeword & Syndrome Bit Calculator")
            self.txt_vis_math.insert(tk.END, "=== HAMMING CODE ENCODING & SYNDROME ANALYSIS ===\n\n")
            self.txt_vis_math.insert(tk.END, enc_res.get("explanation", "") + "\n\n")
            if v_res:
                self.txt_vis_math.insert(tk.END, "=== RECEIVER SYNDROME CALCULATION ===\n\n")
                self.txt_vis_math.insert(tk.END, v_res.get("explanation", "") + "\n")
                
        elif tech == "crc":
            self.lbl_vis_title.config(text="Modulo-2 Polynomial Long Division (Bitwise XOR)")
            self.txt_vis_math.insert(tk.END, "=== CYCLIC REDUNDANCY CHECK (CRC) LONG DIVISION ===\n\n")
            self.txt_vis_math.insert(tk.END, enc_res.get("explanation", "") + "\n\n")
            
            steps = enc_res.get("steps", [])
            self.txt_vis_math.insert(tk.END, "Transmitter Division Steps:\n")
            for idx, s in enumerate(steps[:15]):
                self.txt_vis_math.insert(tk.END, f"Step {idx+1}: Window = {s['window']}, Divisor = {s['divisor_applied']} -> XOR = {s['xor_result']}, Pull down: {s.get('brought_down')}\n")
            if len(steps) > 15:
                self.txt_vis_math.insert(tk.END, f"... [{len(steps)-15} additional division steps omitted for brevity]\n")
                
            if v_res:
                self.txt_vis_math.insert(tk.END, "\n=== RECEIVER POLYNOMIAL VERIFICATION ===\n\n")
                self.txt_vis_math.insert(tk.END, v_res.get("explanation", "") + "\n")
                
        elif tech == "checksum":
            self.lbl_vis_title.config(text="Internet Checksum 1's Complement Block Addition")
            self.txt_vis_math.insert(tk.END, "=== INTERNET CHECKSUM 1'S COMPLEMENT ADDITION ===\n\n")
            self.txt_vis_math.insert(tk.END, enc_res.get("explanation", "") + "\n\n")
            if v_res:
                self.txt_vis_math.insert(tk.END, "=== RECEIVER CHECKSUM VERIFICATION ===\n\n")
                self.txt_vis_math.insert(tk.END, v_res.get("explanation", "") + "\n")
                
        else: # 1D parity
            self.lbl_vis_title.config(text="1D Parity Bit Calculation")
            self.txt_vis_math.insert(tk.END, enc_res.get("explanation", "") + "\n\n")
            if v_res:
                self.txt_vis_math.insert(tk.END, v_res.get("explanation", "") + "\n")

    # -------------------------------------------------------------
    # NS-2 SIMULATION EXECUTION IN THREAD
    # -------------------------------------------------------------
    def execute_ns2_simulation_thread(self):
        self.btn_run_ns2.config(state="disabled", text="⏳ Running NS-2 in WSL...")
        threading.Thread(target=self._run_ns2_worker, daemon=True).start()

    def _run_ns2_worker(self):
        err_rate = self.ns2_err_slider.get()
        num_pkts = self.ns2_pkts_var.get()
        frame = self.current_transmitted_frame or "11010010"
        
        sim_res = run_ns2_simulation(
            encoded_bits=frame,
            error_rate=err_rate,
            num_packets=num_pkts
        )
        
        # Update UI in main thread
        self.after(0, lambda: self._apply_ns2_results(sim_res))

    def _apply_ns2_results(self, sim_res: Dict[str, Any]):
        self.btn_run_ns2.config(state="normal", text="▶ Run Real NS-2 Simulation")
        
        sent = sim_res.get("total_sent", 0)
        corrupted = sim_res.get("total_dropped", 0)
        received = sim_res.get("total_received", 0)
        loss_pct = sim_res.get("loss_percentage", 0.0)
        
        self.ns2_stat_sent.config(text=str(sent))
        self.ns2_stat_corrupted.config(text=str(corrupted), fg=THEME["error"] if corrupted > 0 else THEME["text"])
        self.ns2_stat_received.config(text=str(received), fg=THEME["success"])
        self.ns2_stat_loss.config(text=f"{loss_pct}%", fg=THEME["warning"] if loss_pct > 0 else THEME["success"])
        
        self.txt_ns2_trace.delete("1.0", tk.END)
        self.txt_ns2_trace.insert(tk.END, f"=== NS-2 Discrete Event Simulation Output ===\n")
        self.txt_ns2_trace.insert(tk.END, f"NS-2 Engine: {'Active (/usr/bin/ns in WSL)' if not sim_res.get('used_fallback') else 'Fallback Channel'}\n")
        self.txt_ns2_trace.insert(tk.END, f"Trace File: {sim_res.get('trace_file')}\n")
        self.txt_ns2_trace.insert(tk.END, f"NAM Animation File: {sim_res.get('nam_file')}\n\n")
        self.txt_ns2_trace.insert(tk.END, f"Summary: Transmitted = {sent}, Corrupted/Dropped = {corrupted}, Successfully Received = {received}, Packet Error Rate = {loss_pct}%\n")
        self.txt_ns2_trace.insert(tk.END, "-" * 70 + "\n")
        self.txt_ns2_trace.insert(tk.END, f"{'Time (s)':<10} {'Action':<8} {'Packet ID':<12} {'Description'}\n")
        self.txt_ns2_trace.insert(tk.END, "-" * 70 + "\n")
        
        for ev in sim_res.get("events", []):
            action_code = ev.get("action", "")
            action_name = {
                "+": "ENQUEUE",
                "-": "DEQUEUE",
                "d": "DROP/ERR",
                "r": "RECEIVE"
            }.get(action_code, action_code)
            line = f"{ev.get('time', ''):<10} {action_name:<8} {ev.get('pkt_id', ''):<12} {ev.get('desc', '')}\n"
            self.txt_ns2_trace.insert(tk.END, line)
            
        # Switch to NS-2 tab so user immediately sees results if invoked directly
        if self.channel_sim_var.get() == "ns2":
            self.notebook.select(self.tab_ns2)

    def load_preset(self, p: str):
        presets = {
            "8bit": "11010010",
            "4bit": "1011",
            "12bit": "101100101101",
            "16bit": "1010110001011101"
        }
        self.set_input_data(presets.get(p, "11010010"))

if __name__ == "__main__":
    app = NetworkSimulatorApp()
    app.mainloop()
