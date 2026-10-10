/**
 * Interactive Network Error Detection and Correction Simulator
 * Client Application Logic (BCSE308P)
 */

// Application State
const state = {
    inputData: "11010010",
    technique: "parity",
    parityType: "even",
    p2dRows: 3,
    p2dCols: 4,
    chkBlockSize: 8,
    crcGenerator: "10011",
    encodedFrame: "",
    transmittedFrame: "",
    flippedIndices: new Set(),
    encodingResult: null,
    verificationResult: null,
    ns2Result: null,
    ns2Available: false
};

// Preset CRC Polynomials
const CRC_PRESETS = {
    "CRC-4 (ITU)": "10011",
    "CRC-8 (Standard)": "100000111",
    "CRC-12": "1100000001111",
    "CRC-16 (IBM)": "11000000000000101",
    "CRC-CCITT": "10001000000100001",
    "CRC-32 (IEEE 802.3)": "100000100110000010001110110110111"
};

// Initialize Application
document.addEventListener("DOMContentLoaded", () => {
    initEventListeners();
    checkSystemStatus();
    updateTechParams();
    triggerEncoding();
});

function initEventListeners() {
    // Binary input live validation
    const inputBin = document.getElementById("inputBinary");
    inputBin.addEventListener("input", (e) => {
        let clean = e.target.value.replace(/[^01]/g, "");
        if (clean !== e.target.value) {
            e.target.value = clean;
        }
        state.inputData = clean || "0";
        document.getElementById("bitCountBadge").textContent = `${state.inputData.length} bits`;
        triggerEncoding();
    });

    // Tab Navigation
    document.querySelectorAll(".tab-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
            document.querySelectorAll(".tab-content").forEach(c => c.classList.remove("active"));
            btn.classList.add("active");
            const targetId = btn.getAttribute("data-tab");
            document.getElementById(targetId).classList.add("active");
        });
    });

    // Team Modal
    const modal = document.getElementById("teamModal");
    document.getElementById("btnTeamModal").addEventListener("click", () => {
        modal.classList.add("open");
    });
    document.getElementById("btnCloseModal").addEventListener("click", () => {
        modal.classList.remove("open");
    });
    modal.addEventListener("click", (e) => {
        if (e.target === modal) modal.classList.remove("open");
    });
}

// Check Backend & NS-2 Status
async function checkSystemStatus() {
    const badge = document.getElementById("ns2EngineBadge");
    const text = document.getElementById("ns2EngineText");
    const tabBadge = document.getElementById("ns2TabStatusBadge");

    try {
        const res = await fetch("/api/status");
        if (res.ok) {
            const data = await res.json();
            if (data.ns2 && data.ns2.available) {
                state.ns2Available = true;
                badge.classList.add("online");
                text.textContent = "NS-2 Engine: Connected (WSL)";
                if (tabBadge) tabBadge.textContent = "NS-2 Active (/usr/bin/ns)";
            } else {
                badge.classList.remove("online");
                text.textContent = "NS-2 Engine: Standby (Fallback Mode)";
                if (tabBadge) tabBadge.textContent = "Fallback Channel";
            }
        }
    } catch (err) {
        text.textContent = "NS-2 Engine: Standby";
    }
}

// Preset helpers
function applyPreset(bits, el) {
    document.querySelectorAll(".presets-row .btn-chip").forEach(c => c.classList.remove("active"));
    if (el && el.classList) {
        el.classList.add("active");
    } else {
        document.querySelectorAll(".presets-row .btn-chip").forEach(c => {
            if (c.textContent.trim() === `${bits.length}-bit` || c.getAttribute("onclick")?.includes(`'${bits}'`)) {
                c.classList.add("active");
            }
        });
    }
    const input = document.getElementById("inputBinary");
    input.value = bits;
    state.inputData = bits;
    document.getElementById("bitCountBadge").textContent = `${bits.length} bits`;
    triggerEncoding();
}

function convertTextToBinary() {
    const txt = document.getElementById("asciiInput").value;
    if (!txt) return;
    let binary = "";
    for (let i = 0; i < txt.length; i++) {
        binary += txt.charCodeAt(i).toString(2).padStart(8, '0');
    }
    applyPreset(binary);
}

// Channel Mode Radio Change
function onChanModeChange() {
    const selected = document.querySelector('input[name="chanMode"]:checked')?.value || "direct";
    const directLabel = document.getElementById("chanModeDirectLabel");
    const ns2Label = document.getElementById("chanModeNs2Label");
    if (directLabel) directLabel.classList.toggle("active", selected === "direct");
    if (ns2Label) ns2Label.classList.toggle("active", selected === "ns2");

    if (selected === "ns2") {
        const ns2Tab = document.querySelector('.tab-btn[data-tab="tab-ns2"]');
        if (ns2Tab) ns2Tab.click();
    }
}

