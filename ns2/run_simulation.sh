#!/bin/bash
# ======================================================================
# Shell runner for NS-2 Error Simulation
# ======================================================================

echo "=========================================================="
echo " Running NS-2 Channel Error Simulation"
echo "=========================================================="

PKT_SIZE=${1:-64}
ERR_RATE=${2:-0.2}
NUM_PKTS=${3:-20}
PREFIX=${4:-"manual_run"}

echo "Packet Size: $PKT_SIZE bytes"
echo "Error Rate:  $ERR_RATE (20% bit/packet drop probability)"
echo "Packets:     $NUM_PKTS"
echo "Prefix:      $PREFIX"
echo "----------------------------------------------------------"

ns network_error_sim.tcl $PKT_SIZE $ERR_RATE $NUM_PKTS $PREFIX

if [ $? -eq 0 ]; then
    echo "Simulation completed successfully!"
    echo "Generated Trace file: $PREFIX.tr"
    echo "Generated NAM file:   $PREFIX.nam"
    
    echo ""
    echo "Trace Summary:"
    echo "Packets Enqueued (+): $(grep -c "^+" $PREFIX.tr)"
    echo "Packets Dropped (d):  $(grep -c "^d" $PREFIX.tr)"
    echo "Packets Received (r): $(grep -c "^r" $PREFIX.tr)"
    
    if command -v nam &> /dev/null && [ -n "$DISPLAY" ]; then
        echo "Launching Network Animator (NAM)..."
        nam $PREFIX.nam &
    fi
else
    echo "NS-2 Simulation failed."
fi
