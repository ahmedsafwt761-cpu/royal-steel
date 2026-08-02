#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Royal Steel - Broken Links Fix Script v2
Fixes remaining 404 errors
"""

import shutil
from pathlib import Path

BASE_DIR = Path("frontend")

print("=" * 60)
print("Royal Steel - Broken Links Fix Script v2")
print("=" * 60)

# 1. Create root favicon.png if missing
root_favicon = BASE_DIR / "images" / "favicon.png"
root_favicon.parent.mkdir(parents=True, exist_ok=True)

if not root_favicon.exists():
    # Try to find any existing favicon or image to copy
    existing_images = list((BASE_DIR / "images").glob("*.png")) + \
                      list((BASE_DIR / "images").glob("*.webp")) + \
                      list((BASE_DIR / "images").glob("*.jpg"))

    if existing_images:
        shutil.copy2(existing_images[0], root_favicon)
        print("1. Created root favicon.png from: " + existing_images[0].name)
    else:
        root_favicon.touch()
        print("1. Created placeholder root favicon.png")
else:
    print("1. Root favicon.png already exists")

# 2. Fix troly1 and troly2 (not troy1/troy2)
correct_names = ["troly1", "troly2"]
wrong_names = ["troy1", "troy2"]

for correct, wrong in zip(correct_names, wrong_names):
    wrong_dir = BASE_DIR / wrong / "images"
    correct_dir = BASE_DIR / correct / "images"

    # If wrong folder exists with favicon, copy to correct folder
    wrong_favicon = wrong_dir / "favicon.png"
    correct_favicon = correct_dir / "favicon.png"

    if wrong_favicon.exists() and not correct_favicon.exists():
        correct_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(wrong_favicon, correct_favicon)
        print("2. Copied favicon to correct folder: " + str(correct_dir))
    elif not correct_favicon.exists():
        correct_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(root_favicon, correct_favicon)
        print("2. Created favicon in: " + str(correct_dir))
    else:
        print("2. favicon already exists in: " + str(correct_dir))

# 3. Fix table1.css location (should be in troly1 not troy1)
wrong_css = BASE_DIR / "troy1" / "table1.css"
correct_css = BASE_DIR / "troly1" / "table1.css"

if wrong_css.exists() and not correct_css.exists():
    correct_css.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(wrong_css, correct_css)
    print("3. Copied table1.css to correct location: " + str(correct_css))
elif not correct_css.exists():
    correct_css.parent.mkdir(parents=True, exist_ok=True)
    correct_css.write_text("/* Troly1 page styles */\n", encoding='utf-8')
    print("3. Created table1.css in: " + str(correct_css))
else:
    print("3. table1.css already exists in correct location")

# 4. Also ensure favicon exists in all subdirectories
all_subdirs = ["ksara", "mixer", "makbs", "hala", 
               "troly2", "troly1", "qalep", "table1"]

for subdir in all_subdirs:
    favicon_path = BASE_DIR / subdir / "images" / "favicon.png"
    if not favicon_path.exists():
        favicon_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(root_favicon, favicon_path)
        print("4. Created favicon in: " + subdir)

print("\n" + "=" * 60)
print("Done!")
print("=" * 60)
print("\nNext steps:")
print("  1. git add .")
print('  2. git commit -m "Fix: broken links v2 - favicons, css paths"')
print("  3. git push")
print("\nNote: WhatsApp links (429 errors) are NOT broken.")
print("      WhatsApp blocks automated checkers. These links work fine.")
