#!/bin/bash

# Explicitly tell Xlib not to use the Xauthority file
export XAUTHORITY=/dev/null

# Start Xvfb in the background
Xvfb :99 -screen 0 1024x768x24 -ac &

# Wait for Xvfb to be ready
sleep 2

# Set the display environment variable
export DISPLAY=:99

# Start Fluxbox (the window manager) in the background
fluxbox &> /dev/null &

# Start xterm (the terminal emulator) and your Quart app
exec hypercorn --bind 0.0.0.0:8000 main:app &
exec xterm -geometry 80x24+10+10 &

# Keep the script running to prevent the container from exiting
tail -f /dev/null