// Architecture Flow Pipeline Step Manager
function updatePipelineSteps(stage) {
    for (let i = 1; i <= 6; i++) {
        const step = document.getElementById(`pipeStep${i}`);
        const num = document.getElementById(`pipeNum${i}`);
        if (!step || !num) continue;
        step.classList.remove("completed", "current", "active");

        if (stage === 1) {
            if (i === 1) { step.classList.add("current"); num.textContent = "1"; }
            else if (i === 2) { step.classList.add("active"); num.textContent = "2"; }
            else { num.textContent = String(i); }
        } else if (stage === 2) {
            // Step 1 & 2 Completed (Encoded)
            if (i === 1 || i === 2) {
                step.classList.add("completed");
                num.textContent = "✓";
            } else if (i === 3 || i === 4) {
                step.classList.add("current");
                num.textContent = String(i);
            } else {
                num.textContent = String(i);
            }
        } else if (stage === 3) {
            // Channel & NS-2
            if (i <= 2) { step.classList.add("completed"); num.textContent = "✓"; }
            else if (i === 3) { step.classList.add("current"); num.textContent = "3"; }
            else if (i === 4) { step.classList.add("active"); num.textContent = "4"; }
            else { num.textContent = String(i); }
        } else if (stage === 4) {
            // Error Injection active
            if (i <= 2) { step.classList.add("completed"); num.textContent = "✓"; }
            else if (i === 4) { step.classList.add("current"); num.textContent = "4"; }
            else if (i === 5) { step.classList.add("active"); num.textContent = "5"; }
            else { num.textContent = String(i); }
        } else if (stage >= 5) {
            // Verification and Correction completed
            if (i <= 5) {
                step.classList.add("completed");
                num.textContent = "✓";
            }
            if (i === 6) {
                step.classList.add("completed");
                num.textContent = "✓";
            }
        }
    }
// Toast Notification Manager
function showToast(title, desc, type = "info", icon = "●") {
    const container = document.getElementById("toastContainer");
    if (!container) return;

    const toast = document.createElement("div");
    toast.className = `toast-msg ${type}`;
    toast.innerHTML = `
        <div class="toast-icon">${icon}</div>
        <div class="toast-text">
            <span class="toast-title">${title}</span>
            <span class="toast-desc">${desc}</span>
        </div>
    `;

    container.appendChild(toast);

    // Auto remove after 3s
    setTimeout(() => {
        if (toast.parentNode) {
            toast.parentNode.removeChild(toast);
        }
    }, 3100);
}

// Pipeline Steps Interactive Click Handler with Rich Visual Feedback
function handleStepClick(stepNum) {
    // 1. Highlight the exact clicked step with radiant glowing ring
    document.querySelectorAll(".pipeline-step").forEach(s => s.classList.remove("selected-step"));
    const clicked = document.getElementById(`pipeStep${stepNum}`);
    if (clicked) {
        clicked.classList.add("selected-step");
        setTimeout(() => clicked.classList.remove("selected-step"), 2500);
    }

    if (stepNum === 1) {
        showToast("Step 1: Input Data Module", "Binary source message ready for editing.", "info", "📌");
        const card = document.getElementById("cardInput");
        if (card) {
            card.scrollIntoView({ behavior: "smooth", block: "center" });
            card.classList.add("card-highlight");
            setTimeout(() => card.classList.remove("card-highlight"), 1800);
        }
        const inp = document.getElementById("inputBinary");
        if (inp) { inp.focus(); inp.select(); }
        updatePipelineSteps(1);
    } else if (stepNum === 2) {
        showToast("Step 2: Redundancy Encoding", "Generated check bits & transmitted codeword.", "success", "⚡");
        const card = document.getElementById("cardTechnique");
        if (card) {
            card.scrollIntoView({ behavior: "smooth", block: "center" });
            card.classList.add("card-highlight");
            setTimeout(() => card.classList.remove("card-highlight"), 1800);
        }
        triggerEncoding();
    } else if (stepNum === 3) {
        showToast("Step 3: Network Channel & NS-2", "Link transmission modeling with packet error rate.", "info", "🌐");
        const chanMode = document.querySelector('input[name="chanMode"][value="ns2"]');
        if (chanMode) {
            chanMode.checked = true;
            onChanModeChange();
        }
        const ns2Tab = document.querySelector('.tab-btn[data-tab="tab-ns2"]');
        if (ns2Tab) ns2Tab.click();
        updatePipelineSteps(3);
    } else if (stepNum === 4) {
        showToast("Step 4: Channel Error Injection", "Click any bit below to flip it and simulate noise.", "warn", "🎯");
        const card = document.getElementById("cardChannel");
        if (card) {
            card.scrollIntoView({ behavior: "smooth", block: "center" });
            card.classList.add("card-highlight");
            setTimeout(() => card.classList.remove("card-highlight"), 1800);
        }
        const track = document.getElementById("bitsTrack");
        if (track) {
            track.style.borderColor = "var(--color-warning)";
            setTimeout(() => track.style.borderColor = "var(--border-color)", 1400);
        }
        updatePipelineSteps(4);
    } else if (stepNum === 5) {
        showToast("Step 5: Receiver Verification", "Transmitted across channel & checked at receiver sink.", "info", "🔍");
        const resTab = document.querySelector('.tab-btn[data-tab="tab-results"]');
        if (resTab) resTab.click();
        triggerVerification();
    } else if (stepNum === 6) {
        showToast("Step 6: Diagnosis & Recovery", "Viewing mathematical syndrome & parity grid visualizer.", "success", "🔬");
        const visTab = document.querySelector('.tab-btn[data-tab="tab-visualizer"]');
        if (visTab) visTab.click();
        updatePipelineSteps(6);
    }
}

// Technique Radio Change
function onTechniqueChange() {
    const selected = document.querySelector('input[name="technique"]:checked').value;
    state.technique = selected;
    
    // Style active radio card
    document.querySelectorAll(".radio-card").forEach(c => c.classList.remove("active"));
    const activeRadio = document.querySelector(`input[name="technique"][value="${selected}"]`);
    if (activeRadio) activeRadio.closest(".radio-card").classList.add("active");

    updateTechParams();
    triggerEncoding();
}

// Dynamic Parameters Subcard
function updateTechParams() {
    const container = document.getElementById("techParamsContainer");
    const tech = state.technique;

    if (tech === "parity") {
        container.innerHTML = `
            <div style="display: flex; align-items: center; gap: 14px;">
                <span style="font-size: 0.85rem; font-weight: 600; color: var(--text-secondary);">Parity Scheme:</span>
                <label style="display: flex; align-items: center; gap: 6px; font-size: 0.85rem; color: #fff; cursor: pointer;">
                    <input type="radio" name="parityScheme" value="even" ${state.parityType === 'even' ? 'checked' : ''} onchange="setParityType('even')"> Even Parity
                </label>
                <label style="display: flex; align-items: center; gap: 6px; font-size: 0.85rem; color: #fff; cursor: pointer;">
                    <input type="radio" name="parityScheme" value="odd" ${state.parityType === 'odd' ? 'checked' : ''} onchange="setParityType('odd')"> Odd Parity
                </label>
            </div>
        `;
    } else if (tech === "parity2d") {
        container.innerHTML = `
            <div style="display: grid; grid-template-columns: 1fr 1fr 1.2fr; gap: 10px; align-items: center;">
                <div>
                    <label style="font-size: 0.78rem; color: var(--text-muted); display: block;">Rows:</label>
                    <input type="number" min="2" max="6" value="${state.p2dRows}" style="width: 100%;" onchange="setP2dDim('rows', this.value)">
                </div>
                <div>
                    <label style="font-size: 0.78rem; color: var(--text-muted); display: block;">Cols:</label>
                    <input type="number" min="2" max="6" value="${state.p2dCols}" style="width: 100%;" onchange="setP2dDim('cols', this.value)">
                </div>
                <div>
                    <label style="font-size: 0.78rem; color: var(--text-muted); display: block;">Parity:</label>
                    <select style="width: 100%;" onchange="setParityType(this.value)">
                        <option value="even" ${state.parityType === 'even' ? 'selected' : ''}>Even</option>
                        <option value="odd" ${state.parityType === 'odd' ? 'selected' : ''}>Odd</option>
                    </select>
                </div>
            </div>
        `;
    } else if (tech === "hamming") {
        container.innerHTML = `
            <div style="font-size: 0.82rem; color: var(--text-secondary);">
                <p>Standard Hamming Code (n, k): Parity bits inserted at positions <strong>1, 2, 4, 8, ...</strong></p>
                <p style="color: var(--color-cyan-hover); margin-top: 4px;">Evaluates syndrome bits at receiver to isolate and flip corrupted bit automatically.</p>
            </div>
        `;
    } else if (tech === "checksum") {
        container.innerHTML = `
            <div style="display: flex; align-items: center; gap: 14px;">
                <span style="font-size: 0.85rem; font-weight: 600; color: var(--text-secondary);">Block Size:</span>
                <label style="display: flex; align-items: center; gap: 6px; font-size: 0.85rem; color: #fff; cursor: pointer;">
                    <input type="radio" name="chkBlock" value="4" ${state.chkBlockSize === 4 ? 'checked' : ''} onchange="setBlockSize(4)"> 4-bit
                </label>
                <label style="display: flex; align-items: center; gap: 6px; font-size: 0.85rem; color: #fff; cursor: pointer;">
                    <input type="radio" name="chkBlock" value="8" ${state.chkBlockSize === 8 ? 'checked' : ''} onchange="setBlockSize(8)"> 8-bit
                </label>
                <label style="display: flex; align-items: center; gap: 6px; font-size: 0.85rem; color: #fff; cursor: pointer;">
                    <input type="radio" name="chkBlock" value="16" ${state.chkBlockSize === 16 ? 'checked' : ''} onchange="setBlockSize(16)"> 16-bit
                </label>
            </div>
        `;
    } else if (tech === "crc") {
        container.innerHTML = `
            <div>
                <label style="font-size: 0.78rem; color: var(--text-muted); display: block; margin-bottom: 4px;">Generator Polynomial Preset:</label>
                <select id="crcSelect" style="width: 100%; margin-bottom: 8px;" onchange="onCrcPresetChange(this.value)">
                    <option value="CRC-4 (ITU)">CRC-4 (ITU) [10011]</option>
                    <option value="CRC-8 (Standard)">CRC-8 (Standard) [100000111]</option>
                    <option value="CRC-12">CRC-12 [1100000001111]</option>
                    <option value="CRC-16 (IBM)">CRC-16 (IBM) [11000000000000101]</option>
                    <option value="CRC-CCITT">CRC-CCITT [10001000000100001]</option>
                    <option value="custom">Custom Generator</option>
                </select>
                <input type="text" id="crcCustomInput" value="${state.crcGenerator}" style="width: 100%; font-family: var(--font-mono);" placeholder="Binary generator (e.g. 10011)" onchange="state.crcGenerator=this.value; triggerEncoding();">
            </div>
        `;
    }
}

function setParityType(type) {
    state.parityType = type;
    triggerEncoding();
}

function setP2dDim(key, val) {
    if (key === 'rows') state.p2dRows = parseInt(val) || 3;
    if (key === 'cols') state.p2dCols = parseInt(val) || 4;
    triggerEncoding();
}

function setBlockSize(sz) {
    state.chkBlockSize = sz;
    triggerEncoding();
}

function onCrcPresetChange(val) {
    if (val in CRC_PRESETS) {
        state.crcGenerator = CRC_PRESETS[val];
        document.getElementById("crcCustomInput").value = state.crcGenerator;
    }
    triggerEncoding();
}

// -------------------------------------------------------------
// STEP 1 & 2: ENCODING AND REDUNDANCY GENERATION
// -------------------------------------------------------------
async function triggerEncoding() {
    // Dynamic button clicked feedback
    const btnEnc = document.getElementById("btnEncode");
    const txtEnc = document.getElementById("btnEncodeText");
    if (btnEnc) {
        btnEnc.classList.add("btn-completed");
        if (txtEnc) txtEnc.innerHTML = "✓ Step 1 & 2: Encoded & Redundancy Generated!";
        showToast("Step 1 & 2 Completed", "Frame encoded with check bits attached!", "success", "⚡");
        setTimeout(() => {
            btnEnc.classList.remove("btn-completed");
            if (txtEnc) txtEnc.innerHTML = "⚡ Step 1 & 2: Re-Encode / Update Redundancy";
        }, 2200);
    }

    const payload = {
        data: state.inputData || "11010010",
        technique: state.technique,
        parity_type: state.parityType,
        rows: state.p2dRows,
        cols: state.p2dCols,
        block_size: state.chkBlockSize,
        generator: state.crcGenerator
    };

    let encResult = null;
    try {
        const res = await fetch("/api/encode", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        if (res.ok) {
            const data = await res.json();
            if (data.success) encResult = data.result;
        }
    } catch (err) {
        // Fallback for GitHub Pages / static hosting
    }

    if (!encResult) {
        encResult = clientSideEncode(payload);
    }

    state.encodingResult = encResult;
    state.encodedFrame = encResult.encoded_frame;
    state.transmittedFrame = state.encodedFrame;
    state.flippedIndices.clear();

    updateMetricsOnEncode();
    renderBitButtons();
    renderVisualizer(encResult, null);
    updateStatusBanner("ready", "READY ON CHANNEL", "Frame encoded. Modify bits to simulate channel noise or click 'Transmit & Verify'.");
    updateFlowLog(encResult, null);
    updatePipelineSteps(2);
}

function updateMetricsOnEncode() {
    document.getElementById("metricOrig").textContent = state.inputData;
    document.getElementById("metricTx").textContent = state.encodedFrame;
    document.getElementById("metricRx").textContent = state.transmittedFrame;
    document.getElementById("metricCorrected").textContent = "Pending Verification";
    document.getElementById("packetBitPreview").textContent = state.encodedFrame.substring(0, 8) + (state.encodedFrame.length > 8 ? "..." : "");
    document.getElementById("errorCountBadge").textContent = "0 Bits Flipped";
}

// Render Clickable Bit Buttons
function renderBitButtons() {
    const track = document.getElementById("bitsTrack");
    track.innerHTML = "";
    const frame = state.transmittedFrame;

    for (let i = 0; i < frame.length; i++) {
        const bitVal = frame[i];
        const btn = document.createElement("button");
        btn.className = `bit-btn ${bitVal === '1' ? 'bit-one' : ''}`;
        if (state.flippedIndices.has(i)) {
            btn.classList.add("flipped");
        }
        btn.textContent = bitVal;
        btn.title = `Bit index ${i} (Click to flip)`;
        btn.addEventListener("click", () => toggleBit(i));
        track.appendChild(btn);
    }
}

// Toggle Bit
function toggleBit(idx) {
    const chars = state.transmittedFrame.split("");
    chars[idx] = chars[idx] === '0' ? '1' : '0';
    state.transmittedFrame = chars.join("");

    if (state.flippedIndices.has(idx)) {
        state.flippedIndices.delete(idx);
    } else {
        state.flippedIndices.add(idx);
    }

    document.getElementById("errorCountBadge").textContent = `${state.flippedIndices.size} Bits Flipped`;
    document.getElementById("metricRx").textContent = state.transmittedFrame;
    renderBitButtons();
    updatePipelineSteps(4);
    
    const bitVal = state.transmittedFrame[idx];
    if (state.flippedIndices.has(idx)) {
        showToast("Channel Error Injected", `Bit ${idx} flipped to '${bitVal}' (Simulating noise)`, "warn", "⚡");
    } else {
        showToast("Bit Cleaned", `Bit ${idx} restored to '${bitVal}'`, "info", "✓");
    }
    
    triggerVerification();
}

function flashBtn(btn) {
    if (!btn) return;
    btn.style.transform = "scale(0.93)";
    btn.style.filter = "brightness(1.4)";
    setTimeout(() => {
        btn.style.transform = "";
        btn.style.filter = "";
    }, 220);
}

function injectRandomError(btn) {
    flashBtn(btn);
    if (!state.transmittedFrame) return;
    const idx = Math.floor(Math.random() * state.transmittedFrame.length);
    toggleBit(idx);
}

function injectBurstError(btn) {
    flashBtn(btn);
    if (!state.transmittedFrame) return;
    const n = state.transmittedFrame.length;
    const start = Math.max(0, Math.floor(Math.random() * (n - 2)));
    for (let i = start; i < Math.min(start + 3, n); i++) {
        const chars = state.transmittedFrame.split("");
        chars[i] = chars[i] === '0' ? '1' : '0';
        state.transmittedFrame = chars.join("");
        if (state.flippedIndices.has(i)) {
            state.flippedIndices.delete(i);
        } else {
            state.flippedIndices.add(i);
        }
    }
    document.getElementById("errorCountBadge").textContent = `${state.flippedIndices.size} Bits Flipped`;
    document.getElementById("metricRx").textContent = state.transmittedFrame;
    renderBitButtons();
    updatePipelineSteps(4);
    showToast("Burst Error Injected", "3 consecutive bits corrupted across channel", "warn", "⚡");
    triggerVerification();
}

function clearChannelErrors(btn) {
    flashBtn(btn);
    state.transmittedFrame = state.encodedFrame;
    state.flippedIndices.clear();
    document.getElementById("errorCountBadge").textContent = "0 Bits Flipped";
    document.getElementById("metricRx").textContent = state.transmittedFrame;
    renderBitButtons();
    updatePipelineSteps(4);
    showToast("Channel Cleaned", "All bit errors cleared. Transmitting pure frame.", "success", "✓");
    triggerVerification();
}

// -------------------------------------------------------------
// STEP 4: RECEIVER VERIFICATION & CORRECTION
// -------------------------------------------------------------
async function triggerVerification() {
    // Dynamic button clicked feedback
    const btnVer = document.getElementById("btnVerify");
    const txtVer = document.getElementById("btnVerifyText");
    if (btnVer) {
        btnVer.classList.add("btn-completed");
        if (txtVer) txtVer.innerHTML = "✓ Step 4: Transmitted & Verified at Receiver!";
        showToast("Step 4: Transmitted & Verified", "Receiver executed verification & error diagnosis!", "info", "🔍");
        setTimeout(() => {
            btnVer.classList.remove("btn-completed");
            if (txtVer) txtVer.innerHTML = "🔍 Step 4: Transmit & Verify at Receiver";
        }, 2200);
    }

    const chanMode = document.querySelector('input[name="chanMode"]:checked')?.value || "direct";
    if (chanMode === "ns2") {
        executeNs2Simulation();
    }

    const payload = {
        frame: state.transmittedFrame,
        original_data: state.inputData,
        technique: state.technique,
        parity_type: state.parityType,
        rows: state.p2dRows,
        cols: state.p2dCols,
        block_size: state.chkBlockSize,
        generator: state.crcGenerator
    };

    let verResult = null;
    try {
        const res = await fetch("/api/verify", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        if (res.ok) {
            const data = await res.json();
            if (data.success) verResult = data.result;
        }
    } catch (err) {
        // Fallback for GitHub Pages / static hosting
    }

    if (!verResult) {
        verResult = clientSideVerify(payload);
    }

    state.verificationResult = verResult;
    applyVerificationResults(verResult);
    renderVisualizer(state.encodingResult, verResult);
    updateFlowLog(state.encodingResult, verResult);
    updatePipelineSteps(5);
}

function applyVerificationResults(v) {
    const errDetected = v.error_detected;
    const canCorrect = v.can_correct;

    if (!errDetected) {
        updateStatusBanner("clean", "✓ DATA IS CORRECT (NO ERROR)", "Receiver verification passed successfully. No transmission errors detected.");
        document.getElementById("metricCorrected").textContent = "Not Needed (Clean)";
        document.getElementById("metricCorrected").style.color = "var(--color-success)";
    } else if (canCorrect) {
        const corrected = v.recovered_data || v.corrected_data || v.corrected_frame || "Corrected";
        updateStatusBanner("corrected", "★ ERROR DETECTED & CORRECTED!", `Single-bit error isolated. Recovered data: ${corrected}`);
        document.getElementById("metricCorrected").textContent = corrected;
        document.getElementById("metricCorrected").style.color = "#818cf8";
    } else {
        updateStatusBanner("error", "⚠ ERROR DETECTED!", "Transmission corrupted! Receiver detected bit discrepancy.");
        document.getElementById("metricCorrected").textContent = "Uncorrectable (Detection Only)";
        document.getElementById("metricCorrected").style.color = "var(--color-danger)";
    }

    document.getElementById("quickSummaryContent").textContent = v.explanation || "Verification complete.";
}

function updateStatusBanner(type, title, desc) {
    const banner = document.getElementById("statusBanner");
    banner.className = `status-banner ${type}`;
    document.getElementById("statusTitle").textContent = title;
    document.getElementById("statusDesc").textContent = desc;

    const icons = {
        ready: "●",
        clean: "✓",
        error: "⚠",
        corrected: "★"
    };
    document.getElementById("statusIcon").textContent = icons[type] || "●";
}

// -------------------------------------------------------------
// TAB 2: DETAILED ALGORITHM VISUALIZER
// -------------------------------------------------------------
function renderVisualizer(enc, v) {
    const container = document.getElementById("visAlgoContent");
    const tech = state.technique;
    const title = document.getElementById("visAlgoTitle");

    if (tech === "parity2d") {
        title.textContent = "2D Parity Matrix Grid Visualizer";
        render2DParityMatrix(enc, v, container);
    } else if (tech === "hamming") {
        title.textContent = "Hamming Code Codeword & Syndrome Bit Calculator";
        renderHammingVisualizer(enc, v, container);
    } else if (tech === "crc") {
        title.textContent = "Cyclic Redundancy Check (CRC) Modulo-2 XOR Division";
        renderCrcVisualizer(enc, v, container);
    } else if (tech === "checksum") {
        title.textContent = "Internet Checksum 1's Complement Block Addition";
        renderChecksumVisualizer(enc, v, container);
    } else {
        title.textContent = "1D Parity Check Redundancy Calculation";
        render1DParityVisualizer(enc, v, container);
    }
}

function render2DParityMatrix(enc, v, container) {
    const mat = (v && v.matrix) ? v.matrix : (enc.matrix || []);
    const rowP = (v && v.row_parities) ? v.row_parities : (enc.row_parities || []);
    const colP = (v && v.col_parities) ? v.col_parities : (enc.col_parities || []);
    const cornerP = (v && v.corner_parity) ? v.corner_parity : (enc.corner_parity || "0");
    const failedR = v ? (v.failed_rows || []) : [];
    const failedC = v ? (v.failed_cols || []) : [];

    let html = `
        <div class="matrix-container">
            <h4 style="margin-bottom: 8px; color: var(--color-cyan-hover);">2D Parity Data & Parity Coordinates</h4>
            <table class="matrix-grid-table">
                <thead>
                    <tr>
                        <th>Grid</th>
                        ${colP.map((_, c) => `<th>Col ${c}</th>`).join("")}
                        <th style="background: rgba(99, 102, 241, 0.2); color: #a5b4fc;">Row Parity</th>
                    </tr>
                </thead>
                <tbody>
    `;

    mat.forEach((row, r) => {
        const isRowFail = failedR.includes(r);
        html += `<tr><th>Row ${r} ${isRowFail ? '<span style="color:#f87171">⚠</span>' : ''}</th>`;
        row.forEach((cell, c) => {
            const isColFail = failedC.includes(c);
            let cellClass = "";
            if (isRowFail && isColFail) {
                cellClass = v && v.can_correct ? "corrected-cell" : "error-cell";
            }
            html += `<td class="${cellClass}">${cell}</td>`;
        });
        html += `<td class="parity-cell ${isRowFail ? 'error-cell' : ''}">${rowP[r]}</td></tr>`;
    });

    html += `
        <tr>
            <th style="background: rgba(99, 102, 241, 0.2); color: #a5b4fc;">Col Parity</th>
            ${colP.map((p, c) => `<td class="parity-cell ${failedC.includes(c) ? 'error-cell' : ''}">${p}</td>`).join("")}
            <td class="corner-cell">${cornerP}</td>
        </tr>
        </tbody>
        </table>
        </div>
        <div class="syndrome-box">
            <h4 style="color: #fff;">Mathematical Evaluation:</h4>
            <pre style="font-family: var(--font-mono); font-size: 0.82rem; color: var(--text-secondary);">${v ? v.explanation : enc.explanation}</pre>
        </div>
    `;
    container.innerHTML = html;
}

function renderHammingVisualizer(enc, v, container) {
    const n = enc.n || 7;
    const parityPos = new Set(enc.parity_positions || [1, 2, 4]);
    const frame = (v && v.received_frame) ? v.received_frame : enc.encoded_frame;
    const errPos = v ? v.error_pos : 0;

    let html = `
        <div class="syndrome-box">
            <h4 style="color: var(--color-cyan-hover);">Hamming Codeword Positions (n = ${n})</h4>
            <table class="hamming-table">
                <thead>
                    <tr>
                        <th>Bit Position (1-indexed)</th>
                        ${Array.from({length: n}, (_, i) => `<th>${i+1}</th>`).join("")}
                    </tr>
                    <tr>
                        <th>Designation</th>
                        ${Array.from({length: n}, (_, i) => {
                            const pos = i + 1;
                            return parityPos.has(pos) ? `<th style="color: var(--color-cyan-hover);">P${pos}</th>` : `<th>D${pos}</th>`;
                        }).join("")}
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="font-weight: 700; color: #fff;">Frame Bits</td>
                        ${Array.from({length: n}, (_, i) => {
                            const pos = i + 1;
                            const isErr = (errPos === pos);
                            const isParity = parityPos.has(pos);
                            const cls = isErr ? 'err-bit' : (isParity ? 'parity-bit' : 'data-bit');
                            return `<td class="${cls}">${frame[i] || '_'}</td>`;
                        }).join("")}
                    </tr>
                </tbody>
            </table>
        </div>
        <div class="syndrome-box">
            <h4 style="color: #fff;">Syndrome Calculation & Single-Bit Correction:</h4>
            <pre style="font-family: var(--font-mono); font-size: 0.82rem; color: var(--text-secondary); line-height: 1.6;">${v ? v.explanation : enc.explanation}</pre>
        </div>
    `;
    container.innerHTML = html;
}

function renderCrcVisualizer(enc, v, container) {
    let stepsHtml = "";
    if (enc.steps) {
        stepsHtml = enc.steps.slice(0, 15).map((s, idx) => 
            `Step ${idx+1}: Dividend Window = ${s.window} | Divisor = ${s.divisor_applied} ➔ XOR = ${s.xor_result} | Bring down: ${s.brought_down}`
        ).join("\n");
        if (enc.steps.length > 15) {
            stepsHtml += `\n... [${enc.steps.length - 15} additional polynomial division steps computed]`;
        }
    }

    let html = `
        <div class="syndrome-box">
            <h4 style="color: var(--color-cyan-hover);">Transmitter Modulo-2 Division Steps</h4>
            <pre class="crc-steps-box">${stepsHtml || enc.explanation}</pre>
        </div>
        <div class="syndrome-box">
            <h4 style="color: #fff;">Receiver Verification:</h4>
            <pre style="font-family: var(--font-mono); font-size: 0.82rem; color: var(--text-secondary);">${v ? v.explanation : "Awaiting transmission verification..."}</pre>
        </div>
    `;
    container.innerHTML = html;
}

function renderChecksumVisualizer(enc, v, container) {
    let html = `
        <div class="syndrome-box">
            <h4 style="color: var(--color-cyan-hover);">1's Complement Block Segmentation & Addition Steps</h4>
            <pre style="font-family: var(--font-mono); font-size: 0.82rem; color: var(--text-secondary); line-height: 1.6;">${enc.explanation}</pre>
        </div>
        <div class="syndrome-box">
            <h4 style="color: #fff;">Receiver Checksum Sum & Verification:</h4>
            <pre style="font-family: var(--font-mono); font-size: 0.82rem; color: var(--text-secondary); line-height: 1.6;">${v ? v.explanation : "Awaiting transmission verification..."}</pre>
        </div>
    `;
    container.innerHTML = html;
}

function render1DParityVisualizer(enc, v, container) {
    let html = `
        <div class="syndrome-box">
            <h4 style="color: var(--color-cyan-hover);">1D Parity Bit Redundancy Formulation</h4>
            <pre style="font-family: var(--font-mono); font-size: 0.82rem; color: var(--text-secondary); line-height: 1.6;">${enc.explanation}</pre>
        </div>
        <div class="syndrome-box">
            <h4 style="color: #fff;">Receiver Verification:</h4>
            <pre style="font-family: var(--font-mono); font-size: 0.82rem; color: var(--text-secondary); line-height: 1.6;">${v ? v.explanation : "Awaiting transmission verification..."}</pre>
        </div>
    `;
    container.innerHTML = html;
}

// -------------------------------------------------------------
// TAB 3: NS-2 DISCRETE EVENT SIMULATION
// -------------------------------------------------------------
function updateNs2SliderVal(val) {
    document.getElementById("ns2SliderVal").textContent = `${parseFloat(val).toFixed(2)} (${Math.round(val * 100)}%)`;
}

async function executeNs2Simulation() {
    const btn = document.getElementById("btnExecuteNs2");
    btn.disabled = true;
    btn.innerHTML = `<span>⏳ Simulating in NS-2 (WSL)...</span>`;

    const errRate = parseFloat(document.getElementById("ns2ErrRate").value) || 0.2;
    const numPkts = parseInt(document.getElementById("ns2PacketCount").value) || 15;
    const frame = state.transmittedFrame || "11010010";

    let simResult = null;
    try {
        const res = await fetch("/api/run-ns2", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                frame: frame,
                error_rate: errRate,
                num_packets: numPkts
            })
        });
        if (res.ok) {
            const data = await res.json();
            if (data.success) simResult = data.result;
        }
    } catch (err) {
        // Fallback for GitHub Pages / static hosting
    }

    if (!simResult) {
        simResult = clientSideNs2Sim(frame, errRate, numPkts);
    }

    applyNs2Results(simResult);
    btn.disabled = false;
    btn.innerHTML = `<span>▶ Run Real NS-2 Simulation</span>`;
}

