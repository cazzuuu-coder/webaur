# WEBAUR website (v7)

Independent web design studio site — static HTML, CSS and JavaScript. No required build step.

Finnish is the default language at the site root. English lives in `/en/`. Studio pages are generated from `_tools/build_pages.py`. Concept demos in `demos/` were rebuilt in v6 with distinct typography, multi-page layouts and self-hosted fonts. They remain fictional concept projects.

## Hosting and local preview

Live at `https://webaur.com/` (GitHub Pages, repository `cazzuuu-coder/webaur`, repo root = this folder, custom domain set in `CNAME`).

Internal links, images, fonts, CSS, JavaScript and demos use relative paths, so the site also works in any subfolder. The exception is `404.html`, which uses absolute `/…` paths because GitHub Pages serves it at whatever URL was missing.

```bash
# from this folder
python3 -m http.server 8768 --bind 127.0.0.1
```

Open `http://127.0.0.1:8768/`.

Canonical, Open Graph and sitemap URLs use `https://webaur.com/` (`SITE` and `SITE_PATH` in `_tools/build_pages.py`).

## Languages

- Finnish (default): `index.html`, `services.html`, `pricing.html`, `work.html`, `about.html`, `contact.html`, `privacy.html`, `thanks.html`, `404.html`, and `work/*.html`
- English: the same files under `en/`
- Every studio page has an `hreflang` set (`fi`, `en`, `x-default` → Finnish) and a FI / EN switcher
- Concept demos keep their own brand language. Portfolio descriptions around them are translated.

The Finnish copy was written to sound like natural professional Finnish. A native speaker should still proofread it before launch.

## Pages and demos

- Studio pages as listed above, in both languages
- Pricing (`pricing.html`, also summarised on the home page): Starter €490, Business €890, Premium €1,490
- Work: three concept projects with distinct layouts, large previews, and links to the live demo and the case study
- Case studies: brief, audience, brand identity, page-by-page walkthrough, features and design decisions. All three are labelled as concept projects
- Working concept demos (`noindex`, labelled as concepts; booking buttons do not place a real booking):
  - `demos/barber-studio/` — Hale Barber Studio
  - `demos/detailing/` — Alto Detail
  - `demos/maison-cafe/` — Maison Café

Portfolio screenshots live in `images/work/{hale,alto,maison}/` as AVIF, WebP and JPEG.

## Contact form

**Pages:** `contact.html` and `en/contact.html`. Behaviour is in `js/main.js`.

**Configuration:** `js/site-config.js`

```js
window.WEBAUR_SITE = {
  CONTACT_EMAIL: "hello@webaur.com",
  FORMSPREE_ID: ""
};
```

- With only `CONTACT_EMAIL` set (current setup), the form validates the fields and opens the visitor's own email app with a prepared message to that address (subject "Projektikysely – {business}" / "Project enquiry – {business}"). Nothing is sent until the visitor presses Send in their email app, and the page says so.
- If `FORMSPREE_ID` is set, the form is sent through Formspree instead and the button label changes to "Lähetä viesti" / "Send message".
- The address is also written into the HTML (footer, contact, privacy, thanks) by `_tools/build_pages.py` (`EMAIL`), so it shows without JavaScript. Keep the two values the same.

**Important:** the `hello@webaur.com` mailbox must be created before messages can arrive. Until then, emails sent to the address will bounce.

Budget can be pre-filled with `?package=starter|business|premium#form`.

## Pricing

- Starter €490 — one long single page with several sections
- Business €890 (recommended) — up to 5 separate pages in one website
- Premium €1,490 — up to 8 separate pages, plus more individual design and light animations

One-time payment. The customer owns the site and receives the source code, files and publishing/transfer instructions; no monthly fees or service agreements are offered. Not included: yearly domain fee, hosting, online stores, extensive booking systems, other special features, and new change work after launch (done on request for a separately agreed one-time fee). Package copy lives in `PKG` / `TXT` in `_tools/build_pages.py`.

## Still to complete before a full commercial launch

- Create the `hello@webaur.com` mailbox (the domain is registered; the address is already on the site)
- Legal name, business ID and postal address in the privacy policy
- A native Finnish proofread

Concept locations in the demos are fictional and labelled as such. There is no phone number or street address for the studio.

## Credits

See `CREDITS.md` for every demo photograph, source URL and licence.

Self-hosted typefaces on the studio site: [Instrument Serif](https://fonts.google.com/specimen/Instrument+Serif) (SIL Open Font License 1.1; latin subset) and [Geist](https://vercel.com/font) (SIL Open Font License). Manrope files remain in `fonts/` for possible reuse; Demo typefaces (Cormorant Garamond, Outfit, Big Shoulders Display, Source Sans 3, Bodoni Moda, Manrope) are self-hosted in `fonts/`. See `CREDITS.md`.
