#!/bin/bash
# Check lid state on Hyprland startup and disable eDP-1 if lid is closed

sleep 1  # Give Hyprland a moment to fully initialize

LID_STATE=$(cat /proc/acpi/button/lid/*/state 2>/dev/null | awk '{print $2}')

if [ "$LID_STATE" = "closed" ]; then
    hyprctl keyword monitor "eDP-1, disable"
fi
