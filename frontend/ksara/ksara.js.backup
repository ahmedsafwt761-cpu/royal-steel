const orderBtn = document.getElementById("orderBtn");

orderBtn.addEventListener("click", () => {
  alert("سيتم تحويلك لطلب عرض سعر لمفرمة اللحوم");
});
const modal = document.getElementById("videoModal");
const openBtn = document.getElementById("openModalBtn");
const closeOverlay = document.getElementById("closeModal");
const closeBtn = document.getElementById("closeModalBtn");
const closeBtn2 = document.getElementById("closeModalBtn2");

function openModal(){
  modal.classList.add("is-open");
  modal.setAttribute("aria-hidden", "false");
}

function closeModal(){
  modal.classList.remove("is-open");
  modal.setAttribute("aria-hidden", "true");
}

if(openBtn) openBtn.addEventListener("click", openModal);
if(closeOverlay) closeOverlay.addEventListener("click", closeModal);
if(closeBtn) closeBtn.addEventListener("click", closeModal);
if(closeBtn2) closeBtn2.addEventListener("click", closeModal);

document.addEventListener("keydown", (e) => {
  if(e.key === "Escape") closeModal();
});