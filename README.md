# WEBAUR website (v6)

Independent web design studio site — static HTML, CSS and JavaScript. No required build step.

Finnish is the default language at the site root. English lives in `/en/`. Studio pages are generated from `_tools/build_pages.py`. Concept demos in `demos/` were rebuilt in v6 with distinct typography, multi-page layouts and self-hosted fonts. They remain fictional concept projects.

## Local preview (including the GitHub Pages subdirectory)

The public project is hosted under:

`/halden-barbers-demo/webaur/`

All internal links, images, fonts, CSS, JavaScript and demos use relative paths so they work in that folder, not only at a domain root.

```bash
# from a parent folder that contains halden-barbers-demo/webaur/
python3 -m http.server 8768 --bind 127.0.0.1
```

Open `http://127.0.0.1:8768/halden-barbers-demo/webaur/`.

Canonical, Open Graph and sitemap URLs currently use the GitHub Pages origin:

`https://cazzuuu-coder.github.io/halden-barbers-demo/webaur/`

When a custom domain is connected, update those URLs in `_tools/build_pages.py` (`SITE`) and regenerate, or edit `sitemap.xml`, `robots.txt` and the page tags directly.

## Languages

- Finnish (default): `index.html`, `services.html`, `pricing.html`, `work.html`, `about.html`, `contact.html`, `privacy.html`, `thanks.html`, `404.html`, and `work/*.html`
- English: the same files under `en/`
- Every studio page has an `hreflang` set (`fi`, `en`, `x-default` → Finnish) and a FI / EN switcher
- Concept demos keep their own brand language. Portfolio descriptions around them are translated.

The Finnish copy was written to sound like natural professional Finnish. A native speaker should still proofread it before launch.

## Pages and demos

- Studio pages as listed above, in both languages
- Pricing (`pricing.html`, also summarised on the home page): Starter / Aloitus €490, Business / Yritys €890, Premium €1,490, all excl. VAT 25.5%
- Work: three concept projects with distinct layouts, large previews, and links to the live demo and the case study
- Case studies: brief, audience, brand identity, page-by-page walkthrough, features and design decisions. All three are labelled as concept projects
- Working concept demos (`noindex`, labelled as concepts; booking buttons do not place a real booking):
  - `demos/barber-studio/` — Hale Barber Studio
  - `demos/detailing/` — Alto Detail
  - `demos/maison-cafe/` — Maison Café

Portfolio screenshots live in `images/work/{hale,alto,maison}/` as AVIF, WebP and JPEG.

## Contact form

**Pages:** `contact.html` and `en/contact.html`. Behaviour is in `js/main.js`.

**Configuration — the only file to edit:** `js/site-config.js`

```js
window.WEBAUR_SITE = {
  CONTACT_EMAIL: "",  // e.g. "hello@example.com"
  FORMSPREE_ID: ""    // e.g. "xxxxxxxx" or a full Formspree URL
};
```

- If `FORMSPREE_ID` is set, the form POSTs via `fetch` to Formspree.
- If only `CONTACT_EMAIL` is set, submit opens a prepared `mailto:` message.
- If both are empty, the form shows an honest inline message and nothing is sent. Email links stay hidden until `CONTACT_EMAIL` is set.

There is no public email address on the site until that value is filled in. GitHub Pages cannot process forms by itself.

Budget can be pre-filled with `?package=starter|business|premium#form`.

## Pricing

Starter / Aloitus €490, Business / Yritys €890 (recommended), Premium €1,490.

**Prices excl. VAT (Finnish VAT 25.5% added).** The final price depends on the agreed scope. Revision rounds and the timetable are agreed in the quote. Domain registration and hosting are **not** included, nor are photography or copywriting beyond the agreed scope, ongoing maintenance, or features outside the chosen package.

## Still to complete before a full commercial launch

- A real mailbox and, if desired, a Formspree form id in `js/site-config.js`
- Legal name, business ID and postal address in the privacy policy
- A native Finnish proofread
- A custom domain, if one is connected, reflected in canonical URLs

Concept locations in the demos are fictional and labelled as such. There is no phone number or street address for the studio.

## Credits

See `CREDITS.md` for every demo photograph, source URL and licence.

Self-hosted typefaces on the studio site: [Instrument Serif](https://fonts.google.com/specimen/Instrument+Serif) (SIL Open Font License 1.1; latin subset) and [Geist](https://vercel.com/font) (SIL Open Font License). Manrope files remain in `fonts/` for possible reuse; Demo typefaces (Cormorant Garamond, Outfit, Big Shoulders Display, Source Sans 3, Bodoni Moda, Manrope) are self-hosted in `fonts/`. See `CREDITS.md`.