function applyNs2Results(sim) {
    document.getElementById("ns2StatSent").textContent = sim.total_sent;
    document.getElementById("ns2StatDropped").textContent = sim.total_dropped;
    document.getElementById("ns2StatReceived").textContent = sim.total_received;
    document.getElementById("ns2StatLoss").textContent = `${sim.loss_percentage}%`;
    document.getElementById("traceCountBadge").textContent = `${(sim.events || []).length} Trace Events`;

    const tbody = document.getElementById("ns2TraceTableBody");
    tbody.innerHTML = "";

    const events = sim.events || [];
    if (events.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6" class="text-center text-muted">No events recorded.</td></tr>`;
        return;
    }

    events.forEach(ev => {
        const tr = document.createElement("tr");
        let badgeClass = "enq";
        let actionLabel = "ENQUEUE";

        if (ev.action === "d") {
            badgeClass = "drop";
            actionLabel = "CORRUPTED (DROP)";
        } else if (ev.action === "r") {
            badgeClass = "recv";
            actionLabel = "RECEIVED";
        } else if (ev.action === "-") {
            badgeClass = "deq";
            actionLabel = "DEQUEUE";
        }

        tr.innerHTML = `
            <td><span class="event-badge ${badgeClass}">${actionLabel}</span></td>
            <td>${ev.time}</td>
            <td>Node ${ev.src}</td>
            <td>Node ${ev.dst}</td>
            <td>#${ev.pkt_id}</td>
            <td>${ev.desc}</td>
        `;
        tbody.appendChild(tr);
    });
}

