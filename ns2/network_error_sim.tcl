# ======================================================================
# Network Simulator 2 (NS-2) - Error Detection and Channel Simulation
# Computer Networks Lab Project
# Project: Interactive Network Error Detection and Correction Simulator
# ======================================================================

set pkt_size 64
set err_rate 0.2
set num_pkts 20
set prefix "ns2_sim"
set technique "All_Techniques"
set codeword "11010010"

if {[llength $argv] > 0} { set pkt_size  [lindex $argv 0] }
if {[llength $argv] > 1} { set err_rate   [lindex $argv 1] }
if {[llength $argv] > 2} { set num_pkts   [lindex $argv 2] }
if {[llength $argv] > 3} { set prefix     [lindex $argv 3] }
if {[llength $argv] > 4} { set technique  [lindex $argv 4] }
if {[llength $argv] > 5} { set codeword   [lindex $argv 5] }

# Initialize NS Simulator
set ns [new Simulator]

# Set colors for NAM
$ns color 1 Blue
$ns color 2 Red

# Open Trace and NAM files
set tracefile [open "$prefix.tr" w]
$ns trace-all $tracefile

set namfile [open "$prefix.nam" w]
$ns namtrace-all $namfile

# Define Finish procedure
proc finish {} {
    global ns tracefile namfile prefix technique codeword
    $ns flush-trace
    close $tracefile
    close $namfile
    puts "NS2_SIMULATION_COMPLETED: $prefix.tr"
    puts "NS2_DATA_LINK_TECHNIQUE: $technique"
    puts "NS2_CODEWORD_PAYLOAD: $codeword"
    exit 0
}

# Create Transmitter (n0) and Receiver (n1) Nodes
set n0 [$ns node]
set n1 [$ns node]

# Configure Node Labels for NAM Visualization
$n0 label "Transmitter (Tx)"
$n0 color "blue"
$n1 label "Receiver (Rx)"
$n1 color "darkgreen"

# Create Duplex Link: 2Mb bandwidth, 10ms delay, DropTail queue
$ns duplex-link $n0 $n1 2Mb 10ms DropTail
$ns duplex-link-op $n0 $n1 orient right
$ns duplex-link-op $n0 $n1 queuePos 0.5

# Insert Error Model into the Communication Channel (Link n0 -> n1)
set loss_module [new ErrorModel]
$loss_module set rate_ $err_rate
$loss_module unit pkt
$loss_module ranvar [new RandomVariable/Uniform]
$loss_module drop-target [new Agent/Null]

# Apply loss model to link
$ns lossmodel $loss_module $n0 $n1

# Setup UDP Agent at Transmitter
set udp [new Agent/UDP]
$udp set fid_ 1
$ns attach-agent $n0 $udp

# Setup Null Agent at Receiver
set null [new Agent/Null]
$ns attach-agent $n1 $null

# Connect Transmitter and Receiver Agents
$ns connect $udp $null

# Setup Traffic Generator (CBR - Constant Bit Rate)
set cbr [new Application/Traffic/CBR]
$cbr set packetSize_ $pkt_size
$cbr set interval_ 0.05
$cbr set random_ 1
$cbr attach-agent $udp

# Schedule Events
set sim_duration [expr 0.1 + ($num_pkts * 0.05)]
$ns at 0.1 "$cbr start"
$ns at $sim_duration "$cbr stop"
$ns at [expr $sim_duration + 0.2] "finish"

# Run Simulation
$ns run
