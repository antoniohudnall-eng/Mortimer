#!/usr/bin/env python3
"""
📚 LILLY - Mortimer Reading Loop
Runs in background, keeps reading while Captain sleeps
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime

BRAIN_DIR = Path.home() / "AOS-Brain"
GUTENBERG_DIR = BRAIN_DIR / "curriculum" / "gutenberg"
BOOKS_DIR = GUTENBERG_DIR / "books"
MEMORY_DIR = Path.home() / "mortimer" / "memory"
LOG_FILE = MEMORY_DIR / "lilly_reading_log.md"

# Track what's been read
PROGRESS_FILE = MEMORY_DIR / "lilly_progress.json"

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] 📚 {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

def load_progress():
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE) as f:
            return json.load(f)
    return {"books_read": [], "current": 0, "total_learned": 0}

def save_progress(progress):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=2)

def download_book(book_id, title):
    """Download a Gutenberg book"""
    urls = [
        f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt",
        f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt",
    ]
    
    for url in urls:
        try:
            import urllib.request
            with urllib.request.urlopen(url, timeout=30) as resp:
                content = resp.read().decode('utf-8', errors='ignore')
                if len(content) > 10000:  # Valid book
                    filepath = BOOKS_DIR / f"book_{book_id}.txt"
                    with open(filepath, "w") as f:
                        f.write(content)
                    return filepath, len(content)
        except:
            continue
    return None, 0

def read_and_learn(filepath, title, author):
    """Read book and extract key learnings"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Extract first 1000 lines for analysis
    lines = content.split('\n')
    
    # Clean text - remove Gutenberg header/footer
    clean_lines = []
    in_text = False
    for line in lines:
        if '*** START OF' in line:
            in_text = True
            continue
        if '*** END OF' in line:
            break
        if in_text and len(line) > 10:
            clean_lines.append(line)
    
    # Extract key sentences
    meaningful = [l for l in clean_lines if len(l) > 50][:200]
    
    # Create learning summary
    summary = f"""
## 📖 {title}
### By {author}
### Downloaded: {datetime.now().strftime('%Y-%m-%d %H:%M')}

### Statistics
- Total lines: {len(lines)}
- Meaningful lines: {len(meaningful)}
- Total characters: {len(content)}

### Key Sentences (First 20)
"""
    for i, line in enumerate(meaningful[:20]):
        summary += f"{i+1}. {line[:150]}...\n"
    
    summary += """
### Initial Analysis
- This is a classic text from Project Gutenberg
- Theme exploration ongoing
- More analysis will come with continued reading
"""
    
    # Save to brain memory
    today = datetime.now().strftime("%Y-%m-%d")
    study_file = BRAIN_DIR / "memory" / f"study-{today}.md"
    with open(study_file, "a") as f:
        f.write(summary)
    
    return len(meaningful)

def main():
    log("LILLY Reading Loop started")
    
    # Create directories
    BOOKS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load book queue from curriculum
    curriculum_file = GUTENBERG_DIR / "bookshelf_catalog.json"
    books_to_read = []
    
    if curriculum_file.exists():
        with open(curriculum_file) as f:
            data = json.load(f)
            for category, info in data.get("categories", {}).items():
                for book in info.get("books", []):
                    if not book.get("ingested", False):
                        books_to_read.append({
                            "id": book["id"],
                            "title": book["title"],
                            "author": book.get("author", "Unknown"),
                            "category": category
                        })
    
    log(f"Found {len(books_to_read)} books in queue")
    
    progress = load_progress()
    books_read = progress.get("books_read", [])
    
    for i, book in enumerate(books_to_read):
        book_id = book["id"]
        
        if str(book_id) in books_read:
            continue
        
        log(f"Reading: {book['title']} ({book['author']})")
        
        # Download
        filepath, size = download_book(book_id, book['title'])
        
        if filepath and size > 10000:
            # Read and learn
            lines = read_and_learn(filepath, book['title'], book['author'])
            log(f"✅ Completed: {book['title']} ({lines} lines)")
            
            books_read.append(str(book_id))
            progress["books_read"] = books_read
            progress["total_learned"] = len(books_read)
            save_progress(progress)
            
            # Brief pause between books
            time.sleep(5)
        else:
            log(f"❌ Failed: {book['title']} (ID: {book_id})")
        
        # Rate limit to be respectful to Gutenberg
        time.sleep(2)
    
    log("LILLY Reading Loop complete!")
    log(f"Total books read: {len(books_read)}")

if __name__ == "__main__":
    main()
