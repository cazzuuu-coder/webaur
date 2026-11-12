(function () {
  "use strict";
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var btn = document.querySelector(".menu-toggle");
  var panel = document.querySelector(".nav-links");
  function pinPanel() {
    var h = document.querySelector(".site-header");
    if (!h || !panel) return;
    panel.style.top = Math.max(0, Math.round(h.getBoundingClientRect().bottom)) + "px";
  }
  function setOpen(open) {
    if (!btn || !panel) return;
    if (open) pinPanel();
    btn.setAttribute("aria-expanded", String(open));
    btn.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    panel.classList.toggle("is-open", open);
    document.body.classList.toggle("nav-open", open);
  }
  if (btn && panel) {
    btn.addEventListener("click", function () {
      setOpen(btn.getAttribute("aria-expanded") !== "true");
    });
    panel.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () { setOpen(false); });
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && btn.getAttribute("aria-expanded") === "true") { setOpen(false); btn.focus(); }
    });
    window.addEventListener("resize", function () {
      if (btn.getAttribute("aria-expanded") !== "true") return;
      if (window.innerWidth > 767) setOpen(false); else pinPanel();
    });
  }

  var form = document.getElementById("booking-form");
  if (form) {
    var status = form.querySelector(".form-status");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!status) return;
      status.hidden = false;
      status.textContent = "This is a concept project by WEBAUR. The form does not send a request, and no details have been collected. On a live studio site, this is where a real booking would begin.";
      status.focus && status.scrollIntoView({ block: "nearest", behavior: reduce ? "auto" : "smooth" });
    });
  }

  var shots = Array.prototype.slice.call(document.querySelectorAll(".shot"));
  var box = document.getElementById("lightbox");
  if (!shots.length || !box) return;
  var img = box.querySelector("img");
  var cap = box.querySelector(".lightbox-caption");
  var index = 0;

  function openAt(i) {
    index = (i + shots.length) % shots.length;
    var el = shots[index];
    img.src = el.getAttribute("data-full");
    img.alt = el.getAttribute("aria-label") || "";
    cap.textContent = el.getAttribute("data-caption") || "";
    box.hidden = false;
    box.classList.add("is-open");
    document.body.classList.add("lb-open");
    box.querySelector(".lightbox-close").focus();
  }
  function close() {
    box.classList.remove("is-open");
    box.hidden = true;
    document.body.classList.remove("lb-open");
    img.removeAttribute("src");
  }
  shots.forEach(function (el, i) {
    el.addEventListener("click", function () { openAt(i); });
  });
  box.querySelector(".lightbox-close").addEventListener("click", close);
  box.querySelector(".lightbox-prev").addEventListener("click", function () { openAt(index - 1); });
  box.querySelector(".lightbox-next").addEventListener("click", function () { openAt(index + 1); });
  document.addEventListener("keydown", function (e) {
    if (!box.classList.contains("is-open")) return;
    if (e.key === "Escape") close();
    if (e.key === "ArrowLeft") openAt(index - 1);
    if (e.key === "ArrowRight") openAt(index + 1);
  });
  box.addEventListener("click", function (e) {
    if (e.target === box) close();
  });
})();
