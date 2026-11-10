# WEBAUR v6 — Critical review of the starting point (v5)

Reviewed from `/workspace/webaur-v5` copied to `/workspace/webaur-v6`, served at `/halden-barbers-demo/webaur/`, with viewport screenshots in `previews/before/`. This is a review of the implementation as it actually looks, not of the brief that produced it.

Honest opening: v5 is already a long way past a three-card portfolio. The Work page has three colour-blocked chapters, device frames, and case-study pages. Each demo is already multi-page, clearly labelled as a concept, and typographically more considered than a typical template. That is not the same as it being at a convincing “commissioned studio” standard. The remaining problems are structural, not a missing accent colour.

## Work page

Screenshots: `previews/before/work-desktop.png`, `work-desktop-full.png`, `work-mobile.png`.

What works:
- The typographic introduction is confident, and Hale’s opening spread (text left, desktop frame plus overlapping phone) is the closest the page comes to a portfolio presentation.
- Concept labelling is honest. Prices and claims are not invented here.

What looks basic or template-like:
- **The first screen is only type.** A portfolio page whose job is to show the work opens with a charcoal typographic hero and no picture of a website. The work itself starts below the fold.
- **A repeated chapter formula.** Each project is: kicker + title + short intro + device frames + a three-column “design direction / features / decisions” block + two identical buttons. The backgrounds change (bone, graphite, cream) and the frame arrangement changes slightly (Hale split, Alto full-width then filmstrip, Maison centred collage), but the *information design* is the same stack three times. That is why it can still read as “three project cards,” even though the cards are large.
- **The work is shown too small, and too similarly framed.** Every screenshot sits in the same cheap three-dot browser chrome. Hale’s inner-page thumbs are small. Alto and Maison’s secondary frames are the same device, cropped tightly, so the demos’ typography and photography barely register. A prospective client is being told about the work more than they are being shown it.
- **Case studies inherit the studio voice, not the project’s.** `work/barber-studio.html` (see `case-hale-desktop.png`) opens like every other WEBAUR inner page: Instrument Serif, Geist, charcoal, three equal “Lähtökohta / Tavoite / Yleisö” columns, then a swatch box that literally admits the type specimens are fallbacks (“Näytetty tässä studion Instrument Serifillä”). The brand system is described, not demonstrated.
- **Mobile Work is a long vertical list of the same blocks**, with the phone frame dropped below the desktop rather than composed.

Score for this page as a sales argument: the structure is in place; the art direction is not yet doing the selling.

## Hale Barber Studio

Screenshots: `demo-hale-home-desktop.png`, `demo-hale-services-desktop.png`, `demo-hale-barbers-desktop.png`, `demo-hale-gallery-desktop.png`, `demo-hale-visit-desktop.png`, plus mobile counterparts.

What works:
- The home hero is the strongest single screen in the current portfolio: a calm split, a good chair photograph (Anna Avilova / Pexels), and a headline with a point of view (“The hour is yours.”).
- Honesty is handled carefully (fictional barber, example prices, no fake booking).
- There are already five real pages, and the photography set is cohesive.

What looks basic or template-like:
- **The type is not a distinct brand.** Headlines use Instrument Serif — the same display face as the WEBAUR studio site. In a portfolio, Hale reads as a reskin of the agency, not a commissioned identity. Fonts are also loaded from Google Fonts rather than self-hosted.
- **Inner pages share one layout recipe.** Services, The barber, Gallery and Visit all open the same way: a small kicker, a huge two-word headline (“The menu.” / “The room, close in.” / “How a visit would work.”), a short paragraph, then a single photograph. After the home hero, the site becomes a series of typographic title slides.
- **The services page wastes the fold.** The first screen is almost only the word “The menu.” The actual menu — the thing a real shop would lead with — sits below a wide bench photograph. Pricing is a plain list, not a designed menu.
- **The gallery repeats the hero.** The first two frames at the fold are the same chair run already used on the home page, same angle family. It feels like a short stock set stretched into a page, not a considered room study.
- **The barber page is mostly a disclaimer.** A good portrait is paired with a large apology that the name is fictional. That honesty is required; it currently crowds out craft, tools, and the sitting itself.
- **Visit is thin.** A typographic title, a simple hours table, and the same chairs photograph. The booking path is a note, which is honest, but the page does not feel like a contact experience — just a statement that one cannot book.
- **Chrome and components are generic:** a floating “Concept project” pill that collides with layout, flat forest-green rectangle buttons, a logo of two vertical bars plus “Hale.” Fine, not distinctive.

## Alto Detail

Screenshots: `demo-alto-home-desktop.png`, `demo-alto-services-desktop.png`, `demo-alto-results-desktop.png`, `demo-alto-process-desktop.png`, `demo-alto-contact-desktop.png`.

