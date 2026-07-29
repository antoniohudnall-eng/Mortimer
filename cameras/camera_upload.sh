#!/data/data/com.termux/files/usr/bin/bash
#
# Camera Upload Script v1.0
# Watches for new images and sends to Mortimer VPS
# For O-Kam Pro and FlyCloud cameras
#
# Usage: bash camera_upload.sh [watch_directory]

VPS="31.97.6.30"
PORT="12860"
CAMERA="${2:-okam-pro}"
WATCH_DIR="${1:-/storage/emulated/0/DCIM/Camera}"

echo "🎥 Camera Upload Script"
echo "   VPS: $VPS:$PORT"
echo "   Camera: $CAMERA"
echo "   Watching: $WATCH_DIR"
echo ""

upload_file() {
    local file="$1"
    local filename=$(basename "$file")
    
    echo "📸 Uploading: $filename"
    
    # Determine type from extension
    local ext="${filename##*.}"
    local type="image"
    case "$ext" in
        mp4|webm|avi|mkv|mov) type="video" ;;
        *) type="image" ;;
    esac
    
    # Upload
    curl -s -X POST \
        -F "file=@$file" \
        "http://$VPS:$PORT/upload?camera=$CAMERA&type=$type" 2>&1
    
    echo ""
}

# Watch mode
if [ "${3:-}" = "--watch" ]; then
    echo "🔍 Watch mode enabled. Monitoring for new files..."
    LAST_COUNT=$(ls -1 "$WATCH_DIR"/*.{jpg,jpeg,png,mp4,webm} 2>/dev/null | wc -l)
    
    while true; do
        CURRENT_COUNT=$(ls -1 "$WATCH_DIR"/*.{jpg,jpeg,png,mp4,webm} 2>/dev/null | wc -l)
        
        if [ "$CURRENT_COUNT" -gt "$LAST_COUNT" ]; then
            # Find the newest file
            NEWEST=$(ls -1t "$WATCH_DIR"/*.{jpg,jpeg,png,mp4,webm} 2>/dev/null | head -1)
            if [ -n "$NEWEST" ]; then
                upload_file "$NEWEST"
            fi
        fi
        
        LAST_COUNT=$CURRENT_COUNT
        sleep 5
    done
fi

# One-shot mode - upload latest image
if [ "${3:-}" = "--latest" ]; then
    LATEST=$(ls -1t "$WATCH_DIR"/*.{jpg,jpeg,png,mp4,webm} 2>/dev/null | head -1)
    if [ -n "$LATEST" ]; then
        upload_file "$LATEST"
    else
        echo "❌ No images found in $WATCH_DIR"
    fi
    exit 0
fi

# One-shot mode - upload specific file
if [ "${3:-}" != "" ]; then
    upload_file "$3"
    exit 0
fi

echo "Usage:"
echo "  bash $0 [watch_dir] [camera_name] --watch    Continuous monitoring"
echo "  bash $0 [watch_dir] [camera_name] --latest   Upload latest image"
echo "  bash $0 [watch_dir] [camera_name] file.jpg   Upload specific file"