// -------------------------------------------------------------
// TAB 4: ARCHITECTURE FLOW LOG
// -------------------------------------------------------------
function updateFlowLog(enc, v) {
    const logBox = document.getElementById("flowLogContent");
    const techName = state.technique.toUpperCase();

    let text = `========================================================================\n`;
    text += `   SYSTEM ARCHITECTURE PIPELINE - EXECUTION LOG\n`;
    text += `========================================================================\n\n`;
    text += `1. [Input Message Data]: ${state.inputData} (${state.inputData.length} bits)\n`;
    text += `2. [Selected Technique]: ${techName}\n`;
    text += `3. [Encoding / Redundancy]: ${state.encodedFrame}\n`;
    text += `4. [Transmitter]: Encoded frame prepared for physical link transmission\n`;
    
    if (state.flippedIndices.size > 0) {
        text += `5. [Error Injection]: Injected bit flip(s) at 0-indexed position(s): [${Array.from(state.flippedIndices).join(", ")}]\n`;
        text += `   Corrupted Frame on Channel: ${state.transmittedFrame}\n`;
    } else {
        text += `5. [Error Injection]: None (Clean channel transmission)\n`;
        text += `   Transmitted Frame on Channel: ${state.transmittedFrame}\n`;
    }

    text += `\n6. [Receiver Verification]:\n`;
    if (v) {
        text += `${v.explanation}\n\n`;
        text += `7. [Decision: Error Detected?]: ${v.error_detected ? "YES (Corrupted)" : "NO (Valid Frame)"}\n`;
        if (v.can_correct) {
            text += `8. [Error Correction]: Single-bit error successfully isolated and corrected.\n`;
            text += `   Recovered Message: ${v.recovered_data || v.corrected_data || "-"}\n`;
        }
    } else {
        text += `Awaiting transmission verification.\n`;
    }

    text += `9. [Display Result]: Final status rendered to application sink.\n`;
    logBox.textContent = text;
}

