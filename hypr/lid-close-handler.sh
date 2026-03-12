#!/bin/bash
# Handle lid close - suspend only if no external monitors are active

# Disable laptop display
hyprctl keyword monitor "eDP-1, disable"

# Check if any external monitors are active (not eDP-1 and not disabled)
EXTERNAL_MONITORS=$(hyprctl monitors -j | jq -r '.[] | select(.name != "eDP-1") | .name' | wc -l)

if [ "$EXTERNAL_MONITORS" -gt 0 ]; then
    # External monitor(s) connected - clamshell mode, don't suspend
    notify-send -u low "Clamshell Mode" "External monitor active. Laptop screen disabled." -i video-display
else
    # No external monitors - suspend the system
    systemctl suspend
fi
