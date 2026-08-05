// ============================================
// ROYAL STEEL EGYPT - PROFESSIONAL UI/UX
// Enhanced Interactions & Animations
// ============================================

document.addEventListener("DOMContentLoaded", () => {

  // ================= UTILITY FUNCTIONS =================
  const $ = (selector) => document.querySelector(selector);
  const $$ = (selector) => document.querySelectorAll(selector);
  const debounce = (fn, ms) => {
    let timeout;
    return (...args) => {
      clearTimeout(timeout);
      timeout = setTimeout(() => fn(...args), ms);
    };
  };
  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // ================= LOADING SCREEN =================
  const initLoader = () => {
    const loader = $("#loader");
    if (!loader) return;

    const minLoadTime = 1500;
    const startTime = Date.now();

    const hideLoader = () => {
      const elapsed = Date.now() - startTime;
      const remaining = Math.max(0, minLoadTime - elapsed);

      setTimeout(() => {
        loader.classList.add("hidden");
        document.body.style.overflow = "";

        setTimeout(() => {
          $(".hero__content")?.classList.add("animate-in");
          $(".hero__card")?.classList.add("animate-in");
        }, 300);
      }, remaining);
    };

    document.body.style.overflow = "hidden";

    if (document.readyState === "complete") {
      hideLoader();
    } else {
      window.addEventListener("load", hideLoader);
    }
  };
  initLoader();

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

  // ================= THEME TOGGLE =================
  const initThemeToggle = () => {
    const themeToggle = $("#themeToggle");
    const themeIcon = themeToggle?.querySelector(".theme-toggle__icon");
    if (!themeToggle) return;

    const savedTheme = localStorage.getItem("theme");
    const systemPrefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;

    const applyTheme = (isLight) => {
      document.body.classList.toggle("light-mode", isLight);
      if (themeIcon) themeIcon.textContent = isLight ? "🌙" : "☀️";
      localStorage.setItem("theme", isLight ? "light" : "dark");
    };

    if (savedTheme === "light") {
      applyTheme(true);
    } else if (savedTheme === "dark") {
      applyTheme(false);
    } else if (!systemPrefersDark) {
      applyTheme(true);
    }

    themeToggle.addEventListener("click", () => {
      const isLight = !document.body.classList.contains("light-mode");
      applyTheme(isLight);

      const ripple = document.createElement("span");
      ripple.style.cssText = `
        position: absolute;
        width: 100px;
        height: 100px;
        background: rgba(212,168,67,0.3);
        border-radius: 50%;
        transform: scale(0);
        animation: ripple 0.6s ease-out;
        pointer-events: none;
      `;
      themeToggle.appendChild(ripple);
      setTimeout(() => ripple.remove(), 600);
    });
  };
  initThemeToggle();

  // ================= PARTICLES.JS =================
  const initParticles = () => {
    if (typeof particlesJS === "undefined" || !$("#particles-js")) return;

    particlesJS("particles-js", {
      particles: {
        number: { 
          value: 60, 
          density: { enable: true, value_area: 900 } 
        },
        color: { 
          value: ["#d4a843", "#7ba3c9", "#ffffff"] 
        },
        shape: { type: "circle" },
        opacity: { 
          value: 0.3, 
          random: true,
          anim: { enable: true, speed: 0.5, opacity_min: 0.1, sync: false }
        },
        size: { 
          value: 3, 
          random: true,
          anim: { enable: true, speed: 2, size_min: 0.5, sync: false }
        },
        line_linked: {
          enable: true,
          distance: 180,
          color: "#d4a843",
          opacity: 0.12,
          width: 1
        },
        move: {
          enable: true,
          speed: 0.6,
          direction: "none",
          random: true,
          straight: false,
          out_mode: "out",
          bounce: false,
          attract: { enable: true, rotateX: 600, rotateY: 1200 }
        }
      },
      interactivity: {
        detect_on: "canvas",
        events: {
          onhover: { enable: true, mode: "grab" },
          onclick: { enable: true, mode: "push" },
          resize: true
        },
        modes: {
          grab: { distance: 160, line_linked: { opacity: 0.3 } },
          push: { particles_nb: 4 },
          repulse: { distance: 100, duration: 0.4 }
        }
      },
      retina_detect: true
    });
  };
  initParticles();

  // ================= TYPED.JS =================
  const initTyped = () => {
    if (typeof Typed === "undefined" || !$(".typed-text")) return;

    new Typed(".typed-text", {
      strings: [
        "ماكينات احترافية",
        "خطوط إنتاج متكاملة",
        "معدات غذائية",
        "ستانلس 304"
      ],
      typeSpeed: 70,
      backSpeed: 40,
      backDelay: 2500,
      startDelay: 800,
      loop: true,
      showCursor: true,
      cursorChar: "|",
      smartBackspace: true
    });
  };
  initTyped();

  // ================= COUNTUP.JS =================
  const initCounters = () => {
    const counters = $$(".counter");
    if (counters.length === 0 || typeof countUp === "undefined") return;

    const countUpOptions = {
      duration: 2.5,
      useEasing: true,
      useGrouping: true,
      separator: ",",
      suffix: "+"
    };

    const countObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const target = parseInt(entry.target.getAttribute("data-target"));
          const countUpInstance = new countUp.CountUp(entry.target, target, countUpOptions);
          if (!countUpInstance.error) {
            countUpInstance.start(() => {
              entry.target.style.textShadow = "0 0 20px rgba(212,168,67,0.5)";
              setTimeout(() => {
                entry.target.style.textShadow = "";
              }, 1000);
            });
          }
          countObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });

    counters.forEach(counter => countObserver.observe(counter));
  };
  initCounters();

  // ================= SWIPER (TESTIMONIALS) =================
  const initSwiper = () => {
    if (typeof Swiper === "undefined" || !$(".testimonial-swiper")) return;

    new Swiper(".testimonial-swiper", {
      slidesPerView: 1,
      spaceBetween: 24,
      loop: true,
      autoplay: {
        delay: 5000,
        disableOnInteraction: false,
        pauseOnMouseEnter: true
      },
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
        dynamicBullets: true
      },
      breakpoints: {
        640: { slidesPerView: 2, spaceBetween: 20 },
        1024: { slidesPerView: 3, spaceBetween: 30 }
      },
      effect: "slide",
      speed: 600,
      grabCursor: true
    });
  };
  initSwiper();

  // ================= MOBILE NAVIGATION =================
  const initMobileNav = () => {
    const navToggle = $("#navToggle");
    const navMenu = $("#navMenu");
    if (!navToggle || !navMenu) return;

    let isAnimating = false;

    const openMenu = () => {
      if (isAnimating) return;
      isAnimating = true;

      navMenu.classList.remove("is-closing");
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
      navMenu.classList.add("is-closing");
      navToggle.classList.remove("is-open");
      navToggle.setAttribute("aria-expanded", "false");
      document.body.style.overflow = "";

      setTimeout(() => {
        navMenu.classList.remove("is-closing");
        isAnimating = false;
      }, 250);
    };

    navToggle.addEventListener("click", () => {
      if (navMenu.classList.contains("is-open")) {
        closeMenu();
      } else {
        openMenu();
      }
    });

    navMenu.querySelectorAll("a").forEach(link => {
      link.addEventListener("click", () => {
        closeMenu();
      });
    });

    document.addEventListener("click", (e) => {
      if (navMenu.classList.contains("is-open") && 
          !navMenu.contains(e.target) && 
          !navToggle.contains(e.target)) {
        closeMenu();
      }
    });

    // Close on escape key
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && navMenu.classList.contains("is-open")) {
        closeMenu();
      }
    });
  };
  initMobileNav();

  // ================= ACTIVE NAV LINK =================
  const initActiveNav = () => {
    const sections = $$("section[id]");
    const navLinks = $$('.nav__menu a[href^="#"]');

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const id = entry.target.getAttribute("id");
          navLinks.forEach(link => {
            link.classList.toggle("active", link.getAttribute("href") === `#${id}`);
          });
        }
      });
    }, { threshold: 0.3, rootMargin: "-80px 0px 0px 0px" });

    sections.forEach(section => observer.observe(section));
  };
  initActiveNav();

  // ================= SCROLL REVEAL =================
  const initScrollReveal = () => {
    if (prefersReducedMotion) return;

    const reveals = $$(".reveal");
    if (reveals.length === 0) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry, index) => {
        if (entry.isIntersecting) {
          setTimeout(() => {
            entry.target.classList.add("active");
          }, index * 100);
          observer.unobserve(entry.target);
        }
      });
    }, { 
      threshold: 0.1, 
      rootMargin: "0px 0px -80px 0px" 
    });

    reveals.forEach(el => observer.observe(el));
  };
  initScrollReveal();

  // ================= HEADER SCROLL EFFECT =================
  const initHeaderScroll = () => {
    const header = $(".header");
    if (!header) return;

    let lastScroll = 0;

    window.addEventListener("scroll", debounce(() => {
      const currentScroll = window.scrollY;

      if (currentScroll > 100) {
        header.classList.add("header--scrolled");
      } else {
        header.classList.remove("header--scrolled");
      }

      if (currentScroll > lastScroll && currentScroll > 300) {
        header.style.transform = "translateY(-100%)";
      } else {
        header.style.transform = "translateY(0)";
      }

      lastScroll = currentScroll;
    }, 10), { passive: true });
  };
  initHeaderScroll();

  // ================= SMOOTH SCROLL =================
  const initSmoothScroll = () => {
    $$('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener("click", (e) => {
        e.preventDefault();
        const targetId = anchor.getAttribute("href");
        const target = $(targetId);
        if (!target) return;

        const headerHeight = $(".header")?.offsetHeight || 0;
        const targetPosition = target.getBoundingClientRect().top + window.scrollY - headerHeight - 20;

        window.scrollTo({
          top: targetPosition,
          behavior: prefersReducedMotion ? "auto" : "smooth"
        });
      });
    });
  };
  initSmoothScroll();

  // ================= SCROLL TO TOP =================
  const initScrollTop = () => {
    const scrollTopBtn = $("#scrollTopBtn");
    if (!scrollTopBtn) return;

    window.addEventListener("scroll", debounce(() => {
      if (window.scrollY > 500) {
        scrollTopBtn.classList.add("show");
      } else {
        scrollTopBtn.classList.remove("show");
      }
    }, 50), { passive: true });

    scrollTopBtn.addEventListener("click", () => {
      window.scrollTo({
        top: 0,
        behavior: prefersReducedMotion ? "auto" : "smooth"
      });
    });
  };
  initScrollTop();

  // ================= PARALLAX EFFECT =================
  const initParallax = () => {
    if (prefersReducedMotion) return;

    const hero = $(".hero");
    if (!hero) return;

    window.addEventListener("scroll", () => {
      const scrolled = window.scrollY;
      if (scrolled < 800) {
        const yPos = scrolled * 0.3;
        hero.style.backgroundPositionY = `${yPos}px`;
      }
    }, { passive: true });
  };
  initParallax();

  // ================= CARD 3D TILT EFFECT =================
  const initCardTilt = () => {
    if (prefersReducedMotion || window.innerWidth < 768) return;

    const cards = $$(".card, .feature, .testimonial-card");

    cards.forEach(card => {
      let frame = null;
      let isHovering = false;

      card.addEventListener("mouseenter", () => { 
        isHovering = true; 
      });

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
        if (frame) {
          cancelAnimationFrame(frame);
          frame = null;
        }
        card.style.transform = "";
      });
    });
  };
  initCardTilt();

  // ================= RIPPLE EFFECT ON CARDS =================
  const initRipple = () => {
    $$(".card, .feature, .btn").forEach(el => {
      el.addEventListener("click", (e) => {
        if (e.target.closest("a, button, input, select, textarea")) return;

        const circle = document.createElement("span");
        circle.className = "ripple";

        const rect = el.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);

        circle.style.cssText = `
          width: ${size}px;
          height: ${size}px;
          left: ${e.clientX - rect.left - size / 2}px;
          top: ${e.clientY - rect.top - size / 2}px;
        `;

        el.appendChild(circle);
        setTimeout(() => circle.remove(), 800);
      });
    });
  };
  initRipple();

  // ================= FAQ ACCORDION =================
  const initFAQ = () => {
    const faqItems = $$('.faq-item');
    if (faqItems.length === 0) return;

    faqItems.forEach(item => {
      const question = item.querySelector('.faq-question');
      if (!question) return;

      question.addEventListener('click', () => {
        const isActive = item.classList.contains('active');

        // Close all other items
        faqItems.forEach(otherItem => {
          otherItem.classList.remove('active');
          otherItem.querySelector('.faq-question')?.setAttribute('aria-expanded', 'false');
        });

        // Toggle current item
        if (!isActive) {
          item.classList.add('active');
          question.setAttribute('aria-expanded', 'true');
        }
      });
    });
  };
  initFAQ();

  // ================= PRODUCT DETAIL MODAL =================
  const initProductModal = () => {
    const modal = $('#productModal');
    const modalOverlay = $('#productModalOverlay');
    const modalClose = $('#productModalClose');
    const modalTitle = $('#modalTitle');
    const modalBody = $('#modalBody');
    const modalCta = $('#modalCta');
    const detailBtns = $$('.product-detail-btn');

    if (!modal || detailBtns.length === 0) return;

    const productDetails = {
      ksara: {
        title: 'كسارة اللحوم',
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
        title: 'حلة استاندرد',
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
        title: 'ميكسر التوابل',
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
        title: 'مكبس بسطرمة',
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
      'troly1': {
        title: 'ترولي لانشون',
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
      'troly2': {
        title: 'ترولي صاجات',
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
        title: 'قالب لانشون',
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
        title: 'ترابيزة ستانلس',
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
      modalCta.href = '#contact';
      modal.classList.add('active');
      modal.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
    };

    const closeModal = () => {
      modal.classList.remove('active');
      modal.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
    };

    detailBtns.forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        const product = btn.getAttribute('data-product');
        openModal(product);
      });
    });

    modalClose?.addEventListener('click', closeModal);
    modalOverlay?.addEventListener('click', closeModal);

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && modal.classList.contains('active')) {
        closeModal();
      }
    });

    modalCta?.addEventListener('click', (e) => {
      closeModal();
    });
  };
  initProductModal();

  // ================= FORM INTERACTIONS =================
  const initFormInteractions = () => {
    const inputs = $$("input, select, textarea");

    inputs.forEach(input => {
      input.addEventListener("focus", () => {
        input.parentElement?.classList.add("focused");
      });

      input.addEventListener("blur", () => {
        input.parentElement?.classList.remove("focused");
        if (input.value) {
          input.parentElement?.classList.add("filled");
        } else {
          input.parentElement?.classList.remove("filled");
        }
      });

      if (input.value) {
        input.parentElement?.classList.add("filled");
      }
    });
  };
  initFormInteractions();

  // ================= WHATSAPP FORM =================
  // initWhatsAppForm();

  // ================= FOOTER YEAR =================
  const initFooterYear = () => {
    const yearEl = $("#year");
    if (yearEl) yearEl.textContent = new Date().getFullYear();
  };
  initFooterYear();

  // ================= MAGNETIC BUTTONS =================
  const initMagneticButtons = () => {
    if (prefersReducedMotion || window.innerWidth < 768) return;

    $$(".btn, .whatsapp-float").forEach(btn => {
      btn.addEventListener("mousemove", (e) => {
        const rect = btn.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;

        btn.style.transform = `translate(${x * 0.15}px, ${y * 0.15}px)`;
      });

      btn.addEventListener("mouseleave", () => {
        btn.style.transform = "";
      });
    });
  };
  initMagneticButtons();

  // ================= CURSOR GLOW EFFECT =================
  const initCursorGlow = () => {
    if (prefersReducedMotion || window.innerWidth < 1024) return;

    const cursor = document.createElement("div");
    cursor.className = "cursor-glow";
    cursor.style.cssText = `
      position: fixed;
      width: 300px;
      height: 300px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(212,168,67,0.06), transparent 70%);
      pointer-events: none;
      z-index: 9998;
      transform: translate(-50%, -50%);
      transition: opacity 0.3s ease;
      opacity: 0;
    `;
    document.body.appendChild(cursor);

    let mouseX = 0, mouseY = 0;
    let cursorX = 0, cursorY = 0;

    document.addEventListener("mousemove", (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
      cursor.style.opacity = "1";
    });

    document.addEventListener("mouseleave", () => {
      cursor.style.opacity = "0";
    });

    const animateCursor = () => {
      cursorX += (mouseX - cursorX) * 0.08;
      cursorY += (mouseY - cursorY) * 0.08;
      cursor.style.left = cursorX + "px";
      cursor.style.top = cursorY + "px";
      requestAnimationFrame(animateCursor);
    };
    animateCursor();
  };
  initCursorGlow();

  // ================= INTERSECTION OBSERVER FOR STATS =================
  const initStatsObserver = () => {
    const statsSection = $("#home");
    if (!statsSection) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          $$(".stat").forEach((stat, i) => {
            setTimeout(() => {
              stat.style.animation = "fadeInUp 0.6s ease-out forwards";
            }, i * 150);
          });
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.3 });

    observer.observe(statsSection);
  };
  initStatsObserver();

  // ================= LAZY LOAD IMAGES =================
  const initLazyLoad = () => {
    const images = $$("img[data-src], .card-img");

    const imageObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          if (img.dataset.src) {
            img.src = img.dataset.src;
            img.removeAttribute("data-src");
          }
          img.style.opacity = "0";
          img.style.transition = "opacity 0.5s ease";

          img.onload = () => {
            img.style.opacity = "1";
          };

          imageObserver.unobserve(img);
        }
      });
    }, { threshold: 0.1, rootMargin: "50px" });

    images.forEach(img => imageObserver.observe(img));
  };
  initLazyLoad();

  // ================= KEYBOARD NAVIGATION =================
  const initKeyboardNav = () => {
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") {
        const navMenu = $("#navMenu");
        const navToggle = $("#navToggle");
        if (navMenu?.classList.contains("is-open")) {
          navMenu.classList.remove("is-open");
          navToggle?.setAttribute("aria-expanded", "false");
          navToggle && (navToggle.textContent = "☰");
          navToggle && (navToggle.style.transform = "");
        }

        const modal = $('#productModal');
        if (modal?.classList.contains('active')) {
          modal.classList.remove('active');
          modal.setAttribute('aria-hidden', 'true');
          document.body.style.overflow = '';
        }
      }
    });
  };
  initKeyboardNav();

  // ================= PREFERS REDUCED MOTION LISTENER =================
  const initReducedMotionListener = () => {
    const mediaQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
    mediaQuery.addEventListener("change", (e) => {
      if (e.matches) {
        $$(".reveal").forEach(el => el.classList.add("active"));
      }
    });
  };
  initReducedMotionListener();

  // ================= CATALOG DOWNLOAD =================
  const initCatalogDownload = () => {
    const catalogBtn = $('#downloadCatalog');
    if (!catalogBtn) return;

    catalogBtn.addEventListener('click', (e) => {
      e.preventDefault();
      alert('الكتالوج قيد الإعداد. تواصل معنا مباشرة للحصول على المواصفات التفصيلية.');
    });
  };
  initCatalogDownload();



  // ================= CLIENTS TABS =================
  const initClientsTabs = () => {
    const tabBtns = $$('.clients-tab-btn');
    const tabContents = $$('.logos-grid');

    if (tabBtns.length === 0) return;

    tabBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const targetTab = btn.getAttribute('data-clients-tab');

        // Remove active from all buttons
        tabBtns.forEach(b => b.classList.remove('active'));
        // Add active to clicked button
        btn.classList.add('active');

        // Hide all grids
        tabContents.forEach(content => {
          content.classList.remove('active');
        });

        // Show target grid
        const targetContent = $(`#clients-${targetTab}`);
        if (targetContent) {
          targetContent.classList.add('active');

          // Re-trigger reveal animation for visible items
          const items = targetContent.querySelectorAll('.logo-item');
          items.forEach((item, index) => {
            item.classList.remove('active');
            setTimeout(() => {
              item.classList.add('active');
            }, index * 60);
          });
        }

        // Show/hide international info box
        const infoBox = $('#intlInfoBox');
        if (infoBox) {
          if (targetTab === 'international') {
            infoBox.style.display = '';
            setTimeout(() => infoBox.classList.add('active'), 100);
          } else {
            infoBox.style.display = 'none';
            infoBox.classList.remove('active');
          }
        }
      });
    });
  };
  initClientsTabs();

  // ================= CLIENTS LOGO INTERACTIONS =================
  const initClientsLogos = () => {
    const logoItems = $$('.logo-item');

    logoItems.forEach(item => {
      // Add click ripple effect
      item.addEventListener('click', (e) => {
        const circle = document.createElement('span');
        circle.className = 'ripple';

        const rect = item.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);

        circle.style.cssText = `
          width: ${size}px;
          height: ${size}px;
          left: ${e.clientX - rect.left - size / 2}px;
          top: ${e.clientY - rect.top - size / 2}px;
        `;

        item.appendChild(circle);
        setTimeout(() => circle.remove(), 800);
      });

      // Add 3D tilt effect on desktop
      if (!prefersReducedMotion && window.innerWidth >= 768) {
        let frame = null;
        let isHovering = false;

        item.addEventListener('mouseenter', () => { isHovering = true; });

        item.addEventListener('mousemove', (e) => {
          if (!isHovering || prefersReducedMotion) return;
          if (frame) return;

          frame = requestAnimationFrame(() => {
            const rect = item.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const rotateX = ((y - rect.height / 2) / rect.height) * -3;
            const rotateY = ((x - rect.width / 2) / rect.width) * 3;

            item.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-6px)`;
            frame = null;
          });
        });

        item.addEventListener('mouseleave', () => {
          isHovering = false;
          if (frame) {
            cancelAnimationFrame(frame);
            frame = null;
          }
          item.style.transform = '';
        });
      }
    });
  };
  initClientsLogos();

  console.log("✅ Royal Steel Egypt - UI/UX initialized successfully");
});