function copyFlowLog() {
    const text = document.getElementById("flowLogContent").textContent;
    navigator.clipboard.writeText(text).then(() => {
        alert("Architecture Flow Log copied to clipboard!");
    });
}

// ======================================================================
// PURE JAVASCRIPT ALGORITHM ENGINE (STANDALONE / GITHUB PAGES MODE)
// ======================================================================

function clientSideEncode(payload) {
    const data = payload.data || "11010010";
    const tech = payload.technique || "parity";
    const ptype = payload.parity_type || "even";

    if (tech === "parity") {
        const ones = (data.match(/1/g) || []).length;
        const pBit = (ptype === "even") ? (ones % 2 === 0 ? "0" : "1") : (ones % 2 === 0 ? "1" : "0");
        const frame = data + pBit;
        const explanation = `Original Data: ${data} (Length: ${data.length} bits)\nNumber of 1s in data: ${ones}\nParity Scheme: ${ptype.toUpperCase()} Parity\nParity Bit calculated: '${pBit}'\nTransmitted Frame (Data + Parity): ${data} | ${pBit} = ${frame}`;
        return { original_data: data, parity_type: ptype, parity_bit: pBit, encoded_frame: frame, explanation };
    }

    if (tech === "parity2d") {
        const rows = parseInt(payload.rows) || 3;
        const cols = parseInt(payload.cols) || 4;
        const total = rows * cols;
        const padded = data.padEnd(total, '0').slice(0, total);
        const matrix = [];
        for (let r = 0; r < rows; r++) {
            matrix.push(padded.slice(r * cols, (r + 1) * cols).split(''));
        }
        const rowP = matrix.map(row => {
            const o = row.filter(b => b === '1').length;
            return (ptype === 'even') ? (o % 2 === 0 ? '0' : '1') : (o % 2 === 0 ? '1' : '0');
        });
        const colP = [];
        for (let c = 0; c < cols; c++) {
            let o = 0;
            for (let r = 0; r < rows; r++) if (matrix[r][c] === '1') o++;
            colP.push((ptype === 'even') ? (o % 2 === 0 ? '0' : '1') : (o % 2 === 0 ? '1' : '0'));
        }
        const oRowP = rowP.filter(b => b === '1').length;
        const cornerP = (ptype === 'even') ? (oRowP % 2 === 0 ? '0' : '1') : (oRowP % 2 === 0 ? '1' : '0');
        let frame = "";
        for (let r = 0; r < rows; r++) frame += matrix[r].join('') + rowP[r];
        frame += colP.join('') + cornerP;
        const explanation = `Grid Size: ${rows} rows x ${cols} cols (Total data bits: ${total})\nPadded Data: ${padded}\nParity Type: ${ptype.toUpperCase()} Parity\nCalculated Row Parities: ${rowP.join(', ')}\nCalculated Column Parities: ${colP.join(', ')}\nCorner Parity: ${cornerP}\nTotal Encoded Frame Length: ${frame.length} bits`;
        return { original_data: data, rows, cols, matrix, row_parities: rowP, col_parities: colP, corner_parity: cornerP, encoded_frame: frame, explanation };
    }

    if (tech === "hamming") {
        const m = data.length;
        let r = 1;
        while (Math.pow(2, r) < m + r + 1) r++;
        const n = m + r;
        const code = Array(n + 1).fill('_');
        const parityPositions = [];
        for (let i = 0; i < r; i++) parityPositions.push(Math.pow(2, i));
        let j = 0;
        for (let i = 1; i <= n; i++) {
            if (!parityPositions.includes(i)) code[i] = data[j++];
        }
        for (let pos of parityPositions) {
            let ones = 0;
            for (let i = 1; i <= n; i++) {
                if (i !== pos && (i & pos) !== 0 && code[i] === '1') ones++;
            }
            code[pos] = (ones % 2 === 0) ? '0' : '1';
        }
        const frame = code.slice(1).join('');
        const explanation = `Data Bits (m = ${m}): ${data}\nParity Bits needed (r = ${r}) such that 2^r >= m + r + 1\nTotal Codeword Length (n = ${n}): ${n} bits\nParity Bit Positions: ${parityPositions.join(', ')}\nEncoded Hamming Code: ${frame}`;
        return { original_data: data, m, r, n, parity_positions: parityPositions, encoded_frame: frame, explanation };
    }

    if (tech === "checksum") {
        const blockSz = parseInt(payload.block_size) || 8;
        const rem = data.length % blockSz;
        const padded = (rem !== 0) ? data + '0'.repeat(blockSz - rem) : data;
        const blocks = [];
        for (let i = 0; i < padded.length; i += blockSz) blocks.push(padded.slice(i, i + blockSz));
        const maxVal = (1 << blockSz) - 1;
        let sum = 0;
        const steps = [];
        blocks.forEach((bStr, idx) => {
            const val = parseInt(bStr, 2);
            let total = sum + val;
            while (total > maxVal) total = (total & maxVal) + (total >> blockSz);
            sum = total;
            steps.push(`Block ${idx+1} (${bStr}): Sum so far = ${sum.toString(2).padStart(blockSz, '0')} (${sum})`);
        });
        const chkVal = maxVal ^ sum;
        const chkStr = chkVal.toString(2).padStart(blockSz, '0');
        const frame = padded + chkStr;
        const explanation = `Original Data: ${data} (Block Size: ${blockSz} bits)\nPadded Data: ${padded} (Divided into ${blocks.length} blocks)\nBlocks: ${blocks.join(' | ')}\n1's Complement Addition Steps:\n  ${steps.join('\n  ')}\nFinal 1's Complement Sum: ${sum.toString(2).padStart(blockSz, '0')} (${sum})\nChecksum (Bitwise Inversion): ${chkStr} (${chkVal})\nTransmitted Frame: ${padded} | ${chkStr} = ${frame}`;
        return { original_data: data, padded_data: padded, block_size: blockSz, blocks, checksum_bin: chkStr, encoded_frame: frame, explanation };
    }

    if (tech === "crc") {
        let gen = payload.generator || "10011";
        if (!gen || !/^[01]+$/.test(gen)) gen = "10011";
        const k = gen.length - 1;
        const augmented = data + '0'.repeat(k);
        const { remainder, steps } = clientSideMod2Div(augmented, gen);
        const frame = data + remainder;
        const explanation = `Original Data (M): ${data} (Length: ${data.length})\nGenerator Polynomial (G): ${gen} (Degree: ${k})\nAugmented Data: ${augmented}\nCalculated Remainder / CRC Checksum: ${remainder}\nTransmitted Frame: ${data} | ${remainder} = ${frame}`;
        return { original_data: data, generator: gen, degree: k, augmented_data: augmented, remainder, encoded_frame: frame, steps, explanation };
    }
}

