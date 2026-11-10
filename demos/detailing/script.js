(function () {
  "use strict";
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var btn = document.querySelector(".menu-toggle");
  var panel = document.querySelector(".site-nav");
  function closeNav() {
    if (!btn || !panel) return;
    btn.setAttribute("aria-expanded", "false");
    btn.setAttribute("aria-label", "Open menu");
    panel.classList.remove("is-open");
    document.body.classList.remove("nav-open");
  }
  function openNav() {
    btn.setAttribute("aria-expanded", "true");
    btn.setAttribute("aria-label", "Close menu");
    panel.classList.add("is-open");
    document.body.classList.add("nav-open");
  }
  if (btn && panel) {
    btn.addEventListener("click", function () {
      if (btn.getAttribute("aria-expanded") === "true") closeNav();
      else openNav();
    });
    panel.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", closeNav);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeNav();
    });
  }

  function setupCompare(root) {
    var frame = root.querySelector(".compare-frame");
    var clip = root.querySelector(".compare-before-clip");
    var rule = root.querySelector(".compare-rule");
    var range = root.querySelector(".compare-range");
    var beforeImgs = clip ? clip.querySelectorAll("img") : [];
    if (!frame || !clip || !rule || !range) return;

    function syncImageWidth() {
      var w = frame.clientWidth + "px";
      beforeImgs.forEach(function (img) {
        img.style.width = w;
        img.style.maxWidth = "none";
        img.style.height = "100%";
        img.style.objectFit = "cover";
      });
    }
    function set(value) {
      var pct = Math.max(0, Math.min(100, Number(value)));
      clip.style.width = pct + "%";
      rule.style.left = pct + "%";
      range.value = String(pct);
      range.setAttribute("aria-valuenow", String(Math.round(pct)));
    }
    range.addEventListener("input", function (e) { set(e.target.value); });
    range.addEventListener("change", function (e) { set(e.target.value); });
    window.addEventListener("resize", syncImageWidth);
    if (window.ResizeObserver) new ResizeObserver(syncImageWidth).observe(frame);
    syncImageWidth();
    set(range.value || 50);
  }
  document.querySelectorAll(".compare").forEach(setupCompare);

  var form = document.getElementById("enquiry");
  if (form) {
    var status = form.querySelector(".form-status");
    var params = new URLSearchParams(window.location.search);
    var preset = params.get("package");
    var select = form.querySelector("#package");
    if (preset && select) {
      var allowed = ["essential", "signature", "atelier", "unsure"];
      if (allowed.indexOf(preset) !== -1) select.value = preset;
    }
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!status) return;
      status.hidden = false;
      status.textContent = "This is a concept project by WEBAUR. The form does not send a message, and no details have been collected.";
      status.focus && status.scrollIntoView({ block: "nearest", behavior: reduce ? "auto" : "smooth" });
    });
  }
})();
