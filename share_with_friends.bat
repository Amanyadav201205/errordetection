@echo off
title Share Simulator With Friends
echo ======================================================================
echo Share Network Simulator With Friends
echo ======================================================================
echo.
echo OPTION 1: IF YOUR FRIEND IS ON THE SAME WI-FI / MOBILE HOTSPOT:
echo   Tell your friend to open this in their phone or laptop browser:
echo.
echo   http://172.16.213.102:5000
echo.
echo ======================================================================
echo OPTION 2: IF YOUR FRIEND IS ON DIFFERENT WI-FI / MOBILE DATA:
echo Generating a secure public link via localtunnel...
echo (Send the URL printed below to your friend)
echo ======================================================================
echo.
npx -y localtunnel --port 5000
pause
