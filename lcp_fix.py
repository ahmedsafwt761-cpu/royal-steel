#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix LCP: Inline Critical CSS + Async style.css
"""

from pathlib import Path
import re

BASE = Path("frontend")
html_file = BASE / "index.html"

if not html_file.exists():
    print("❌ index.html مش موجود"); exit(1)

c = html_file.read_text(encoding='utf-8')

# ========== 1. Inline Critical CSS ==========
CRITICAL_CSS = '''  <!-- ⚡ INLINE CRITICAL CSS - prevents FOUC & fixes LCP -->
  <style>
    /* SYSTEM FONT FALLBACK - text appears immediately */
    html { font-family: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif; }
    
    /* Body basics */
    body { margin: 0; padding: 0; background: #0a0a0a; color: #fff; overflow-x: hidden; direction: rtl; line-height: 1.6; }
    *, *::before, *::after { box-sizing: border-box; }
    
    /* CRITICAL: Navbar (prevents layout shift) */
    .navbar, .header { position: fixed; top: 0; left: 0; width: 100%; z-index: 1000; background: rgba(10,10,10,0.95); backdrop-filter: blur(10px); padding: 1rem 0; border-bottom: 1px solid rgba(212,168,67,0.2); }
    .navbar .container, .header .container { display: flex; justify-content: space-between; align-items: center; width: 90%; max-width: 1200px; margin: 0 auto; padding: 0 15px; }
    .logo, .brand__logo { font-size: 1.5rem; font-weight: 800; color: #d4a843; text-decoration: none; }
    .nav-links, .nav__menu { display: flex; gap: 2rem; list-style: none; margin: 0; padding: 0; }
    .nav-links a, .nav__menu a { color: #ccc; font-weight: 600; text-decoration: none; }
    .mobile-menu-btn, .nav__toggle { display: none; background: none; border: none; color: #d4a843; font-size: 1.5rem; cursor: pointer; }
    
    /* CRITICAL: Hero - LCP element (must match style.css exactly) */
    .hero { min-height: 100vh; display: flex; align-items: center; justify-content: center; text-align: center; padding-top: 80px; position: relative; overflow: hidden; background: #0a0a0a; }
    .hero-content, .hero__content { position: relative; z-index: 2; padding: 0 20px; }
    .hero h1, .hero__title { font-size: 2.5rem; font-weight: 800; margin: 0 0 1rem 0; line-height: 1.2; color: #fff; }
    .hero h1 span, .hero__title span { color: #d4a843; }
    .hero p, .hero__subtitle { font-size: 1.1rem; color: #ccc; margin: 0 auto 2rem auto; max-width: 600px; }
    .btn, .hero__cta { display: inline-block; padding: 1rem 2.5rem; background: #d4a843; color: #0a0a0a; font-weight: 700; border-radius: 50px; text-decoration: none; }
    
    /* Mobile */
    @media(max-width:768px) { 
      .hero h1, .hero__title { font-size: 2rem; } 
      .nav-links, .nav__menu { display: none; } 
      .mobile-menu-btn, .nav__toggle { display: block; } 
    }
  </style>

'''

# Insert after <head>
c = c.replace('<head>', '<head>\n' + CRITICAL_CSS)

# ========== 2. Convert style.css to async (preload) ==========
# Replace synchronous style.css with preload
c = c.replace(
    '  <link rel="stylesheet" href="style.css" />',
    '''  <!-- style.css loads asynchronously after critical CSS -->
  <link rel="preload" href="style.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="style.css"></noscript>'''
)

# ========== 3. Make sure Google Fonts is async too ==========
if 'fonts.googleapis.com' in c and 'preload' not in c.split('fonts.googleapis.com')[0].split('<link')[-1]:
    # If Google Fonts is still synchronous, make it async
    c = c.replace(
        '<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">',
        '''<link rel="preload" href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800;900&display=swap" as="style" onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800;900&display=swap" rel="stylesheet"></noscript>'''
    )

html_file.write_text(c, encoding='utf-8')

print("=" * 55)
print("⚡ LCP Fix Applied")
print("=" * 55)
print("✅ Inline Critical CSS added (~2.5 KB)")
print("✅ style.css → preload (async)")
print("✅ Google Fonts → preload (async)")
print("\n🚀 Deploy:")
print("   git add .")
print('   git commit -m "Perf: inline critical CSS, async style.css"')
print("   git push")
print("\n⏳ استنى 3 دقايق وافحص:")
print("   https://pagespeed.web.dev/")
print("\n⚠️  لو ظهرت الصفحة مكسورة:")
print("   git revert HEAD")
print("=" * 55)