function clientSideMod2Div(dividend, divisor) {
    const divLen = divisor.length;
    let cur = dividend.slice(0, divLen).split('');
    let cursor = divLen;
    const steps = [];
    while (true) {
        const curStr = cur.join('');
        const applied = (cur[0] === '1') ? divisor : '0'.repeat(divLen);
        let res = "";
        for (let i = 0; i < divLen; i++) res += (curStr[i] === applied[i] ? '0' : '1');
        const nextVal = res.slice(1).split('');
        const brought = (cursor < dividend.length) ? dividend[cursor] : "None";
        steps.push({ window: curStr, divisor_applied: applied, xor_result: res, brought_down: brought });
        if (cursor < dividend.length) {
            nextVal.push(dividend[cursor++]);
            cur = nextVal;
        } else {
            return { remainder: res.slice(1), steps };
        }
    }
}

function clientSideVerify(payload) {
    const frame = payload.frame || "";
    const tech = payload.technique || "parity";
    const ptype = payload.parity_type || "even";
    const origData = payload.original_data || "";

    if (tech === "parity") {
        if (frame.length < 2) {
            return { error_detected: true, can_correct: false, status: "Frame too short", explanation: "Frame too short" };
        }
        const ones = (frame.match(/1/g) || []).length;
        const err = (ptype === 'even') ? (ones % 2 !== 0) : (ones % 2 === 0);
        const rxData = frame.slice(0, -1);
        const rxParity = frame.slice(-1);
        const expParity = (rxData.match(/1/g) || []).length % 2 === 0 ? (ptype === 'even' ? '0' : '1') : (ptype === 'even' ? '1' : '0');
        const explanation = `Received Frame: ${frame}\nExtracted Data: ${rxData}, Received Parity Bit: ${rxParity}\nTotal 1s in Frame: ${ones}\nExpected Parity: '${expParity}'\nParity Condition (${ptype.toUpperCase()}): Total 1s is ${ones % 2 === 0 ? 'EVEN' : 'ODD'}\nResult: ${err ? 'ERROR DETECTED! Frame corrupted.' : 'NO ERROR DETECTED. Frame is valid.'}`;
        return { received_data: rxData, received_parity: rxParity, expected_parity: expParity, error_detected: err, status: err ? "Error Detected" : "Data is Correct (No Error)", can_correct: false, explanation };
    }

    if (tech === "parity2d") {
        const rows = parseInt(payload.rows) || 3;
        const cols = parseInt(payload.cols) || 4;
        const expectedLen = (rows + 1) * (cols + 1);
        if (frame.length !== expectedLen) {
            return { error_detected: true, can_correct: false, status: "Length Mismatch", explanation: "Frame length mismatch", matrix: [], row_parities: [], col_parities: [] };
        }
        const stride = cols + 1;
        const rxMat = [];
        const rxRowP = [];
        for (let r = 0; r < rows; r++) {
            const chunk = frame.slice(r * stride, (r + 1) * stride);
            rxMat.push(chunk.slice(0, cols).split(''));
            rxRowP.push(chunk[cols]);
        }
        const lastRow = frame.slice(rows * stride);
        const rxColP = lastRow.slice(0, cols).split('');
        const rxCornerP = lastRow[cols];

        const failedRows = [];
        for (let r = 0; r < rows; r++) {
            const totalOnes = (rxMat[r].join('') + rxRowP[r]).match(/1/g)?.length || 0;
            if ((ptype === 'even' && totalOnes % 2 !== 0) || (ptype === 'odd' && totalOnes % 2 === 0)) failedRows.push(r);
        }
        const failedCols = [];
        for (let c = 0; c < cols; c++) {
            let colStr = "";
            for (let r = 0; r < rows; r++) colStr += rxMat[r][c];
            colStr += rxColP[c];
            const totalOnes = colStr.match(/1/g)?.length || 0;
            if ((ptype === 'even' && totalOnes % 2 !== 0) || (ptype === 'odd' && totalOnes % 2 === 0)) failedCols.push(c);
        }

        const errDetected = failedRows.length > 0 || failedCols.length > 0;
        let canCorrect = false;
        let correctedData = "";
        let explanation = "";
        const correctedMat = rxMat.map(row => [...row]);

        if (failedRows.length === 1 && failedCols.length === 1) {
            canCorrect = true;
            const errR = failedRows[0];
            const errC = failedCols[0];
            correctedMat[errR][errC] = correctedMat[errR][errC] === '0' ? '1' : '0';
            correctedData = correctedMat.map(r => r.join('')).join('');
            explanation = `Single-bit error isolated at Row ${errR + 1}, Col ${errC + 1}. Bit flipped and corrected successfully!`;
        } else if (errDetected) {
            explanation = `Multiple errors detected (Failed Rows: ${failedRows}, Failed Cols: ${failedCols}). Cannot uniquely pinpoint single bit.`;
        } else {
            explanation = "All row and column parities verified successfully. No error.";
        }

        return {
            matrix: rxMat,
            row_parities: rxRowP,
            col_parities: rxColP,
            corner_parity: rxCornerP,
            failed_rows: failedRows,
            failed_cols: failedCols,
            error_detected: errDetected,
            can_correct: canCorrect,
            corrected_data: canCorrect ? correctedData : rxMat.map(r => r.join('')).join(''),
            status: canCorrect ? "Error Corrected" : (errDetected ? "Error Detected" : "Data is Correct (No Error)"),
            explanation
        };
    }

    if (tech === "hamming") {
        const n = frame.length;
        if (n < 3) return { error_detected: true, can_correct: false, status: "Frame too short", explanation: "Frame too short" };
        let r = 0;
        while (Math.pow(2, r) <= n) r++;
        const code = ['_'].concat(frame.split(''));
        let errorPos = 0;
        const details = [];
        const parityPos = [];
        for (let pIdx = 0; pIdx < r; pIdx++) {
            const pos = Math.pow(2, pIdx);
            parityPos.push(pos);
            let ones = 0;
            const covered = [];
            for (let i = 1; i <= n; i++) {
                if ((i & pos) !== 0) {
                    covered.push(i);
                    if (code[i] === '1') ones++;
                }
            }
            const sVal = (ones % 2 !== 0) ? 1 : 0;
            if (sVal === 1) errorPos += pos;
            details.push(`S${pos} (covers [${covered.join(', ')}]) = ${sVal === 1 ? '1 (Parity Error)' : '0 (OK)'}`);
        }

        const errDetected = (errorPos !== 0);
        let canCorrect = false;
        const correctedCode = [...code];
        let correctedFrame = frame;

        if (errDetected && errorPos <= n) {
            canCorrect = true;
            correctedCode[errorPos] = (code[errorPos] === '0') ? '1' : '0';
            correctedFrame = correctedCode.slice(1).join('');
        }

        const recoveredData = [];
        for (let i = 1; i <= n; i++) {
            if (!parityPos.includes(i)) recoveredData.push(correctedCode[i]);
        }
        const recoveredStr = recoveredData.join('');

        let explanation = `Received Codeword: ${frame} (Length: ${n})\nSyndrome Evaluation:\n  ${details.join('\n  ')}\nSyndrome Decimal Value (Error Position): ${errorPos}\n`;
        if (errDetected && canCorrect) {
            explanation += `==> Single-Bit Error Detected at Position ${errorPos}!\n==> Bit at Position ${errorPos} flipped from '${code[errorPos]}' to '${correctedCode[errorPos]}'.\nCorrected Codeword: ${correctedFrame}\nRecovered Message Bits: ${recoveredStr}`;
        } else if (errDetected) {
            explanation += "==> Multiple errors detected. Unable to correct.";
        } else {
            explanation += `==> Syndrome = 0. All parity checks passed. Data received correctly!\nRecovered Message Bits: ${recoveredStr}`;
        }

        return {
            received_frame: frame,
            n, r, error_pos: errorPos,
            error_detected: errDetected,
            can_correct: canCorrect,
            corrected_frame: correctedFrame,
            recovered_data: recoveredStr,
            status: canCorrect ? "Error Detected & Corrected" : (errDetected ? "Error Detected" : "Data is Correct (No Error)"),
            explanation
        };
    }

    if (tech === "checksum") {
        const blockSz = parseInt(payload.block_size) || 8;
        if (frame.length < blockSz * 2) {
            return { error_detected: true, can_correct: false, status: "Frame too short", explanation: "Frame too short" };
        }
        const rem = frame.length % blockSz;
        const padded = (rem !== 0) ? frame + '0'.repeat(blockSz - rem) : frame;
        const blocks = [];
        for (let i = 0; i < padded.length; i += blockSz) blocks.push(padded.slice(i, i + blockSz));
        const maxVal = (1 << blockSz) - 1;
        let sum = 0;
        const steps = [];
        blocks.forEach((bStr, idx) => {
            const val = parseInt(bStr, 2);
            let total = sum + val;
            while (total > maxVal) total = (total & maxVal) + (total >> blockSz);
            sum = total;
            const isChk = (idx === blocks.length - 1);
            steps.push(`Add ${isChk ? 'Checksum' : 'Data Block ' + (idx + 1)} (${bStr}) -> Running Sum: ${sum.toString(2).padStart(blockSz, '0')}`);
        });
        const comp = maxVal ^ sum;
        const errDetected = (comp !== 0);
        const explanation = `Received Frame: ${frame}\nReceiver Addition Steps:\n  ${steps.join('\n  ')}\nReceiver Total Sum: ${sum.toString(2).padStart(blockSz, '0')} (${sum})\nComplemented Result: ${comp.toString(2).padStart(blockSz, '0')} (${comp})\nStatus: ${errDetected ? 'ERROR DETECTED! Non-zero complemented sum.' : 'DATA IS CORRECT! Complemented sum is all 0s.'}`;
        return { received_frame: frame, error_detected: errDetected, status: errDetected ? "Error Detected" : "Data is Correct (No Error)", can_correct: false, explanation };
    }

    if (tech === "crc") {
        let gen = payload.generator || "10011";
        const k = gen.length - 1;
        if (frame.length <= k) {
            return { error_detected: true, can_correct: false, status: "Frame too short", explanation: "Frame too short" };
        }
        const { remainder, steps } = clientSideMod2Div(frame, gen);
        const errDetected = remainder.includes('1');
        const rxData = frame.slice(0, -k);
        const rxCrc = frame.slice(-k);
        const explanation = `Received Codeword: ${frame}\nExtracted Data: ${rxData}, Extracted CRC: ${rxCrc}\nGenerator Polynomial: ${gen}\nReceiver Division Remainder (Syndrome): ${remainder}\nCheck: Remainder is ${errDetected ? 'NON-ZERO (Error)' : 'ALL ZEROS (Valid)'}\nStatus: ${errDetected ? 'ERROR DETECTED! Data corrupted during transmission.' : 'DATA IS CORRECT! (No Error)'}`;
        return { received_frame: frame, received_data: rxData, received_crc: rxCrc, generator: gen, remainder, error_detected: errDetected, status: errDetected ? "Error Detected" : "Data is Correct (No Error)", can_correct: false, steps, explanation };
    }
}

