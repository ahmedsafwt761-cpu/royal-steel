// ============================================
// ROYAL STEEL EGYPT - PRODUCTS PAGE
// Dedicated JavaScript for products.html
// ============================================

document.addEventListener("DOMContentLoaded", () => {

  const $ = (selector) => document.querySelector(selector);
  const $$ = (selector) => document.querySelectorAll(selector);
  const debounce = (fn, ms) => {
    let timeout;
    return (...args) => { clearTimeout(timeout); timeout = setTimeout(() => fn(...args), ms); };
  };
  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // ================= PROGRESS BAR =================
  const initProgressBar = () => {
    const progressBar = $("#progressBar");
    if (!progressBar) return;
    const updateProgress = () => {
      const scrollTop = window.scrollY;
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      const scrollPercent = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
      progressBar.style.width = scrollPercent + "%";
    };
    window.addEventListener("scroll", updateProgress, { passive: true });
    updateProgress();
  };
  initProgressBar();

  // ================= MOBILE NAVIGATION =================
  const initMobileNav = () => {
    const navToggle = $("#navToggle");
    const navMenu = $("#navMenu");
    if (!navToggle || !navMenu) return;
    let isAnimating = false;

    const openMenu = () => {
      if (isAnimating) return;
      isAnimating = true;
      navMenu.classList.add("is-open");
      navToggle.classList.add("is-open");
      navToggle.setAttribute("aria-expanded", "true");
      document.body.style.overflow = "hidden";
      setTimeout(() => { isAnimating = false; }, 350);
    };
    const closeMenu = () => {
      if (isAnimating) return;
      isAnimating = true;
      navMenu.classList.remove("is-open");
      navToggle.classList.remove("is-open");
      navToggle.setAttribute("aria-expanded", "false");
      document.body.style.overflow = "";
      setTimeout(() => { isAnimating = false; }, 250);
    };

    navToggle.addEventListener("click", () => {
      navMenu.classList.contains("is-open") ? closeMenu() : openMenu();
    });
    navMenu.querySelectorAll("a").forEach(link => link.addEventListener("click", closeMenu));
    document.addEventListener("click", (e) => {
      if (navMenu.classList.contains("is-open") && !navMenu.contains(e.target) && !navToggle.contains(e.target)) {
        closeMenu();
      }
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && navMenu.classList.contains("is-open")) closeMenu();
    });
  };
  initMobileNav();

  // ================= HEADER SCROLL EFFECT =================
  const initHeaderScroll = () => {
    const header = $(".header");
    if (!header) return;
    let lastScroll = 0;
    window.addEventListener("scroll", debounce(() => {
      const currentScroll = window.scrollY;
      if (currentScroll > 100) header.classList.add("header--scrolled");
      else header.classList.remove("header--scrolled");
      if (currentScroll > lastScroll && currentScroll > 300) header.style.transform = "translateY(-100%)";
      else header.style.transform = "translateY(0)";
      lastScroll = currentScroll;
    }, 10), { passive: true });
  };
  initHeaderScroll();

  // ================= SCROLL REVEAL =================
  const initScrollReveal = () => {
    if (prefersReducedMotion) return;
    const reveals = $$(".reveal");
    if (reveals.length === 0) return;
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry, index) => {
        if (entry.isIntersecting) {
          setTimeout(() => { entry.target.classList.add("active"); }, index * 100);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: "0px 0px -80px 0px" });
    reveals.forEach(el => observer.observe(el));
  };
  initScrollReveal();

  // ================= SCROLL TO TOP =================
  const initScrollTop = () => {
    const scrollTopBtn = $("#scrollTopBtn");
    if (!scrollTopBtn) return;
    window.addEventListener("scroll", debounce(() => {
      scrollTopBtn.classList.toggle("show", window.scrollY > 500);
    }, 50), { passive: true });
    scrollTopBtn.addEventListener("click", () => {
      window.scrollTo({ top: 0, behavior: prefersReducedMotion ? "auto" : "smooth" });
    });
  };
  initScrollTop();

  // ================= PRODUCT DETAIL MODAL =================
  const initProductModal = () => {
    const modal = $("#productModal");
    const modalOverlay = $("#productModalOverlay");
    const modalClose = $("#productModalClose");
    const modalTitle = $("#modalTitle");
    const modalBody = $("#modalBody");
    const modalCta = $("#modalCta");
    const detailBtns = $$(".product-detail-btn");
    if (!modal || detailBtns.length === 0) return;

    const productDetails = {
      ksara: {
        title: "كسارة اللحوم",
        content: `
          <p>كسارة متخصصة لتكسير اللحوم المجمدة حتى درجة -40 مئوية. مصنعة بالكامل من ستانلس 304 مع شفرات حادة ومتينة.</p>
          <h4>المواصفات التقنية:</h4>
          <ul>
            <li>الخامة: ستانلس 304 أصلي</li>
            <li>الموتور: تركي - 3-7 كيلو وات</li>
            <li>القدرة: 500-2000 كجم/ساعة</li>
            <li>الجهد: 220V/380V</li>
            <li>الأبعاد: حسب الطلب</li>
          </ul>
          <h4>المميزات:</h4>
          <ul>
            <li>شفرات قابلة للاستبدال</li>
            <li>سهولة التنظيف والصيانة</li>
            <li>تصميم هيكلي قوي يتحمل الاستخدام المستمر</li>
            <li>ضمان 12 شهر شامل</li>
          </ul>
        `
      },
      hala: {
        title: "حلة استاندرد",
        content: `
          <p>حلة استاندرد لتحميل وتخزين المنتج والاستخدام على الماكينات. مصنعة من ستانلس 304 مع عجلات صناعية مقاومة.</p>
          <h4>المواصفات التقنية:</h4>
          <ul>
            <li>الخامة: ستانلس 304 أصلي</li>
            <li>السعة: 50-200 لتر</li>
            <li>العجلات: صناعية مقاومة للتآكل</li>
            <li>الأبعاد: حسب الطلب</li>
          </ul>
          <h4>المميزات:</h4>
          <ul>
            <li>سهولة الحركة والتنقل</li>
            <li>سطح ناعم يسهل التنظيف</li>
            <li>تصميم مريح للاستخدام اليومي</li>
            <li>ضمان 12 شهر شامل</li>
          </ul>
        `
      },
      mixer: {
        title: "ميكسر التوابل",
        content: `
          <p>ميكسر متخصص لتجهيز خلط متجانس للتوابل والمواد المضافة. قدرات مختلفة مع شفرات ستانلس وجودة خلط ثابتة.</p>
          <h4>المواصفات التقنية:</h4>
          <ul>
            <li>الخامة: ستانلس 304 أصلي</li>
            <li>الموتور: تركي/ألماني - 2-5 كيلو وات</li>
            <li>القدرة: 100-1000 لتر</li>
            <li>الجهد: 220V/380V</li>
            <li>سرعة الدوران: قابلة للتعديل</li>
          </ul>
          <h4>المميزات:</h4>
          <ul>
            <li>خلط متجانس بنسبة 99%</li>
            <li>شفرات قابلة للاستبدال</li>
            <li>لوحة تحكم رقمية</li>
            <li>ضمان 12 شهر شامل</li>
          </ul>
        `
      },
      makbs: {
        title: "مكبس بسطرمة",
        content: `
          <p>مكبس متخصص لضغط متساوي على جميع أطراف المنتج. قدرات مختلفة مع جودة كبس ثابتة.</p>
          <h4>المواصفات التقنية:</h4>
          <ul>
            <li>الخامة: ستانلس 304 وحديد مقاوم</li>
            <li>نوع الضغط: هيدروليكي/كهربائي</li>
            <li>قوة الضغط: حسب الطلب</li>
            <li>الأبعاد: حسب الطلب</li>
          </ul>
          <h4>المميزات:</h4>
          <ul>
            <li>ضغط متساوي على جميع الأطراف</li>
            <li>سهولة التشغيل والصيانة</li>
            <li>تصميم هيكلي قوي</li>
            <li>ضمان 12 شهر شامل</li>
          </ul>
        `
      },
      troly1: {
        title: "ترولي لانشون",
        content: `
          <p>ترولي مخصص لتحميل وتخزين منتج اللانشون. تصميم مخصص يسهل العمل اليومي.</p>
          <h4>المواصفات التقنية:</h4>
          <ul>
            <li>الخامة: ستانلس 304 أصلي</li>
            <li>السعة: 50-150 كجم</li>
            <li>العجلات: صناعية مقاومة</li>
            <li>الأبعاد: حسب الطلب</li>
          </ul>
          <h4>المميزات:</h4>
          <ul>
            <li>تصميم مخصص للانشون</li>
            <li>سهولة الحركة والتنقل</li>
            <li>سطح ناعم يسهل التنظيف</li>
            <li>ضمان 12 شهر شامل</li>
          </ul>
        `
      },
      troly2: {
        title: "ترولي صاجات",
        content: `
          <p>ترولي متخصص لتحميل وتخزين المنتج على صاجات متعددة. تصميم عملي يسهل الاستخدام.</p>
          <h4>المواصفات التقنية:</h4>
          <ul>
            <li>الخامة: ستانلس 304 أصلي</li>
            <li>عدد الصاجات: 10-30 صاج</li>
            <li>العجلات: صناعية مقاومة</li>
            <li>الأبعاد: حسب الطلب</li>
          </ul>
          <h4>المميزات:</h4>
          <ul>
            <li>تصميم عملي للاستخدام اليومي</li>
            <li>سهولة الحركة والتنقل</li>
            <li>سطح ناعم يسهل التنظيف</li>
            <li>ضمان 12 شهر شامل</li>
          </ul>
        `
      },
      qalep: {
        title: "قالب لانشون",
        content: `
          <p>قالب متخصص لتعبئة وتفريغ منتج اللانشون. دقة في التصنيع مع سطح ناعم يسهل التنظيف.</p>
          <h4>المواصفات التقنية:</h4>
          <ul>
            <li>الخامة: ستانلس 304 أصلي</li>
            <li>السعة: 2-10 كجم/قالب</li>
            <li>الأبعاد: حسب الطلب</li>
          </ul>
          <h4>المميزات:</h4>
          <ul>
            <li>سهولة التعبئة والتفريغ</li>
            <li>سطح ناعم يسهل التنظيف</li>
            <li>تصميم دقيق</li>
            <li>ضمان 12 شهر شامل</li>
          </ul>
        `
      },
      table1: {
        title: "ترابيزة ستانلس",
        content: `
          <p>ترابيزة صناعية مصنعة من ستانلس 304. سهلة في الاستخدام ودقة في التصنيع.</p>
          <h4>المواصفات التقنية:</h4>
          <ul>
            <li>الخامة: ستانلس 304 أصلي</li>
            <li>سمك الصاج: 1.5-3 مم</li>
            <li>الأبعاد: حسب الطلب</li>
          </ul>
          <h4>المميزات:</h4>
          <ul>
            <li>تصميم قوي يتحمل الاستخدام المستمر</li>
            <li>سطح ناعم يسهل التنظيف</li>
            <li>أرجل قابلة للتعديل</li>
            <li>ضمان 12 شهر شامل</li>
          </ul>
        `
      }
    };

    const openModal = (productKey) => {
      const details = productDetails[productKey];
      if (!details) return;
      modalTitle.textContent = details.title;
      modalBody.innerHTML = details.content;
      modalCta.href = "index.html#contact";
      modal.classList.add("active");
      modal.setAttribute("aria-hidden", "false");
      document.body.style.overflow = "hidden";
    };
    const closeModal = () => {
      modal.classList.remove("active");
      modal.setAttribute("aria-hidden", "true");
      document.body.style.overflow = "";
    };

    detailBtns.forEach(btn => {
      btn.addEventListener("click", (e) => {
        e.preventDefault();
        openModal(btn.getAttribute("data-product"));
      });
    });
    modalClose?.addEventListener("click", closeModal);
    modalOverlay?.addEventListener("click", closeModal);
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && modal.classList.contains("active")) closeModal();
    });
    modalCta?.addEventListener("click", closeModal);
  };
  initProductModal();

  // ================= FOOTER YEAR =================
  const yearEl = $("#year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // ================= CARD 3D TILT EFFECT =================
  const initCardTilt = () => {
    if (prefersReducedMotion || window.innerWidth < 768) return;
    const cards = $$(".card");
    cards.forEach(card => {
      let frame = null, isHovering = false;
      card.addEventListener("mouseenter", () => { isHovering = true; });
      card.addEventListener("mousemove", (e) => {
        if (!isHovering || prefersReducedMotion) return;
        if (frame) return;
        frame = requestAnimationFrame(() => {
          const rect = card.getBoundingClientRect();
          const x = e.clientX - rect.left;
          const y = e.clientY - rect.top;
          const rotateX = ((y - rect.height / 2) / rect.height) * -6;
          const rotateY = ((x - rect.width / 2) / rect.width) * 6;
          card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-8px)`;
          frame = null;
        });
      });
      card.addEventListener("mouseleave", () => {
        isHovering = false;
        if (frame) { cancelAnimationFrame(frame); frame = null; }
        card.style.transform = "";
      });
    });
  };
  initCardTilt();

  // ================= RIPPLE EFFECT =================
  const initRipple = () => {
    $$(".card, .btn").forEach(el => {
      el.addEventListener("click", (e) => {
        if (e.target.closest("a, button, input, select, textarea")) return;
        const circle = document.createElement("span");
        circle.className = "ripple";
        const rect = el.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        circle.style.cssText = `
          position: absolute; border-radius: 50%;
          background: rgba(212,168,67,0.3); transform: scale(0);
          animation: ripple 0.8s cubic-bezier(0.4, 0, 0.2, 1);
          pointer-events: none; width: ${size}px; height: ${size}px;
          left: ${e.clientX - rect.left - size / 2}px;
          top: ${e.clientY - rect.top - size / 2}px;
        `;
        el.appendChild(circle);
        setTimeout(() => circle.remove(), 800);
      });
    });
  };
  initRipple();

  // ================= KEYBOARD NAVIGATION =================
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      const navMenu = $("#navMenu");
      const navToggle = $("#navToggle");
      if (navMenu?.classList.contains("is-open")) {
        navMenu.classList.remove("is-open");
        navToggle?.classList.remove("is-open");
        navToggle?.setAttribute("aria-expanded", "false");
      }
      const modal = $("#productModal");
      if (modal?.classList.contains("active")) {
        modal.classList.remove("active");
        modal.setAttribute("aria-hidden", "true");
        document.body.style.overflow = "";
      }
    }
  });

  console.log("✅ Products page initialized successfully");
});
