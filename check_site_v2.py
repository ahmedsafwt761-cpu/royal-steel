#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 Royal Steel Egypt — HTML Validator & SEO Checker v2
 ====================================================
 يفحص كل ملفات HTML ويطلع تقرير بالأخطاء الحقيقية فقط

 طريقة الاستخدام:
   python check_site.py
"""

import re
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(__file__).parent

# الأرقام الغلط اللي لازم ندور عليها
WRONG_PHONES = [
    "201225585826",
    "+201145553855",
    "2011157093334",
]

# CSS files الغلط (الصح style.css و table1.css)
WRONG_CSS = {
    "styel.css": "style.css",
    "troly1.css": "table1.css",
}

# ملفات ماستثنيها من الفحص
SKIP_FILES = {
    "google70f956c0d5f7625d.html",
}

def find_html_files():
    html_files = []
    for path in BASE_DIR.rglob("*.html"):
        if any(p.startswith(".") or p == "node_modules" or p == "backups" for p in path.parts):
            continue
        if path.name in SKIP_FILES:
            continue
        html_files.append(path)
    return sorted(html_files)

def check_file(filepath):
    errors = []
    warnings = []
    infos = []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return [("FATAL", f"مش قادر أقرأ الملف: {e}")], [], []

    filename = filepath.name

    # 1. Unclosed tags (li, p, a, h3)
    for tag in ["li", "p", "a", "h3"]:
        open_count = len(re.findall(rf"<{tag}[\s/>]", content, re.I))
        close_count = len(re.findall(rf"</{tag}>", content, re.I))
        self_close = len(re.findall(rf"<{tag}\b[^>]*?/>", content, re.I))
        open_count -= self_close
        if open_count != close_count:
            errors.append(("HTML", f"عدد <{tag}> المفتوحة ({open_count}) ≠ المقفولة ({close_count})"))

    # 2. Meta Description فاضية أو مكررة
    desc_pattern = r'<meta[^>]*name=["\']description["\'][^>]*>'
    desc_matches = list(re.finditer(desc_pattern, content, re.I))
    if len(desc_matches) > 1:
        errors.append(("SEO", f"Description مكررة ({len(desc_matches)} مرة)"))
    for m in desc_matches:
        tag = m.group(0)
        if 'content=""' in tag or "content=''" in tag:
            errors.append(("SEO", 'Description فاضية (content="")'))

    # 3. theme-color ناقص
    if not re.search(r'<meta[^>]*name=["\']theme-color["\']', content, re.I):
        errors.append(("SEO", 'ناقص <meta name="theme-color" content="#d4a843" />'))

    # 4. أرقام غلط
    for wrong in WRONG_PHONES:
        if wrong in content:
            errors.append(("PHONE", f"رقم غلط موجود: {wrong}"))

    # 5. Schema telephone
    schema_phone = re.search(r'"telephone"\s*:\s*"([^"]+)"', content)
    if schema_phone:
        phone = schema_phone.group(1)
        if phone in WRONG_PHONES:
            errors.append(("SCHEMA", f'Schema telephone غلط: {phone}'))

    # 6. OG URL غلط في clients.html
    if filename == "clients.html":
        og_url = re.search(r'<meta[^>]*property=["\']og:url["\'][^>]*content=["\']([^"\']+)["\']', content, re.I)
        if og_url and og_url.group(1) == "https://royal-steel.vercel.app/":
            errors.append(("OG", "OG URL بيشير للرئيسية مش لصفحة العملاء"))

    # 7. CSS غلط — ندور على الـ wrong values بس
    for wrong, correct in WRONG_CSS.items():
        if wrong in content:
            errors.append(("CSS", f"ملف CSS غلط: {wrong} → {correct}"))

    # 8. HTML مكسور — ناقص " بعد .webp
    broken = re.findall(r'src=["\'][^"\']*\.webp\s+[^"\']*["\']', content)
    if broken:
        errors.append(("HTML", f"HTML مكسور: ناقص quote بعد .webp"))

    # 9. h3 جوه role=img
    if re.search(r'role=["\']img["\'][^>]*>[^<]*<h3', content, re.I | re.DOTALL):
        errors.append(("A11Y", '<h3> جوه عنصر بـ role="img" (ممنوع)'))

    # 10. WhatsApp رقم غلط
    wa_matches = re.findall(r'wa\.me/(\d{10,})', content)
    for num in wa_matches:
        if num in ["201225585826", "2011157093334"]:
            errors.append(("WHATSAPP", f"WhatsApp رقم غلط: {num}"))

    # 11. Canonical ناقص
    if not re.search(r'<link[^>]*rel=["\']canonical["\']', content, re.I):
        warnings.append(("SEO", 'ناقص <link rel="canonical" />'))

    # 12. Favicon inline SVG (info)
    if 'data:image/svg+xml' in content:
        infos.append(("INFO", "Favicon inline SVG — ممكن تغيّره لـ favicon.png"))

    return errors, warnings, infos

def main():
    print("=" * 65)
    print("  Royal Steel Egypt — HTML & SEO Checker v2")
    print("=" * 65)

    html_files = find_html_files()
    if not html_files:
        print("❌ مفيش ملفات HTML!")
        return

    print(f"🔍 لقيت {len(html_files)} ملف HTML")
    print("-" * 65)

    total_errors = 0
    total_warnings = 0
    report_lines = []

    for filepath in html_files:
        rel_path = filepath.relative_to(BASE_DIR)
        errs, warns, infs = check_file(filepath)

        if not errs and not warns:
            print(f"✅ {rel_path}")
            report_lines.append(f"✅ {rel_path}")
            for _, msg in infs:
                report_lines.append(f"   ℹ️  {msg}")
            continue

        status = "🔴" if errs else "⚠️"
        print(f"{status} {rel_path}")
        report_lines.append(f"{status} {rel_path}")

        for cat, msg in errs:
            print(f"   ❌ [{cat}] {msg}")
            report_lines.append(f"   ❌ [{cat}] {msg}")
            total_errors += 1

        for cat, msg in warns:
            print(f"   ⚠️  [{cat}] {msg}")
            report_lines.append(f"   ⚠️  [{cat}] {msg}")
            total_warnings += 1

        for _, msg in infs:
            report_lines.append(f"   ℹ️  {msg}")

    print("\n" + "=" * 65)
    print(f"📊 المجموع: {total_errors} خطأ | {total_warnings} تحذير")
    print("=" * 65)

    report_text = "\n".join(report_lines)
    with open("site_report.txt", "w", encoding="utf-8") as f:
        f.write(report_text + f"\n\nالمجموع: {total_errors} خطأ | {total_warnings} تحذير\n")
    print("📄 التقرير اتحفظ في: site_report.txt")

if __name__ == "__main__":
    main()