function clientSideNs2Sim(frame, errRate, numPkts) {
    const sent = numPkts;
    let dropped = 0;
    let received = 0;
    const events = [];

    for (let i = 0; i < numPkts; i++) {
        const t = (0.1 + (i * 0.05)).toFixed(3);
        events.push({ action: "+", time: t, src: "0", dst: "1", pkt_id: String(i), desc: `Packet ${i} queued at Transmitter (Node 0)` });
        events.push({ action: "-", time: t, src: "0", dst: "1", pkt_id: String(i), desc: `Packet ${i} transmitted onto communication link` });

        if (Math.random() < errRate) {
            dropped++;
            const tDrop = (parseFloat(t) + 0.005).toFixed(3);
            events.push({ action: "d", time: tDrop, src: "0", dst: "1", pkt_id: String(i), desc: `Packet ${i} CORRUPTED/DROPPED by ErrorModel on channel` });
        } else {
            received++;
            const tRecv = (parseFloat(t) + 0.010).toFixed(3);
            events.push({ action: "r", time: tRecv, src: "0", dst: "1", pkt_id: String(i), desc: `Packet ${i} successfully received at Receiver (Node 1)` });
        }
    }

    const lossRatio = ((dropped / Math.max(1, (received + dropped))) * 100.0).toFixed(2);
    return {
        success: true,
        used_fallback: true,
        trace_file: "gui_run.tr",
        nam_file: "gui_run.nam",
        total_sent: sent,
        total_received: received,
        total_dropped: dropped,
        loss_percentage: parseFloat(lossRatio),
        events
    };
}

