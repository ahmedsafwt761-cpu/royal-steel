#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 Royal Steel Egypt — Auto Fix Script
=======================================
بيصلح كل الأخطاء تلقائيًا في كل ملفات HTML

طريقة الاستخدام:
    1. حط الملف ده في فولدر المشروع (أعلى فولدر فيه frontend/ والمنتجات/)
    2. شغله:  python auto_fix.py
    3. هيعمل backup من كل ملف قبل التعديل
    4. هيطلع تقرير بالتعديلات اللي اتعملت
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime

# ==================== الإعدادات ====================
BASE_DIR = Path(__file__).parent
BACKUP_DIR = BASE_DIR / "backups" / datetime.now().strftime("%Y%m%d_%H%M%S")

# الأرقام الصحيحة
CORRECT_PHONE = "+201115709334"
CORRECT_PHONE_NO_PLUS = "201115709334"

# الأرقام الغلط → الصح
PHONE_REPLACEMENTS = {
    "201225585826": CORRECT_PHONE_NO_PLUS,
    "+201145553855": CORRECT_PHONE,
    "2011157093334": CORRECT_PHONE_NO_PLUS,
}

# WhatsApp replacements
WHATSAPP_REPLACEMENTS = {
    "wa.me/201225585826": f"wa.me/{CORRECT_PHONE_NO_PLUS}",
    "wa.me/2011157093334": f"wa.me/{CORRECT_PHONE_NO_PLUS}",
}

# CSS replacements
CSS_REPLACEMENTS = {
    'href="style.css"': 'href="style.css"',
    "href='style.css'": "href='style.css'",
    'href="troly1.css"': 'href="table1.css"',
    "href='troly1.css'": "href='table1.css'",
}

# Canonical URLs حسب الملف
CANONICAL_URLS = {
    "index.html": "https://royal-steel.vercel.app/",
    "clients.html": "https://royal-steel.vercel.app/clients.html",
    "products.html": "https://royal-steel.vercel.app/products.html",
    "ksara.html": "https://royal-steel.vercel.app/products/ksara.html",
    "mixer.html": "https://royal-steel.vercel.app/products/mixer.html",
    "makbs.html": "https://royal-steel.vercel.app/products/makbs.html",
    "hala.html": "https://royal-steel.vercel.app/products/hala.html",
    "table1.html": "https://royal-steel.vercel.app/products/table1.html",
    "troly1.html": "https://royal-steel.vercel.app/products/troly1.html",
    "troly2.html": "https://royal-steel.vercel.app/products/troly2.html",
    "qalep.html": "https://royal-steel.vercel.app/products/qalep.html",
}

# ==================== دوال المساعدة ====================
def find_html_files():
    """يلاقي كل ملفات HTML"""
    html_files = []
    for path in BASE_DIR.rglob("*.html"):
        # استثني ملفات .git و node_modules و backups
        if any(part.startswith(".") or part == "node_modules" or part == "backups"
               for part in path.parts):
            continue
        html_files.append(path)
    return sorted(html_files)

def backup_file(filepath):
    """يعمل backup من الملف"""
    rel_path = filepath.relative_to(BASE_DIR)
    backup_path = BACKUP_DIR / rel_path
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(filepath, backup_path)
    return backup_path

def add_theme_color(content):
    """يضيف theme-color لو ناقص"""
    if 'name="theme-color"' in content or "name='theme-color'" in content:
        return content, False

    theme_line = '    <meta name="theme-color" content="#d4a843" />\n'

    if '<link rel="canonical"' in content:
        content = re.sub(
            r'(<link rel="canonical"[^>]*>)\n?',
            r'\1\n' + theme_line.rstrip(),
            content
        )
        return content, True

    if 'name="viewport"' in content:
        content = re.sub(
            r'(<meta[^>]*name="viewport"[^>]*>)\n?',
            r'\1\n' + theme_line.rstrip(),
            content
        )
        return content, True

    if 'charset="UTF-8"' in content:
        content = re.sub(
            r'(<meta[^>]*charset="UTF-8"[^>]*>)\n?',
            r'\1\n' + theme_line.rstrip(),
            content
        )
        return content, True

    return content, False

def add_canonical(content, filename):
    """يضيف canonical لو ناقص"""
    if '<link rel="canonical"' in content:
        return content, False

    if filename not in CANONICAL_URLS:
        return content, False

    canonical_line = f'    <link rel="canonical" href="{CANONICAL_URLS[filename]}" />\n'

    if 'name="theme-color"' in content:
        content = re.sub(
            r'(<meta[^>]*name="theme-color"[^>]*>)\n?',
            r'\1\n' + canonical_line.rstrip(),
            content
        )
        return content, True

    if 'name="viewport"' in content:
        content = re.sub(
            r'(<meta[^>]*name="viewport"[^>]*>)\n?',
            r'\1\n' + canonical_line.rstrip(),
            content
        )
        return content, True

    return content, False

def fix_favicon(content):
    """يصلح الـ favicon"""
    if 'data:image/svg+xml' in content:
        old_pattern = r'<link[^>]*rel="icon"[^>]*href="data:image/svg\+xml[^"]*"[^>]*>'
        new_favicon = '<link rel="icon" type="image/png" href="images/favicon.png" />'
        if re.search(old_pattern, content):
            content = re.sub(old_pattern, new_favicon, content)
            return content, True
    return content, False

