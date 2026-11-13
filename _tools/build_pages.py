#!/usr/bin/env python3
"""Generate bilingual WEBAUR v5 studio pages. Finnish is default; English lives in /en/."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://webaur.com"
SITE_PATH = "/"  # absolute path used by the 404 page (served at any URL depth)
EMAIL = "hello@webaur.com"  # keep in sync with js/site-config.js CONTACT_EMAIL

NAV = [
    ("work.html", "work", "Work", "Työt"),
    ("services.html", "services", "Services", "Palvelut"),
    ("pricing.html", "pricing", "Pricing", "Hinnat"),
    ("about.html", "about", "About", "Meistä"),
    ("contact.html", "contact", "Contact", "Yhteystiedot"),
]


ABSOLUTE = {"on": False}


def asset_prefix(lang, depth):
    if ABSOLUTE["on"]:
        return SITE_PATH
    if lang == "fi":
        return "../" * depth
    return "../" * (depth + 1)


def href(lang, page, dest_lang, dest_page):
    src_depth = 1 if page.startswith("work/") else 0
    climb = asset_prefix(lang, src_depth)
    if ABSOLUTE["on"]:
        climb = SITE_PATH
    if dest_lang == "en":
        return f"{climb}en/{dest_page}"
    return f"{climb}{dest_page}"


def logo(lang, page):
    pre = asset_prefix(lang, 1 if page.startswith("work/") else 0)
    home = f"{pre}index.html" if lang == "fi" else f"{pre}en/index.html"
    return f'<a class="logo" href="{home}" aria-label="WEBAUR"><span class="wm">WEB<span class="wm-a">A</span>UR</span></a>'


def header(lang, page, active):
    links = []
    for dest, key, en, fi in NAV:
        label = en if lang == "en" else fi
        url = href(lang, page, lang, dest)
        cur = ' aria-current="page"' if key == active else ""
        links.append(f'<li><a href="{url}"{cur}>{label}</a></li>')
    fi_url = href(lang, page, "fi", page)
    en_url = href(lang, page, "en", page)
    if lang == "fi":
        fi_el = '<span aria-current="true">FI</span>'
        en_el = f'<a href="{en_url}" lang="en" hreflang="en">EN</a>'
    else:
        fi_el = f'<a href="{fi_url}" lang="fi" hreflang="fi">FI</a>'
        en_el = '<span aria-current="true">EN</span>'
    cta = "Start a project" if lang == "en" else "Aloita projekti"
    cta_url = href(lang, page, lang, "contact.html")
    menu = "Open menu" if lang == "en" else "Avaa valikko"
    skip = "Skip to content" if lang == "en" else "Siirry sisältöön"
    lang_label = "Language" if lang == "en" else "Kieli"
    return f'''<a class="skip" href="#content">{skip}</a>
<header class="site-header">
  <div class="wrap nav">
    {logo(lang, page)}
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="nav-panel" aria-label="{menu}"><span></span><span></span><span></span></button>
    <div class="nav-panel" id="nav-panel">
      <ul class="nav-links">
        {"".join(links)}
      </ul>
      <nav class="lang-switch" aria-label="{lang_label}">{fi_el}<span class="sep" aria-hidden="true">/</span>{en_el}</nav>
      <a class="nav-cta" href="{cta_url}">{cta}</a>
    </div>
  </div>
</header>'''


def footer(lang, page):
    t = {
        "en": dict(
            desc="Independent web design studio. We design and build modern websites that help businesses stand out and turn visitors into customers.",
            nav="Navigate", services="Services", contact="Get in touch",
            email_l="Email", privacy="Privacy Policy",
            copy="© 2026 WEBAUR. All rights reserved.",
            indie="Independent design studio based in Finland.",
            d="Website Design", dev="Website Development", m="Launch and handover",
        ),
        "fi": dict(
            desc="Itsenäinen verkkosuunnittelustudio. Suunnittelemme ja rakennamme nykyaikaisia sivustoja, jotka auttavat yritystä erottumaan ja muuttamaan kävijät asiakkaiksi.",
            nav="Sivusto", services="Palvelut", contact="Ota yhteyttä",
            email_l="Sähköposti", privacy="Tietosuoja",
            copy="© 2026 WEBAUR. Kaikki oikeudet pidätetään.",
            indie="Itsenäinen suunnittelustudio Suomesta.",
            d="Verkkosivujen suunnittelu", dev="Verkkosivujen toteutus", m="Julkaisu ja luovutus",
        ),
    }[lang]

    def l(dest, label):
        return f'<li><a href="{href(lang, page, lang, dest)}">{label}</a></li>'

    fi_url = href(lang, page, "fi", page)
    en_url = href(lang, page, "en", page)
    nav_items = "".join(l(dest, (en if lang == "en" else fi)) for dest, key, en, fi in NAV)
    fi_cur = ' aria-current="true"' if lang == "fi" else ""
    en_cur = ' aria-current="true"' if lang == "en" else ""
    return f'''<footer class="site-footer">
  <div class="wrap footer-grid">
    <div>
      {logo(lang, page)}
      <p class="footer-note">{t["desc"]}</p>
    </div>
    <div>
      <ul class="footer-col">
        <li><strong>{t["nav"]}</strong></li>
        {nav_items}
      </ul>
    </div>
    <div>
      <ul class="footer-col">
        <li><strong>{t["services"]}</strong></li>
        {l("services.html#design", t["d"])}
        {l("services.html#development", t["dev"])}
        {l("services.html#handover", t["m"])}
        {l("pricing.html", "Pricing" if lang == "en" else "Hinnat")}
      </ul>
    </div>
    <div>
      <ul class="footer-col">
        <li><strong>{t["contact"]}</strong></li>
        <li class="js-email-wrap footer-email"><a href="mailto:{EMAIL}" data-email-slot>{EMAIL}</a></li>
        {l("contact.html", "Contact" if lang == "en" else "Yhteystiedot")}
        {l("privacy.html", t["privacy"])}
        <li class="lang-switch" style="margin-top:8px"><a href="{fi_url}" lang="fi" hreflang="fi"{fi_cur}>FI</a><span class="sep" aria-hidden="true"> / </span><a href="{en_url}" lang="en" hreflang="en"{en_cur}>EN</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap legal">
    <span>{t["copy"]}</span>
    <span>{t["indie"]}</span>
  </div>
</footer>'''


def cta(lang, page):
    if lang == "en":
        k, h, p, b = "Start a project", "Let’s build something your customers will remember.", "Tell us about your business and what you would like to improve. We’ll take it from there.", "Start a project"
    else:
        k, h, p, b = "Aloita projekti", "Rakennetaan jotain, jonka asiakkaasi muistavat.", "Kerro yrityksestäsi ja siitä, mitä haluaisit parantaa, niin jatketaan siitä yhdessä.", "Aloita projekti"
    return f'''<section class="cta-band" aria-labelledby="cta-title">
  <div class="wrap">
    <p class="eyebrow">{k}</p>
    <h2 id="cta-title" class="display">{h}</h2>
    <p class="lead">{p}</p>
    <p style="margin-top:32px"><a class="btn btn-accent" href="{href(lang, page, lang, "contact.html")}">{b}</a></p>
  </div>
</section>'''


def pic(prefix, path, alt, loading="lazy", sizes=None):
    """path is e.g. hale/home-desktop or alto/results-mobile (no extension)."""
    name = path.rsplit("/", 1)[-1]
    is_mob = name.endswith("-mobile")
    src = f"{prefix}images/work/{path}"
    if is_mob:
        sizes = sizes or "(min-width: 1100px) 200px, 40vw"
        w, h = 780, 1688
        sources = f'''<source type="image/avif" srcset="{src}-390.avif 390w, {src}.avif 780w" sizes="{sizes}" />
  <source type="image/webp" srcset="{src}.webp 780w" sizes="{sizes}" />'''
        srcset = f'{src}.jpg 780w'
    else:
        sizes = sizes or "(min-width: 1100px) 960px, 100vw"
        w, h = 1440, 900
        sources = f'''<source type="image/avif" srcset="{src}-800.avif 800w, {src}.avif 1440w" sizes="{sizes}" />
  <source type="image/webp" srcset="{src}.webp 1440w" sizes="{sizes}" />'''
        srcset = f'{src}.jpg 1440w'
    prio = ' fetchpriority="high"' if loading == "eager" else ""
    return f'''<picture>
  {sources}
  <img src="{src}.jpg" srcset="{srcset}" sizes="{sizes}" width="{w}" height="{h}" alt="{alt}" loading="{loading}" decoding="async"{prio} />
</picture>'''


def device_desktop(prefix, path, alt, loading="lazy", sizes=None):
    return f'''<div class="device-desktop">
  <div class="chrome" aria-hidden="true"><i></i><i></i><i></i></div>
  <div class="screen">{pic(prefix, path, alt, loading, sizes)}</div>
</div>'''


def device_mobile(prefix, path, alt, loading="lazy", sizes=None):
    return f'''<div class="device-mobile">
  <div class="notch" aria-hidden="true"></div>
  <div class="screen">{pic(prefix, path, alt, loading, sizes)}</div>
</div>'''


def canon_path(lang, page):
    if page == "index.html":
        return "" if lang == "fi" else "en/"
    return page if lang == "fi" else f"en/{page}"


def page_shell(lang, page, title, description, active, body):
    depth = 1 if page.startswith("work/") else 0
    pre = asset_prefix(lang, depth)
    css, js, cfg = f"{pre}css/styles.css", f"{pre}js/main.js", f"{pre}js/site-config.js"
    fav, ico, apple = f"{pre}images/brand/favicon.svg", f"{pre}images/brand/favicon-32.png", f"{pre}images/brand/apple-touch-icon.png"
    path = canon_path(lang, page)
    path_fi = canon_path("fi", page)
    path_en = canon_path("en", page)
    canon = f"{SITE}/{path}"
    fi_abs = f"{SITE}/{path_fi}"
    en_abs = f"{SITE}/{path_en}"
    og = f"{SITE}/images/og/og-{lang}.jpg"
    font_serif = f"{pre}fonts/instrument-serif-400.woff2"
    font_sans = f"{pre}fonts/Geist-Regular.woff2"
    robots = '  <meta name="robots" content="noindex" />' if page in ("thanks.html", "404.html") else ""
    lcp_preload = ""
    if page == "index.html":
        lcp_preload = f'  <link rel="preload" as="image" type="image/avif" href="{pre}images/work/hale/home-desktop.avif" fetchpriority="high" />\n'
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
  <title>{title}</title>
{robots}
  <meta name="description" content="{description}" />
  <link rel="canonical" href="{canon}" />
  <link rel="alternate" hreflang="fi" href="{fi_abs}" />
  <link rel="alternate" hreflang="en" href="{en_abs}" />
  <link rel="alternate" hreflang="x-default" href="{fi_abs}" />
  <meta name="theme-color" content="#0E0F0C" />
  <meta property="og:type" content="website" />
  <meta property="og:locale" content="{"fi_FI" if lang == "fi" else "en_GB"}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:url" content="{canon}" />
  <meta property="og:site_name" content="WEBAUR" />
  <meta property="og:image" content="{og}" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:image:alt" content="{"WEBAUR – Yrityksesi ansaitsee paremmat verkkosivut." if lang == "fi" else "WEBAUR – Websites built to move businesses forward."}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:image" content="{og}" />
  <link rel="icon" href="{fav}" type="image/svg+xml" />
  <link rel="icon" href="{ico}" type="image/png" sizes="32x32" />
  <link rel="apple-touch-icon" href="{apple}" />
  <link rel="preload" href="{font_serif}" as="font" type="font/woff2" crossorigin />
  <link rel="preload" href="{font_sans}" as="font" type="font/woff2" crossorigin />
{lcp_preload}  <link rel="stylesheet" href="{css}" />
</head>
<body>
{header(lang, page, active)}
<main id="content">
{body}
</main>
{footer(lang, page)}
<script src="{cfg}"></script>
<script src="{js}" defer></script>
</body>
</html>
'''

def pricing_block(lang, page, heading_tag="h2", compact=False):
    return _pricing_block(lang, page, heading_tag, compact)


PKG = {
    "fi": [
        dict(key="starter", name="Starter", price="490 €", pages="1 sivu, useita osioita",
             fit="Pienelle yritykselle, joka tarvitsee selkeät ja tyylikkäät verkkosivut ilman erillisiä alasivuja.",
             items=["Yksi pitkä sivu, jossa on kaikki tärkein",
                    "Yrityksen ja palveluiden esittely",
                    "Hinnasto tai palveluiden hinnat",
                    "Yhteystiedot ja yhteydenottolomake",
                    "Valikko, joka vie suoraan sivun eri osioihin",
                    "Yrityksen brändiin sopiva visuaalinen ilme",
                    "Perustason hakukoneoptimointi"],
             ready="Yksi valmis verkkosivu. Osioita voi olla useita, mutta ne ovat kaikki samalla sivulla."),
        dict(key="business", name="Business", price="890 €", pages="Enintään 5 sivua",
             fit="Yritykselle, joka tarvitsee enemmän sisältöä ja omat sivut eri palveluilleen.",
             items=["Etusivu ja yrityksen esittelysivu",
                    "Palveluille omat sivut tarpeen mukaan",
                    "Hinnasto tai palveluiden hinnat",
                    "Referenssi- tai kuvagalleria",
                    "Yhteystiedot ja yhteydenottolomake",
                    "Yrityksen tarpeisiin suunniteltu visuaalinen ilme",
                    "Selkeä navigaatio sivujen välillä",
                    "Perustason hakukoneoptimointi jokaiselle sivulle"],
             ready="Yksi verkkosivusto, jossa on enintään 5 erillistä sivua. Kyse ei ole viidestä eri sivustosta."),
        dict(key="premium", name="Premium", price="1&nbsp;490 €", pages="Enintään 8 sivua",
             fit="Yritykselle, joka haluaa tavallista näyttävämmän, yksilöllisemmän ja viimeistellymmän sivuston.",
             items=["Kaikki Business-paketin ominaisuudet",
                    "Yksilöllisempi ja näyttävämpi visuaalinen suunnittelu",
                    "Harkitut animaatiot ja liikkuvat elementit",
                    "Sulavat siirtymät ja interaktiiviset yksityiskohdat",
                    "Näyttävämmät kuva- ja sisältöasettelut",
                    "Yksityiskohtaisempi visuaalinen viimeistely",
                    "Perustason hakukoneoptimointi jokaiselle sivulle"],
             ready="Yksi verkkosivusto, jossa on enintään 8 erillistä sivua. Animaatiot pidetään kevyinä, jotta sivu pysyy nopeana."),
    ],
    "en": [
        dict(key="starter", name="Starter", price="€490", pages="1 page, several sections",
             fit="For a small business that needs a clear, well-designed website without separate subpages.",
             items=["One long page with everything important",
                    "Introduction to the business and its services",
                    "Price list or service prices",
                    "Contact details and a contact form",
                    "A menu that jumps straight to each section",
                    "A visual look that fits your brand",
                    "Basic search engine optimisation"],
             ready="One finished web page. It can have several sections, but they all sit on the same page."),
        dict(key="business", name="Business", price="€890", pages="Up to 5 pages",
             fit="For a business that needs more content and separate pages for its services.",
             items=["Home page and an about page",
                    "Separate service pages as needed",
                    "Price list or service prices",
                    "Reference or photo gallery",
                    "Contact details and a contact form",
                    "A visual look designed around the business",
                    "Clear navigation between pages",
                    "Basic search engine optimisation for every page"],
             ready="One website with up to 5 separate pages. This means five pages, not five different websites."),
        dict(key="premium", name="Premium", price="€1,490", pages="Up to 8 pages",
             fit="For a business that wants a more striking, more individual and more polished website.",
             items=["Everything in the Business package",
                    "More individual, more striking visual design",
                    "Considered animations and moving elements",
                    "Smooth transitions and interactive details",
                    "Richer image and content layouts",
                    "More detailed visual finishing",
                    "Basic search engine optimisation for every page"],
             ready="One website with up to 8 separate pages. Animations are kept light so the site stays fast."),
    ],
}

TXT = {
    "fi": dict(
        eyebrow="Paketit", title="Kolme pakettia. Yksi kertamaksu.",
        lead="Maksat sivustosta kerran, ja se on sinun. WEBAURille ei makseta kuukausimaksuja.",
        rec="Suositeltu", cta="Pyydä tarjous", for_l="Kenelle", what_l="Mitä tehdään", ready_l="Valmiina saat",
        compact_note='Sama tekninen laatu kaikissa paketeissa. Verkkotunnus ja hosting maksetaan suoraan palveluntarjoajalle.',
        compact_link="Katso, mitä hintaan sisältyy ja mitä ei",
        q_title="Sama tekninen laatu kaikissa paketeissa",
        q_lead="Halvempi paketti ei tarkoita huonommin toimivaa sivustoa. Hintaero tulee sivujen määrästä, suunnittelutyön laajuudesta ja visuaalisista lisäominaisuuksista.",
        quality=["Responsiivinen toteutus puhelimelle, tabletille ja tietokoneelle",
                 "Toimivat linkit ja painikkeet",
                 "Toimiva yhteydenottolomake, kun lomakkeen palvelut ja asetukset on määritetty",
                 "Selkeä ja helppokäyttöinen rakenne",
                 "Hyvä latausnopeus",
                 "Hakukoneoptimoinnin perustaso",
                 "Kuvien ja koodin optimointi",
                 "Sivuston testaus ennen julkaisua",
                 "Toimivuuden tarkistus yleisimmillä selaimilla",
                 "Virheiden korjaus ennen luovutusta"],
        own_title="Sivusto on sinun",
        own_lead="Kertamaksu ilman sitoutumista. Valmiin sivuston mukana saat:",
        own=["Valmiin, julkaistun verkkosivuston",
             "Sivuston lähdekoodin ja tiedostot",
             "Julkaisu- ja siirto-ohjeet",
             "Verkkotunnuksen omiin nimiisi",
             "Mahdollisuuden jatkaa sivuston käyttöä ilman WEBAURia",
             "Mahdollisuuden siirtää sivusto toiselle palveluntarjoajalle tai tekijälle"],
        own_note="Verkkotunnus ja hosting eivät sisälly pakettihintaan. Maksat ne itse suoraan palveluntarjoajalle, ja ne rekisteröidään mahdollisuuksien mukaan omiin nimiisi ja tileihisi.",
        later_title="Muutokset julkaisun jälkeen",
        later="Sivusto toimii ilman meitä. Jos haluat myöhemmin vaihtaa tekstejä, kuvia tai hintoja, lisätä palvelun tai uuden sivun, teemme sen erikseen sovittavalla kertamaksulla. Hinta sovitaan ennen työn aloittamista.",
        before_title="Ennen julkaisua",
        before=["Käymme sivuston sisällön ja ulkoasun kanssasi läpi ennen julkaisua.",
                "Kohtuulliset tekstien, kuvien, värien ja asettelun muutokset sovitun kokonaisuuden sisällä kuuluvat hintaan.",
                "Toteutuksessa ilmenevät virheet korjataan ilman lisämaksua.",
                "Uudet ominaisuudet, laajat uudistukset ja sovitun ulkopuoliset lisätyöt sovitaan erikseen."],
        not_title="Mitä pakettihintaan ei sisälly",
        not_items=["Verkkotunnuksen vuosimaksu",
                   "Hosting- tai webhotellimaksut",
                   "Verkkokaupan rakentaminen",
                   "Laajat ajanvarausjärjestelmät",
                   "Muut erikseen sovittavat erikoistoiminnot",
                   "Julkaisun jälkeiset uudet muutostyöt"],
        notes_title="Huomioithan",
        notes=["Sisältö, hinta ja aikataulu vahvistetaan kirjallisessa tarjouksessa ennen työn alkua."],
        follow_h="Etkö ole varma, mikä paketti sopii?",
        follow_p="Kerro lyhyesti yrityksestäsi, niin ehdotamme sopivaa pakettia.",
        follow_b="Ota yhteyttä",
        jump=[("included", "Sama laatu kaikissa paketeissa"), ("ownership", "Sivusto on sinun"), ("not-included", "Mitä hintaan ei sisälly")],
    ),
    "en": dict(
        eyebrow="Packages", title="Three packages. One payment.",
        lead="You pay for the website once, and it is yours. There are no monthly fees to WEBAUR.",
        rec="Recommended", cta="Request a quote", for_l="Who it is for", what_l="What we do", ready_l="What you get",
        compact_note='The same technical quality in every package. Domain and hosting are paid directly to the provider.',
        compact_link="See what is included and what is not",
        q_title="The same technical quality in every package",
        q_lead="A cheaper package does not mean a website that works less well. The price difference comes from the number of pages, the scope of the design work and the visual extras.",
        quality=["Responsive build for phone, tablet and computer",
                 "Working links and buttons",
                 "A working contact form once its services and settings are configured",
                 "A clear, easy-to-use structure",
                 "Good loading speed",
                 "Basic search engine optimisation",
                 "Optimised images and code",
                 "Testing before launch",
                 "Checks in the most common browsers",
                 "Bugs fixed before handover"],
        own_title="The website is yours",
        own_lead="One payment, no commitment. With the finished site you get:",
        own=["The finished, published website",
             "The source code and files",
             "Instructions for publishing and moving the site",
             "The domain in your own name",
             "The freedom to keep using the site without WEBAUR",
             "The freedom to move the site to another provider or developer"],
        own_note="Domain and hosting are not included in the package price. You pay them directly to the provider, and where possible they are registered in your own name and accounts.",
        later_title="Changes after launch",
        later="The site works without us. If you later want to change text, photos or prices, or add a service or a new page, we do it for a separately agreed one-time fee. The price is agreed before the work starts.",
        before_title="Before launch",
        before=["We go through the content and the look of the site with you before launch.",
                "Reasonable changes to text, images, colours and layout within the agreed scope are included.",
                "Bugs found in the build are fixed at no extra cost.",
                "New features, large redesigns and work outside the agreed scope are agreed separately."],
        not_title="Not included in the package price",
        not_items=["Yearly domain fee",
                   "Hosting or web hotel fees",
                   "Building an online store",
                   "Extensive booking systems",
                   "Other special features agreed separately",
                   "New change work after launch"],
        notes_title="Please note",
        notes=["Content, price and timetable are confirmed in a written quote before work begins."],
        follow_h="Not sure which package fits?",
        follow_p="Tell us briefly about your business and we will suggest a package.",
        follow_b="Get in touch",
        jump=[("included", "Same quality in every package"), ("ownership", "The site is yours"), ("not-included", "What is not included")],
    ),
}


def _li(items):
    return "".join(f"<li>{x}</li>" for x in items)


def _pricing_block(lang, page, heading_tag="h2", compact=False):
    contact = href(lang, page, lang, "contact.html")
    pricing = href(lang, page, lang, "pricing.html")
    t = TXT[lang]
    cards = []
    for p in PKG[lang]:
        featured = p["key"] == "business"
        cls = "price-card featured" if featured else "price-card"
        rec = f'<span class="popular">{t["rec"]}</span>' if featured else ""
        btn = "btn btn-accent" if featured else "btn btn-ghost"
        cards.append(f'''      <article class="{cls}" aria-labelledby="pkg-{p["key"]}">
        {rec}<h3 id="pkg-{p["key"]}">{p["name"]}</h3>
        <p class="price">{p["price"]}</p>
        <p class="price-pages">{p["pages"]}</p>
        <p class="price-for"><span class="price-label">{t["for_l"]}</span>{p["fit"]}</p>
        <p class="price-label">{t["what_l"]}</p>
        <ul>{_li(p["items"])}</ul>
        <p class="price-ready"><span class="price-label">{t["ready_l"]}</span>{p["ready"]}</p>
        <a class="{btn}" href="{contact}?package={p["key"]}#form">{t["cta"]}<span class="sr-only"> – {p["name"]}</span></a>
      </article>''')
    head = f'''
<section class="section" id="pricing" aria-labelledby="pricing-title">
  <div class="wrap">
    <p class="eyebrow">{t["eyebrow"]}</p>
    <{heading_tag} id="pricing-title" class="section-title" style="margin:12px 0 12px">{t["title"]}</{heading_tag}>
    <p class="lead price-lead">{t["lead"]}</p>
    <div class="price-grid">
{chr(10).join(cards)}
    </div>'''
    if compact:
        return head + f'''
    <p class="price-more">{t["compact_note"]} <a href="{pricing}#included">{t["compact_link"]}</a></p>
  </div>
</section>'''
    return head + f'''
    <p class="price-jump">{"".join(f'<a href="#{i}">{l}</a>' for i, l in t["jump"])}</p>
    <div class="price-quality" id="included">
      <h2>{t["q_title"]}</h2>
      <p class="muted">{t["q_lead"]}</p>
      <ul class="quality-list">{_li(t["quality"])}</ul>
    </div>
    <div class="price-own" id="ownership">
      <div>
        <h2>{t["own_title"]}</h2>
        <p class="muted">{t["own_lead"]}</p>
        <ul class="quality-list">{_li(t["own"])}</ul>
        <p class="muted price-small">{t["own_note"]}</p>
      </div>
      <div class="price-later">
        <h3>{t["later_title"]}</h3>
        <p class="muted">{t["later"]}</p>
      </div>
    </div>
    <div class="price-notes">
      <div>
        <h2>{t["before_title"]}</h2>
        <ul>{_li(t["before"])}</ul>
      </div>
      <div id="not-included">
        <h2>{t["not_title"]}</h2>
        <ul>{_li(t["not_items"])}</ul>
        <h3 class="price-notes-sub">{t["notes_title"]}</h3>
        <ul>{_li(t["notes"])}</ul>
      </div>
    </div>
    <div class="price-follow">
      <h2>{t["follow_h"]}</h2>
      <p class="muted">{t["follow_p"]}</p>
      <p style="margin-top:16px"><a class="btn btn-accent" href="{contact}#form">{t["follow_b"]}</a></p>
    </div>
  </div>
</section>'''


def faq_block(lang):
    if lang == "en":
        items = [
            ("Is Starter really one page?",
             "Yes. Starter is one long page with several sections: introduction, services, prices and contact. The menu jumps straight to each section."),
            ("Does “up to 5 pages” mean five websites?",
             "No. Business is one website with up to five separate pages, for example home, about, services, gallery and contact. Premium can have up to eight."),
            ("Are there monthly fees?",
             "No. You pay WEBAUR once. The only recurring costs are the domain and hosting, which you pay directly to the provider."),
            ("How long does a project take?",
             "It depends on the scope and how smoothly drafts can be reviewed together. The timetable is agreed after the first messages, once the work is clear — we do not promise a standard delivery date in advance."),
            ("Can I use my own photographs and copy?",
             "Yes. If you have photographs or text you want to use, we work with them. Photography or copywriting beyond the agreed scope is priced separately."),
            ("Do you build online stores or booking systems?",
             "Online stores are not part of our services at the moment. Extensive booking systems and other special features are not included in the package prices and are agreed separately."),
        ]
        title = "Frequently asked questions"
    else:
        items = [
            ("Onko Starter todella yksi sivu?",
             "Kyllä. Starter on yksi pitkä sivu, jossa on useita osioita: esittely, palvelut, hinnat ja yhteystiedot. Valikko vie suoraan oikeaan osioon."),
            ("Tarkoittaako ”enintään 5 sivua” viittä sivustoa?",
             "Ei. Business on yksi verkkosivusto, jossa on enintään viisi erillistä sivua, esimerkiksi etusivu, esittely, palvelut, galleria ja yhteystiedot. Premiumissa sivuja voi olla enintään kahdeksan."),
            ("Onko kuukausimaksuja?",
             "Ei. Maksat WEBAURille kerran. Ainoat toistuvat kulut ovat verkkotunnus ja hosting, jotka maksat suoraan palveluntarjoajalle."),
            ("Kuinka kauan projekti kestää?",
             "Se riippuu työn laajuudesta ja siitä, miten sujuvasti luonnoksia voidaan käydä yhdessä läpi. Aikataulu sovitaan ensimmäisten viestien jälkeen, kun työ on selvillä — emme lupaa vakioitua päivämäärää etukäteen."),
            ("Voinko käyttää omia kuvia ja tekstejä?",
             "Kyllä. Jos sinulla on valokuvia tai tekstejä, joita haluat käyttää, työskentelemme niiden kanssa. Sovittua laajemmat kuvaukset tai tekstityöt hinnoitellaan erikseen."),
            ("Teettekö verkkokauppoja tai ajanvarausjärjestelmiä?",
             "Verkkokauppa ei tällä hetkellä kuulu palveluihimme. Laajat ajanvarausjärjestelmät ja muut erikoistoiminnot eivät sisälly pakettihintoihin, ja niistä sovitaan erikseen."),
        ]
        title = "Usein kysyttyä"
    rows = "".join(
        f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in items
    )
    return f'''<section class="section" style="padding-top:0" aria-labelledby="faq-title">
  <div class="wrap">
    <h2 id="faq-title" class="section-title">{title}</h2>
    <div class="faq">{rows}</div>
  </div>
</section>'''

def process_block(lang, heading="h2"):
    if lang == "en":
        steps = [
            ("01", "Discovery", "We start by understanding the business, its customers and what the new site needs to do."),
            ("02", "Design", "We shape the visual direction, typography and page structure before anything is built."),
            ("03", "Development", "We build a responsive, carefully coded website that holds up on a phone and a desktop."),
            ("04", "Review and launch", "We go through the content and look with you, test in common browsers, fix any bugs and publish the site."),
            ("05", "Handover", "You receive the source code, the files and instructions for publishing and moving the site. It is yours to keep."),
        ]
        eyebrow, title = "The process", "From the first message to a finished website you own."
    else:
        steps = [
            ("01", "Kartoitus", "Aloitamme tutustumalla yritykseen, asiakkaisiin ja siihen, mitä uuden sivuston pitää saada aikaan."),
            ("02", "Suunnittelu", "Muodostamme visuaalisen suunnan, typografian ja sivurakenteen ennen kuin mitään rakennetaan."),
            ("03", "Toteutus", "Rakennamme responsiivisen, huolella koodatun sivuston, joka kestää tarkastelun puhelimessa ja työpöydällä."),
            ("04", "Läpikäynti ja julkaisu", "Käymme sisällön ja ulkoasun kanssasi läpi, testaamme yleisimmillä selaimilla, korjaamme virheet ja julkaisemme sivuston."),
            ("05", "Luovutus", "Saat sivuston lähdekoodin, tiedostot sekä julkaisu- ja siirto-ohjeet. Sivusto on sinun."),
        ]
        eyebrow, title = "Työskentelytapa", "Ensimmäisestä viestistä valmiiseen sivustoon, joka on sinun."
    rows = []
    for i, (num, name, text) in enumerate(steps):
        cls = "process-step is-last" if i == len(steps) - 1 else "process-step"
        rows.append(f'<li class="{cls}"><div class="num">{num}</div><h3>{name}</h3><p class="muted">{text}</p></li>')
    return f'''<section class="section" aria-labelledby="process-title">
  <div class="wrap">
    <p class="eyebrow">{eyebrow}</p>
    <{heading} id="process-title" class="section-title" style="margin:12px 0 40px">{title}</{heading}>
    <ol class="process-rail">{"".join(rows)}</ol>
  </div>
</section>'''


def home(lang):
    page = "index.html"
    pre = asset_prefix(lang, 0)
    work = href(lang, page, lang, "work.html")
    contact = href(lang, page, lang, "contact.html")
    services = href(lang, page, lang, "services.html")
    about = href(lang, page, lang, "about.html")
    hale_case = href(lang, page, lang, "work/barber-studio.html")
    alto_case = href(lang, page, lang, "work/detailing.html")
    maison_case = href(lang, page, lang, "work/maison-cafe.html")

    hero_visual = f'''<div class="hero-stage">
      <div class="hero-layer hero-layer-alto">
        {device_desktop(pre, "alto/home-desktop", "Alto Detail -konseptisivuston etusivu työpöydällä" if lang=="fi" else "Desktop preview of the Alto Detail concept homepage", "lazy", "(min-width: 1100px) 420px, 70vw")}
      </div>
      <div class="hero-layer hero-layer-maison">
        {device_desktop(pre, "maison/home-desktop", "Maison Café -konseptisivuston etusivu työpöydällä" if lang=="fi" else "Desktop preview of the Maison Café concept homepage", "lazy", "(min-width: 1100px) 420px, 70vw")}
      </div>
      <div class="hero-layer hero-layer-hale">
        {device_desktop(pre, "hale/home-desktop", "Hale Barber Studio -konseptisivuston etusivu työpöydällä" if lang=="fi" else "Desktop preview of the Hale Barber Studio concept homepage", "eager", "(min-width: 1100px) 640px, 85vw")}
        {device_mobile(pre, "hale/home-mobile", "Hale Barber Studio -konseptisivuston etusivu puhelimella" if lang=="fi" else "Mobile preview of the Hale Barber Studio concept homepage", "lazy")}
      </div>
    </div>'''

    if lang == "en":
        trust = [
            ("Modern design", "A look and structure that belong to the business, not a reused template."),
            ("Mobile-first development", "Layouts that stay clear on a phone first, then hold up on a tablet and a desktop."),
            ("Professional execution", "Clean front-end code, considered typography and lightweight pages that load quickly."),
            ("Clear pricing", "Three published packages, paid once. What is not included is stated in the open."),
            ("Personal service", "A short path from the first message to a quote. Content and design are reviewed together before launch."),
            ("The site is yours", "No monthly fees. You get the source code, the files and instructions, and can carry on without us."),
        ]
        services_rows = [
            ("01", "design", False, "Website Design", "Professional layouts, visual identity, user experience and responsive design built around your brand.",
             ["A look and structure that belong to your business, not a template", "Layouts that stay clear on a phone, a tablet and a computer", "A visitor can understand what you do and what to do next"],
             "Read about design", "services.html#design"),
            ("02", "development", True, "Website Development", "Modern, functional, fast and responsive websites that are easy to work on later.",
             ["Clean front-end code that another developer can pick up", "Careful work so pages load quickly and stay readable", "A contact path that is ready to receive enquiries", "Technical foundations that help people find you"],
             "Read about development", "services.html#development"),
            ("03", "handover", False, "Launch and handover", "We publish the site and hand it over to you, with no monthly fees.",
             ["Testing in common browsers and bug fixes before handover", "Source code, files and instructions for publishing and moving the site", "Later changes on request, for a separately agreed one-time fee"],
             "Read about handover", "services.html#handover"),
        ]
        body = f'''
<section class="hero home-hero">
  <div class="wrap hero-grid">
    <div class="reveal">
      <p class="eyebrow">Independent web design studio</p>
      <h1 class="display">Websites built to move businesses forward.</h1>
      <p class="lead">WEBAUR designs and builds considered, modern websites that help a business stand out, earn trust and turn visitors into customers.</p>
      <div class="btn-row">
        <a class="btn btn-accent" href="{contact}">Start a project</a>
        <a class="btn btn-ghost" href="{work}">View the work</a>
      </div>
      <p class="avail"><i aria-hidden="true"></i> Currently taking on new projects</p>
    </div>
    {hero_visual}
  </div>
</section>
<section class="section" style="padding-top:0" aria-labelledby="trust-title">
  <div class="wrap">
    <p class="eyebrow">Why WEBAUR</p>
    <h2 id="trust-title" class="section-title" style="margin:12px 0 40px">A clearer first impression, built with care.</h2>
    <div class="trust-grid">
      {"".join(f'<article class="trust-item"><h3>{t}</h3><p>{d}</p></article>' for t,d in trust)}
    </div>
  </div>
</section>
<section class="section band band-line home-services" aria-labelledby="services-title">
  <div class="wrap">
    <p class="eyebrow">Services</p>
    <h2 id="services-title" class="section-title" style="margin:12px 0 8px">Design, development and launch — without the extras you do not need.</h2>
    <p class="lead" style="margin-bottom:8px">Websites for local small businesses: barbers and hair salons, car washes and detailers, garages, restaurants and cafés, beauty, cleaning and renovation companies.</p>
    {"".join(f'''<article class="service-row{" is-alt" if alt else ""}" id="{sid}">
      <div class="num">{num}</div>
      <div>
        <h3>{title}</h3>
        <p class="muted">{desc}</p>
      </div>
      <ul>{"".join(f"<li>{x}</li>" for x in items)}</ul>
      <div class="service-cta"><a class="btn btn-ghost" href="{href(lang, page, lang, link)}">{cta}</a></div>
    </article>''' for num,sid,alt,title,desc,items,cta,link in services_rows)}
  </div>
</section>
<section class="section home-work" aria-labelledby="work-title">
  <div class="wrap">
    <div class="section-head">
      <div>
        <p class="eyebrow">Selected concept work</p>
        <h2 id="work-title" class="section-title" style="margin-top:12px">Different businesses. Different digital experiences.</h2>
      </div>
    </div>
    <article class="teaser-featured">
      <div class="device-stack">
        {device_desktop(pre, "hale/home-desktop", "Hale Barber Studio — homepage, desktop", "lazy")}
        {device_mobile(pre, "hale/home-mobile", "Hale Barber Studio — homepage, mobile", "lazy")}
      </div>
      <div class="teaser-copy">
        <div class="folio-kicker-row">
          <span class="badge">Concept project</span>
          <span class="kicker">Barber</span>
        </div>
        <h3><a href="{hale_case}">Hale Barber Studio</a></h3>
        <p class="teaser-line">A five-page concept for an independent barbershop: bone, forest green, and photographs of the room rather than stock smiles.</p>
        <a class="teaser-link" href="{hale_case}">Read the project</a>
      </div>
    </article>
    <div class="teaser-pair">
      <article class="teaser-alto">
        {device_desktop(pre, "alto/home-desktop", "Alto Detail — homepage, desktop")}
        <div class="teaser-copy">
          <div class="folio-kicker-row">
            <span class="badge">Concept project</span>
            <span class="kicker">Automotive detailing</span>
          </div>
          <h3><a href="{alto_case}">Alto Detail</a></h3>
          <p class="teaser-line">A showroom-like detailing concept with priced packages and an honest before-and-after comparison.</p>
          <a class="teaser-link" href="{alto_case}">Read the project</a>
        </div>
      </article>
      <article class="teaser-maison">
        <div class="teaser-copy">
          <div class="folio-kicker-row">
            <span class="badge">Concept project</span>
            <span class="kicker">Café</span>
          </div>
          <h3><a href="{maison_case}">Maison Café</a></h3>
          <p class="teaser-line">A five-page café concept, built like a short publication: a menu, a room, a story, and a visit that lives only in the story.</p>
          <a class="teaser-link" href="{maison_case}">Read the project</a>
        </div>
        {device_desktop(pre, "maison/home-desktop", "Maison Café — homepage, desktop")}
      </article>
    </div>
    <div class="home-teaser-foot">
      <a class="btn btn-ghost" href="{work}">See all work</a>
    </div>
  </div>
</section>
{process_block(lang)}
{pricing_block(lang, page, compact=True)}
<section class="section band band-line" aria-labelledby="about-title">
  <div class="wrap about-split">
    <div>
      <p class="eyebrow">About</p>
      <h2 id="about-title" class="section-title">An independent studio, focused on the work.</h2>
    </div>
    <div>
      <p class="lead">WEBAUR helps businesses strengthen their online presence with considered design, careful development and clear communication. There is no invented team, office or list of awards here — the concepts in the portfolio are the clearest picture of how a project is approached.</p>
      <p style="margin-top:24px"><a class="btn btn-ghost" href="{about}">More about the studio</a></p>
    </div>
  </div>
</section>
{cta(lang, page)}
'''
        return page_shell(lang, page, "WEBAUR — Independent web design studio",
            "WEBAUR designs and builds thoughtful, modern websites that help businesses stand out, build trust and turn visitors into customers.",
            "", body)

    trust = [
        ("Nykyaikainen suunnittelu", "Ilme ja rakenne, jotka kuuluvat juuri kyseiselle yritykselle, ei uudelleenkäytettyyn mallipohjaan."),
        ("Mobiili edellä", "Asettelut, jotka pysyvät selkeinä ensin puhelimessa ja kestävät myös tabletin ja työpöydän."),
        ("Huolellinen toteutus", "Siistiä front-end-koodia, harkittua typografiaa ja kevyitä sivuja, jotka latautuvat nopeasti."),
        ("Selkeä hinnoittelu", "Kolme julkaistua pakettia kertamaksulla. Se, mitä hintaan ei sisälly, kerrotaan avoimesti."),
        ("Henkilökohtainen palvelu", "Lyhyt matka ensimmäisestä viestistä tarjoukseen. Sisältö ja ulkoasu käydään yhdessä läpi ennen julkaisua."),
        ("Sivusto on sinun", "Ei kuukausimaksuja. Saat lähdekoodin, tiedostot ja ohjeet, ja voit jatkaa ilman meitä."),
    ]
    services_rows = [
        ("01", "design", False, "Verkkosivujen suunnittelu", "Ammattimaiset asettelut, visuaalinen identiteetti, käyttökokemus ja responsiivinen suunnittelu brändisi ympärille.",
         ["Ilme ja rakenne, jotka kuuluvat juuri sinun yrityksellesi — ei valmista mallipohjaa", "Asettelut, jotka pysyvät selkeinä puhelimessa, tabletilla ja tietokoneella", "Kävijä ymmärtää, mitä teet ja mitä häneltä toivotaan seuraavaksi"],
         "Lue suunnittelusta", "services.html#design"),
        ("02", "development", True, "Verkkosivujen toteutus", "Nykyaikaiset, toimivat, nopeat ja responsiiviset sivustot, joita on helppo muokata myöhemmin.",
         ["Siistiä front-end-koodia, jota myös toinen tekijä voi jatkaa", "Huolellinen toteutus, jotta sivut latautuvat nopeasti ja pysyvät luettavina", "Yhteydenottopolku, joka on valmis ottamaan viestit vastaan", "Tekninen perusta, joka auttaa asiakkaita löytämään sinut"],
         "Lue toteutuksesta", "services.html#development"),
        ("03", "handover", False, "Julkaisu ja luovutus", "Julkaisemme sivuston ja luovutamme sen sinulle ilman kuukausimaksuja.",
         ["Testaus yleisimmillä selaimilla ja virheiden korjaus ennen luovutusta", "Lähdekoodi, tiedostot sekä julkaisu- ja siirto-ohjeet", "Myöhemmät muutokset tarvittaessa erikseen sovittavalla kertamaksulla"],
         "Lue luovutuksesta", "services.html#handover"),
    ]
    body = f'''
<section class="hero home-hero">
  <div class="wrap hero-grid">
    <div class="reveal">
      <p class="eyebrow">Itsenäinen verkkosuunnittelustudio</p>
      <h1 class="display">Yrityksesi ansaitsee paremmat verkkosivut.</h1>
      <p class="lead">Suunnittelemme ja rakennamme harkittuja, nykyaikaisia verkkosivuja, joiden avulla yritys erottuu, herättää luottamusta ja muuttaa kävijät asiakkaiksi.</p>
      <div class="btn-row">
        <a class="btn btn-accent" href="{contact}">Aloita projekti</a>
        <a class="btn btn-ghost" href="{work}">Tutustu töihimme</a>
      </div>
      <p class="avail"><i aria-hidden="true"></i> Otamme tällä hetkellä vastaan uusia projekteja</p>
    </div>
    {hero_visual}
  </div>
</section>
<section class="section" style="padding-top:0" aria-labelledby="trust-title">
  <div class="wrap">
    <p class="eyebrow">Miksi WEBAUR</p>
    <h2 id="trust-title" class="section-title" style="margin:12px 0 40px">Selkeämpi ensivaikutelma, rakennettu huolella.</h2>
    <div class="trust-grid">
      {"".join(f'<article class="trust-item"><h3>{t}</h3><p>{d}</p></article>' for t,d in trust)}
    </div>
  </div>
</section>
<section class="section band band-line home-services" aria-labelledby="services-title">
  <div class="wrap">
    <p class="eyebrow">Palvelut</p>
    <h2 id="services-title" class="section-title" style="margin:12px 0 8px">Suunnittelu, toteutus ja julkaisu — ilman turhia lisäkerroksia.</h2>
    <p class="lead" style="margin-bottom:8px">Verkkosivuja paikallisille pienyrityksille: parturi-kampaamoille, autopesuloille ja autonhoitoon, autokorjaamoille, ravintoloille ja kahviloille sekä kauneus-, siivous- ja remonttialan yrityksille.</p>
    {"".join(f'''<article class="service-row{" is-alt" if alt else ""}" id="{sid}">
      <div class="num">{num}</div>
      <div>
        <h3>{title}</h3>
        <p class="muted">{desc}</p>
      </div>
      <ul>{"".join(f"<li>{x}</li>" for x in items)}</ul>
      <div class="service-cta"><a class="btn btn-ghost" href="{href(lang, page, lang, link)}">{cta}</a></div>
    </article>''' for num,sid,alt,title,desc,items,cta,link in services_rows)}
  </div>
</section>
<section class="section home-work" aria-labelledby="work-title">
  <div class="wrap">
    <div class="section-head">
      <div>
        <p class="eyebrow">Valittuja konseptitöitä</p>
        <h2 id="work-title" class="section-title" style="margin-top:12px">Eri yrityksiä. Erilaisia digitaalisia kokemuksia.</h2>
      </div>
    </div>
    <article class="teaser-featured">
      <div class="device-stack">
        {device_desktop(pre, "hale/home-desktop", "Hale Barber Studio — etusivu, työpöytä", "lazy")}
        {device_mobile(pre, "hale/home-mobile", "Hale Barber Studio — etusivu, puhelin", "lazy")}
      </div>
      <div class="teaser-copy">
        <div class="folio-kicker-row">
          <span class="badge">Konseptiprojekti</span>
          <span class="kicker">Parturi</span>
        </div>
        <h3><a href="{hale_case}">Hale Barber Studio</a></h3>
        <p class="teaser-line">Viisisivuinen konsepti itsenäiselle parturille: luunväri, metsänvihreä ja kuvia huoneesta, ei valmiskuvien hymyistä.</p>
        <a class="teaser-link" href="{hale_case}">Lue projektiesittely</a>
      </div>
    </article>
    <div class="teaser-pair">
      <article class="teaser-alto">
        {device_desktop(pre, "alto/home-desktop", "Alto Detail — etusivu, työpöytä")}
        <div class="teaser-copy">
          <div class="folio-kicker-row">
            <span class="badge">Konseptiprojekti</span>
            <span class="kicker">Autonhoito ja detailing</span>
          </div>
          <h3><a href="{alto_case}">Alto Detail</a></h3>
          <p class="teaser-line">Showroom-henkinen detailing-konsepti hinnoiteltuine paketteineen ja rehellisine ennen–jälkeen-vertailuineen.</p>
          <a class="teaser-link" href="{alto_case}">Lue projektiesittely</a>
        </div>
      </article>
      <article class="teaser-maison">
        <div class="teaser-copy">
          <div class="folio-kicker-row">
            <span class="badge">Konseptiprojekti</span>
            <span class="kicker">Kahvila</span>
          </div>
          <h3><a href="{maison_case}">Maison Café</a></h3>
          <p class="teaser-line">Viisisivuinen kahvilakonsepti, rakennettu kuin lyhyt julkaisu: ruokalista, huone, tarina ja vierailu, joka elää vain tarinassa.</p>
          <a class="teaser-link" href="{maison_case}">Lue projektiesittely</a>
        </div>
        {device_desktop(pre, "maison/home-desktop", "Maison Café — etusivu, työpöytä")}
      </article>
    </div>
    <div class="home-teaser-foot">
      <a class="btn btn-ghost" href="{work}">Katso kaikki työt</a>
    </div>
  </div>
</section>
{process_block(lang)}
{pricing_block(lang, page, compact=True)}
<section class="section band band-line" aria-labelledby="about-title">
  <div class="wrap about-split">
    <div>
      <p class="eyebrow">Meistä</p>
      <h2 id="about-title" class="section-title">Itsenäinen studio, jonka keskiössä on työ.</h2>
    </div>
    <div>
      <p class="lead">WEBAUR auttaa yrityksiä vahvistamaan verkkoläsnäoloaan harkitulla suunnittelulla, huolellisella toteutuksella ja selkeällä viestinnällä. Täällä ei ole keksittyä tiimiä, toimistoa tai palkintolistaa — portfolion konseptit kertovat selvimmin, miten projektia lähestytään.</p>
      <p style="margin-top:24px"><a class="btn btn-ghost" href="{about}">Lisää studiosta</a></p>
    </div>
  </div>
</section>
{cta(lang, page)}
'''
    return page_shell(lang, page, "WEBAUR — Itsenäinen verkkosuunnittelustudio",
        "WEBAUR suunnittelee ja rakentaa harkittuja, nykyaikaisia verkkosivuja, joiden avulla yritys erottuu, herättää luottamusta ja muuttaa kävijät asiakkaiksi.",
        "", body)

def services_page(lang):
    page = "services.html"
    if lang == "en":
        rows = [
            ("01", "design", False, "Website Design",
             "Considered visual design built around your brand, your customers and the goals of the business.",
             "You get a clear structure, considered typography and a visual system that belongs to your business. The aim is that a first-time visitor understands what you do and feels ready to get in touch."),
            ("02", "development", True, "Website Development",
             "Fast, responsive and reliable websites that work well across devices.",
             "We build with clean front-end code, pay attention to loading speed, and make sure the contact path is ready. The technical foundations of search visibility are part of the work, not an afterthought."),
            ("03", "handover", False, "Launch and handover",
             "We test, publish and hand the finished site over to you. You pay once, and the site is yours.",
             "You receive the source code, the files and instructions for publishing and moving the site, and the domain is registered in your name. There are no monthly fees: you can keep the site without WEBAUR or move it to another developer. If you later want changes, we do them for a separately agreed one-time fee."),
        ]
        body = f'''
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">Services</p>
    <h1 class="display">Everything you need for a stronger first impression online.</h1>
    <p class="lead">Design, development and launch for local small businesses — from barbers, car washes and garages to restaurants, cafés, beauty, cleaning and renovation companies.</p>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap">
    {"".join(f'''<article class="service-row{" is-alt" if alt else ""}" id="{sid}">
      <div class="num">{num}</div>
      <div>
        <h2>{title}</h2>
        <p>{intro}</p>
        <p class="muted" style="margin-top:12px">{more}</p>
      </div>
      <div class="service-cta"><a class="btn btn-accent" href="{href(lang, page, lang, "contact.html")}">Start a project</a></div>
    </article>''' for num,sid,alt,title,intro,more in rows)}
  </div>
</section>
{process_block(lang)}
<p class="wrap" style="padding-bottom:8px"><a class="btn btn-ghost" href="{href(lang, page, lang, "pricing.html")}">See packages and prices</a></p>
{cta(lang, page)}
'''
        return page_shell(lang, page, "Services — WEBAUR",
            "Website design, development and launch for small businesses. One-time payment, no monthly fees — the finished site is yours.",
            "services", body)
    rows = [
        ("01", "design", False, "Verkkosivujen suunnittelu",
         "Harkittu visuaalinen suunnittelu, joka rakentuu brändisi, asiakkaidesi ja liiketoimintasi tavoitteiden ympärille.",
         "Saat selkeän rakenteen, harkitun typografian ja visuaalisen järjestelmän, joka kuuluu juuri sinun yrityksellesi. Tavoitteena on, että ensikertalainen kävijä ymmärtää, mitä teet, ja uskaltaa ottaa yhteyttä."),
        ("02", "development", True, "Verkkosivujen toteutus",
         "Nopeat, responsiiviset ja luotettavat sivustot, jotka toimivat kaikilla laitteilla.",
         "Rakennamme siistillä front-end-koodilla, kiinnitämme huomiota latausnopeuteen ja varmistamme, että yhteydenottopolku on valmis. Hakukoneoptimoinnin tekninen perusta kuuluu työhön, ei jää jälkiajatukseksi."),
        ("03", "handover", False, "Julkaisu ja luovutus",
         "Testaamme, julkaisemme ja luovutamme valmiin sivuston sinulle. Maksat kerran, ja sivusto on sinun.",
         "Saat lähdekoodin, tiedostot sekä julkaisu- ja siirto-ohjeet, ja verkkotunnus rekisteröidään omiin nimiisi. Kuukausimaksuja ei ole: voit jatkaa ilman WEBAURia tai siirtää sivuston toiselle tekijälle. Jos haluat myöhemmin muutoksia, teemme ne erikseen sovittavalla kertamaksulla."),
    ]
    body = f'''
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">Palvelut</p>
    <h1 class="display">Kaikki, mitä tarvitset vahvempaan ensivaikutelmaan verkossa.</h1>
    <p class="lead">Suunnittelu, toteutus ja julkaisu paikallisille pienyrityksille — parturi-kampaamoista, autopesuloista ja korjaamoista ravintoloihin, kahviloihin sekä kauneus-, siivous- ja remonttialan yrityksiin.</p>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap">
    {"".join(f'''<article class="service-row{" is-alt" if alt else ""}" id="{sid}">
      <div class="num">{num}</div>
      <div>
        <h2>{title}</h2>
        <p>{intro}</p>
        <p class="muted" style="margin-top:12px">{more}</p>
      </div>
      <div class="service-cta"><a class="btn btn-accent" href="{href(lang, page, lang, "contact.html")}">Aloita projekti</a></div>
    </article>''' for num,sid,alt,title,intro,more in rows)}
  </div>
</section>
{process_block(lang)}
<p class="wrap" style="padding-bottom:8px"><a class="btn btn-ghost" href="{href(lang, page, lang, "pricing.html")}">Katso paketit ja hinnat</a></p>
{cta(lang, page)}
'''
    return page_shell(lang, page, "Palvelut — WEBAUR",
        "Verkkosivujen suunnittelu, toteutus ja julkaisu pienyrityksille. Kertamaksu, ei kuukausimaksuja – valmis sivusto on sinun.",
        "services", body)


def pricing_page(lang):
    page = "pricing.html"
    if lang == "en":
        intro = '''
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">Pricing</p>
    <h1 class="display">Three packages, clearly priced.</h1>
    <p class="lead">Starter, Business and Premium: one page, up to five pages or up to eight pages.</p>
  </div>
</section>'''
        title, desc = "Pricing — WEBAUR", "WEBAUR website packages paid once: Starter €490, Business €890, Premium €1,490. No monthly fees — the site is yours."
    else:
        intro = '''
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">Hinnat</p>
    <h1 class="display">Kolme pakettia, selkeästi hinnoiteltuna.</h1>
    <p class="lead">Starter, Business ja Premium: yksi sivu, enintään viisi tai enintään kahdeksan sivua.</p>
  </div>
</section>'''
        title, desc = "Hinnat — WEBAUR", "WEBAURin verkkosivupaketit kertamaksulla: Starter 490 €, Business 890 € ja Premium 1 490 €. Ei kuukausimaksuja – sivusto on sinun."
    # pricing_block already has a section-title; on this page the h1 is in the hero, so keep h2 in the block
    body = intro + pricing_block(lang, page, "h2") + faq_block(lang) + cta(lang, page)
    return page_shell(lang, page, title, desc, "pricing", body)


def about_page(lang):
    page = "about.html"
    if lang == "en":
        points = [
            ("Design quality", "A website should look like your business, not like a template. We pay attention to typography, spacing, photography and hierarchy so the first impression feels intentional."),
            ("Technical care", "Design only works if the site is fast, readable and reliable on every screen. We build with clean front-end code, thoughtful performance and a structure that is easy to work on later."),
            ("Clear communication", "The process is straightforward: discovery, design, development, review and launch, and handover. You will always know what is happening and what we need from you."),
            ("Tailored solutions", "Every project is planned around the individual business. We do not sell a single layout with the logo swapped."),
            ("Attention to detail", "Small things — a clear button, a readable menu on a phone, a form that is honest about what happens next — are what make a site feel considered. No invented awards, client logos or years in business. The work should speak for itself."),
        ]
        body = f'''
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">About</p>
    <h1 class="display">Attention to the details that build trust.</h1>
    <p class="lead">WEBAUR is an independent web design studio. We help businesses improve their online presence with considered design, careful development and clear communication.</p>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="about-points">
      {"".join(f'<article><h2>{t}</h2><p class="muted">{d}</p></article>' for t,d in points)}
    </div>
    <p style="margin-top:40px"><a class="btn btn-accent" href="{href(lang, page, lang, "contact.html")}">Start a project</a></p>
  </div>
</section>
'''
        return page_shell(lang, page, "About — WEBAUR",
            "WEBAUR is an independent web design studio focused on design quality, technical care and clear communication.",
            "about", body)
    points = [
        ("Suunnittelun laatu", "Sivuston pitäisi näyttää sinun yritykseltäsi, ei mallipohjalta. Kiinnitämme huomiota typografiaan, tilaan, valokuviin ja hierarkiaan, jotta ensivaikutelma tuntuu harkitulta."),
        ("Tekninen huolellisuus", "Suunnittelu toimii vain, jos sivusto on nopea, luettava ja luotettava kaikilla näytöillä. Rakennamme siistillä front-end-koodilla, harkitulla suorituskyvyllä ja rakenteella, jota on helppo muokata myöhemmin."),
        ("Selkeä viestintä", "Prosessi on suora: kartoitus, suunnittelu, toteutus, läpikäynti ja julkaisu sekä luovutus. Tiedät aina, mitä tapahtuu ja mitä tarvitsemme sinulta."),
        ("Räätälöidyt ratkaisut", "Jokainen projekti suunnitellaan kyseisen yrityksen ympärille. Emme myy yhtä ja samaa asettelua, johon vaihdetaan logo."),
        ("Huomio yksityiskohtiin", "Pienet asiat — selkeä painike, luettava valikko puhelimessa, lomake, joka kertoo rehellisesti, mitä seuraavaksi tapahtuu — tekevät sivustosta harkitun. Emme keksi palkintoja, asiakaslogoja tai toimintavuosia. Työn pitää puhua puolestaan."),
    ]
    body = f'''
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">Meistä</p>
    <h1 class="display">Huomiota niihin yksityiskohtiin, jotka rakentavat luottamusta.</h1>
    <p class="lead">WEBAUR on itsenäinen verkkosuunnittelustudio. Autamme yrityksiä vahvistamaan verkkoläsnäoloaan harkitulla suunnittelulla, huolellisella toteutuksella ja selkeällä viestinnällä.</p>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="about-points">
      {"".join(f'<article><h2>{t}</h2><p class="muted">{d}</p></article>' for t,d in points)}
    </div>
    <p style="margin-top:40px"><a class="btn btn-accent" href="{href(lang, page, lang, "contact.html")}">Aloita projekti</a></p>
  </div>
</section>
'''
    return page_shell(lang, page, "Meistä — WEBAUR",
        "WEBAUR on itsenäinen verkkosuunnittelustudio, jonka työn ytimessä ovat suunnittelun laatu, tekninen huolellisuus ja selkeä viestintä.",
        "about", body)

def contact_form(lang, privacy):
    en = lang == "en"
    T = (lambda e, f: e if en else f)
    return f'''<form class="contact-form" name="contact" action="mailto:{EMAIL}" method="post" enctype="text/plain" novalidate>
      <p class="hp" aria-hidden="true"><label>Company website <input type="text" name="company-website" tabindex="-1" autocomplete="off" /></label></p>
      <div class="field-row">
        <div class="field">
          <label for="name">{T("Name", "Nimi")}</label>
          <input id="name" name="name" type="text" autocomplete="name" required />
        </div>
        <div class="field">
          <label for="business">{T("Business name", "Yrityksen nimi")}</label>
          <input id="business" name="business" type="text" autocomplete="organization" required />
        </div>
      </div>
      <div class="field">
        <label for="email">{T("Your email", "Sähköpostiosoitteesi")}</label>
        <input id="email" name="email" type="email" autocomplete="email" inputmode="email" data-mail-label="{T("Email", "Sähköposti")}" required />
      </div>
      <div class="field-row">
        <div class="field">
          <label for="type">{T("Type of website", "Sivuston tyyppi")}</label>
          <select id="type" name="type" required>
            <option value="">{T("Please select", "Valitse")}</option>
            <option>{T("New website", "Uusi verkkosivusto")}</option>
            <option>{T("Redesign", "Nykyisen sivuston uudistus")}</option>
            <option>{T("Landing page", "Yksisivuinen sivusto")}</option>
            <option>{T("Changes to an existing site", "Muutos olemassa olevaan sivustoon")}</option>
            <option>{T("Other", "Muu")}</option>
          </select>
        </div>
        <div class="field">
          <label for="budget">{T("Package (optional)", "Paketti (valinnainen)")}</label>
          <select id="budget" name="budget">
            <option value="">{T("I’d rather not say", "En osaa vielä sanoa")}</option>
            <option value="starter">{T("Starter — 1 page — €490", "Starter — 1 sivu — 490 €")}</option>
            <option value="business">{T("Business — up to 5 pages — €890", "Business — enintään 5 sivua — 890 €")}</option>
            <option value="premium">{T("Premium — up to 8 pages — €1,490", "Premium — enintään 8 sivua — 1&nbsp;490 €")}</option>
            <option value="unsure">{T("Not sure yet — help me choose", "Tarvitsen apua valintaan")}</option>
          </select>
        </div>
      </div>
      <div class="field">
        <label for="website">{T("Current website (optional)", "Nykyinen verkkosivusto (valinnainen)")}</label>
        <input id="website" name="website" type="url" autocomplete="url" inputmode="url" placeholder="https://" />
      </div>
      <div class="field">
        <label for="message">{T("About the project", "Kerro projektista")}</label>
        <textarea id="message" name="message" rows="5" required></textarea>
      </div>
      <label class="consent">
        <input id="consent" type="checkbox" name="consent" value="yes" required />
        <span>{T(f'I agree that WEBAUR may use this information to reply to my enquiry. Read the <a href="{privacy}">privacy policy</a>.', f'Hyväksyn, että WEBAUR käyttää näitä tietoja vastatakseen yhteydenottooni. Lue <a href="{privacy}">tietosuojaseloste</a>.')}</span>
      </label>
      <button class="btn btn-accent btn-block" type="submit" data-label="{T("Open the email", "Avaa valmis sähköposti")}">{T("Open the email", "Avaa valmis sähköposti")}</button>
      <p class="form-note">{T(f'The button opens your own email app with the message filled in. It is sent only when you press Send there. If nothing opens, write to <a href="mailto:{EMAIL}" data-email-slot>{EMAIL}</a>.', f'Painike avaa oman sähköpostiohjelmasi, jossa viesti on valmiiksi täytettynä. Viesti lähtee vasta, kun painat siellä Lähetä. Jos mitään ei avaudu, kirjoita osoitteeseen <a href="mailto:{EMAIL}" data-email-slot>{EMAIL}</a>.')}</p>
      <div class="form-alert" id="form-status" hidden tabindex="-1" role="status" aria-live="polite"></div>
    </form>'''


def contact_page(lang):
    page = "contact.html"
    privacy = href(lang, page, lang, "privacy.html")
    pricing = href(lang, page, lang, "pricing.html")
    en = lang == "en"
    T = (lambda e, f: e if en else f)
    body = f'''
<section class="page-hero contact-hero">
  <div class="wrap">
    <p class="eyebrow">{T("Contact", "Yhteystiedot")}</p>
    <h1 class="display">{T("Tell us about your project.", "Kerro projektistasi.")}</h1>
    <p class="lead">{T("Share a little about the business and what you need. We reply by email and walk through the next step with you.", "Kerro hieman yrityksestäsi ja siitä, mitä tarvitset. Vastaamme sähköpostitse ja käymme seuraavan askeleen läpi kanssasi.")}</p>
  </div>
</section>
<section class="section contact-section" id="form">
  <div class="wrap form-layout">
    <aside class="contact-aside" aria-label="{T("Contact details", "Yhteystiedot")}">
      <div class="contact-card js-email-wrap">
        <p class="contact-label">{T("Email", "Sähköposti")}</p>
        <p class="contact-email"><a href="mailto:{EMAIL}" data-email-slot>{EMAIL}</a></p>
        <p class="muted">{T("Write directly, or use the form — it prepares the email for you.", "Kirjoita suoraan tai käytä lomaketta, joka kokoaa viestin valmiiksi.")}</p>
      </div>
      <dl class="contact-facts">
        <div><dt>{T("Studio", "Studio")}</dt><dd>{T("Independent, based in Finland", "Itsenäinen, Suomessa")}</dd></div>
        <div><dt>{T("How to reach us", "Yhteydenotto")}</dt><dd>{T("By email", "Sähköpostitse")}</dd></div>
        <div><dt>{T("Prices", "Hinnat")}</dt><dd><a href="{pricing}">{T("€490 / €890 / €1,490", "490 € / 890 € / 1&nbsp;490 €")}</a></dd></div>
        <div><dt>{T("Payment", "Maksu")}</dt><dd>{T("One-time, no monthly fees", "Kertamaksu, ei kuukausimaksuja")}</dd></div>
      </dl>
      <div class="contact-next">
        <h2>{T("What happens next", "Mitä seuraavaksi tapahtuu")}</h2>
        <ol>
          <li>{T("We read your message and reply by email.", "Luemme viestisi ja vastaamme sähköpostitse.")}</li>
          <li>{T("If anything needs clarifying, we ask by email.", "Jos jokin vaatii tarkennusta, kysymme sen sähköpostitse.")}</li>
          <li>{T("You receive a written quote with the scope, price and timetable.", "Saat kirjallisen tarjouksen, jossa on laajuus, hinta ja aikataulu.")}</li>
        </ol>
      </div>
    </aside>
    {contact_form(lang, privacy)}
  </div>
</section>
'''
    if en:
        return page_shell(lang, page, "Contact — WEBAUR",
            f"Tell WEBAUR about your project. Email {EMAIL} or use the form to tell us about a new website or a redesign.",
            "contact", body)
    return page_shell(lang, page, "Yhteystiedot — WEBAUR",
        f"Kerro WEBAURille projektistasi. Kirjoita osoitteeseen {EMAIL} tai käytä lomaketta ja kerro uudesta sivustosta tai uudistuksesta.",
        "contact", body)


def thanks_page(lang):
    page = "thanks.html"
    home = href(lang, page, lang, "index.html")
    contact = href(lang, page, lang, "contact.html")
    if lang == "en":
        body = f'''
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">Thank you</p>
    <h1 class="display">Thanks for getting in touch.</h1>
    <p class="lead">If you sent a message to <a href="mailto:{EMAIL}" data-email-slot>{EMAIL}</a>, we will reply by email. If you have not sent one yet, the contact page will prepare it for you.</p>
    <div class="btn-row" style="margin-top:32px"><a class="btn btn-accent" href="{home}">Back to home</a><a class="btn btn-ghost" href="{contact}">Contact page</a></div>
  </div>
</section>'''
        return page_shell(lang, page, "Thank you — WEBAUR", "Thank you for contacting WEBAUR.", "", body)
    body = f'''
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">Kiitos</p>
    <h1 class="display">Kiitos yhteydenotosta.</h1>
    <p class="lead">Jos lähetit viestin osoitteeseen <a href="mailto:{EMAIL}" data-email-slot>{EMAIL}</a>, vastaamme sähköpostitse. Jos et ole vielä lähettänyt viestiä, yhteystietosivu kokoaa sen valmiiksi.</p>
    <div class="btn-row" style="margin-top:32px"><a class="btn btn-accent" href="{home}">Takaisin etusivulle</a><a class="btn btn-ghost" href="{contact}">Yhteystiedot</a></div>
  </div>
</section>'''
    return page_shell(lang, page, "Kiitos — WEBAUR", "Kiitos yhteydenotostasi WEBAURiin.", "", body)


def privacy_page(lang):
    page = "privacy.html"
    contact = href(lang, page, lang, "contact.html")
    mail = f'<a href="mailto:{EMAIL}" data-email-slot>{EMAIL}</a>'
    if lang == "en":
        body = f'''
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">Privacy</p>
    <h1 class="display">Privacy Policy</h1>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap prose">
    <p>This policy explains how WEBAUR handles the information you share when you contact us. WEBAUR has not yet published its official company details (legal name, business ID and postal address); they will be added here once they are confirmed.</p>
    <h2>Data controller and contact</h2>
    <p>WEBAUR, an independent web design studio based in Finland. Questions and requests about your data: {mail}.</p>
    <h2>What we collect</h2>
    <p>The <a href="{contact}">contact form</a> does not store or send anything by itself. It prepares an email in your own email app, and you decide whether to send it. If you do, we receive what you wrote: your name, business name, email address, the type of website, an optional package choice, an optional current website, your message and your consent. If you email us directly, we receive the content of that email.</p>
    <h2>Why we collect it</h2>
    <p>To reply to your enquiry and, if you wish, to prepare a quote. The legal basis is your consent and steps taken at your request before a possible agreement. We do not add enquiries to marketing lists.</p>
    <h2>Where it is processed</h2>
    <p>The website is hosted on GitHub Pages (GitHub, Inc.). GitHub may log technical data such as visitors’ IP addresses for security purposes. Emails are handled in the email service WEBAUR uses. The site uses no analytics, no advertising and no tracking cookies, and its fonts and images are served from the site itself.</p>
    <h2>Retention and your rights</h2>
    <p>Enquiries are kept only as long as needed to handle the enquiry and any resulting work. You may ask to access, correct or delete your data by writing to {mail}. You may also lodge a complaint with a data protection authority — in Finland, the Office of the Data Protection Ombudsman.</p>
    <p class="prose-date">Last updated: 12 November 2026.</p>
  </div>
</section>'''
        return page_shell(lang, page, "Privacy Policy — WEBAUR",
            f"How WEBAUR handles the information you share when you get in touch. Contact: {EMAIL}.",
            "", body)
    body = f'''
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">Tietosuoja</p>
    <h1 class="display">Tietosuojaseloste</h1>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap prose">
    <p>Tämä seloste kertoo, miten WEBAUR käsittelee tietoja, jotka annat ottaessasi yhteyttä. WEBAUR ei ole vielä julkaissut virallisia yritystietojaan (virallinen nimi, Y-tunnus ja postiosoite). Ne lisätään tähän, kun ne on vahvistettu.</p>
    <h2>Rekisterinpitäjä ja yhteystiedot</h2>
    <p>WEBAUR, itsenäinen verkkosuunnittelustudio Suomesta. Tietosuojaa koskevat kysymykset ja pyynnöt: {mail}.</p>
    <h2>Mitä tietoja keräämme</h2>
    <p><a href="{contact}">Yhteydenottolomake</a> ei itse tallenna eikä lähetä mitään. Se kokoaa viestin omaan sähköpostiohjelmaasi, ja sinä päätät, lähetätkö sen. Jos lähetät, saamme kirjoittamasi tiedot: nimen, yrityksen nimen, sähköpostiosoitteen, sivuston tyypin, valinnaisen pakettivalinnan, valinnaisen nykyisen sivuston osoitteen, viestin ja suostumuksesi. Jos kirjoitat meille suoraan, saamme sähköpostisi sisällön.</p>
    <h2>Miksi käsittelemme tietoja</h2>
    <p>Vastataksemme yhteydenottoosi ja tarvittaessa laatiaksemme tarjouksen. Käsittelyn perusteena on suostumuksesi sekä pyynnöstäsi tehtävät toimet ennen mahdollista sopimusta. Emme lisää yhteydenottoja markkinointilistoille.</p>
    <h2>Missä tietoja käsitellään</h2>
    <p>Sivusto toimii GitHub Pages -palvelussa (GitHub, Inc.). GitHub voi tallentaa teknisiä tietoja, kuten kävijöiden IP-osoitteita, palvelun tietoturvan vuoksi. Sähköpostit käsitellään WEBAURin käyttämässä sähköpostipalvelussa. Sivusto ei käytä analytiikkaa, mainontaa eikä seurantaevästeitä, ja sen fontit ja kuvat ladataan sivustolta itseltään.</p>
    <h2>Säilytys ja oikeutesi</h2>
    <p>Yhteydenottoja säilytetään vain niin kauan kuin viestiin vastaaminen ja mahdollinen työ edellyttävät. Voit pyytää tietojesi tarkastamista, korjaamista tai poistamista kirjoittamalla osoitteeseen {mail}. Voit myös tehdä valituksen valvontaviranomaiselle, Suomessa tietosuojavaltuutetun toimistolle.</p>
    <p class="prose-date">Päivitetty 12. marraskuuta 2026.</p>
  </div>
</section>'''
    return page_shell(lang, page, "Tietosuojaseloste — WEBAUR",
        f"Miten WEBAUR käsittelee tietoja, jotka annat ottaessasi yhteyttä. Yhteystiedot: {EMAIL}.",
        "", body)


def not_found_page(lang):
    page = "404.html"
    home = href(lang, page, lang, "index.html")
    other = href(lang, page, "en" if lang == "fi" else "fi", "404.html")
    if lang == "en":
        body = f'''
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">404</p>
    <h1 class="display">This page could not be found.</h1>
    <p class="lead">The address may have changed, or the page may not exist.</p>
    <div class="btn-row" style="margin-top:32px">
      <a class="btn btn-accent" href="{home}">Back to home</a>
      <a class="btn btn-ghost" href="{other}" lang="fi" hreflang="fi">Suomeksi</a>
    </div>
  </div>
</section>'''
        return page_shell(lang, page, "Page not found — WEBAUR", "The page you requested could not be found.", "", body)
    body = f'''
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">404</p>
    <h1 class="display">Sivua ei löytynyt.</h1>
    <p class="lead">Osoite on voinut muuttua, tai sivua ei ole olemassa.</p>
    <div class="btn-row" style="margin-top:32px">
      <a class="btn btn-accent" href="{home}">Takaisin etusivulle</a>
      <a class="btn btn-ghost" href="{other}" lang="en" hreflang="en">In English</a>
    </div>
  </div>
</section>'''
    return page_shell(lang, page, "Sivua ei löytynyt — WEBAUR", "Pyytämääsi sivua ei löytynyt.", "", body)

def work_page(lang):
    page = "work.html"
    pre = asset_prefix(lang, 0)
    hale = href(lang, page, lang, "work/barber-studio.html")
    alto = href(lang, page, lang, "work/detailing.html")
    maison = href(lang, page, lang, "work/maison-cafe.html")
    demo_h = f"{pre}demos/barber-studio/index.html"
    demo_a = f"{pre}demos/detailing/index.html"
    demo_m = f"{pre}demos/maison-cafe/index.html"
    if lang == "en":
        concept, live, read = "Concept project", "View live demo", "Read the project"
        intro_h, intro_l = "Different businesses. Different digital experiences.", "Three finished concept projects, each built as a multi-page brand site. They are independent design concepts — not paying-client work — and show how WEBAUR would approach different businesses."
        hale_intro = "A five-page concept for an independent barbershop. The site is built around a quiet hour in the chair: bone, forest green, and photographs of the room, not stock smiles."
        alto_intro = "A dark showroom concept for a detailing studio: graphite, oxide red, and a cinematic opening with the car and the headline in the same frame. Five pages, including a results page whose sliders are the main object."
        alto_key = "The same car, twice. The sliders compare two treatments of the same photograph. They are illustrative, not evidence of paid work."
        maison_intro = "A five-page café concept on parchment, bottle green and copper. The site is built like a short publication: a table, a menu with food photography, a room study, a story, and a visit page that admits it lives only in the story."
        titles = {
            "dir": "Design direction", "feat": "Main features", "dec": "Design decisions",
            "hale_dir": "Editorial and calm, and no longer in the studio’s own display face. Cormorant Garamond for the voice, Outfit for body text, a bone surface, forest green and a brass monogram.",
            "hale_feat": ["Five pages: home, services, barbers, gallery, visit", "A service menu with example prices", "A staff introduction and a close-in gallery of the room", "A visit page that does not pretend to take real appointments"],
            "hale_dec": ["A typographic wordmark instead of a drawn logo", "Photographs of the room and the work, not lifestyle poses", "A booking path that stays honest as a concept"],
            "alto_dir": "Cinematic and industrial. Big Shoulders for an automotive voice, Source Sans 3 for reading, a graphite ground and an oxide-red accent — closer to a night bay than to a light-grey app.",
            "alto_feat": ["Five pages: home, services, results, process, contact", "Three named packages with example prices", "Working before-and-after sliders, described honestly", "A process page that walks through a day in the bay"],
            "alto_dec": ["A typographic mark that reads like a manufacturer’s name", "Comparisons that admit the “before” frame is processed", "Prices on the page, not behind a quote form"],
            "maison_dir": "Warm and typographic. Bodoni Moda for the display voice, Manrope for body text, a parchment surface, bottle-green bands and a copper accent.",
            "maison_feat": ["Five pages: home, menu, the room, story, visit", "An editorial menu with example prices", "A longer story page about the house", "A visit page that does not invent a real door on a real street"],
            "maison_dec": ["A strong serif as the café’s voice", "Food photographs in sequences, not a tiled catalogue", "Hospitable writing that stays fictional and labelled"],
            "thumbs_h": ["Services", "Barbers", "Gallery"],
            "thumbs_a": ["Services", "Results", "Process"],
            "thumbs_m": ["Menu", "The room", "Story"],
        }
        h1e, title, desc = "Work", "Work — WEBAUR", "Concept website projects by WEBAUR: Hale Barber Studio, Alto Detail and Maison Café. Independent design concepts, not client work."
    else:
        concept, live, read = "Konseptiprojekti", "Avaa live-demo", "Lue projektiesittely"
        intro_h, intro_l = "Eri yrityksiä. Erilaisia digitaalisia kokemuksia.", "Kolme valmista konseptiprojektia, kukin rakennettu monisivuisena brändisivustona. Ne ovat itsenäisiä suunnittelukonsepteja — eivät maksavan asiakkaan töitä — ja näyttävät, miten WEBAUR lähestyisi eri yrityksiä."
        hale_intro = "Viisisivuinen konsepti itsenäiselle parturille. Sivusto rakentuu rauhalliselle hetkelle tuolissa: luunväri, metsänvihreä ja kuvia huoneesta, ei valmiskuvien hymyistä."
        alto_intro = "Tumma showroom-konsepti detailing-studiolle: grafiitti, oksidinpunainen ja elokuvallinen avaus, jossa auto ja otsikko ovat samassa kehyksessä. Viisi sivua, joista tulossivun keskiössä ovat ennen–jälkeen-liukusäätimet."
        alto_key = "Sama auto, kahdesti. Liukusäätimet vertaavat saman valokuvan kahta käsittelyä. Ne ovat havainnollistavia, eivät todiste maksavasta työstä."
        maison_intro = "Viisisivuinen kahvilakonsepti pergamentilla, pullonvihreällä ja kuparilla. Sivusto on rakennettu kuin lyhyt julkaisu: pöytä, ruokalista ruokakuvin, huonetutkielma, tarina ja vierailusivu, joka myöntää elävänsä vain tarinassa."
        titles = {
            "dir": "Suunnittelusuunta", "feat": "Keskeiset ominaisuudet", "dec": "Suunnitteluratkaisut",
            "hale_dir": "Toimituksellinen ja rauhallinen, omalla typografialla studion fonttien sijaan. Cormorant Garamond äänelle, Outfit leipätekstille, luunvärinen pinta, metsänvihreä ja messinkinen monogrammi.",
            "hale_feat": ["Viisi sivua: etusivu, palvelut, parturit, galleria, vierailu", "Palveluvalikko esimerkkihinnoin", "Henkilöesittely ja lähikuvagalleria huoneesta", "Vierailusivu, joka ei teeskentele oikeaa ajanvarausta"],
            "hale_dec": ["Typografinen nimilogo piirretyn tunnuksen sijaan", "Kuvia huoneesta ja työstä, ei poseerattuja lifestyle-kuvia", "Varauspolku, joka pysyy rehellisenä konseptina"],
            "alto_dir": "Elokuvallinen ja teollinen. Big Shoulders otsikoille, Source Sans 3 leipätekstille, grafiittinen pinta ja oksidinpunainen aksentti — lähempänä illan hallia kuin vaaleanharmaata sovellusta.",
            "alto_feat": ["Viisi sivua: etusivu, palvelut, tulokset, prosessi, yhteys", "Kolme nimettyä pakettia esimerkkihinnoin", "Toimivat ennen–jälkeen-liukusäätimet, rehellisesti kuvailtuina", "Prosessisivu, joka kulkee työpäivän vaiheet läpi"],
            "alto_dec": ["Typografinen merkki, joka luetaan kuin valmistajan nimi", "Vertailut, jotka myöntävät “ennen”-kuvan olevan käsitelty", "Hinnat sivulla, ei tarjouslomakkeen takana"],
            "maison_dir": "Lämmin ja typografinen. Bodoni Moda näyttöäänelle, Manrope leipätekstille, pergamenttipinta, pullonvihreät kaistat ja kuparinen aksentti.",
            "maison_feat": ["Viisi sivua: etusivu, ruokalista, huone, tarina, vierailu", "Toimituksellinen ruokalista esimerkkihinnoin", "Pidempi tarinasivu talosta", "Vierailusivu, joka ei keksi todellista osoitetta"],
            "maison_dec": ["Vahva serif-kirjasin kahvilan äänenä", "Ruokakuvat jaksoina, ei laatoitettuna katalogina", "Lämmin teksti, joka on selvästi merkitty kuvitteelliseksi"],
            "thumbs_h": ["Palvelut", "Parturit", "Galleria"],
            "thumbs_a": ["Palvelut", "Tulokset", "Prosessi"],
            "thumbs_m": ["Ruokalista", "Huone", "Tarina"],
        }
        h1e, title, desc = "Työt", "Työt — WEBAUR", "WEBAURin konseptisivustot: Hale Barber Studio, Alto Detail ja Maison Café. Itsenäisiä suunnittelukonsepteja, ei asiakastöitä."

    def ul(items):
        return "<ul>" + "".join(f"<li>{x}</li>" for x in items) + "</ul>"

    def meta(dir_t, feat, dec):
        return f'''<div class="folio-meta">
      <div><h3>{titles["dir"]}</h3><p class="muted">{dir_t}</p></div>
      <div><h3>{titles["feat"]}</h3>{ul(feat)}</div>
      <div><h3>{titles["dec"]}</h3>{ul(dec)}</div>
    </div>'''

    hale_block = f'''
<section class="folio-project folio-hale" aria-labelledby="hale-title">
  <div class="wrap folio-layout">
    <div class="folio-copy">
      <div class="folio-kicker-row">
        <span class="folio-num">01</span>
        <span class="badge">{concept}</span>
        <span class="kicker">{"Barber" if lang=="en" else "Parturi"}</span>
      </div>
      <h2 id="hale-title" class="folio-title">Hale Barber Studio</h2>
      <p class="folio-intro">{hale_intro}</p>
      {meta(titles["hale_dir"], titles["hale_feat"], titles["hale_dec"])}
      <div class="folio-actions">
        <a class="btn btn-ink" href="{demo_h}">{live}</a>
        <a class="btn btn-ghost" href="{hale}">{read}</a>
      </div>
    </div>
    <div>
      <div class="folio-stage">
        {device_desktop(pre, "hale/home-desktop", "Hale Barber Studio — home, desktop")}
        {device_mobile(pre, "hale/home-mobile", "Hale Barber Studio — home, mobile")}
      </div>
      <div class="folio-frames">
        <figure>{device_desktop(pre, "hale/services-desktop", "Hale — services", sizes="(min-width: 1100px) 320px, 100vw")}<figcaption>{titles["thumbs_h"][0]}</figcaption></figure>
        <figure>{device_desktop(pre, "hale/barbers-desktop", "Hale — barbers", sizes="(min-width: 1100px) 320px, 100vw")}<figcaption>{titles["thumbs_h"][1]}</figcaption></figure>
        <figure>{device_desktop(pre, "hale/gallery-desktop", "Hale — gallery", sizes="(min-width: 1100px) 320px, 100vw")}<figcaption>{titles["thumbs_h"][2]}</figcaption></figure>
      </div>
    </div>
  </div>
</section>'''

    alto_block = f'''
<section class="folio-project folio-alto" aria-labelledby="alto-title">
  <div class="wrap folio-alto-board">
    <div class="folio-copy">
        <div class="folio-kicker-row">
          <span class="folio-num">02</span>
          <span class="badge">{concept}</span>
          <span class="kicker">{"Automotive detailing" if lang=="en" else "Autonhoito ja detailing"}</span>
        </div>
        <h2 id="alto-title" class="folio-title">Alto Detail</h2>
        <p class="folio-intro">{alto_intro}</p>
        <p class="key-feature"><strong>{"Key feature" if lang=="en" else "Keskeinen toiminto"}.</strong> {alto_key}</p>
        {meta(titles["alto_dir"], titles["alto_feat"], titles["alto_dec"])}
        <div class="folio-actions">
          <a class="btn btn-ink" href="{demo_a}">{live}</a>
          <a class="btn btn-ghost" href="{alto}">{read}</a>
        </div>
    </div>
    <div>
      <div class="folio-stage folio-stage-dark">
        {device_desktop(pre, "alto/home-desktop", "Alto Detail — home, desktop", sizes="(min-width: 1100px) 820px, 100vw")}
        {device_mobile(pre, "alto/home-mobile", "Alto Detail — home, mobile")}
      </div>
    </div>
  </div>
  <div class="wrap">
    <div class="folio-frames">
      <figure>{device_desktop(pre, "alto/services-desktop", "Alto — services", sizes="(min-width: 1100px) 380px, 100vw")}<figcaption>{titles["thumbs_a"][0]}</figcaption></figure>
      <figure>{device_desktop(pre, "alto/results-slider-desktop", "Alto — results slider", sizes="(min-width: 1100px) 380px, 100vw")}<figcaption>{titles["thumbs_a"][1]}</figcaption></figure>
      <figure>{device_desktop(pre, "alto/process-desktop", "Alto — process", sizes="(min-width: 1100px) 380px, 100vw")}<figcaption>{titles["thumbs_a"][2]}</figcaption></figure>
    </div>
  </div>
</section>'''

    maison_block = f'''
<section class="folio-project folio-maison" aria-labelledby="maison-title">
  <div class="wrap">
    <div class="folio-masthead">
      <div class="folio-kicker-row">
        <span class="folio-num">03</span>
        <span class="badge">{concept}</span>
        <span class="kicker">{"Café" if lang=="en" else "Kahvila"}</span>
      </div>
      <h2 id="maison-title" class="folio-title">Maison Café</h2>
      <p class="folio-intro">{maison_intro}</p>
    </div>
    <div class="folio-collage">
      <div class="cell-main">{device_desktop(pre, "maison/home-desktop", "Maison Café — home, desktop")}</div>
      <div class="cell-side">{device_desktop(pre, "maison/menu-desktop", "Maison Café — menu", sizes="(min-width: 1100px) 400px, 100vw")}<p class="folio-cap">{titles["thumbs_m"][0]}</p></div>
      <div class="cell-side">{device_desktop(pre, "maison/room-desktop", "Maison Café — the room", sizes="(min-width: 1100px) 400px, 100vw")}<p class="folio-cap">{titles["thumbs_m"][1]}</p></div>
    </div>
    <div class="walk-pair" style="margin-top:28px">
      {device_desktop(pre, "maison/story-desktop", "Maison Café — story", sizes="(min-width: 1100px) 900px, 100vw")}
      {device_mobile(pre, "maison/home-mobile", "Maison Café — home, mobile")}
    </div>
    <div style="margin-top:48px">
      {meta(titles["maison_dir"], titles["maison_feat"], titles["maison_dec"])}
    </div>
    <div class="folio-actions">
      <a class="btn btn-ink" href="{demo_m}">{live}</a>
      <a class="btn btn-ghost" href="{maison}">{read}</a>
    </div>
  </div>
</section>'''

    skip = "View the projects" if lang=="en" else "Siirry projekteihin"
    body = f'''
<section class="page-hero work-hero">
  <div class="wrap">
    <p class="eyebrow">{h1e}</p>
    <h1 class="display">{intro_h}</h1>
    <p class="lead">{intro_l}</p>
    <nav class="work-index" aria-label="{skip}">
      <a href="#hale-title" class="work-index-item">
        {device_desktop(pre, "hale/home-desktop", "Hale Barber Studio", loading="eager", sizes="(min-width: 1100px) 380px, 100vw")}
        <span>01 · Hale</span>
      </a>
      <a href="#alto-title" class="work-index-item">
        {device_desktop(pre, "alto/home-desktop", "Alto Detail", loading="eager", sizes="(min-width: 1100px) 380px, 100vw")}
        <span>02 · Alto</span>
      </a>
      <a href="#maison-title" class="work-index-item">
        {device_desktop(pre, "maison/home-desktop", "Maison Café", loading="eager", sizes="(min-width: 1100px) 380px, 100vw")}
        <span>03 · Maison</span>
      </a>
    </nav>
  </div>
</section>
{hale_block}
{alto_block}
{maison_block}
{cta(lang, page)}
'''
    return page_shell(lang, page, title, desc, "work", body)

def walk_item(prefix, lang, title, lede, copy, desk, mob, desk_alt, mob_alt, demo_href, open_label, alt=False):
    pair = f'''<div class="walk-pair">
      {device_desktop(prefix, desk, desk_alt)}
      {device_mobile(prefix, mob, mob_alt)}
    </div>'''
    text = f'''<div class="walk-copy">
      <h3>{title}</h3>
      <p class="kicker" style="margin-bottom:8px">{lede}</p>
      <p class="muted">{copy}</p>
      <p style="margin-top:16px"><a class="teaser-link" href="{demo_href}">{open_label}</a></p>
    </div>'''
    inner = (text + pair) if not alt else (pair + text)
    return f'<article class="walk-item{" is-alt" if alt else ""}">{inner}</article>'


def case_shell(lang, page, title, desc, crumb, eyebrow, h1, intro, live, back, demo, actions_top, brief, notice, identity, walk, features_title, features, feature_note, decisions_title, decisions):
    pre = asset_prefix(lang, 1)
    work = href(lang, page, lang, "work.html")
    body = f'''
<section class="page-hero case-hero">
  <div class="wrap">
    <p class="crumb"><a href="{work}">{crumb}</a> / {h1}</p>
    <p class="eyebrow">{eyebrow}</p>
    <h1 class="display">{h1}</h1>
    <p class="lead">{intro}</p>
    <div class="btn-row" style="margin-top:28px">
      <a class="btn btn-accent" href="{demo}">{live}</a>
      <a class="btn btn-ghost" href="{work}">{back}</a>
    </div>
  </div>
</section>
<section class="section" style="padding-top:24px">
  <div class="wrap">
    <div class="case-copy">
      {"".join(f'<div><h2>{t}</h2><p class="muted">{c}</p></div>' for t,c in brief)}
    </div>
    <p class="case-notice">{notice}</p>
    {identity}
    <h2 class="section-title" style="margin:56px 0 8px">{walk[0]}</h2>
    <p class="muted" style="margin-bottom:32px">{walk[1]}</p>
    <div class="walk">{walk[2]}</div>
    <h2 class="section-title" style="margin:72px 0 16px">{features_title}</h2>
    <ul class="feature-list">{"".join(f"<li>{x}</li>" for x in features)}</ul>
    <p class="muted" style="margin-top:16px;max-width:44rem">{feature_note}</p>
    <h2 class="section-title" style="margin:72px 0 16px">{decisions_title}</h2>
    <div class="decisions">
      {"".join(f'<article><h3>{t}</h3><p class="muted">{c}</p></article>' for t,c in decisions)}
    </div>
    <div class="folio-actions">
      <a class="btn btn-accent" href="{demo}">{live}</a>
      <a class="btn btn-ghost" href="{work}">{back}</a>
    </div>
  </div>
</section>
{cta(lang, page)}
'''
    return page_shell(lang, page, title, desc, "work", body)


def swatches(items):
    return '<div class="swatches">' + "".join(
        f'<div class="swatch"><i style="background:{hex_}"></i><span>{name}<br>{hex_}</span></div>'
        for name, hex_ in items
    ) + "</div>"


def case_hale(lang):
    page = "work/barber-studio.html"
    pre = asset_prefix(lang, 1)
    demo = f"{pre}demos/barber-studio/"
    identity = f'''<div class="case-identity is-hale">
      <div>
        <h2>{"Brand identity" if lang=="en" else "Brändi-identiteetti"}</h2>
        <p class="wordmark-demo type-hale-display">Hale<br><span style="font-size:.55em;letter-spacing:.18em;text-transform:uppercase;font-family:Outfit,sans-serif;font-style:normal">Barber Studio</span></p>
        <h3 style="margin-top:24px">{"Colour palette" if lang=="en" else "Väripaletti"}</h3>
        {swatches([("Paper","#E7DFD2"),("Paper 2","#DCD2C2"),("Ink","#16120E"),("Forest","#1E3328"),("Brass","#8F7344")])}
      </div>
      <div>
        <h3>{"Typefaces" if lang=="en" else "Kirjasimet"}</h3>
        <div class="type-spec">
          <p><strong>Cormorant Garamond</strong><span class="type-display type-hale-display">The hour is <em>yours.</em></span><span class="muted" style="display:block;margin-top:6px">{"The same self-hosted face as the live demo — not the studio’s Instrument Serif." if lang=="en" else "Sama kirjasin kuin livedemossa, ladattuna sivustolta itseltään — ei studion Instrument Serif."}</span></p>
          <p><strong>Outfit</strong><span class="type-body type-hale-body">Cuts, colour and a chair that is yours for the hour.</span><span class="muted" style="display:block;margin-top:6px">{"Self-hosted Outfit, as on the live demo." if lang=="en" else "Outfit, ladattuna sivustolta itseltään kuten livedemossa."}</span></p>
        </div>
      </div>
    </div>'''
    if lang == "en":
        open_l = "Open this page"
        pages = [
            ("Home", "The hour is yours.", "A split hero: a quiet chair, a bone field and a short promise. The first screen feels like a studio, not a ready-made template.", "hale/home-desktop", "hale/home-mobile", "index.html"),
            ("Services", "The menu.", "A service list with example prices. Typography treats the list as editorial, not a cramped table.", "hale/services-desktop", "hale/services-mobile", "services.html"),
            ("Barbers", "Aino Vartiainen.", "One fictional barber, introduced with a portrait and a short biography. The person in the photograph is a model; the name and studio are invented.", "hale/barbers-desktop", "hale/barbers-mobile", "barbers.html"),
            ("Gallery", "The room, close in.", "Close photographs of the room and the work: chairs, tools, light. The pictures carry the brand more than slogans do.", "hale/gallery-desktop", "hale/gallery-mobile", "gallery.html"),
            ("Visit", "How a visit would work.", "An address, hours and an invitation, clearly labelled as a concept. Nothing on this page makes a real booking.", "hale/visit-desktop", "hale/visit-mobile", "visit.html"),
        ]
        walk_html = "".join(
            walk_item(pre, lang, t, lede, copy, d, m, f"Hale — {t}, desktop", f"Hale — {t}, mobile", demo + hrefp, open_l, i % 2 == 1)
            for i, (t, lede, copy, d, m, hrefp) in enumerate(pages)
        )
        return case_shell(
            lang, page,
            "Hale Barber Studio — Concept project — WEBAUR",
            "A five-page concept website for an independent barbershop, designed by WEBAUR. Not a client project.",
            "Work", "Concept project", "Hale Barber Studio",
            "A five-page concept for an independent barbershop. The site is built around a quiet hour in the chair: bone, forest green, and photographs of the room, not stock smiles.",
            "View live demo", "Back to work", demo + "index.html", "",
            [("Starting point", "To design a complete barbershop site that would stand as commissioned work: its own identity, several real pages, and a visit experience without invented bookings or reviews."),
             ("Aim", "To show how WEBAUR would approach a small service business: typography, photography and a clear path, without a generic template."),
             ("Audience", "An independent barber who wants a site as careful as the cut — small, precise and calm, not loud advertising.")],
            "This is a concept project. It is not a paying client’s website, and it does not invent customers, reviews or results.",
            identity,
            ("Page by page", "Hale Barber Studio", walk_html),
            "Main features",
            ["Five pages: home, services, barbers, gallery, visit", "A service menu with example prices", "A staff introduction and a close-in gallery of the room", "A visit page that does not pretend to take real appointments"],
            "The visit page includes hours, a fictional address, and a booking form that does not send. It states plainly that this is a concept.",
            "Design decisions",
            [("Let typography carry the brand.", "Cormorant Garamond is the studio’s voice; Outfit keeps the body text readable. A brass monogram and typographic wordmark keep Hale distinct from WEBAUR’s own Instrument Serif."),
             ("Photograph the room, not a campaign.", "The gallery and hero speak of chairs, light and tools. That is closer to a real trade than posed portraits."),
             ("Stay honest about contact.", "A real business would need a real booking tool. This concept does not pretend that one already exists.")],
        )
    open_l = "Avaa tämä sivu"
    pages = [
        ("Etusivu", "The hour is yours.", "Kaksijakoinen avausnäkymä: hiljainen tuoli, luunvärinen kenttä ja lyhyt lupaus. Ensimmäinen näkymä tuntuu studiolta, ei valmiilta mallilta.", "hale/home-desktop", "hale/home-mobile", "index.html"),
        ("Palvelut", "The menu.", "Palvelulista esimerkkihinnoin. Typografia käsittelee listaa toimituksellisena, ei ahtaana taulukkona.", "hale/services-desktop", "hale/services-mobile", "services.html"),
        ("Parturit", "Aino Vartiainen.", "Yksi kuvitteellinen parturi, esitelty muotokuvalla ja lyhyellä esittelyllä. Valokuvan henkilö on kuvapankin malli; nimi ja studio ovat keksittyjä.", "hale/barbers-desktop", "hale/barbers-mobile", "barbers.html"),
        ("Galleria", "The room, close in.", "Lähikuvaa huoneesta ja työstä: tuolit, välineet, valo. Valokuvat kantavat brändiä enemmän kuin iskulauseet.", "hale/gallery-desktop", "hale/gallery-mobile", "gallery.html"),
        ("Vierailu", "How a visit would work.", "Osoite, aukiolo ja vierailukutsu, merkitty selvästi konseptiksi. Mikään tällä sivulla ei tee oikeaa varausta.", "hale/visit-desktop", "hale/visit-mobile", "visit.html"),
    ]
    walk_html = "".join(
        walk_item(pre, lang, t, lede, copy, d, m, f"Hale — {t}, työpöytä", f"Hale — {t}, puhelin", demo + hrefp, open_l, i % 2 == 1)
        for i, (t, lede, copy, d, m, hrefp) in enumerate(pages)
    )
    return case_shell(
        lang, page,
        "Hale Barber Studio — Konseptiprojekti — WEBAUR",
        "Viisisivuinen konseptisivusto itsenäiselle parturille, suunniteltu WEBAURilla. Ei asiakasprojekti.",
        "Työt", "Konseptiprojekti", "Hale Barber Studio",
        "Viisisivuinen konsepti itsenäiselle parturille. Sivusto rakentuu rauhalliselle hetkelle tuolissa: luunväri, metsänvihreä ja kuvia huoneesta, ei valmiskuvien hymyistä.",
        "Avaa live-demo", "Takaisin töihin", demo + "index.html", "",
        [("Lähtökohta", "Suunnitella kokonainen parturisivusto, joka kelpaisi tilaustyöksi: oma identiteetti, useita oikeita sivuja ja vierailukokemus ilman keksittyjä varauksia tai arvosteluja."),
         ("Tavoite", "Näyttää, miten WEBAUR lähestyisi pientä palveluyritystä: typografia, valokuvat ja selkeä polku, ilman geneeristä mallipohjaa."),
         ("Yleisö", "Itsenäinen parturi, joka haluaa sivuston yhtä huolellisen kuin leikkaus — pienen, tarkan ja rauhallisen, ei äänekästä mainontaa.")],
        "Tämä on konseptiprojekti. Se ei ole maksavan asiakkaan sivusto, eikä se keksi asiakkaita, arvosteluja tai tuloksia.",
        identity,
        ("Sivu sivulta", "Hale Barber Studio", walk_html),
        "Keskeiset ominaisuudet",
        ["Viisi sivua: etusivu, palvelut, parturit, galleria, vierailu", "Palveluvalikko esimerkkihinnoin", "Henkilöesittely ja lähikuvagalleria huoneesta", "Vierailusivu, joka ei teeskentele oikeaa ajanvarausta"],
        "Vierailusivulla on aukiolo, kuvitteellinen osoite ja varauslomake, joka ei lähetä. Sivu toteaa suoraan, että kyseessä on konsepti.",
        "Suunnitteluratkaisut",
        [("Anna typografian kantaa brändiä.", "Cormorant Garamond on studion ääni, Outfit pitää leipätekstin luettavana. Messinkinen monogrammi ja typografinen wordmark erottavat Halen WEBAURin omasta Instrument Serifistä."),
         ("Kuvaa huonetta, ei kampanjaa.", "Galleria ja avausnäkymä kertovat tuoleista, valosta ja välineistä. Ne ovat lähempänä oikeaa liikettä kuin poseeratut muotokuvat."),
         ("Pysy rehellisenä yhteydenotossa.", "Oikea liike tarvitsisi oikean varausvälineen. Tämä konsepti ei teeskentele, että sellainen on jo olemassa.")],
    )

def case_alto(lang):
    page = "work/detailing.html"
    pre = asset_prefix(lang, 1)
    demo = f"{pre}demos/detailing/"
    identity = f'''<div class="case-identity is-alto">
      <div>
        <h2>{"Brand identity" if lang=="en" else "Brändi-identiteetti"}</h2>
        <p class="wordmark-demo type-alto-display">ALTO<br><span style="font-size:.45em;letter-spacing:.2em">DETAIL</span></p>
        <h3 style="margin-top:24px">{"Colour palette" if lang=="en" else "Väripaletti"}</h3>
        {swatches([("Graphite","#0C0E10"),("Bay","#14181C"),("Silver","#C5CDD4"),("Oxide","#C44932")])}
      </div>
      <div>
        <h3>{"Typefaces" if lang=="en" else "Kirjasimet"}</h3>
        <div class="type-spec">
          <p><strong>Big Shoulders Display</strong><span class="type-display type-alto-display">A quieter shine.</span><span class="muted" style="display:block;margin-top:6px">{"The same self-hosted face as the live demo." if lang=="en" else "Sama kirjasin kuin livedemossa, ladattuna sivustolta itseltään."}</span></p>
          <p><strong>Source Sans 3</strong><span class="type-body type-alto-body">Essential, Signature and Atelier — packages stated in the open.</span><span class="muted" style="display:block;margin-top:6px">{"Self-hosted Source Sans 3, as on the live demo." if lang=="en" else "Source Sans 3, ladattuna sivustolta itseltään kuten livedemossa."}</span></p>
        </div>
      </div>
    </div>'''
    if lang == "en":
        open_l = "Open this page"
        pages = [
            ("Home", "A quieter shine.", "A dark cinematic opening: the car and the headline share one frame. The first impression is a night bay, not a light-grey brochure.", "alto/home-desktop", "alto/home-mobile", "index.html"),
            ("Services", "Essential, Signature, Atelier.", "Three packages with example prices starting at €189. The offering is readable immediately, without hiding the price behind a quote request.", "alto/services-desktop", "alto/services-mobile", "services.html"),
            ("Results", "The same car, twice.", "Before-and-after sliders are the main interaction. The before frames are processed versions of the same photograph — not a second car, and not documented client work. The page says this plainly.", "alto/results-slider-desktop", "alto/results-mobile", "results.html"),
            ("Process", "A day in the bay.", "The work is walked through as a day in the shop, so the service feels like stages rather than slogans.", "alto/process-desktop", "alto/process-mobile", "process.html"),
            ("Contact", "Request a place in the bay.", "A request form and contact details, labelled as a concept. The page does not invent a waiting list or a confirmed booking.", "alto/contact-desktop", "alto/contact-mobile", "contact.html"),
        ]
        walk_html = "".join(
            walk_item(pre, lang, t, lede, copy, d, m, f"Alto — {t}, desktop", f"Alto — {t}, mobile", demo + hrefp, open_l, i % 2 == 1)
            for i, (t, lede, copy, d, m, hrefp) in enumerate(pages)
        )
        return case_shell(lang, page,
            "Alto Detail — Concept project — WEBAUR",
            "A five-page concept website for an automotive detailing studio, designed by WEBAUR. Not a client project.",
            "Work", "Concept project", "Alto Detail",
            "A dark showroom concept for a detailing studio: graphite, oxide red, and a cinematic opening with the car and the headline in the same frame. Five pages, including a results page whose sliders are the main object.",
            "View live demo", "Back to work", demo + "index.html", "",
            [("Starting point", "To build a complete detailing site with its own brand, priced packages, a visual comparison and a contact path that does not invent results."),
             ("Aim", "To show how WEBAUR would treat a technical service brand: photography, typography and a function (the slider) that actually does something."),
             ("Audience", "A detailing studio that wants to look as precise as the work — closer to a showroom than to loud garage advertising.")],
            "This is a concept project. It is not a paying client’s website, and it does not invent customers, reviews or results.",
            identity, ("Page by page", "Alto Detail", walk_html),
            "Main features",
            ["Five pages: home, services, results, process, contact", "Three named packages with example prices", "Working before-and-after sliders, described honestly", "A process page that walks through a day in the bay"],
            "The sliders compare two treatments of the same photograph. They are illustrative, not evidence of paid work.",
            "Design decisions",
            [("Give the brand a manufacturer’s voice.", "Big Shoulders is wide and mechanical; Source Sans 3 keeps packages and process text readable. Oxide red is used sparingly, like a painted caliper."),
             ("Keep the comparison honest.", "A slider is only convincing if the caption is true. Both sides are the same photograph; the “before” is a processed frame, and the page says so."),
             ("Put the price next to the package.", "Essential, Signature and Atelier are listed with example figures so a visitor can judge the offer without a gate.")],
        )
    open_l = "Avaa tämä sivu"
    pages = [
        ("Etusivu", "A quieter shine.", "Tumma elokuvallinen avaus: auto ja otsikko jakavat saman kehyksen. Ensimmäinen vaikutelma on illan halli, ei vaaleanharmaa esite.", "alto/home-desktop", "alto/home-mobile", "index.html"),
        ("Palvelut", "Essential, Signature, Atelier.", "Kolme pakettia esimerkkihinnoin alkaen 189 €. Valikoima on luettavissa heti, ilman että hinta piilotetaan tarjouspyynnön taakse.", "alto/services-desktop", "alto/services-mobile", "services.html"),
        ("Tulokset", "The same car, twice.", "Ennen–jälkeen-liukusäätimet ovat sivun päätoiminto. Ennen-kuvat ovat saman valokuvan käsiteltyjä versioita — eivät toista autoa eivätkä dokumentoitua asiakastyötä. Sivu sanoo tämän suoraan.", "alto/results-slider-desktop", "alto/results-mobile", "results.html"),
        ("Prosessi", "A day in the bay.", "Työ kerrotaan yhden hallipäivän vaiheina, jotta palvelu tuntuu konkreettiselta eikä jää iskusanoiksi.", "alto/process-desktop", "alto/process-mobile", "process.html"),
        ("Yhteys", "Request a place in the bay.", "Pyyntölomake ja yhteystiedot, merkitty konseptiksi. Sivu ei keksi jonotuslistaa tai valmista varausta.", "alto/contact-desktop", "alto/contact-mobile", "contact.html"),
    ]
    walk_html = "".join(
        walk_item(pre, lang, t, lede, copy, d, m, f"Alto — {t}, työpöytä", f"Alto — {t}, puhelin", demo + hrefp, open_l, i % 2 == 1)
        for i, (t, lede, copy, d, m, hrefp) in enumerate(pages)
    )
    return case_shell(lang, page,
        "Alto Detail — Konseptiprojekti — WEBAUR",
        "Viisisivuinen konseptisivusto detailing-studiolle, suunniteltu WEBAURilla. Ei asiakasprojekti.",
        "Työt", "Konseptiprojekti", "Alto Detail",
        "Tumma showroom-konsepti detailing-studiolle: grafiitti, oksidinpunainen ja elokuvallinen avaus, jossa auto ja otsikko ovat samassa kehyksessä. Viisi sivua, joista tulossivun keskiössä ovat ennen–jälkeen-liukusäätimet.",
        "Avaa live-demo", "Takaisin töihin", demo + "index.html", "",
        [("Lähtökohta", "Rakentaa kokonainen detailing-sivusto omalla brändillä, hinnoitelluilla paketeilla, visuaalisella vertailulla ja yhteydenottopolulla, joka ei keksi tuloksia."),
         ("Tavoite", "Näyttää, miten WEBAUR käsittelisi teknistä palvelubrändiä: valokuvat, typografia ja toiminto (liukusäädin), joka tekee oikeasti jotain."),
         ("Yleisö", "Detailing-studio, joka haluaa näyttää yhtä täsmälliseltä kuin työ — lähempänä showroomia kuin äänekästä autohuoltomainosta.")],
        "Tämä on konseptiprojekti. Se ei ole maksavan asiakkaan sivusto, eikä se keksi asiakkaita, arvosteluja tai tuloksia.",
        identity, ("Sivu sivulta", "Alto Detail", walk_html),
        "Keskeiset ominaisuudet",
        ["Viisi sivua: etusivu, palvelut, tulokset, prosessi, yhteys", "Kolme nimettyä pakettia esimerkkihinnoin", "Toimivat ennen–jälkeen-liukusäätimet, rehellisesti kuvailtuina", "Prosessisivu, joka kulkee työpäivän vaiheet läpi"],
        "Liukusäätimet vertaavat saman valokuvan kahta käsittelyä. Ne ovat havainnollistavia, eivät todiste maksavasta työstä.",
        "Suunnitteluratkaisut",
        [("Anna brändille valmistajan ääni.", "Big Shoulders on leveä ja mekaaninen; Source Sans 3 pitää paketit ja prosessitekstit luettavina. Oksidinpunaista käytetään säästeliäästi, kuin maalattua jarrusatulaa."),
         ("Pidä vertailu rehellisenä.", "Liukusäädin vakuuttaa vain, jos kuvateksti on totta. Molemmat puolet ovat sama valokuva; “ennen” on käsitelty kehys, ja sivu sanoo sen."),
         ("Laita hinta paketin viereen.", "Essential, Signature ja Atelier on listattu esimerkkihinnoin, jotta kävijä voi arvioida tarjonnan ilman porttia.")],
    )


def case_maison(lang):
    page = "work/maison-cafe.html"
    pre = asset_prefix(lang, 1)
    demo = f"{pre}demos/maison-cafe/"
    identity = f'''<div class="case-identity is-maison">
      <div>
        <h2>{"Brand identity" if lang=="en" else "Brändi-identiteetti"}</h2>
        <p class="wordmark-demo type-maison-display"><em>Maison</em><br><span style="font-size:.45em;letter-spacing:.2em;font-style:normal;font-family:Manrope,sans-serif">CAFÉ</span></p>
        <h3 style="margin-top:24px">{"Colour palette" if lang=="en" else "Väripaletti"}</h3>
        {swatches([("Parchment","#f3e6d0"),("Parchment 2","#e8d4b8"),("Foam","#fbf6ec"),("Ink","#1c1510"),("Bottle green","#3a4632"),("Copper","#8e4024")])}
      </div>
      <div>
        <h3>{"Typefaces" if lang=="en" else "Kirjasimet"}</h3>
        <div class="type-spec">
          <p><strong>Bodoni Moda</strong><span class="type-display type-maison-display">A quiet <em>table.</em></span><span class="muted" style="display:block;margin-top:6px">{"The same self-hosted face as the live demo." if lang=="en" else "Sama kirjasin kuin livedemossa, ladattuna sivustolta itseltään."}</span></p>
          <p><strong>Manrope</strong><span class="type-body type-maison-body">Pastry, coffee and a room that holds the afternoon.</span><span class="muted" style="display:block;margin-top:6px">{"Self-hosted Manrope, as on the live demo." if lang=="en" else "Manrope, ladattuna sivustolta itseltään kuten livedemossa."}</span></p>
        </div>
      </div>
    </div>'''
    if lang == "en":
        open_l = "Open this page"
        pages = [
            ("Home", "A quiet table.", "A conservatory table and a short invitation. The opening is photographic and typographic, closer to a publication than a takeaway site.", "maison/home-desktop", "maison/home-mobile", "index.html"),
            ("Menu", "The list.", "Coffee, pastry and plates as an editorial list, with food photography sitting beside the prices — not a title slide and a plant. The prices are concept examples, not a living kitchen’s menu.", "maison/menu-desktop", "maison/menu-mobile", "menu.html"),
            ("The room", "Stay until the lamps come on.", "An atmosphere page: evening lamps, the conservatory table, the taller green room. It is a designed interior, labelled as licensed stills, not a café on a street.", "maison/room-desktop", "maison/room-mobile", "room.html"),
            ("Story", "The house is a study.", "A longer text about the house and the room. It is written as atmosphere, and it does not invent a founding year or a family history as fact.", "maison/story-desktop", "maison/story-mobile", "story.html"),
            ("Visit", "Come in only in the story.", "Hours and an invitation, stated plainly: this is a story, not a street address you can walk to. A table cannot be reserved.", "maison/visit-desktop", "maison/visit-mobile", "visit.html"),
        ]
        walk_html = "".join(
            walk_item(pre, lang, t, lede, copy, d, m, f"Maison — {t}, desktop", f"Maison — {t}, mobile", demo + hrefp, open_l, i % 2 == 1)
            for i, (t, lede, copy, d, m, hrefp) in enumerate(pages)
        )
        return case_shell(lang, page,
            "Maison Café — Concept project — WEBAUR",
            "A five-page concept website for a café, designed by WEBAUR. Not a client project.",
            "Work", "Concept project", "Maison Café",
            "A five-page café concept on parchment, bottle green and copper. The site is built like a short publication: a table, a menu with food photography, a room study, a story, and a visit page that admits it lives only in the story.",
            "View live demo", "Back to work", demo + "index.html", "",
            [("Starting point", "To design a complete café site with its own identity, a readable list, a sense of place, and a visit path that does not invent reservations."),
             ("Aim", "To show how WEBAUR would approach hospitality: typography, photography and rhythm, without turning the café into a templated front."),
             ("Audience", "An independent café or small restaurant that wants a site as warm as the room — slower and more considered than a takeaway list.")],
            "This is a concept project. It is not a paying client’s website, and it does not invent customers, reviews or results.",
            identity, ("Page by page", "Maison Café", walk_html),
            "Main features",
            ["Five pages: home, menu, the room, story, visit", "An editorial menu with example prices", "A longer story page about the house", "A visit page that does not invent a real door on a real street"],
            "The visit page is direct: you come in only in the story, not on the street. A table cannot be booked.",
            "Design decisions",
            [("Let the serif set the temperature.", "Bodoni Moda gives the name and headlines a printed quality; Manrope keeps the list and the story pleasant to read. Copper is used like warm metal, not a neon accent."),
             ("Treat the list as a publication.", "Dishes are set in a spacious list, not a cramped card grid. Photographs support the list rather than replacing it."),
             ("Do not invent a door.", "A real café would publish a real address and a real booking path. This concept keeps the invitation and says that it is fictional.")],
        )
    open_l = "Avaa tämä sivu"
    pages = [
        ("Etusivu", "A quiet table.", "Talvipuutarhapöytä ja lyhyt kutsu. Avaus on valokuvallinen ja typografinen, lähempänä julkaisua kuin noutoruokasivua.", "maison/home-desktop", "maison/home-mobile", "index.html"),
        ("Ruokalista", "The list.", "Kahvi, leivonnaiset ja annokset toimituksellisena listana, ruokakuvat hintojen vieressä — ei pelkkää kuvaa ja otsikkoa. Hinnat ovat konseptin esimerkkejä, eivät elävän keittiön listaa.", "maison/menu-desktop", "maison/menu-mobile", "menu.html"),
        ("Huone", "Stay until the lamps come on.", "Tunnelmasivu: illan lamput, talvipuutarhapöytä, korkeampi vihreä huone. Suunniteltu sisätila, joka on merkitty lisensoiduiksi kuviksi eikä oikeaksi kahvilaksi.", "maison/room-desktop", "maison/room-mobile", "room.html"),
        ("Tarina", "The house is a study.", "Pidempi teksti talosta ja huoneesta. Se on kirjoitettu tunnelmaksi, eikä se keksi perustamisvuotta tai sukuhistoriaa faktana.", "maison/story-desktop", "maison/story-mobile", "story.html"),
        ("Vierailu", "Come in only in the story.", "Aukiolo ja vierailukutsu, sanottu suoraan: tämä on tarina, ei katuosoite, johon voi kävellä. Pöytää ei varata.", "maison/visit-desktop", "maison/visit-mobile", "visit.html"),
    ]
    walk_html = "".join(
        walk_item(pre, lang, t, lede, copy, d, m, f"Maison — {t}, työpöytä", f"Maison — {t}, puhelin", demo + hrefp, open_l, i % 2 == 1)
        for i, (t, lede, copy, d, m, hrefp) in enumerate(pages)
    )
    return case_shell(lang, page,
        "Maison Café — Konseptiprojekti — WEBAUR",
        "Viisisivuinen konseptisivusto kahvilalle, suunniteltu WEBAURilla. Ei asiakasprojekti.",
        "Työt", "Konseptiprojekti", "Maison Café",
        "Viisisivuinen kahvilakonsepti pergamentilla, pullonvihreällä ja kuparilla. Sivusto on rakennettu kuin lyhyt julkaisu: pöytä, ruokalista ruokakuvin, huonetutkielma, tarina ja vierailusivu, joka myöntää elävänsä vain tarinassa.",
        "Avaa live-demo", "Takaisin töihin", demo + "index.html", "",
        [("Lähtökohta", "Suunnitella kokonainen kahvilasivusto omalla identiteetillä, luettavalla listalla, paikan tuntuella ja vierailupolulla, joka ei keksi varauksia."),
         ("Tavoite", "Näyttää, miten WEBAUR lähestyisi ravintola-alaa: typografia, valokuvat ja rytmi, ilman että kahvilasta tulee mallipohjainen julkisivu."),
         ("Yleisö", "Itsenäinen kahvila tai pieni ravintola, joka haluaa sivuston yhtä lämpimän kuin huone — hitaamman ja harkitumman kuin noutolista.")],
        "Tämä on konseptiprojekti. Se ei ole maksavan asiakkaan sivusto, eikä se keksi asiakkaita, arvosteluja tai tuloksia.",
        identity, ("Sivu sivulta", "Maison Café", walk_html),
        "Keskeiset ominaisuudet",
        ["Viisi sivua: etusivu, ruokalista, huone, tarina, vierailu", "Toimituksellinen ruokalista esimerkkihinnoin", "Pidempi tarinasivu talosta", "Vierailusivu, joka ei keksi todellista osoitetta"],
        "Vierailusivu on suora: sisään tullaan vain tarinassa, ei kadulla. Pöytää ei ole varattavissa.",
        "Suunnitteluratkaisut",
        [("Anna serif-kirjasimen luoda tunnelma.", "Bodoni Moda antaa nimelle ja otsikoille painetun laadun; Manrope pitää listan ja tarinan miellyttävinä lukea. Kuparia käytetään kuin lämmintä metallia, ei neonaksenttia."),
         ("Käsittele listaa julkaisuna.", "Annokset on ladottu väljään listaan, ei ahdettuun korttiruudukkoon. Valokuvat tukevat listaa eivätkä korvaa sitä."),
         ("Älä keksi ovea.", "Oikea kahvila julkaisisi oikean osoitteen ja oikean varauspolun. Tämä konsepti pitää kutsun ja kertoo, että se on kuvitteellinen.")],
    )


def write(rel, html):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    print("wrote", rel)


def build():
    pages = [
        ("index.html", home),
        ("services.html", services_page),
        ("pricing.html", pricing_page),
        ("about.html", about_page),
        ("contact.html", contact_page),
        ("thanks.html", thanks_page),
        ("privacy.html", privacy_page),
        ("404.html", not_found_page),
        ("work.html", work_page),
        ("work/barber-studio.html", case_hale),
        ("work/detailing.html", case_alto),
        ("work/maison-cafe.html", case_maison),
    ]
    for rel, fn in pages:
        ABSOLUTE["on"] = rel == "404.html"
        write(rel, fn("fi"))
        write(f"en/{rel}", fn("en"))
        ABSOLUTE["on"] = False

    studio = [
        "", "services.html", "pricing.html", "about.html", "contact.html",
        "privacy.html", "work.html",
        "work/barber-studio.html", "work/detailing.html", "work/maison-cafe.html",
    ]
    urls = []
    for p in studio:
        loc = f"{SITE}/{p}" if p else f"{SITE}/"
        urls.append(f"  <url><loc>{loc}</loc></url>")
        en = f"{SITE}/en/{p}" if p else f"{SITE}/en/"
        urls.append(f"  <url><loc>{en}</loc></url>")
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls) + "\n</urlset>\n",
        encoding="utf-8",
    )
    (ROOT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n",
        encoding="utf-8",
    )
    print("sitemap and robots updated")


if __name__ == "__main__":
    build()
