const API_BASE = "https://royal-steel-backend.onrender.com/api";

async function safeReadJson(response) {
  const text = await response.text();
  try {
    return JSON.parse(text);
  } catch {
    return { raw: text };
  }
}

function handleQuoteForm(formId, statusId, fixedSlug) {
  const form = document.getElementById(formId);
  const statusEl = document.getElementById(statusId);

  if (!form || !statusEl) {
    console.warn("Form/Status not found:", formId, statusId);
    return;
  }

  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const productSlug = fixedSlug || (form.product_slug ? form.product_slug.value : "");

    if (!productSlug) {
      statusEl.textContent = "من فضلك اختر نوع المنتج";
      statusEl.style.display = "block";
      return;
    }

    const payload = {
      product_slug: productSlug,
      name: (form.name?.value || "").trim(),
      phone: (form.phone?.value || "").trim(),
      email: (form.email?.value || "").trim(),
      company: (form.company?.value || "").trim(),
      message: (form.message?.value || "").trim(),
    };

    if (!payload.name || !payload.phone) {
      statusEl.textContent = "من فضلك اكتب الاسم ورقم الموبايل";
      statusEl.style.display = "block";
      return;
    }

    statusEl.textContent = "جاري الإرسال...";
    statusEl.style.display = "block";
    statusEl.style.color = "var(--accent-gold)";

    // 1. أولاً: ابعت للـ Backend (Django API)
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 15000);

    let apiSuccess = false;

    try {
      const res = await fetch(`${API_BASE}/quotes/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
        signal: controller.signal,
      });

      clearTimeout(timer);

      const data = await safeReadJson(res);

      if (res.ok) {
        apiSuccess = true;
        statusEl.textContent = "تم حفظ الطلب ✅ جاري فتح واتساب...";
        statusEl.style.color = "#10b981";
      } else {
        const msg = (data && (data.detail || data.error)) || "حصل خطأ في حفظ الطلب.";
        statusEl.textContent = msg;
        statusEl.style.color = "#ef4444";
        console.error("API error:", res.status, data);
      }
    } catch (err) {
      clearTimeout(timer);
      if (err.name === "AbortError") {
        statusEl.textContent = "السيرفر اتأخر في الرد.";
      } else {
        statusEl.textContent = "تعذر الاتصال بالسيرفر ❌";
      }
      statusEl.style.color = "#ef4444";
      console.error("Fetch error:", err);
    }

    // 2. بعدين: افتح واتساب (سواء نجح الـ API ولا لأ)
    const WHATSAPP_NUMBER = "201115709334";
    const msg = `طلب عرض سعر - Royal Steel Egypt
━━━━━━━━━━━━━━━━━━━━
👤 الاسم: ${payload.name}
📱 الموبايل: ${payload.phone}
📧 الإيميل: ${payload.email || "—"}
🏢 الشركة: ${payload.company || "—"}
🔧 نوع المنتج: ${productSlug}
📝 الطلب:
${payload.message}
━━━━━━━━━━━━━━━━━━━━`;

    const encoded = encodeURIComponent(msg);
    window.open(`https://wa.me/${WHATSAPP_NUMBER}?text=${encoded}`, "_blank", "noopener,noreferrer");

    // 3. لو الـ API نجح، امسح الـ Form
    if (apiSuccess) {
      setTimeout(() => {
        form.reset();
        statusEl.textContent = "تم الإرسال بنجاح! ✅";
        statusEl.style.color = "#10b981";
      }, 2000);
    }
  });
}

// Initialize the form when DOM is ready
document.addEventListener("DOMContentLoaded", () => {
  handleQuoteForm("homeQuoteForm", "homeFormStatus");
});