def fix_duplicate_description(content, filename):
    """يمسح Description المكررة أو الفاضية"""
    fixed = False

    # امسح description الفاضية - using double quotes for the string
    empty_desc = r"<meta[^>]*name=[\"']description[\"'][^>]*content=[\"'][\"'][^>]*>"
    if re.search(empty_desc, content, re.I):
        content = re.sub(empty_desc, '', content, flags=re.I)
        fixed = True

    # لو فيه أكتر من description، امسح التانية
    desc_pattern = r"<meta[^>]*name=[\"']description[\"'][^>]*>"
    desc_matches = list(re.finditer(desc_pattern, content, re.I))
    if len(desc_matches) > 1:
        for match in desc_matches[1:]:
            content = content[:match.start()] + content[match.end():]
        fixed = True
        content = re.sub(r'\n\s*\n', '\n', content)

    return content, fixed

def fix_unclosed_p(content, filename):
    """يصلح <p> مش مقفول"""
    if filename != "index.html":
        return content, False

    open_p = len(re.findall(r'<p[\s>]', content, re.I))
    close_p = len(re.findall(r'</p>', content, re.I))

    if open_p > close_p:
        patterns = [
            r'(معايير HACCP وسلامة الغذاء\.\.\.)\s*</div>',
            r'(معايير HACCP وسلامة الغذاء[^<]*)</div>',
        ]
        for pattern in patterns:
            if re.search(pattern, content, re.I):
                content = re.sub(pattern, r'\1</p>\n              </div>', content, flags=re.I)
                return content, True

    return content, False

def fix_og_url(content, filename):
    """يصلح OG URL في clients.html"""
    if filename != "clients.html":
        return content, False

    wrong_url = 'content="https://royal-steel.vercel.app/"'
    correct_url = 'content="https://royal-steel.vercel.app/clients.html"'

    if wrong_url in content and 'property="og:url"' in content:
        content = content.replace(wrong_url, correct_url, 1)
        return content, True

    return content, False

# ==================== الدالة الرئيسية ====================
def fix_file(filepath):
    """تصلح ملف HTML واحد"""
    filename = filepath.name
    changes = []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return [("FATAL", f"مش قادر أقرأ الملف: {e}")]

    original = content

    # 1. صلّح CSS
    for old, new in CSS_REPLACEMENTS.items():
        if old in content:
            content = content.replace(old, new)
            changes.append(("CSS", f"{old} → {new}"))

    # 2. صلّح أرقام التليفون
    for old, new in PHONE_REPLACEMENTS.items():
        if old in content:
            content = content.replace(old, new)
            changes.append(("PHONE", f"{old} → {new}"))

    # 3. صلّح WhatsApp
    for old, new in WHATSAPP_REPLACEMENTS.items():
        if old in content:
            content = content.replace(old, new)
            changes.append(("WHATSAPP", f"{old} → {new}"))

    # 4. ضيف theme-color
    content, fixed = add_theme_color(content)
    if fixed:
        changes.append(("SEO", "ضيف theme-color"))

    # 5. ضيف canonical
    content, fixed = add_canonical(content, filename)
    if fixed:
        changes.append(("SEO", f"ضيف canonical → {CANONICAL_URLS.get(filename, 'N/A')}"))

    # 6. صلّح favicon
    content, fixed = fix_favicon(content)
    if fixed:
        changes.append(("HTML", "صلّح favicon SVG"))

    # 7. صلّح description مكررة/فاضية
    content, fixed = fix_duplicate_description(content, filename)
    if fixed:
        changes.append(("SEO", "صلّح Description (مكررة/فاضية)"))

    # 8. صلّح <p> مش مقفول
    content, fixed = fix_unclosed_p(content, filename)
    if fixed:
        changes.append(("HTML", "أقفل <p> اللي كان ناقص"))

    # 9. صلّح OG URL في clients.html
    content, fixed = fix_og_url(content, filename)
    if fixed:
        changes.append(("OG", "صلّح OG URL → /clients.html"))

    # احفظ لو فيه تغييرات
    if content != original:
        backup_file(filepath)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    return changes

def main():
    print("=" * 65)
    print("  Royal Steel Egypt — Auto Fix Script")
    print("=" * 65)

    html_files = find_html_files()

    if not html_files:
        print("❌ مفيش ملفات HTML!")
        return

    print(f"🔍 لقيت {len(html_files)} ملف HTML")
    print(f"💾 Backup هيتحفظ في: {BACKUP_DIR}")
    print("-" * 65)

    total_changes = 0
    files_changed = 0
    report_lines = []

    for filepath in html_files:
        rel_path = filepath.relative_to(BASE_DIR)
        changes = fix_file(filepath)

        if changes:
            files_changed += 1
            total_changes += len(changes)
            print(f"🔧 {rel_path} ({len(changes)} تعديل)")
            report_lines.append(f"🔧 {rel_path}")
            for cat, msg in changes:
                print(f"   ✓ [{cat}] {msg}")
                report_lines.append(f"   ✓ [{cat}] {msg}")
        else:
            print(f"✅ {rel_path} — مفيش تعديلات")

    print("\n" + "=" * 65)
    print(f"📊 تمام! {files_changed} ملف اتعدل | {total_changes} تعديل إجمالي")
    print(f"💾 Backup موجود في: {BACKUP_DIR}")
    print("=" * 65)
    print("\n⚠️  قبل الـ Deploy:")
    print("   1. افحص الملفات اللي اتعدلت")
    print("   2. تأكد إن كل حاجة شغالة صح")
    print("   3. اعمل git add . → git commit → git push")

    report_text = "\n".join(report_lines)
    report_path = BASE_DIR / "auto_fix_report.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("Auto Fix Report — Royal Steel Egypt\n")
        f.write("=" * 50 + "\n\n")
        f.write(report_text)
        f.write(f"\n\nTotal: {files_changed} files | {total_changes} changes\n")
    print(f"\n📄 التقرير اتحفظ في: {report_path}")

if __name__ == "__main__":
    main()