# WEBAUR v6 — Comparison and scorecard

Compared against the v5 starting point reviewed in `REVIEW-before.md`. Screenshots: `previews/before/` and `previews/after/`. Side-by-side frames are in `previews/compare-*.png`. This is an honest account. I will not call the result “premium” as a slogan; I will say where the implementation now holds up and where it still does not.

## What actually changed

### Work page

The first screen is no longer only type. Under the introduction there is a three-frame index of the live demo homes, so a visitor sees the work immediately. Each project is still a long chapter, but the information design is less like three stacked cards:

- **Hale** is a sticky text column (introduction, direction, features, decisions, actions) beside a large desktop frame, an overlapping phone, and three inner-page frames (services, barbers, gallery) recaptured from the rebuilt site.
- **Alto** is a dark split: copy and metadata on the left, a large cinematic home frame plus phone on the right, then a film of services, the results slider, and process.
- **Maison** is a centred magazine masthead, a collage of the home, the food-led menu and the new room page, then a wide story frame with a phone beside it.

Portfolio frames in `images/work/` were recaptured from the rebuilt demos (WebP, AVIF, JPEG). Case-study type specimens now load the same self-hosted faces as the demos (Cormorant Garamond, Outfit, Big Shoulders Display, Source Sans 3, Bodoni Moda, Manrope) instead of admitting a fallback. Maison gained a walkthrough of the new “The room” page. The chapter copy was updated so it no longer describes v5’s typography or palettes.

**Still weak.** The device chrome is still the same three-dot browser frame. Case-study openings still use the studio’s charcoal Instrument Serif voice before the brand system appears. The three chapters still share a rhythm (copy, large frames, supporting frames). It is a better portfolio presentation, not a completely different kind of page.

### Hale Barber Studio

A distinct identity, no longer Instrument Serif (the studio’s own display face). Self-hosted Cormorant Garamond and Outfit, a bone/forest/brass palette, a typographic monogram, and a slim concept rail instead of a floating pill that collided with the layout.

- **Services** is a designed menu at the first fold (time and example prices), with the bench and a working photograph held beside the list — not a title slide that buries the menu.
- **The barber** is a full-height editorial portrait of the fictional Aino Vartiainen, with the required honesty moved into a short note instead of dominating the headline.
- **Gallery** uses a varied mosaic (leather, tools, parting, wash, sitting) and an accessible lightbox. The hero chairs photograph is deliberately kept off this page so it does not repeat the home.
- **Visit** now includes hours, the fictional address, and a booking form that does not send.

Photography is still the same Anna Avilova sitting. That set is cohesive and good; it is also finite. The site is a better use of those pictures, not a new photographic production.

### Alto Detail

Moved off the light-grey “app” field onto graphite, with oxide as a sparse accent. The home hero is the largest single jump: the AMG and the headline “A quieter shine.” share one frame, with an honest caption that this is licensed product photography, not a job from the workshop.

- **Services** still opens typographically, but the first package (wash photograph and price) reaches the first fold, and the home now has a specification-style package table.
- **Results** keeps the honest “same photograph, processed” explanation, then puts the sliders where they can be used. The sliders are keyboard-accessible; the divider moves with the range input and arrow keys.
- **Process** is a four-step timeline with workshop photographs.
- **Contact** keeps an honest demo form (nothing is sent) and adds a bay photograph beside the invented address.

The hero car is still an outdoor product shot, not a car in a detailing bay. The indoor wash/foam/polish set does that work later. Packages and contact are stronger, not lavish.

### Maison Café

The home was already the strongest of the three v5 homes and remains a magazine-like split. The real gains are inside:

- **Menu** now opens with croissant photography, then a typographic list with latte, a midday plate and an iced cup beside it — not plants standing in for food.
- **The room** is a new page (every previous nav item already led somewhere; this one earns its place). Evening lamps, the conservatory table, the taller green interior.
- **Story** is still a short essay, now with portafilters and pour/latte stills.
- **Visit** keeps the invented plan (honest, not a fake map) and adds a reservation form that does not send.

The atmosphere set is still a small number of licensed interiors, reused with more care. It is a more complete café site, not a new building.

### Studio site elsewhere

Home teasers pick up the new screenshots automatically. Copy that still said “four-page café” or described v5 type was updated. Prices remain €490 / €890 / €1,490. The contact form is still honestly unconfigured when `CONTACT_EMAIL` and `FORMSPREE_ID` are empty. Nothing was published.

## QA

