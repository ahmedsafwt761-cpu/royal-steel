// مكبس بسطرمة - Royal Steel Egypt

document.addEventListener('DOMContentLoaded', function() {
  const productName = 'مكبس بسطرمة';

  // Mobile menu
  const toggle = document.querySelector('.navbar__toggle');
  const menu = document.querySelector('.navbar__menu');
  if (toggle && menu) {
    toggle.addEventListener('click', () => {
      menu.classList.toggle('active');
      toggle.textContent = menu.classList.contains('active') ? '✕' : '☰';
    });
  }

  // Quote form
  const form = document.getElementById('quoteForm');
  if (form) {
    form.addEventListener('submit', function(e) {
      e.preventDefault();
      const name = form.querySelector('[name="name"]')?.value.trim();
      const phone = form.querySelector('[name="phone"]')?.value.trim();

      if (!name || !phone) {
        showToast('الرجاء إدخال الاسم والموبايل', 'error');
        return;
      }

      const email = form.querySelector('[name="email"]')?.value.trim() || '';
      const company = form.querySelector('[name="company"]')?.value.trim() || '';
      const message = form.querySelector('[name="message"]')?.value.trim() || '';

      let msg = `طلب عرض سعر - ${productName}\n\nالاسم: ${name}\nالموبايل: ${phone}`;
      if (email) msg += `\nالإيميل: ${email}`;
      if (company) msg += `\nالشركة: ${company}`;
      if (message) msg += `\n\nالتفاصيل: ${message}`;

      const btn = form.querySelector('button[type="submit"]');
      const original = btn.innerHTML;
      btn.innerHTML = '⏳ جاري الإرسال...';
      btn.disabled = true;

      setTimeout(() => {
        window.open(`https://wa.me/201225585826?text=${encodeURIComponent(msg)}`, '_blank');
        showToast('تم فتح واتساب!', 'success');
        btn.innerHTML = original;
        btn.disabled = false;
        form.reset();
      }, 700);
    });
  }

  // Toast
  function showToast(message, type = 'info') {
    let container = document.querySelector('.toast-container');
    if (!container) {
      container = document.createElement('div');
      container.className = 'toast-container';
      document.body.appendChild(container);
    }
    const toast = document.createElement('div');
    toast.className = `toast toast--${type}`;
    toast.innerHTML = type === 'success' ? '✓ ' + message : '✕ ' + message;
    container.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
  }
  window.showToast = showToast;

  // Smooth scroll
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const id = a.getAttribute('href');
      if (id === '#') return;
      const el = document.querySelector(id);
      if (el) { e.preventDefault(); el.scrollIntoView({ behavior: 'smooth' }); }
    });
  });

  console.log('✅ مكبس بسطرمة Page Loaded');
});