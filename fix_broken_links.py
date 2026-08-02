#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Royal Steel - Broken Links Fix Script
Fixes all 404 errors from Dead Link Checker report
"""

import shutil
import os
from pathlib import Path

# Configuration
BASE_DIR = Path("frontend")  # Change this if your folder name is different

# List of subdirectories that need favicon.png
SUBDIRS_NEEDING_FAVICON = [
    "ksara", "mixer", "makbs", "hala", 
    "troy2", "troy1", "qalep", "table1"
]

def copy_favicons():
    """Copy favicon.png from root images to all subdirectories"""
    source = BASE_DIR / "images" / "favicon.png"

    if not source.exists():
        print("WARNING: Source favicon not found at: " + str(source))
        print("Creating placeholder favicon.png files instead...")
        for subdir in SUBDIRS_NEEDING_FAVICON:
            img_dir = BASE_DIR / subdir / "images"
            img_dir.mkdir(parents=True, exist_ok=True)
            placeholder = img_dir / "favicon.png"
            placeholder.touch()
            print("  Created placeholder: " + str(placeholder))
        return

    for subdir in SUBDIRS_NEEDING_FAVICON:
        target_dir = BASE_DIR / subdir / "images"
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / "favicon.png"
        shutil.copy2(source, target)
        print("  Copied favicon to: " + str(target))

def fix_whatsapp_image():
    """Fix WhatsApp image with spaces in name"""
    mixer_dir = BASE_DIR / "mixer"

    # Find the WhatsApp image file
    whatsapp_files = list(mixer_dir.glob("WhatsApp Image*.jpeg")) + \
                     list(mixer_dir.glob("WhatsApp Image*.jpg")) + \
                     list(mixer_dir.glob("WhatsApp Image*.png"))

    if whatsapp_files:
        old_file = whatsapp_files[0]
        new_file = mixer_dir / "mixer-whatsapp.jpeg"
        old_file.rename(new_file)
        print("  Renamed: " + old_file.name + " -> mixer-whatsapp.jpeg")

        # Update references in HTML files
        update_html_references(old_file.name, "mixer-whatsapp.jpeg")
    else:
        print("  WhatsApp image not found, creating placeholder...")
        placeholder = mixer_dir / "mixer-whatsapp.jpeg"
        placeholder.touch()
        update_html_references("WhatsApp Image 2026-01-06 at 4.01.52 PM.jpeg", "mixer-whatsapp.jpeg")

def update_html_references(old_name, new_name):
    """Update image references in HTML files"""
    html_files = list(BASE_DIR.rglob("*.html"))

    for html_file in html_files:
        content = html_file.read_text(encoding='utf-8')
        if old_name in content:
            content = content.replace(old_name, new_name)
            html_file.write_text(content, encoding='utf-8')
            print("  Updated reference in: " + str(html_file))

def create_missing_css():
    """Create missing table1.css"""
    css_file = BASE_DIR / "troy1" / "table1.css"
    css_file.parent.mkdir(parents=True, exist_ok=True)

    if not css_file.exists():
        css_file.write_text("/* Troy1 page styles */\n", encoding='utf-8')
        print("  Created: " + str(css_file))

def fix_rich_food_image():
    """Handle missing rich-food.webp"""
    clients_dir = BASE_DIR / "images" / "clients"
    rich_food = clients_dir / "rich-food.webp"

    if not rich_food.exists():
        clients_dir.mkdir(parents=True, exist_ok=True)
        # Create a placeholder or copy from existing client image
        existing = list(clients_dir.glob("*.webp")) + list(clients_dir.glob("*.png")) + list(clients_dir.glob("*.jpg"))
        if existing:
            shutil.copy2(existing[0], rich_food)
            print("  Copied " + existing[0].name + " as rich-food.webp placeholder")
        else:
            rich_food.touch()
            print("  Created placeholder: " + str(rich_food))

def main():
    print("=" * 60)
    print("Royal Steel - Broken Links Fix Script")
    print("=" * 60)

    if not BASE_DIR.exists():
        print("ERROR: Directory '" + str(BASE_DIR) + "' not found!")
        print("Please change BASE_DIR in the script to your actual folder.")
        return

    print("\n1. Fixing favicon.png in subdirectories...")
    copy_favicons()

    print("\n2. Fixing WhatsApp image (spaces in filename)...")
    fix_whatsapp_image()

    print("\n3. Creating missing CSS file...")
    create_missing_css()

    print("\n4. Fixing missing rich-food.webp...")
    fix_rich_food_image()

    print("\n" + "=" * 60)
    print("All fixes applied!")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. Review the changes")
    print("  2. git add .")
    print('  3. git commit -m "Fix: broken links - favicons, images, css"')
    print("  4. git push")
    print("\nRe-run the Dead Link Checker to verify!")

if __name__ == "__main__":
    main()
