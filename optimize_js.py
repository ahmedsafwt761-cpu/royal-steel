#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Royal Steel - JS Performance Optimizer
"""

import re
from pathlib import Path

FRONTEND = Path("frontend")

def optimize_js():
    js_file = FRONTEND / "style.js"

    if not js_file.exists():
        print("ERROR: style.js not found!")
        return

    with open(js_file, 'r', encoding='utf-8') as f:
        content = f.read()

    original_size = len(content)

    # 1. Reduce particles count (60 -> 25)
    content = re.sub(r'value:\s*60,', 'value: 25,', content)

    # 2. Reduce line_linked distance (180 -> 120)
    content = re.sub(r'distance:\s*180,', 'distance: 120,', content)

    # 3. Reduce particles speed (0.6 -> 0.4)
    content = re.sub(r'speed:\s*0\.6,', 'speed: 0.4,', content)

    # 4. Reduce loader minimum time (1500 -> 800ms)
    content = re.sub(r'minLoadTime = 1500;', 'minLoadTime = 800;', content)

    # 5. Reduce parallax intensity (0.3 -> 0.15)
    content = re.sub(r'scrolled \* 0\.3;', 'scrolled * 0.15;', content)

    # 6. Disable card tilt on mobile (add touch check)
    content = re.sub(
        r'if \(prefersReducedMotion \|\| window\.innerWidth < 768\) return;',
        'if (prefersReducedMotion || window.innerWidth < 1024 || "ontouchstart" in window) return;',
        content
    )

    # 7. Disable magnetic buttons on mobile (add touch check)
    content = re.sub(
        r'if \(prefersReducedMotion \|\| window\.innerWidth < 768\) return;',
        'if (prefersReducedMotion || window.innerWidth < 1024 || "ontouchstart" in window) return;',
        content
    )

    # 8. Skip particles on mobile
    content = re.sub(
        r'(const initParticles = \(\) => \{)',
        r'\1\n    if ("ontouchstart" in window && window.innerWidth < 768) return;',
        content
    )

    # 9. Skip cursor glow on mobile
    content = re.sub(
        r'if \(prefersReducedMotion \|\| window\.innerWidth < 1024\) return;',
        'if (prefersReducedMotion || window.innerWidth < 1024 || "ontouchstart" in window) return;',
        content
    )

    new_size = len(content)

    with open(js_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print("OK: style.js optimized!")
    print(f"   Before: {original_size:,} bytes")
    print(f"   After:  {new_size:,} bytes")
    print()
    print("Changes:")
    print("   - particles: 60 -> 25 (disabled on mobile)")
    print("   - loader time: 1500ms -> 800ms")
    print("   - cursor glow: disabled on mobile")
    print("   - card tilt: disabled on mobile")
    print("   - magnetic buttons: disabled on mobile")
    print("   - parallax: 0.3 -> 0.15")

def main():
    print("=" * 50)
    print("JS Performance Optimizer")
    print("=" * 50)

    if not FRONTEND.exists():
        print("ERROR: frontend folder not found!")
        return

    optimize_js()

    print()
    print("Done! Run:")
    print("   git add .")
    print('   git commit -m "Perf: optimize JS animations"')
    print("   git push")

if __name__ == "__main__":
    main()
