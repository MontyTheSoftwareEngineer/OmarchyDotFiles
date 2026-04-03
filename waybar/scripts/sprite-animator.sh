#!/bin/bash

ANIMATIONS_DIR="$HOME/.config/waybar/animations"
CACHE_DIR="$HOME/.cache/waybar-sprites"
STATE_FILE="$CACHE_DIR/current_sprite.state"
FRAME_SIZE=64

mkdir -p "$CACHE_DIR"

get_frame_count() {
    local sprite="$1"
    local width=$(magick identify -format "%w" "$sprite" 2>/dev/null)
    echo $((width / FRAME_SIZE))
}

extract_frame() {
    local sprite="$1"
    local frame_num="$2"
    local output="$3"
    local offset=$((frame_num * FRAME_SIZE))
    
    magick "$sprite" -crop "${FRAME_SIZE}x${FRAME_SIZE}+${offset}+0" +repage "$output" 2>/dev/null
}

select_random_sprite() {
    local sprites=("$ANIMATIONS_DIR"/*.png)
    local random_index=$((RANDOM % ${#sprites[@]}))
    echo "${sprites[$random_index]}"
}

initialize_sprite() {
    local sprite="$1"
    local sprite_name=$(basename "$sprite" .png)
    local frame_count=$(get_frame_count "$sprite")
    
    echo "$sprite|$sprite_name|$frame_count|0" > "$STATE_FILE"
    
    # Extract all frames
    rm -rf "$CACHE_DIR/$sprite_name"
    mkdir -p "$CACHE_DIR/$sprite_name"
    
    for ((i=0; i<frame_count; i++)); do
        extract_frame "$sprite" "$i" "$CACHE_DIR/$sprite_name/frame_$i.png"
    done
}

# Read or initialize state
if [ ! -f "$STATE_FILE" ]; then
    sprite=$(select_random_sprite)
    initialize_sprite "$sprite"
fi

# Read current state
IFS='|' read -r sprite sprite_name frame_count current_frame < "$STATE_FILE"

# Verify sprite still exists
if [ ! -f "$sprite" ]; then
    sprite=$(select_random_sprite)
    initialize_sprite "$sprite"
    IFS='|' read -r sprite sprite_name frame_count current_frame < "$STATE_FILE"
fi

# Display current frame with a simple icon representation
current_image="$CACHE_DIR/$sprite_name/frame_$current_frame.png"

# Use different icons based on sprite type
case "$sprite_name" in
    "RUN")
        icon="🏃"
        ;;
    "WALK")
        icon="🚶"
        ;;
    "IDLE")
        icon="🧍"
        ;;
    "JUMP")
        icon="🦘"
        ;;
    "attack")
        icon="⚔️"
        ;;
    "HURT")
        icon="💥"
        ;;
    "JR")
        icon="🎮"
        ;;
    *)
        icon="👾"
        ;;
esac

# Output for waybar with sprite name and frame indicator
frame_indicator=$(printf '▰%.0s' $(seq 1 $((current_frame % 3 + 1))))
echo "{\"text\":\"$icon $frame_indicator\",\"tooltip\":\"$sprite_name\\nFrame $((current_frame+1))/$frame_count\",\"class\":\"sprite-$sprite_name\"}"

# Advance to next frame
next_frame=$(((current_frame + 1) % frame_count))
echo "$sprite|$sprite_name|$frame_count|$next_frame" > "$STATE_FILE"
