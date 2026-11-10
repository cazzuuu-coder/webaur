(function () {
  "use strict";
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var btn = document.querySelector(".menu-toggle");
  var panel = document.querySelector(".nav-links");
  function setOpen(open) {
    if (!btn || !panel) return;
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
      if (e.key === "Escape") setOpen(false);
    });
  }
  var form = document.getElementById("reserve-form");
  if (form) {
    var status = form.querySelector(".form-status");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!status) return;
      status.hidden = false;
      status.textContent = "This is a concept project by WEBAUR. The form does not send a reservation, and no details have been collected.";
      status.scrollIntoView({ block: "nearest", behavior: reduce ? "auto" : "smooth" });
    });
  }
})();
