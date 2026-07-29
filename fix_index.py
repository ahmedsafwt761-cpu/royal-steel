#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Royal Steel Egypt — Fix index.html Errors
==========================================
يصلح الأخطاء المتبقية في index.html:
  1. يشيل role="img" من hero__card
  2. يصلح ترتيب <a> في كروت المنتجات
"""

import re
from pathlib import Path
import shutil

# ─── إعدادات ─────────────────────────────────────
FILE_PATH = Path("frontend/index.html")
BACKUP_DIR = Path("backups") / "20260729_fix"

# ─── Backup ────────────────────────────────────────
BACKUP_DIR.mkdir(parents=True, exist_ok=True)
shutil.copy(FILE_PATH, BACKUP_DIR / FILE_PATH.name)
print(f"📦 Backup saved: {BACKUP_DIR / FILE_PATH.name}")

# ─── اقرأ الملف ────────────────────────────────────
with open(FILE_PATH, "r", encoding="utf-8") as f:
    content = f.read()

original = content

# ═══════════════════════════════════════════════════
# 🔧 FIX 1: Remove role="img" from hero__card
# ═══════════════════════════════════════════════════
content = re.sub(
    r'<div class="hero__card" role="img" aria-label="([^"]*)">',
    r'<div class="hero__card" aria-label="\1">',
    content
)
if content != original:
    print("✅ Fixed: removed role='img' from hero__card")
else:
    print("⚠️  Pattern not found for hero__card fix")

# ═══════════════════════════════════════════════════
# 🔧 FIX 2: Fix machine-card nesting
# ═══════════════════════════════════════════════════
# Pattern: <a href="..."> <div class="machine-card"> ... <div class="machine-card__img"> <img ...> </div> </a>
# Should be: <div class="machine-card"> <a href="..."> <div class="machine-card__img"> <img ...> </div> </a>

pattern = re.compile(
    r'<a href="([^"]+)">\s*'
    r'<div class="machine-card">\s*'
    r'<div class="machine-card__img">\s*'
    r'<img([^>]*?)>\s*'
    r'</div>\s*'
    r'</a>',
    re.DOTALL
)

def replace_card(match):
    href = match.group(1)
    img_attrs = match.group(2)
    # Preserve indentation (14 spaces for inner content)
    return (
        f'<div class="machine-card">\n'
        f'                <a href="{href}">\n'
        f'                  <div class="machine-card__img">\n'
        f'                    <img{img_attrs}>\n'
        f'                  </div>\n'
        f'                </a>'
    )

content, count = pattern.subn(replace_card, content)
if count > 0:
    print(f"✅ Fixed: {count} machine-card nesting error(s)")
else:
    print("⚠️  Pattern not found for machine-card fix")

# ═══════════════════════════════════════════════════
# 💾 احفظ الملف ────────────────────────────────────
with open(FILE_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("\n🎉 Done! Check the file and deploy.")
print("   If something breaks, restore from:", BACKUP_DIR / FILE_PATH.name)
