#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 Royal Steel Egypt — HTML Validator & SEO Checker
 =================================================
 يفحص كل ملفات HTML في المشروع ويطلع تقرير بالأخطاء

 طريقة الاستخدام:
   1. احفظ الملف باسم check_site.py في فولدر المشروع
   2. شغله:  python check_site.py
   3. هيطلع تقرير في الملف:  site_report.txt
"""

import os
import re
from pathlib import Path
from collections import defaultdict

# الأرقام الصحيحة
CORRECT_PHONE = "+201115709334"
CORRECT_WHATSAPP = "201115709334"

# الأرقام الغلط اللي لازم ندور عليها
WRONG_PHONES = [
    "201225585826",
    "+201145553855",
    "2011157093334",
]

# CSS files الغلط
WRONG_CSS = {
    "styel.css": "style.css",
    "troly1.css": "table1.css",
}

# الـ URLs الصحيحة للـ OG
CORRECT_OG_URLS = {
    "index.html": "https://royal-steel.vercel.app/",
    "clients.html": "https://royal-steel.vercel.app/clients.html",
    "products.html": "https://royal-steel.vercel.app/products.html",
}

def find_html_files(root_dir="."):
    """يلاقي كل ملفات HTML"""
    html_files = []
    for path in Path(root_dir).rglob("*.html"):
        # استثني ملفات node_modules و .git
        if any(part.startswith(".") or part == "node_modules" for part in path.parts):
            continue
        html_files.append(path)
    return sorted(html_files)

def check_file(filepath):
    """يفحص ملف HTML واحد ويرجع قائمة بالأخطاء"""
    errors = []
    warnings = []
    infos = []
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            lines = content.splitlines()
    except Exception as e:
        return [("FATAL", f"مش قادر أقرأ الملف: {e}")], [], []
    
    filename = filepath.name
    
    # ─── 1. Unclosed tags ─────────────────────────────
    for tag in ["li", "p", "div", "section", "a", "span", "h3"]:
        open_count = len(re.findall(rf"<{tag}[\s/>]", content, re.I))
        close_count = len(re.findall(rf"</{tag}>", content, re.I))
        if tag in ["div", "section", "span", "a"]:
            self_close = len(re.findall(rf"<{tag}\b[^>]*?/>", content, re.I))
            open_count -= self_close
        if open_count != close_count and tag in ["li", "p", "a", "h3"]:
            errors.append(("HTML", f"عدد <{tag}> المفتوحة ({open_count}) ≠ المقفولة ({close_count})"))
    
    # ─── 2. Meta Description فاضية أو مكررة ───────────
    desc_tags = re.findall(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\']', content, re.I)
    desc_tags += re.findall(r'<meta[^>]*content=["\']([^"\']*)["\'][^>]*name=["\']description["\']', content, re.I)
    
    if len(desc_tags) > 1:
        errors.append(("SEO", f"Description مكررة ({len(desc_tags)} مرة)"))
    for d in desc_tags:
        if d.strip() == "":
            errors.append(("SEO", 'Description فاضية (content="")'))
    
    # ─── 3. theme-color ───────────────────────────────
    if not re.search(r'<meta[^>]*name=["\']theme-color["\']', content, re.I):
        errors.append(("SEO", 'ناقص <meta name="theme-color" content="#d4a843" />'))
    
    # ─── 4. أرقام غلط ─────────────────────────────────
    for wrong in WRONG_PHONES:
        if wrong in content:
            errors.append(("PHONE", f"رقم غلط موجود: {wrong} → يتغير لـ {CORRECT_PHONE}"))
    
    # ─── 5. Schema telephone ──────────────────────────
    schema_phone = re.search(r'"telephone"\s*:\s*"([^"]+)"', content)
    if schema_phone:
        phone = schema_phone.group(1)
        if phone != CORRECT_PHONE:
            errors.append(("SCHEMA", f'Schema telephone غلط: {phone} → {CORRECT_PHONE}'))
    
    # ─── 6. OG URL ────────────────────────────────────
    og_url_match = re.search(r'<meta[^>]*property=["\']og:url["\'][^>]*content=["\']([^"\']+)["\']', content, re.I)
    if og_url_match and filename in CORRECT_OG_URLS:
        og_url = og_url_match.group(1)
        correct = CORRECT_OG_URLS[filename]
        if og_url != correct:
            errors.append(("OG", f"OG URL غلط: {og_url} → {correct}"))
    
    # ─── 7. CSS غلط ───────────────────────────────────
    for wrong, correct in WRONG_CSS.items():
        if wrong in content:
            errors.append(("CSS", f"ملف CSS غلط: {wrong} → {correct}"))
    
    # ─── 8. HTML مكسور — ناقص " ──────────────────────
    broken_img = re.findall(r'src=["\'][^"\']*\.webp\s+[^"\']*["\']', content)
    if broken_img:
        errors.append(("HTML", f"HTML مكسور: ناقص quote بعد .webp → {broken_img[0][:50]}"))
    
    # ─── 9. h3 جوه role=img ───────────────────────────
    if re.search(r'role=["\']img["\'][^>]*>[^<]*<h3', content, re.I | re.DOTALL):
        errors.append(("A11Y", '<h3> جوه عنصر بـ role="img" (ممنوع)'))
    
    # ─── 10. Favicon — space في href ──────────────────
    if re.search(r'href=["\']data:image/svg\+xml[^"\']*\s[^"\']*["\']', content):
        errors.append(("HTML", "Favicon SVG: فيه space غلط في الـ data URI"))
    
    # ─── 11. WhatsApp رقم غلط ─────────────────────────
    wa_wrong = re.findall(r'wa\.me/(\d{10,})', content)
    for num in wa_wrong:
        if num != CORRECT_WHATSAPP:
            errors.append(("WHATSAPP", f"WhatsApp رقم غلط: {num} → {CORRECT_WHATSAPP}"))
    
    # ─── 12. Trailing slash على void elements (Info) ──
    void_tags = ["meta", "link", "img", "br", "hr", "input"]
    for tag in void_tags:
        count = len(re.findall(rf"<{tag}\b[^>]*?/>", content, re.I))
        if count > 0:
            infos.append(("INFO", f"Trailing slash على <{tag}> ({count} مرة) — مش خطأ بس ممكن تشيلها"))
    
    # ─── 13. Canonical ناقص ───────────────────────────
    if not re.search(r'<link[^>]*rel=["\']canonical["\']', content, re.I):
        warnings.append(("SEO", 'ناقص <link rel="canonical" />'))
    
    return errors, warnings, infos

def main():
    print("=" * 60)
    print("  Royal Steel Egypt — HTML & SEO Checker")
    print("=" * 60)
    
    html_files = find_html_files()
    
    if not html_files:
        print("❌ مفيش ملفات HTML في الفولدر ده!")
        return
    
    print(f"🔍 لقيت {len(html_files)} ملف HTML")
    print("-" * 60)
    
    all_errors = defaultdict(list)
    all_warnings = defaultdict(list)
    all_infos = defaultdict(list)
    
    for filepath in html_files:
        rel_path = filepath.relative_to(Path("."))
        errs, warns, infs = check_file(filepath)
        all_errors[rel_path] = errs
        all_warnings[rel_path] = warns
        all_infos[rel_path] = infs
    
    report_lines = []
    report_lines.append("=" * 70)
    report_lines.append("  تقرير فحص ملفات HTML — Royal Steel Egypt")
    report_lines.append("=" * 70)
    report_lines.append("")
    
    total_errors = 0
    total_warnings = 0
    
    for filepath in sorted(all_errors.keys()):
        errs = all_errors[filepath]
        warns = all_warnings[filepath]
        infs = all_infos[filepath]
        
        if not errs and not warns:
            status = "✅"
            print(f"{status} {filepath}")
            report_lines.append(f"✅ {filepath} — تمام")
            if infs:
                report_lines.append("   ℹ️  ملاحظات:")
                for _, msg in infs:
                    report_lines.append(f"      • {msg}")
            continue
        
        status = "🔴" if errs else "⚠️"
        print(f"{status} {filepath}")
        report_lines.append(f"{status} {filepath}")
        
        for cat, msg in errs:
            print(f"   ❌ [{cat}] {msg}")
            report_lines.append(f"   ❌ [{cat}] {msg}")
            total_errors += 1
        
        for cat, msg in warns:
            print(f"   ⚠️  [{cat}] {msg}")
            report_lines.append(f"   ⚠️  [{cat}] {msg}")
            total_warnings += 1
        
        for cat, msg in infs:
            report_lines.append(f"   ℹ️  [{cat}] {msg}")
    
    report_lines.append("")
    report_lines.append("=" * 70)
    report_lines.append(f"  المجموع: {total_errors} خطأ | {total_warnings} تحذير")
    report_lines.append("=" * 70)
    
    report_text = "\n".join(report_lines)
    with open("site_report.txt", "w", encoding="utf-8") as f:
        f.write(report_text)
    
    print("\n" + "=" * 60)
    print(f"📊 المجموع: {total_errors} خطأ | {total_warnings} تحذير")
    print("📄 التقرير اتحفظ في: site_report.txt")
    print("=" * 60)

if __name__ == "__main__":
    main()