What works:
- Big Shoulders Display is a real typographic decision and already separates Alto from Hale and Maison.
- The AMG hero photograph is striking. Workshop images (wash bay, foam, polish) are the right subject matter.
- The comparison sliders exist and are documented as illustrative, not as proof of paid work. The enquiry form already fails closed in demo mode.

What looks basic or template-like:
- **The home page splits image and message.** The first screen is a car on a pale sky, with the headline “A quieter shine.” sitting underneath, almost as a caption. It looks like a stock photo landing page, not a tightly art-directed showroom. The car is also a clean outdoor product shot, not a car in a detailing bay — the caption “atmosphere photograph” overclaims.
- **The light grey field (`#edeeef`) feels like an app background**, not a luxury workshop. Combined with a lot of leftover white space, Services, Results and Contact read as blog posts with a loud headline.
- **Services leads with a typographic poster** (“The work, itemised.”) and only then a single package. There is no immediate comparison of packages, no specification-sheet density, no sense of a priced programme.
- **The Results page hides its only distinctive interaction.** The first screen is disclaimer copy and a huge title. The sliders — the feature the Work page itself calls out — appear as a sliver at the bottom of the fold. If this page is the proof of craft, the comparison should be the primary object.
- **Contact is a generic two-column form** on the same grey, with no workshop atmosphere and a large heading that does most of the “design.”
- Fonts are Google-hosted. The identity is not carried into the WEBAUR case study (which substitutes studio fonts).

## Maison Café

Screenshots: `demo-maison-home-desktop.png`, `demo-maison-menu-desktop.png`, `demo-maison-story-desktop.png`, `demo-maison-visit-desktop.png`.

What works:
- Bodoni Moda with a warm paper ground is a clear editorial direction. The home hero (conservatory table + “A quiet table, for as long as you need it.”) is already close to a café magazine cover.
- Copy is careful and the concept labelling is good. The invented plan on Visit is an honest alternative to a fake Google map.

What looks basic or template-like:
- **Inner pages revert to the same title-slide template** as Hale: kicker, enormous headline, lead, then content below the fold. Story and Menu in particular spend the first screen on words and cream.
- **The menu does not present food.** At the first fold the only photograph is plants. The site already has licensed croissant, plate, latte, pour and iced-coffee photographs; they are not doing the work on the page that should be selling a kitchen. The menu typography also starts late and is sparse rather than *designed* (no poster-like menu object, weak interweaving of plates and prices).
- **Atmosphere is one conservatory image, reused.** Home, Story and the general mood all lean on the same glasshouse/plants family. The “CAFE” sign interior and the pastry stills are underused. Visual storytelling is thinner than the brief asks.
- **Visit is typography plus a flat diagram.** No hours presented as a designed object at the first fold, no photograph of the room, little sense of place beyond the invented map. It feels unfinished rather than quietly minimal.
- **Layout kinship with Hale.** Both sites are light, serif-led, kicker-plus-headline-plus-two-buttons, with a dark rectangular primary button. A client flipping between demos will feel a shared template under the palettes.
- Fonts are Google-hosted. Manrope is already in the studio `fonts/` folder and is not used locally.

## Shared issues across the portfolio

1. **A common page grammar** (kicker → huge serif or condensed headline → two-sentence lead → one image) is used so consistently that the three brands do not feel independently commissioned once you leave the home heroes.
2. **Honesty copy is visually dominant** on inner pages. The disclosures are necessary; they should not be the main typographic event.
3. **Work-page screenshots cannot outrun the demos.** If Services, Menu, Results and Visit look like title slides, the portfolio will look like title slides in a browser frame.
4. **Case studies are not yet a brand-system presentation.** Fallback type, studio chrome, modest walkthroughs.
5. **Motion is already restrained** (good). `prefers-reduced-motion` exists on the studio site and Maison; it should be consistent everywhere.

## What v6 must change to count as a substantial improvement

- Rebuild the Work page so each project is a different composition, with large, freshly captured screenshots of the rebuilt demos, and with direction / features / decisions integrated into the spread rather than tacked on as three identical columns.
- Give Hale a display face that is not Instrument Serif; redesign Services as a menu, Gallery as a varied study of the room, Visit as a contact experience (still demo-honest).
- Move Alto onto a darker, more technical showroom language; put packages and the comparison slider in the primary view of their pages; art-direct the hero so the headline and the car belong to the same frame.
- Treat Maison as a food magazine: menu as a designed object with food photography, story as editorial longform, visit/atmosphere as a room with hours — not another cream title slide.
- Self-host the demo typefaces, load them on the case-study pages, and recapture every portfolio frame from the rebuilt sites.

This review does not call the current site “premium.” Parts of it (Hale’s hero, Maison’s home, Alto’s typeface choice) are already good. The portfolio as a whole still does not sufficiently demonstrate what WEBAUR would make for a paying client, because too much of the work is described in large type and too little of it is *shown* with a distinct layout grammar on every page.