Served at `/halden-barbers-demo/webaur/`. Playwright across 39 pages and 7 viewports (375×812, 390×844, 430×932, 768×1024, 1024×768, 1440×900, 1920×1080):

- 0 console errors
- 0 broken links, images, stylesheets or scripts (after checking `href`, `src` and `srcset`)
- 0 horizontal overflow, after fixing an Alto package table that overflowed on small phones (the table now stacks)
- Mobile menus open and close (Escape) on the studio site and all three demos
- Alto comparison sliders move (tested 50 → 20)
- Hale, Alto and Maison demo forms prevent submission and show an honest concept message

`html-validate` (recommended rules, with the project’s existing exceptions): 0 errors after fixing a misused `aria-label`, a lightbox `<img>` without `src`, a duplicate `class` attribute, and implicit input types.

Lighthouse (local, Chrome, this turn):

| Page | Form | Perf | A11y | Best practices | SEO |
| --- | --- | --- | --- | --- | --- |
| Studio home | mobile / desktop | 96 / 100 | 100 / 100 | 100 / 100 | 100 / 100 |
| Work | mobile / desktop | 96 / 100 | 96 / 95* | 100 / 100 | 100 / 100 |
| Case study (Hale) | mobile / desktop | 99 / 100 | 100 / 100 | 100 / 100 | 100 / 100 |
| Hale demo home | mobile / desktop | 99 / 100 | 96 / 93* | 100 / 100 | 63† |
| Alto demo home | mobile / desktop | 100 / 100 | 96 / 95* | 100 / 100 | 63† |
| Maison demo home | mobile / desktop | 98 / 100 | 100 / 100 | 100 / 100 | 63† |

\*Colour-contrast failures were found on Hale brass kickers, Alto oxide eyebrows, and Work-page captions inheriting the studio muted grey on bone/cream. Contrast tokens and caption colours were corrected after this run; Lighthouse was not fully re-run. Alto also lacked a header cell for the package-table’s last column; a visually hidden header was added.

†Demo SEO is 63 because the demos send `noindex`. That is intentional: they are fictional concept sites, not businesses to be indexed.

## Remaining weaknesses

1. **The photograph libraries did not grow.** Hale is still one licensed sitting. Alto’s hero is still a clean outdoor AMG, not a bay. Maison still recycles a short conservatory/interior set. Better art direction is not the same as a new shoot.
2. **A family resemblance remains on inner pages** (kicker, large display line, lead). It is less rigid than v5, but a careful client will still see a shared hand.
3. **Case studies open in the studio voice.** The brand system is now accurate; the first screen is still WEBAUR charcoal and Instrument Serif.
4. **The contact form on the studio site is still not connected.** That is honest, not finished.
5. **Legal entity details on the privacy page, and a native Finnish proofread, were out of scope here** and remain as they were.
6. **I would not describe this as an award-winning site.** It is a substantial step up from v5 and is closer to work you could show a small business. It is not in the same league as the studios named in the v5 brief as quality references.

## Scorecard (1–10)

Scores are for this implementation against a convincing commissioned-studio standard, not against a generic template.

| Area | v5 (start) | v6 | Note |
| --- | --- | --- | --- |
| Work page as a portfolio experience | 5.5 | 7.5 | Work is shown on the first screen; chapters are better composed; still a familiar device-frame grammar. |
| Hale Barber Studio | 6.5 | 8 | Distinct type, a real menu, a stronger barber and visit page. Same photographs. |
| Alto Detail | 6 | 8 | The cinematic dark home is a genuine upgrade; sliders and packages are more useful. Hero car still looks like stock. |
| Maison Café | 7 | 8 | Home was already good; menu photography and the room page make the set more convincing. |
| Distinctness between the three demos | 6.5 | 8 | Three type systems, three palettes, three layout grammars, self-hosted. Inner-page kinship remains. |
| Honesty (concept labelling, no fake results) | 9 | 9 | Held. Forms still fail closed. |
| Technical quality (paths, responsive, a11y of interactions) | 8 | 8.5 | Clean QA; contrast fixes landed after Lighthouse. |
| Overall convincingness for a paying client | 6 | 7.5 | Better evidence of “this is the kind of site we would make.” Not yet a book of commissioned work, because it still isn’t one. |

**Overall: 7.5 / 10.** A substantial design-quality improvement, not a palette change. I would show this to Casper as the current best argument for WEBAUR, with the weaknesses above stated plainly. I would not tell him the result is premium.

Not published. Zip: `/workspace/webaur-v6.zip`.
