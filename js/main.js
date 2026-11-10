(function () {
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const toggle = document.querySelector(".menu-toggle");
  const panel = document.querySelector(".nav-panel");
  const header = document.querySelector(".site-header");
  const cfg = window.WEBAUR_SITE || {};
  const email = String(cfg.CONTACT_EMAIL || "").trim();
  const formspreeRaw = String(cfg.FORMSPREE_ID || "").trim();
  const fi = document.documentElement.lang === "fi";

  function formspreeUrl() {
    if (!formspreeRaw) return "";
    if (/^https?:\/\//i.test(formspreeRaw)) return formspreeRaw;
    return "https://formspree.io/f/" + formspreeRaw.replace(/^\/+/, "");
  }

  function setMenu(open) {
    if (!toggle || !panel) return;
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open
      ? (fi ? "Sulje valikko" : "Close menu")
      : (fi ? "Avaa valikko" : "Open menu"));
    panel.classList.toggle("is-open", open);
    document.body.classList.toggle("menu-open", open);
    if (open) {
      const first = panel.querySelector("a");
      if (first) first.focus();
    } else {
      toggle.focus();
    }
  }

  if (toggle && panel) {
    toggle.addEventListener("click", function () {
      setMenu(toggle.getAttribute("aria-expanded") !== "true");
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
        setMenu(false);
      }
      if (e.key === "Tab" && toggle.getAttribute("aria-expanded") === "true") {
        const focusable = [toggle].concat(Array.from(panel.querySelectorAll("a, button")));
        const first = focusable[0], last = focusable[focusable.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });
    panel.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () { setMenu(false); });
    });
    window.addEventListener("resize", function () {
      if (window.innerWidth > 767 && toggle.getAttribute("aria-expanded") === "true") setMenu(false);
    });
  }

  if (header) {
    var onScroll = function () { header.classList.toggle("is-scrolled", window.scrollY > 8); };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }
  if (reduce) document.querySelectorAll(".reveal").forEach(function (el) { el.style.animation = "none"; });

  // Reveal configured email; hide placeholders when unset.
  document.querySelectorAll("[data-email-slot]").forEach(function (slot) {
    if (!email) {
      var wrap = slot.closest(".js-email-wrap") || slot;
      wrap.hidden = true;
      return;
    }
    var a = document.createElement("a");
    a.href = "mailto:" + email;
    a.textContent = email;
    slot.replaceChildren(a);
    var wrap = slot.closest(".js-email-wrap");
    if (wrap) wrap.hidden = false;
  });

  var params = new URLSearchParams(window.location.search);
  var pkg = (params.get("package") || "").toLowerCase();
  var budget = document.getElementById("budget");
  if (budget && pkg) {
    var options = Array.from(budget.options);
    var found = options.find(function (o) { return (o.value || "").toLowerCase().indexOf(pkg) !== -1; });
    if (found) budget.value = found.value;
  }

  var form = document.querySelector("form[name='contact']");
  if (form) {
    var endpoint = formspreeUrl();
    var alertBox = document.getElementById("form-status");
    var submitBtn = form.querySelector("[type='submit']");
    var i18n = fi ? {
      required: "Tämä kenttä on pakollinen.",
      email: "Anna kelvollinen sähköpostiosoite.",
      consent: "Tarvitsemme suostumuksesi, jotta voimme vastata viestiisi.",
      sending: "Lähetetään…",
      success: "Kiitos, viestisi on vastaanotettu. Palaamme asiaan mahdollisimman pian.",
      error: "Lähetys ei onnistunut. Yritä uudelleen tai käytä sähköpostia, jos osoite on näkyvissä.",
      mailto: "Sähköpostiohjelmasi pitäisi avautua valmiilla viestillä. Jos näin ei käy, kopioi viesti ja lähetä se osoitteeseen, joka näkyy tällä sivulla.",
      unconfigured: "Yhteydenottolomaketta ei ole vielä kytketty lähetyspalveluun, eikä sähköpostiosoitetta ole julkaistu. Viestiä ei lähetetty. Lisää FORMSPREE_ID tai CONTACT_EMAIL tiedostoon js/site-config.js."
    } : {
      required: "This field is required.",
      email: "Please enter a valid email address.",
      consent: "Please confirm we may use this information to reply.",
      sending: "Sending…",
      success: "Thank you — your message has been received. We will get back to you as soon as we can.",
      error: "The message could not be sent. Please try again, or use the email address on this page if one is shown.",
      mailto: "Your email app should open with a prepared message. If it does not, copy the message and send it to the address shown on this page.",
      unconfigured: "This form is not connected to a sending service yet, and no public email address has been published. No message was sent. Add FORMSPREE_ID or CONTACT_EMAIL in js/site-config.js."
    };

    function showAlert(kind, text) {
      if (!alertBox) return;
      alertBox.hidden = false;
      alertBox.classList.remove("is-error", "is-success", "is-info");
      if (kind) alertBox.classList.add("is-" + kind);
      alertBox.textContent = text;
      alertBox.focus();
    }

    function msg(el, text) {
      var err = el.parentElement.querySelector(".field-error");
      if (!err) {
        err = document.createElement("p");
        err.className = "field-error";
        err.id = el.id + "-error";
        el.parentElement.appendChild(err);
      }
      el.setAttribute("aria-invalid", text ? "true" : "false");
      if (text) el.setAttribute("aria-describedby", err.id);
      else el.removeAttribute("aria-describedby");
      err.textContent = text || "";
      err.hidden = !text;
    }

    function validate() {
      var ok = true;
      form.querySelectorAll("[required]").forEach(function (el) {
        if (el.type === "checkbox") {
          if (!el.checked) { msg(el, i18n.consent); ok = false; } else msg(el, "");
        } else if (!el.value.trim()) { msg(el, i18n.required); ok = false; }
        else if (el.type === "email" && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(el.value)) { msg(el, i18n.email); ok = false; }
        else msg(el, "");
      });
      return ok;
    }

    form.querySelectorAll("[required]").forEach(function (el) {
      el.addEventListener("blur", function () { validate(); });
    });

    function bodyText() {
      var lines = [];
      Array.from(form.elements).forEach(function (el) {
        if (!el.name || el.type === "submit" || el.name === "company-website") return;
        if (el.type === "checkbox") lines.push(el.name + ": " + (el.checked ? "yes" : "no"));
        else lines.push(el.name + ": " + (el.value || ""));
      });
      return lines.join("\n");
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!validate()) return;
      var hp = form.querySelector("[name='company-website']");
      if (hp && hp.value) return;

      if (endpoint) {
        if (submitBtn) { submitBtn.disabled = true; submitBtn.textContent = i18n.sending; }
        var data = new FormData(form);
        data.delete("company-website");
        fetch(endpoint, {
          method: "POST",
          body: data,
          headers: { Accept: "application/json" }
        }).then(function (res) {
          if (!res.ok) throw new Error("formspree");
          form.reset();
          showAlert("success", i18n.success);
        }).catch(function () {
          showAlert("error", i18n.error);
        }).finally(function () {
          if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.textContent = submitBtn.getAttribute("data-label") || (fi ? "Lähetä viesti" : "Send message");
          }
        });
        return;
      }

      if (email) {
        var subject = fi ? "Yhteydenotto WEBAURille" : "Enquiry for WEBAUR";
        var href = "mailto:" + encodeURIComponent(email) +
          "?subject=" + encodeURIComponent(subject) +
          "&body=" + encodeURIComponent(bodyText());
        window.location.href = href;
        showAlert("info", i18n.mailto);
        return;
      }

      form.classList.add("is-unconfigured");
      showAlert("info", i18n.unconfigured);
    });
  }
})();
