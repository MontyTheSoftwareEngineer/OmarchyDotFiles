#!/bin/bash

# Helper script to change sprite animation
# Usage: sprite-changer.sh [sprite_name]

CACHE_DIR="$HOME/.cache/waybar-sprites"
STATE_FILE="$CACHE_DIR/current_sprite.state"

# Remove state file to force a new random sprite selection
rm -f "$STATE_FILE"

# If a specific sprite is provided, you can extend this script to set it
if [ -n "$1" ]; then
    ANIMATIONS_DIR="$HOME/.config/waybar/animations"
    SPRITE="$ANIMATIONS_DIR/$1.png"
    
    if [ -f "$SPRITE" ]; then
        echo "Switching to $1 animation..."
    else
        echo "Sprite $1 not found. Available sprites:"
        ls -1 "$ANIMATIONS_DIR" | sed 's/.png$//'
        exit 1
    fi
fi

# Find waybar process and send signal to refresh
WAYBAR_PID=$(pgrep -x waybar)
if [ -n "$WAYBAR_PID" ]; then
    kill -SIGRTMIN+10 "$WAYBAR_PID"
    echo "Waybar refreshed with new sprite"
else
    echo "Waybar not running"
fi
