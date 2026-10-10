# Interactive Network Error Detection and Correction Simulator

**Computer Networks Lab Project**  

### Team Details
- **AMAN KUMAR YADAV**
- **PRATIK BHARADBHUNJE**
- **DEVRISHI GADIA**

---

## 1. Project Overview & Abstract

Data transmission over physical communication channels in computer networks is susceptible to noise, attenuation, and interference, causing bits to flip during transmission. Reliable network communication necessitates robust error control mechanisms at the **Data Link Layer**.

This project provides an **Interactive Network Error Detection and Correction Simulator** with **Network Simulator 2 (NS-2)** channel integration. The system implements:
1. **1D Parity Check** (Even and Odd Parity)
2. **2D Parity Check** (Matrix / Grid Parity with Row & Column Parity, single-bit error localization)
3. **Hamming Code** (General $n, k$ encoding, syndrome computation, and automatic single-bit correction)
4. **Internet Checksum** (Variable block segmentation, 1's complement binary addition with end-around carry)
5. **Cyclic Redundancy Check (CRC)** (Modulo-2 XOR polynomial division with standard presets and custom generator polynomials)
6. **Error Injection Module** (Interactive bit-flipping, random error generation, and burst error simulation)
7. **NS-2 Channel Simulator** (Discrete-event simulation modeling Transmitter $\rightarrow$ Link with `ErrorModel` $\rightarrow$ Receiver with `.tr` trace and `.nam` animations)

---

## 2. Where & How NS-2 is Integrated into the Architecture

### The Role of NS-2 in Error Detection & Correction
In Computer Networks:
- **Data Link Layer** (Software / Protocol Logic): Generates frame redundancy (Parity bits, Hamming bits, Checksums, CRC FCS) and performs receiver verification / error correction.
- **Physical & Transmission Channel** (Network Link): Data travels through physical media (wires, fiber, wireless links) where noise causes packet corruption or bit alterations.

```
+---------------------------------------------------------------------------------------+
|                                DATA LINK LAYER (TRANSMITTER)                          |
|  [Input Data] ---> [Encoding & Redundancy: Parity / Hamming / Checksum / CRC]        |
+-------------------------------------------+-------------------------------------------+
                                            | Encoded Frame
                                            v
+---------------------------------------------------------------------------------------+
|                        NS-2 NETWORK SIMULATOR (TRANSMISSION CHANNEL)                  |
|                                                                                       |
|   Transmitter Node (n0) ========= Duplex Link (2Mb, 10ms) =========> Receiver Node (n1)  |
|                                         |                                             |
|                                   [ErrorModel]                                        |
|                          (Uniform Loss / Corruption)                                  |
|                                         |                                             |
|                         Generates .tr (Trace) & .nam (NAM)                            |
+-------------------------------------------+-------------------------------------------+
                                            | Received (Possibly Corrupted) Frame
                                            v
+---------------------------------------------------------------------------------------+
|                                 DATA LINK LAYER (RECEIVER)                            |
|  [Receiver Verification] ---> [Error Detected? Yes/No] ---> [Error Correction / Result]
+---------------------------------------------------------------------------------------+
```

### Where NS-2 is used:
1. **Channel Modeling (`ns2/network_error_sim.tcl`):**
   - Transmitter node (`$n0`) sends discrete packets across a duplex link to Receiver node (`$n1`).
   - An `ErrorModel` (`set loss_module [new ErrorModel]`) is attached to the communication link to simulate channel bit and packet corruption with configurable error probabilities.
   - NS-2 records real-time transmission events in `gui_run.tr`:
     - `+`: Enqueued at transmitter
     - `-`: Dequeued onto link
     - `d`: Dropped / corrupted by the channel `ErrorModel`
     - `r`: Successfully received by receiver sink
2. **Interactive Bridge (`modules/ns2_bridge.py`):**
   - The Python application triggers the NS-2 engine (via WSL Ubuntu or native NS-2).
   - Trace events are parsed and displayed live in the GUI's **NS-2 Network Simulator 2** tab, showing packets sent, corrupted, received, and packet error rate (PER).
   - Generates NAM animation files (`.nam`) that can be viewed using the Network Animator.

---

## 3. System Architecture Flowchart (Matches PDF Proposal)

```
                              [ Start ]
                                  |
                    [ Input Message Data (Binary) ]
                                  |
                        [ Select Technique ]
                    1. Parity Check (Even/Odd)
                    2. 2D Parity Check (Matrix)
                    3. Hamming Code
                    4. Internet Checksum
                    5. Cyclic Redundancy Check (CRC)
                                  |
                 [ Encoding / Redundancy Generation ]
               (Compute parity bits, checksum, CRC, or
                     Hamming codeword)
                                  |
                           [ Transmitter ]
                 (Send Data over Communication Channel)
                                  |
                      [ NS-2 / Error Injection ]
                 (Flip bits or apply NS-2 ErrorModel)
                                  |
                    [ Receiver Side Verification ]
                (Check received data with selected technique)
                                  |
                       < Error Detected? >
                          /           \
                     Yes /             \ No
                        /               \
       [ Error Detection / Correction ]  [ Data is Correct (No Error) ]
       • Parity / 2D / Checksum / CRC:   |
         Detect error                     |
       • Hamming Code & 2D Parity:        |
         Detect and correct single-bit    |
                        \                 /
                         \               /
                          v             v
                          [ Display Result ]
                      • Original data
                      • Transmitted frame
                      • Received frame
                      • Error status (Green/Red/Blue)
                      • Corrected data (if applicable)
                                  |
                               [ Stop ]
```

---

## 4. Module Breakdown (9 Modules)

| Module | Name | Functionality |
| :--- | :--- | :--- |
| **Module 1** | Input Data Module | Validates binary input ($0$ and $1$), includes ASCII text-to-binary converter, and offers one-click presets ($4$-bit, $8$-bit, $12$-bit, $16$-bit). |
| **Module 2** | Parity Check Module | Implements Even and Odd parity; computes parity bit $P$ such that $\sum \text{bits} \equiv 0 \pmod 2$ (Even) or $1 \pmod 2$ (Odd). |
| **Module 3** | 2D Parity Check Module | Arranges bits into an $R \times C$ matrix, calculates row parities and column parities, and pinpoints exact $(r, c)$ intersection of flipped bits. |
| **Module 4** | Hamming Code Module | Computes parity positions at powers of $2$ ($1, 2, 4, 8, \dots$), evaluates syndrome bits $S_r \dots S_1$, pinpoints flipped bit location $S$, and corrects it. |
| **Module 5** | Checksum Module | Segments data into $k$-bit blocks, executes 1's complement addition with end-around carry, inverts sum to generate Checksum, and verifies receiver total. |
| **Module 6** | CRC Module | Modulo-2 binary long division using XOR; supports CRC-4, CRC-8, CRC-16, CRC-32, and custom user generator polynomials with step-by-step division trace. |
| **Module 7** | Error Injection Module | Interactive clickable bit toggle, random bit corruption, and burst error simulation. |
| **Module 8** | Receiver Verification | Analyzes received frames, executes syndrome/parity/polynomial checks, and handles recovery. |
| **Module 9** | Result & Visualization | Color-coded status banners, step-by-step math breakdowns, metric comparison cards, and NS-2 trace event timeline. |

---

## 5. How to Run the Simulator

### Option A: Launch Interactive Graphical Interface (GUI)
Double-click `run_app.bat` or run:
```bash
python main.py
```

### Option B: Run Command-Line Demonstration (CLI)
For a terminal demonstration showing all 5 techniques and NS-2 simulation:
```bash
python cli_demo.py
```

### Option C: Run Standalone NS-2 Simulation directly in WSL/Linux
```bash
wsl bash -c "cd /mnt/d/CNLFINAL/ns2 && ns network_error_sim.tcl 64 0.25 20 my_run"
```
Or view the animation with NAM:
```bash
wsl nam /mnt/d/CNLFINAL/ns2/my_run.nam
```

---

## 6. Project Directory Structure

```
d:\CNLFINAL\
│
├── main.py                     # Main Tkinter Interactive Application
├── cli_demo.py                 # Command-line demonstration of all 9 modules
├── test_all_modules.py         # Automated unit test suite (100% passing)
├── run_app.bat                 # 1-click Windows launcher
├── requirements.txt            # Zero-dependency specification (Python Standard Library)
├── README.md                   # Complete Project Documentation
│
├── modules\                    # Modular Python Packages
│   ├── __init__.py
│   ├── parity.py               # Module 2: 1D Parity (Even/Odd)
│   ├── parity2d.py             # Module 3: 2D Matrix Parity & Error Pinpointing
│   ├── hamming.py              # Module 4: Hamming Code (Syndrome & Bit Correction)
│   ├── checksum.py             # Module 5: Internet Checksum (1's complement)
│   ├── crc.py                  # Module 6: CRC (Modulo-2 XOR Polynomial Division)
│   ├── error_injection.py      # Module 7: Channel Noise & Bit-Flipping
│   └── ns2_bridge.py           # NS-2 WSL Integration & Trace Parsing (.tr)
│
└── ns2\                        # Network Simulator 2 Scripts & Artifacts
    ├── network_error_sim.tcl   # NS-2 OTcl Script with ErrorModel
    ├── run_simulation.sh       # Linux/WSL Shell Runner
    ├── gui_run.tr              # Generated NS-2 Trace File
    └── gui_run.nam             # Generated Network Animator File
```

---

## 7. Viva & Lab Evaluation Questions

**Q1: Where does NS-2 fit in an Error Detection/Correction project?**  
*Answer:* In real networks, error detection and correction algorithms operate at the Data Link Layer (Layer 2). NS-2 acts as the physical/link channel simulator between Node 0 (Transmitter) and Node 1 (Receiver). By attaching an `ErrorModel` to the link in NS-2, we simulate realistic channel noise, packet loss, and corruption. The Data Link Layer algorithms then detect and correct corrupted data.

**Q2: What is the syndrome in Hamming Code?**  
*Answer:* The syndrome $S = (s_r s_{r-1} \dots s_1)_2$ is formed by evaluating parity checks on the received codeword. If $S = 0$, no error occurred. If $S > 0$, the decimal value of $S$ directly represents the 1-indexed bit position of the corrupted bit, allowing immediate single-bit correction by flipping that bit.

**Q3: Why does Internet Checksum use 1's complement addition?**  
*Answer:* 1's complement addition handles end-around carries (adding overflow back to the LSB) and makes verification very simple: at the receiver, adding all data blocks plus the checksum yields all 1s (which, when complemented, equals 0). Additionally, 1's complement checksums are independent of machine endianness (byte ordering).

**Q4: How does CRC detect errors?**  
*Answer:* The transmitter appends $r$ zeros to the data (where $r$ is the degree of generator polynomial $G$) and performs Modulo-2 binary long division (using bitwise XOR). The remainder is attached to the message. The receiver performs the same Modulo-2 division on the received frame. If the remainder is all zeros, no error was detected; otherwise, an error occurred.
