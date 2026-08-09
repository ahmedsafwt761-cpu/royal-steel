#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Final Boost: 78 → 90+ Mobile
"""

import re
from pathlib import Path

BASE = Path("frontend")

def fix_js():
    js = BASE / "style.js"
    if not js.exists():
        print("❌ style.js مش موجود"); return
    
    c = js.read_text(encoding='utf-8')
    
    # 1. Loader: غيّر minLoadTime من 800 أو 300 لـ 0
    c = c.replace('const minLoadTime = 800;', 'const minLoadTime = 0;')
    c = c.replace('const minLoadTime = 300;', 'const minLoadTime = 0;')
    
    # 2. Particles: اظهر/اخفى الـ container
    old_particles = '''const initParticles = () => {
    if ("ontouchstart" in window && window.innerWidth < 768) return;
    if (typeof particlesJS === "undefined" || !$("#particles-js")) return;'''
    
    new_particles = '''const initParticles = () => {
    const container = $("#particles-js");
    if (!container) return;
    if ("ontouchstart" in window && window.innerWidth < 768) {
        container.style.display = "none"; return;
    }
    container.style.display = "";
    if (typeof particlesJS === "undefined") return;'''
    
    c = c.replace(old_particles, new_particles)
    
    js.write_text(c, encoding='utf-8')
    print("✅ style.js: Loader = 0ms, Particles mobile hidden")

def fix_html():
    html = BASE / "index.html"
    if not html.exists():
        print("❌ index.html مش موجود"); return
    
    c = html.read_text(encoding='utf-8')
    
    # 1. Fix doctype مكرر
    c = c.replace('<!doctype html>\n<html lang="ar" dir="rtl">\n  <!doctype html>\n<html lang="ar" dir="rtl">',
                  '<!doctype html>\n<html lang="ar" dir="rtl">')
    
    # 2. System font fallback + preload Google Fonts
    old_head = '<link rel="preconnect" href="https://fonts.googleapis.com">'
    new_head = '''<!-- System font fallback -->
<style>html{font-family:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif}</style>

<!-- Preconnect -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

<!-- Preload Fonts -->
<link rel="preload" href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800;900&display=swap" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800;900&display=swap" rel="stylesheet"></noscript>'''
    
    c = c.replace(old_head, new_head)
    
    # 3. Logo: اشيل loading="lazy" وحط fetchpriority
    c = c.replace('loading="lazy" src="images/logo.webp"', 'src="images/logo.webp" fetchpriority="high"')
    
    # 4. Particles div
    c = c.replace('<div id="particles-js" class="particles-container"></div>',
                  '<div id="particles-js" class="particles-container" style="display:none"></div>')
    
    # 5. Iframe: أضف width و aspect-ratio
    c = c.replace('height="200" style="width:100%;', 'width="100%" height="200" style="')
    if 'aspect-ratio' not in c:
        c = c.replace('style="border:0; border-radius:12px;"',
                      'style="border:0; border-radius:12px; aspect-ratio:16/9;"')
    
    html.write_text(c, encoding='utf-8')
    print("✅ index.html: Doctype, Fonts, Logo, Particles, Iframe")

def fix_css():
    css = BASE / "style.css"
    if not css.exists():
        print("❌ style.css مش موجود"); return
    
    c = css.read_text(encoding='utf-8')
    
    # 1. Line-clamp: أضف الـ standard property
    c = c.replace('-webkit-line-clamp: 3;', '-webkit-line-clamp: 3;\n  line-clamp: 3;')
    
    # 2. Aspect ratio للصور
    if 'aspect-ratio: 4 / 3' not in c:
        c += '''
/* === AUTO-ADDED: Aspect Ratio (يمنع CLS) === */
.card__img, .machine-card__img img, .ph__img img, .product__img img {
  aspect-ratio: 4 / 3;
  object-fit: cover;
}
.testimonial__avatar img {
  aspect-ratio: 1 / 1;
  object-fit: cover;
  border-radius: 50%;
}
.map iframe {
  aspect-ratio: 16 / 9;
  width: 100%;
  height: auto;
}
'''
    
    css.write_text(c, encoding='utf-8')
    print("✅ style.css: Line-clamp, Aspect-ratio")

print("=" * 50)
print("🚀 Final Boost: 78 → 90+")
print("=" * 50)
fix_js()
fix_html()
fix_css()
print("\n🎉 Deploy:")
print("   git add .")
print('   git commit -m "Perf: eliminate loader delay, fix LCP/CLS"')
print("   git push")
print("\n⏳ استنى 3 دقايق وافحص:")
print("   https://pagespeed.web.dev/")