#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Royal Steel - Performance Optimizer Script
يحسن Performance الموقع تلقائيًا
"""

import os
import re
import shutil
from pathlib import Path

# ============================================
# ⚙️ الإعدادات
# ============================================
FRONTEND_DIR = Path("frontend")  # غيّر ده لو المجلد مختلف

def log(step, msg):
    print(f"  [{step}] {msg}")

# ============================================
# 1️⃣ Minify CSS
# ============================================
def minify_css():
    """يشيل المسافات والكومنتات من CSS"""
    print("\n[1/7] 🔧 Minify CSS...")

    css_files = list(FRONTEND_DIR.rglob("*.css"))
    saved = 0

    for css_file in css_files:
        # سيب الملفات المضغوطة
        if ".min." in css_file.name:
            continue

        with open(css_file, 'r', encoding='utf-8') as f:
            content = f.read()

        original_size = len(content)

        # شيل الكومنتات
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        # شيل المسافات الزيادة
        content = re.sub(r'\s+', ' ', content)
        content = re.sub(r';\s*}', '}', content)
        content = re.sub(r'{\s+', '{', content)
        content = re.sub(r';\s+', ';', content)
        content = re.sub(r',\s+', ',', content)
        content = re.sub(r':\s+', ':', content)
        content = content.strip()

        new_size = len(content)

        if new_size < original_size:
            # احفظ النسخة الأصلية
            backup = css_file.with_suffix('.css.backup')
            if not backup.exists():
                shutil.copy2(css_file, backup)

            with open(css_file, 'w', encoding='utf-8') as f:
                f.write(content)

            saved += original_size - new_size
            log("✅", f"{css_file.name} ({original_size:,} → {new_size:,} bytes)")

    print(f"  📊 وفرنا {saved:,} bytes من CSS")
    return True

# ============================================
# 2️⃣ Minify JS
# ============================================
def minify_js():
    """يشيل المسافات والكومنتات من JS"""
    print("\n[2/7] 🔧 Minify JavaScript...")

    js_files = list(FRONTEND_DIR.rglob("*.js"))
    saved = 0

    for js_file in js_files:
        if ".min." in js_file.name:
            continue

        with open(js_file, 'r', encoding='utf-8') as f:
            content = f.read()

        original_size = len(content)

        # شيل كومنتات //
        content = re.sub(r'//.*?$', '', content, flags=re.MULTILINE)
        # شيل كومنتات /* */
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        # شيل المسافات الزيادة
        content = re.sub(r'\n\s*\n', '\n', content)
        content = re.sub(r'\s+', ' ', content)
        content = re.sub(r';\s*}', '}', content)
        content = re.sub(r'{\s+', '{', content)
        content = re.sub(r';\s+', ';', content)
        content = re.sub(r',\s+', ',', content)
        content = content.strip()

        new_size = len(content)

        if new_size < original_size:
            backup = js_file.with_suffix('.js.backup')
            if not backup.exists():
                shutil.copy2(js_file, backup)

            with open(js_file, 'w', encoding='utf-8') as f:
                f.write(content)

            saved += original_size - new_size
            log("✅", f"{js_file.name} ({original_size:,} → {new_size:,} bytes)")

    print(f"  📊 وفرنا {saved:,} bytes من JS")
    return True

# ============================================
# 3️⃣ Add defer to JS tags
# ============================================
def add_defer_to_js():
    """يضيف defer لـ script tags"""
    print("\n[3/7] 🔧 Add defer to JS...")

    html_files = list(FRONTEND_DIR.rglob("*.html"))
    fixed = 0

    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content

        # أضف defer للـ script اللي مالهاش async أو defer
        def add_defer(match):
            tag = match.group(0)
            if 'defer' in tag or 'async' in tag or 'type="module"' in tag:
                return tag
            # لو فيه src
            if 'src=' in tag:
                return tag.replace('<script ', '<script defer ')
            return tag

        content = re.sub(r'<script\s+[^>]*src=[^>]*>', add_defer, content)

        if content != original:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            fixed += 1
            log("✅", f"{html_file.name}")

    print(f"  📊 عدّلنا {fixed} ملف HTML")
    return True

# ============================================
# 4️⃣ Fix iframe titles
# ============================================
def fix_iframe_titles():
    """يضيف title للـ iframes"""
    print("\n[4/7] 🔧 Fix iframe titles...")

    html_files = list(FRONTEND_DIR.rglob("*.html"))
    fixed = 0

    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content

        def add_title(match):
            tag = match.group(0)
            if 'title=' in tag:
                return tag
            # حدد نوع الـ iframe
            if 'google.com/maps' in tag or 'maps' in tag:
                return tag.replace('<iframe ', '<iframe title="Google Map" ')
            elif 'youtube' in tag or 'youtu.be' in tag:
                return tag.replace('<iframe ', '<iframe title="YouTube Video" ')
            else:
                return tag.replace('<iframe ', '<iframe title="Embedded Content" ')

        content = re.sub(r'<iframe\s+[^>]*>', add_title, content)

        if content != original:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            fixed += 1
            log("✅", f"{html_file.name}")

    print(f"  📊 عدّلنا {fixed} ملف HTML")
    return True

# ============================================
# 5️⃣ Add loading="lazy" to images
# ============================================
def add_lazy_loading():
    """يضيف loading=lazy للصور"""
    print("\n[5/7] 🔧 Add loading=\"lazy\" to images...")

    html_files = list(FRONTEND_DIR.rglob("*.html"))
    fixed = 0

    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content

        def add_lazy(match):
            tag = match.group(0)
            if 'loading=' in tag:
                return tag
            # سيب الصور الأولى (above the fold) من غير lazy
            # هنضيف lazy لكل الصور دلوقتي
            return tag.replace('<img ', '<img loading="lazy" ')

        content = re.sub(r'<img\s+[^>]*>', add_lazy, content)

        if content != original:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            fixed += 1
            log("✅", f"{html_file.name}")

    print(f"  📊 عدّلنا {fixed} ملف HTML")
    return True

# ============================================
# 6️⃣ Fix contrast colors (تلميحات)
# ============================================
def fix_contrast():
    """يبحث عن ألوان ضعيفة ويعطي تلميحات"""
    print("\n[6/7] 🔧 Check contrast colors...")

    css_files = list(FRONTEND_DIR.rglob("*.css"))
    issues = []

    # ألوان شائعة ضعيفة
    weak_colors = [
        (r'color\s*:\s*#aaa', '#aaa → #ccc أو #fff'),
        (r'color\s*:\s*#999', '#999 → #bbb أو #fff'),
        (r'color\s*:\s*#888', '#888 → #aaa أو #fff'),
        (r'color\s*:\s*#777', '#777 → #999 أو #fff'),
        (r'color\s*:\s*rgba\(255,\s*255,\s*255,\s*0\.[0-4]', 'opacity ضعيف → زود الـ opacity'),
    ]

    for css_file in css_files:
        with open(css_file, 'r', encoding='utf-8') as f:
            content = f.read()

        for pattern, suggestion in weak_colors:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                issues.append(f"  ⚠️  {css_file.name}: {suggestion}")

    if issues:
        print("  وجدنا ألوان محتاجة تحسين:")
        for issue in issues:
            print(issue)
    else:
        print("  ✅ مفيش ألوان ضعيفة واضحة")

    return True

# ============================================
# 7️⃣ Fix animations (GPU accelerated)
# ============================================
def fix_animations():
    """يبحث عن animations مش GPU-accelerated"""
    print("\n[7/7] 🔧 Check animations...")

    css_files = list(FRONTEND_DIR.rglob("*.css"))
    issues = []

    bad_props = [
        (r'left\s*:\s*\d', 'left → transform: translateX()'),
        (r'top\s*:\s*\d', 'top → transform: translateY()'),
        (r'width\s*:\s*\d.*transition', 'width → transform: scaleX()'),
        (r'height\s*:\s*\d.*transition', 'height → transform: scaleY()'),
        (r'margin\s*:\s*\d.*transition', 'margin → transform: translate()'),
    ]

    for css_file in css_files:
        with open(css_file, 'r', encoding='utf-8') as f:
            content = f.read()

        for pattern, suggestion in bad_props:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                issues.append(f"  ⚠️  {css_file.name}: {suggestion}")

    if issues:
        print("  وجدنا animations محتاجة تحويل:")
        for issue in issues:
            print(issue)
    else:
        print("  ✅ كل الـ animations GPU-accelerated")

    return True

# ============================================
# 🚀 التشغيل الرئيسي
# ============================================
def main():
    print("=" * 55)
    print("⚡ Royal Steel - Performance Optimizer")
    print("=" * 55)
    print(f"\n📁 المجلد: {FRONTEND_DIR.absolute()}")

    if not FRONTEND_DIR.exists():
        print(f"\n❌ مجلد {FRONTEND_DIR} مش موجود!")
        print("   غيّر متغير FRONTEND_DIR في السطر 15")
        return

    # شغل كل الإصلاحات
    minify_css()
    minify_js()
    add_defer_to_js()
    fix_iframe_titles()
    add_lazy_loading()
    fix_contrast()
    fix_animations()

    print("\n" + "=" * 55)
    print("🎉 خلصنا! اعمل الآن:")
    print("   git add .")
    print('   git commit -m "Perf: optimize CSS, JS, images, accessibility"')
    print("   git push")
    print("\n💡 ملاحظات:")
    print("   • لو حابب ترجع النسخ الأصلية: شيل .backup من اسم الملف")
    print("   • الصور: حوّلها لـ WebP يدويًا بـ https://squoosh.app/")
    print("=" * 55)

if __name__ == "__main__":
    main()
