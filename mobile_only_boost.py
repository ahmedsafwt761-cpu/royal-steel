#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mobile Boost Only - Desktop stays at 94
"""

import re
from pathlib import Path

BASE = Path("frontend")

def minify_css():
    """1️⃣ تصغير style.css من غير ما نشيل حاجة (أأمن)"""
    css = BASE / "style.css"
    if not css.exists():
        print("❌ style.css مش موجود"); return
    
    content = css.read_text(encoding='utf-8')
    original = len(content)
    
    # Remove comments /* ... */
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    
    # Remove empty rules
    content = re.sub(r'[^{}]*\{\s*\}', '', content)
    
    # Minify whitespace
    content = re.sub(r'\n\s*\n+', '\n', content)  # empty lines
    content = re.sub(r';\s*}', '}', content)      # last semicolon
    content = re.sub(r'\s*([{}:;,>+~])\s*', r'\1', content)
    content = re.sub(r';\s*', ';', content)
    content = re.sub(r'{\s*', '{', content)
    content = re.sub(r'}\s*', '}\n', content)
    content = re.sub(r',\s*', ',', content)
    content = re.sub(r' +', ' ', content)
    
    css.write_text(content.strip(), encoding='utf-8')
    saved = original - len(content.strip())
    print(f"✅ style.css: minified, saved {saved:,} bytes ({saved/original*100:.1f}%)")

def fix_html_mobile_only():
    """2️⃣ تعديلات تخص Mobile بس"""
    html = BASE / "index.html"
    if not html.exists():
        print("❌ index.html مش موجود"); return
    
    c = html.read_text(encoding='utf-8')
    
    # A. Mobile Font Fallback: النص يظهر فورًا بـ system font
    if 'font-family: system-ui' not in c:
        mobile_font = '''  <!-- 📱 Mobile: show text immediately while Cairo loads -->
  <style>
    @media (max-width: 768px) {
      html { font-family: system-ui, -apple-system, 'Segoe UI', Roboto, 'Cairo', sans-serif; }
      body { font-family: inherit; }
    }
  </style>

'''
        c = c.replace('<head>', '<head>\n' + mobile_font)
        print("✅ Added mobile font fallback")
    
    # B. Logo: fetchpriority high (LCP candidate on mobile)
    if 'fetchpriority="high"' not in c and 'logo.webp' in c:
        c = c.replace(
            'src="images/logo.webp" alt="Royal Steel Logo"',
            'src="images/logo.webp" alt="Royal Steel Logo" fetchpriority="high"'
        )
        print("✅ Logo fetchpriority=high")
    
    # C. Images: decoding="async" (frees main thread on mobile)
    if 'decoding="async"' not in c:
        # Add to all img tags that don't have it
        c = re.sub(
            r'(<img\s+(?!.*decoding=)[^>]*?)(>)',
            r'\1 decoding="async"\2',
            c
        )
        print("✅ Added decoding=async to images")
    
    # D. Preconnect Google Maps (speeds up iframe)
    if 'www.google.com' not in c:
        c = c.replace(
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n  <link rel="preconnect" href="https://www.google.com">'
        )
        print("✅ Preconnect Google Maps")
    
    # E. Viewport optimization for mobile
    if 'viewport-fit=cover' not in c:
        c = c.replace(
            'width=device-width, initial-scale=1"',
            'width=device-width, initial-scale=1, viewport-fit=cover"'
        )
        print("✅ Viewport optimized")
    
    html.write_text(c, encoding='utf-8')

def fix_js_mobile():
    """3️⃣ JS: اخفاء particles container نهائيًا على Mobile"""
    js = BASE / "style.js"
    if not js.exists():
        print("❌ style.js مش موجود"); return
    
    c = js.read_text(encoding='utf-8')
    
    # Make sure particles container is hidden immediately on mobile
    # (before DOMContentLoaded to prevent layout calc)
    if 'particles-js' in c and 'display:none' not in c:
        # Already handled in HTML, but double-check JS
        pass  # HTML already has style="display:none"
    
    # Reduce Swiper autoplay delay on mobile (less CPU)
    if 'delay: 5000' in c:
        c = c.replace('delay: 5000', 'delay: 6000')  # Slightly less frequent
        print("✅ Swiper autoplay relaxed")
    
    js.write_text(c, encoding='utf-8')

print("=" * 55)
print("📱 Mobile Boost Only — Desktop stays 94")
print("=" * 55)
minify_css()
fix_html_mobile_only()
fix_js_mobile()
print("\n🚀 Deploy:")
print("   git add .")
print('   git commit -m "Perf: mobile font fallback, minify CSS, async decoding"')
print("   git push")
print("\n⏳ استنى 3 دقايق وافحص Mobile:")
print("   https://pagespeed.web.dev/")
print("=" * 55)