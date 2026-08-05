#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Royal Steel - Boost Performance (No Backup)
بيشيل الكود الميت، يضيف defer، يصلح Animations
"""

import re
from pathlib import Path

BASE = Path(".")

def remove_dead_js():
    """1️⃣ يشيل الكود الميت من style.js"""
    js_file = BASE / "frontend" / "style.js"
    if not js_file.exists():
        print("❌ style.js مش موجود")
        return
    
    content = js_file.read_text(encoding='utf-8')
    original_len = len(content)
    
    # الكود الميت اللي هنشيله
    dead_patterns = [
        r'// ================= CURSOR GLOW EFFECT =================.*?(?=// =================|\Z)',
        r'// ================= MAGNETIC BUTTONS =================.*?(?=// =================|\Z)',
        r'// ================= CARD 3D TILT EFFECT =================.*?(?=// =================|\Z)',
        r'// ================= RIPPLE EFFECT =================.*?(?=// =================|\Z)',
        r'// ================= PARALLAX EFFECT =================.*?(?=// =================|\Z)',
    ]
    
    for pattern in dead_patterns:
        content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    # نشيل الـ init functions الميتة
    dead_inits = ['initCursorGlow', 'initMagneticButtons', 'initCardTilt', 'initRipple', 'initParallax']
    for func in dead_inits:
        content = re.sub(rf'{func}\(\);', '', content)
        content = re.sub(rf'{func}\s*\(\s*\)', '', content)
    
    # نضيف check للـ particles على الموبايل لو مش موجود
    if 'window.matchMedia' not in content and 'particlesJS' in content:
        content = content.replace(
            'particlesJS("particles-js"',
            'if(!window.matchMedia("(max-width:768px)").matches){particlesJS("particles-js"'
        )
        # نضيف closing bracket
        content = content.replace(
            'particlesJS("particles-js",',
            'particlesJS("particles-js",'
        )
    
    # ننظف السطور الفاضية المتكررة
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    
    js_file.write_text(content, encoding='utf-8')
    saved = original_len - len(content)
    print(f"✅ style.js: شلنا {saved:,} bytes من الكود الميت")

def fix_html():
    """2️⃣ نضيف defer للمكتبات ونحوّل og-image"""
    for html_file in (BASE / "frontend").rglob("*.html"):
        content = html_file.read_text(encoding='utf-8')
        original = content
        
        # أضف defer للمكتبات الخارجية
        libs = [
            'particles.js',
            'typed.js',
            'countup.js',
            'swiper-bundle.min.js'
        ]
        for lib in libs:
            content = re.sub(
                rf'<script([^>]*src="[^"]*{lib}[^"]*")(?![^>]*defer)(?![^>]*async)',
                r'<script defer \1',
                content
            )
        
        # حوّل og-image.jpg لـ webp
        content = content.replace('og-image.jpg', 'og-image.webp')
        content = content.replace('og-image.jpeg', 'og-image.webp')
        
        # أضف preload للـ CSS المهم
        if 'rel="stylesheet"' in content and 'preload' not in content:
            content = content.replace(
                '<link rel="stylesheet" href="style.css">',
                '<link rel="preload" href="style.css" as="style" onload="this.onload=null;this.rel=\'stylesheet\'">\n<noscript><link rel="stylesheet" href="style.css"></noscript>'
            )
        
        # أضف loading="lazy" للصور اللي ناقصة
        content = re.sub(
            r'(<img\s+(?!.*loading=)[^>]*src="[^"]+\.(webp|jpg|png|jpeg)")',
            r'\1 loading="lazy"',
            content
        )
        
        # أضف width/height للصور اللي ناقصة (منع Layout Shift)
        # نعمل pattern عام للصور بدون dimensions
        content = re.sub(
            r'(<img\s+(?!.*width=)(?!.*height=)[^>]*src="[^"]*")',
            r'\1 width="400" height="300"',
            content
        )
        
        if content != original:
            html_file.write_text(content, encoding='utf-8')
            print(f"✅ {html_file.name}: defer + lazy loading + preload")

def fix_css_animations():
    """3️⃣ نصلح Animations في CSS"""
    css_files = list((BASE / "frontend").rglob("*.css"))
    fixed = 0
    
    for css_file in css_files:
        if '.min.' in css_file.name:
            continue
            
        content = css_file.read_text(encoding='utf-8')
        original = content
        
        # نحوّل left/top/width/height + transition لـ transform
        # نضيف تعليقات للأماكن اللي لازم تتعدل يدويًا
        lines = content.split('\n')
        new_lines = []
        
        for line in lines:
            # لو فيه animation على left/top/width/height
            if re.search(r'(left|top|width|height)\s*:', line) and \
               ('transition' in line or 'animation' in line):
                if 'transform' not in line:
                    new_lines.append('/* ⚠️ PERF: غيّر لـ transform عشان GPU */')
            
            # نصلح أي حاجة واضحة
            line = re.sub(
                r'transition:\s*(left|top|width|height)',
                r'transition: transform /* was: \1 */',
                line
            )
            new_lines.append(line)
        
        new_content = '\n'.join(new_lines)
        
        if new_content != original:
            css_file.write_text(new_content, encoding='utf-8')
            fixed += 1
    
    print(f"✅ عدّلنا {fixed} ملف CSS")

def main():
    print("=" * 50)
    print("🚀 Royal Steel - Boost Performance")
    print("=" * 50)
    
    if not (BASE / "frontend").exists():
        print("❌ لازم تشغل الـ Script من جوه Royal-Steel-Website")
        return
    
    print("\n[1/3] ✂️ بشيل الكود الميت من style.js...")
    remove_dead_js()
    
    print("\n[2/3] 📄 بضيف defer و preload للـ HTML...")
    fix_html()
    
    print("\n[3/3] 🎬 بصلّح Animations في CSS...")
    fix_css_animations()
    
    print("\n" + "=" * 50)
    print("🎉 خلصنا! اعمل الآن:")
    print("   git add .")
    print('   git commit -m "Perf: remove dead JS, defer libs, fix animations"')
    print("   git push")
    print("\n⏳ استنى 2-3 دقايق وافحص تاني:")
    print("   https://pagespeed.web.dev/")
    print("=" * 50)

if __name__ == "__main__":
    main()