#!/bin/bash
# Handle lid open - properly wake display and enable laptop screen

# Give the system a moment to fully wake from suspend
sleep 0.5

# Force display power on
hyprctl dispatch dpms on

# Small delay to let display controller wake up
sleep 0.3

# Re-enable laptop monitor
hyprctl keyword monitor "eDP-1, preferred, auto, 1"

# Ensure display is on again
sleep 0.2
hyprctl dispatch dpms on

# Restore brightness
brightnessctl -r 2>/dev/null

notify-send -u low "Laptop Mode" "Laptop screen enabled." -i computer
