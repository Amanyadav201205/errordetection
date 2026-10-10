@echo off
title Interactive Network Error Detection and Correction Simulator
echo ======================================================================
echo Interactive Network Error Detection and Correction Simulator
echo Course: BCSE308P - Computer Networks Lab
echo Team: Aman Kumar Yadav, Pratik Bharadbhunje, Devrishi Gadia
echo ======================================================================
echo Starting Application...
python main.py
if errorlevel 1 (
    echo.
    echo An error occurred while running the simulator.
    pause
)
