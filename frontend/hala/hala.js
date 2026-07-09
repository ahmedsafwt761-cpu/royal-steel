console.log("mixer.js loaded");

// ===== زر الطلب (اختياري) =====
const orderBtn = document.getElementById("orderBtn");
if (orderBtn) {
  orderBtn.addEventListener("click", () => {
    alert("سيتم تحويلك لطلب عرض سعر");
  });
} else {
  console.warn("orderBtn مش موجود في الصفحة (ده طبيعي لو انت مش مستخدمه).");
}

// ===== Modal =====
const modal = document.getElementById("videoModal");
const openBtn = document.getElementById("openModalBtn");
const closeOverlay = document.getElementById("closeModal");
const closeBtn = document.getElementById("closeModalBtn");
const closeBtn2 = document.getElementById("closeModalBtn2");

function openModal() {
  if (!modal) return;
  modal.classList.add("is-open");
  modal.setAttribute("aria-hidden", "false");
}

function closeModal() {
  if (!modal) return;
  modal.classList.remove("is-open");
  modal.setAttribute("aria-hidden", "true");
}

if (openBtn) openBtn.addEventListener("click", openModal);
if (closeOverlay) closeOverlay.addEventListener("click", closeModal);
if (closeBtn) closeBtn.addEventListener("click", closeModal);
if (closeBtn2) closeBtn2.addEventListener("click", closeModal);

document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") closeModal();
});

// ===== Quote Form (ربط الفرونت بالباك اند) =====
const form = document.getElementById("quoteForm");
const statusEl = document.getElementById("formStatus");

// لازم يطابق slug في الـ Admin (بالإنجليزي)
const PRODUCT_SLUG = "mixer";

if (form && statusEl) {
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const payload = {
      product_slug: PRODUCT_SLUG,
      name: form.name.value.trim(),
      phone: form.phone.value.trim(),
      email: form.email.value.trim(),
      company: form.company.value.trim(),
      message: form.message.value.trim(),
    };

    // تحقق بسيط
    if (!payload.name || !payload.phone) {
      statusEl.textContent = "من فضلك اكتب الاسم ورقم الموبايل ✅";
      return;
    }

    statusEl.textContent = "جاري الإرسال...";

    try {
      console.log("Sending payload:", payload);

      const res = await fetch("http://127.0.0.1:8000/api/quotes/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      // أوقات السيرفر يرجّع نص بدل JSON
      const text = await res.text();
      let data;
      try {
        data = JSON.parse(text);
      } catch {
        data = { raw: text };
      }

      console.log("Response status:", res.status);
      console.log("Response body:", data);

      if (!res.ok) {
        statusEl.textContent = "حصل خطأ: " + JSON.stringify(data);
        return;
      }

      statusEl.textContent = "تم إرسال الطلب ✅";
      form.reset();
    } catch (err) {
      console.error("Fetch error:", err);
      statusEl.textContent = "تعذر الاتصال بالسيرفر ❌";
    }
  });
} else {
  console.warn("quoteForm أو formStatus مش موجودين في الصفحة — تأكد إن الفورم مكتوب في HTML وأن script تحت في آخر الصفحة.");
}
