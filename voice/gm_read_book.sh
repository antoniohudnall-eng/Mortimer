#!/bin/bash
# gm_read_book.sh - Read a book using GM/PI voice
# Usage: gm_read_book.sh <book.txt>

VOICE="en-us"
SPEED=161
PITCH=51
AMP=113
KEYTONE=4
OUTPUT="/tmp/book_reading.wav"

BOOK="$1"

if [ -z "$BOOK" ]; then
    echo "Usage: gm_read_book.sh <book.txt>"
    echo ""
    echo "Available books:"
    ls ~/AOS-Brain/curriculum/gutenberg/books/*.txt 2>/dev/null | head -10
    exit 1
fi

if [ ! -f "$BOOK" ]; then
    echo "File not found: $BOOK"
    exit 1
fi

echo "📚 Reading: $BOOK"
echo ""

# Read the book (limit to first 5000 chars for demo)
TEXT=$(head -c 5000 "$BOOK")

# Generate voice
espeak -v "$VOICE" -s "$SPEED" -p "$PITCH" -a "$AMP" -k "$KEYTONE" -w "$OUTPUT" "$TEXT"

# Play
echo "🎙️ Playing with GM/PI voice..."
termux-media-player play "$OUTPUT"

echo "✅ Done!"
