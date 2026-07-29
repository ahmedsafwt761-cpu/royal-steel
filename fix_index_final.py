#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Royal Steel Egypt — Fix ALL index.html Validator Errors
=========================================================
يصلح كل الأخطاء اللي طلعت في Validator:
  1. aria-label على div → يغير لـ figure
  2. h3 بعد h1 → يغير لـ h2
  3. div مش مقفول في كروت المنتجات
  4. مسافات في أسماء ملفات الصور
  5. width="100%" في iframe
  6. -- داخل comments
"""

import re
from pathlib import Path
import shutil

FILE_PATH = Path("frontend/index.html")
BACKUP_DIR = Path("backups") / "20260729_final_fix"

BACKUP_DIR.mkdir(parents=True, exist_ok=True)
shutil.copy(FILE_PATH, BACKUP_DIR / FILE_PATH.name)
print(f"📦 Backup saved: {BACKUP_DIR / FILE_PATH.name}")

with open(FILE_PATH, "r", encoding="utf-8") as f:
    content = f.read()

original = content
fixes = []

# ═══════════════════════════════════════════════════
# FIX 1: aria-label on div → change to figure
# ═══════════════════════════════════════════════════
content = re.sub(
    r'<div class="hero__card" aria-label="([^"]*)">',
    r'<figure class="hero__card" aria-label="\1">',
    content
)
# Also close it
content = re.sub(
    r'</div>\s*(?=\s*<!-- hero -->|\s*</section>|\s*<div class="hero__stats")',
    r'</figure>',
    content
)
if 'hero__card' in content and '<figure' in content:
    fixes.append("Changed hero__card div to figure (fixes aria-label error)")

# ═══════════════════════════════════════════════════
# FIX 2: h3 after h1 → change to h2
# ═══════════════════════════════════════════════════
# Find h3 inside hero__card and change to h2
content = re.sub(
    r'(<div class="hero__card"[^>]*>.*?<h3>)',
    lambda m: m.group(1).replace('<h3>', '<h2>'),
    content,
    flags=re.DOTALL
)
content = re.sub(
    r'(</h3>.*?<!-- hero -->|</h3>.*?</figure>)',
    lambda m: m.group(1).replace('</h3>', '</h2>'),
    content,
    flags=re.DOTALL
)
# More robust: find h3 that follows h1 pattern in hero
hero_h3_pattern = re.compile(
    r'(<div class="hero__card"[^>]*>.*?)<h3>([^<]+)</h3>(.*?</div>)',
    re.DOTALL
)
def fix_hero_heading(m):
    before = m.group(1)
    text = m.group(2)
    after = m.group(3)
    return f'{before}<h2>{text}</h2>{after}'
content = hero_h3_pattern.sub(fix_hero_heading, content)
if '<h2>' in content and 'hero__card' in content:
    fixes.append("Changed hero h3 to h2 (fixes heading hierarchy)")

# ═══════════════════════════════════════════════════
# FIX 3: Fix machine-card nesting (mixer & makbs)
# ═══════════════════════════════════════════════════

# Mixer: <div class="machine-card"></div>  (empty, self-closing-ish)
mixer_fix = re.compile(
    r'(<article class="card reveal" data-product="mixer"[^>]*>\s*)'
    r'<div class="machine-card"></div>\s*'
    r'(<a href="mixer/mixer\.html">\s*'
    r'<div class="machine-card__img">\s*'
    r'<img\s+([^>]+)>\s*'
    r'</div>\s*'
    r'</a>\s*'
    r'<h3>([^<]+)</h3>\s*'
    r'<p>([^<]+)</p>\s*'
    r'</div>)',
    re.DOTALL
)
def fix_mixer_card(m):
    article = m.group(1)
    img_tag = m.group(3)
    h3_text = m.group(4)
    p_text = m.group(5)
    return (
        f'{article}'
        f'<div class="machine-card">\n'
        f'                <a href="mixer/mixer.html">\n'
        f'                  <div class="machine-card__img">\n'
        f'                    <img {img_tag}>\n'
        f'                  </div>\n'
        f'                </a>\n'
        f'                <h3>{h3_text}</h3>\n'
        f'                <p>{p_text}</p>\n'
        f'              </div>'
    )
content, count = mixer_fix.subn(fix_mixer_card, content)
if count > 0:
    fixes.append(f"Fixed mixer card nesting ({count}x)")

# Makbs: <a> before <div class="machine-card">
makbs_fix = re.compile(
    r'(<article class="card reveal" data-product="makbs"[^>]*>\s*)'
    r'<a href="makbs/makbs\.html">\s*'
    r'<div class="machine-card">\s*'
    r'(<div class="machine-card__img">\s*'
    r'<img\s+([^>]+)>\s*'
    r'</div>\s*)'
    r'</a>\s*'
    r'(<h3>([^<]+)</h3>\s*'
    r'<p>([^<]+)</p>\s*'
    r'</div>)',
    re.DOTALL
)
def fix_makbs_card(m):
    article = m.group(1)
    img_section = m.group(2)
    img_tag = m.group(3)
    text_section = m.group(4)
    h3_text = m.group(5)
    p_text = m.group(6)
    return (
        f'{article}'
        f'<div class="machine-card">\n'
        f'                <a href="makbs/makbs.html">\n'
        f'                  {img_section.strip()}\n'
        f'                </a>\n'
        f'                <h3>{h3_text}</h3>\n'
        f'                <p>{p_text}</p>\n'
        f'              </div>'
    )
content, count = makbs_fix.subn(fix_makbs_card, content)
if count > 0:
    fixes.append(f"Fixed makbs card nesting ({count}x)")

# ═══════════════════════════════════════════════════
# FIX 4: Spaces in image filenames → %20
# ═══════════════════════════════════════════════════
content = content.replace(
    'images/clients/Halwani Brothers.webp',
    'images/clients/Halwani%20Brothers.webp'
)
content = content.replace(
    'images/clients/Elhassan w Elhussein.webp',
    'images/clients/Elhassan%20w%20Elhussein.webp'
)
if '%20' in content:
    fixes.append("Fixed spaces in image filenames (%20)")

# ═══════════════════════════════════════════════════
# FIX 5: iframe width="100%" → style
# ═══════════════════════════════════════════════════
content = re.sub(
    r'<iframe\s+',
    r'<iframe style="width:100%;border:0;border-radius:12px;" ',
    content
)
content = re.sub(
    r'\s+width="100%"',
    r'',
    content
)
if 'style="width:100%' in content:
    fixes.append("Fixed iframe width=100% (moved to style)")

# ═══════════════════════════════════════════════════
# FIX 6: -- inside HTML comments → ==
# ═══════════════════════════════════════════════════
# Find comments containing btn--outline and replace -- with ==
comment_pattern = re.compile(r'<!--(.*?)-->', re.DOTALL)
def fix_comment(m):
    inner = m.group(1)
    inner = inner.replace('btn--small', 'btn==small')
    inner = inner.replace('btn--outline', 'btn==outline')
    return f'<!--{inner}-->'
content = comment_pattern.sub(fix_comment, content)
if 'btn==outline' in content:
    fixes.append("Fixed -- inside HTML comments")

# ═══════════════════════════════════════════════════
# Save
# ═══════════════════════════════════════════════════
with open(FILE_PATH, "w", encoding="utf-8") as f:
    f.write(content)

if fixes:
    print("\n✅ Fixes applied:")
    for f in fixes:
        print(f"   • {f}")
else:
    print("\n⚠️  No fixes applied — patterns may differ.")
    print("   Please send the actual code around the error lines.")

print(f"\n📄 File saved: {FILE_PATH}")
print(f"   Backup: {BACKUP_DIR / FILE_PATH.name}")
