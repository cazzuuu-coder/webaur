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

  // Email links are rendered in the HTML; js/site-config.js stays the source of truth.
  document.querySelectorAll("[data-email-slot]").forEach(function (slot) {
    if (!email) {
      var wrap = slot.closest(".js-email-wrap") || slot;
      wrap.hidden = true;
      return;
    }
    var a = slot;
    if (slot.tagName !== "A") {
      a = document.createElement("a");
      slot.replaceChildren(a);
    }
    a.href = "mailto:" + email;
    a.textContent = email;
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
      mailto: "Sähköpostiohjelmasi avautuu nyt, ja viesti on valmiiksi täytetty. Tarkista se ja paina siellä Lähetä. Viestiä ei ole lähetetty ennen sitä. Jos mitään ei avautunut, kirjoita suoraan osoitteeseen ",
      unconfigured: "Lomakkeen lähetystä ei ole vielä otettu käyttöön, joten viestiä ei lähetetty. Yritä myöhemmin uudelleen.",
      send: "Lähetä viesti",
      subject: "Projektikysely",
      yes: "kyllä", no: "ei"
    } : {
      required: "This field is required.",
      email: "Please enter a valid email address.",
      consent: "Please confirm we may use this information to reply.",
      sending: "Sending…",
      success: "Thank you — your message has been received. We will get back to you as soon as we can.",
      error: "The message could not be sent. Please try again, or use the email address on this page if one is shown.",
      mailto: "Your email app is opening with the message filled in. Check it and press Send there — nothing has been sent until you do. If nothing opened, write directly to ",
      unconfigured: "Sending is not switched on for this form yet, so no message was sent. Please try again later.",
      send: "Send message",
      subject: "Project enquiry",
      yes: "yes", no: "no"
    };

    if (endpoint && submitBtn) {
      submitBtn.textContent = i18n.send;
      submitBtn.setAttribute("data-label", i18n.send);
    }

    function showAlert(kind, text, mail) {
      if (!alertBox) return;
      alertBox.hidden = false;
      alertBox.classList.remove("is-error", "is-success", "is-info");
      if (kind) alertBox.classList.add("is-" + kind);
      alertBox.textContent = text;
      if (mail) {
        var a = document.createElement("a");
        a.href = "mailto:" + mail;
        a.textContent = mail;
        alertBox.appendChild(a);
        alertBox.appendChild(document.createTextNode("."));
      }
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

    function validateField(el) {
      if (el.type === "checkbox") {
        if (!el.checked) { msg(el, i18n.consent); return false; }
      } else if (!el.value.trim()) { msg(el, i18n.required); return false; }
      else if (el.type === "email" && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(el.value.trim())) { msg(el, i18n.email); return false; }
      msg(el, "");
      return true;
    }

    function validate() {
      var ok = true, first = null;
      form.querySelectorAll("[required]").forEach(function (el) {
        if (!validateField(el)) { ok = false; if (!first) first = el; }
      });
      if (first) first.focus();
      return ok;
    }

    // Validate a field only after the visitor has interacted with it, so errors
    // never appear on fields they have not reached yet (and the layout stays put).
    form.querySelectorAll("[required]").forEach(function (el) {
      el.addEventListener("blur", function () {
        if (el.value.trim() || el.getAttribute("aria-invalid") === "true") validateField(el);
      });
      el.addEventListener(el.type === "checkbox" || el.tagName === "SELECT" ? "change" : "input", function () {
        if (el.getAttribute("aria-invalid") === "true") validateField(el);
      });
    });

    function labelFor(el) {
      var l = el.id && form.querySelector("label[for='" + el.id + "']");
      var t = l ? l.textContent : el.name;
      return t.replace(/\s*\((valinnainen|optional)\)\s*/i, "").trim();
    }

    function fieldValue(name) {
      var el = form.elements[name];
      return el ? String(el.value || "").trim() : "";
    }

    function bodyText() {
      var lines = [];
      var message = "";
      Array.from(form.elements).forEach(function (el) {
        if (!el.name || el.type === "submit" || el.name === "company-website") return;
        if (el.name === "message") { message = el.value.trim(); return; }
        if (el.type === "checkbox") { lines.push((fi ? "Suostumus" : "Consent") + ": " + (el.checked ? i18n.yes : i18n.no)); return; }
        var lbl = el.getAttribute("data-mail-label") || labelFor(el);
        var v = el.tagName === "SELECT" ? (el.value ? el.options[el.selectedIndex].text : "") : el.value.trim();
        if (v) lines.push(lbl + ": " + v);
      });
      return (fi ? "Hei WEBAUR,\n\n" : "Hello WEBAUR,\n\n") + message + "\n\n---\n" + lines.join("\n") + "\n";
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
        var business = fieldValue("business");
        var subject = i18n.subject + (business ? " – " + business : "");
        var href = "mailto:" + email +
          "?subject=" + encodeURIComponent(subject) +
          "&body=" + encodeURIComponent(bodyText());
        showAlert("info", i18n.mailto, email);
        window.location.href = href;
        return;
      }

      form.classList.add("is-unconfigured");
      showAlert("info", i18n.unconfigured);
    });
  }
})();
