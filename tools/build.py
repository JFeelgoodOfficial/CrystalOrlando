#!/usr/bin/env python3
"""Generates the static pages for crystalorlando.com.

Edit the page content below, then run `python3 tools/build.py` from the repo root.
Output: index.html, <slug>/index.html for each page, 404.html, sitemap.xml.
No dependencies beyond the standard library.
"""
import json, os, datetime, html

SITE = "https://crystalorlando.com"
NAME = "Crystal Orlando"
EMAIL = "crystalorlando@gmail.com"
TODAY = datetime.date.today().isoformat()
SAME_AS = [
    "https://www.instagram.com/orlandostudio/",
    "https://www.facebook.com/crystalorlandoartist/",
    "https://faso.com/artists/crystalorlando.html",
    "https://www.artrenewal.org/16thARCSalon/artist/crystal-orlando/29892",
]

FONTS = ("https://fonts.googleapis.com/css2?"
         "family=Bodoni+Moda:ital,opsz,wght@0,6..96,400;0,6..96,500;1,6..96,400"
         "&family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;0,6..72,500;1,6..72,300;1,6..72,400"
         "&display=swap")

NAV = [("/works/", "Works"), ("/about/", "Artist"), ("/commissions/", "Commissions"),
       ("/galleries/", "Galleries"), ("/faq/", "FAQ")]

# ── Shared schema entities ─────────────────────────────────────────────────
PERSON = {
    "@type": "Person",
    "@id": SITE + "/#artist",
    "name": NAME,
    "alternateName": "Crystal Orlando Fine Art",
    "url": SITE + "/",
    "image": SITE + "/assets/img/og-image.jpg",
    "jobTitle": "Visual Artist",
    "description": "American fine artist drawing hyper-realistic horses, wildlife and figurative subjects in charcoal and graphite, often at large scale on canvas.",
    "knowsAbout": ["Charcoal drawing", "Graphite drawing", "Equine art", "Wildlife art", "Western art", "Hyper-realism"],
    "homeLocation": {"@type": "Place", "address": {"@type": "PostalAddress", "addressRegion": "TX", "addressCountry": "US"}},
    "alumniOf": {"@type": "CollegeOrUniversity", "name": "North Central Texas College", "address": {"@type": "PostalAddress", "addressLocality": "Gainesville", "addressRegion": "TX", "addressCountry": "US"}},
    "award": [
        "Emerging Artist of the Year 2013, Art Galleries and Artists of the South Magazine",
        "Artist of the Year 2024, Cowgirl Artists of America",
    ],
    "email": "mailto:" + EMAIL,
    "sameAs": SAME_AS,
}
WEBSITE = {
    "@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "Crystal Orlando Fine Art",
    "description": "Charcoal and graphite fine art by Crystal Orlando: horses, North American wildlife and figurative works on canvas.",
    "publisher": {"@id": SITE + "/#artist"}, "inLanguage": "en-US",
}
AMARAN = {
    "@type": "ArtGallery", "@id": SITE + "/galleries/#amaran", "name": "Amaran Gallery", "url": "https://amarangallery.com",
    "telephone": "+1-307-200-6757",
    "address": {"@type": "PostalAddress", "streetAddress": "36 E Broadway Ave", "addressLocality": "Jackson", "addressRegion": "WY", "postalCode": "83001", "addressCountry": "US"},
}
DAVIS = {
    "@type": "ArtGallery", "@id": SITE + "/galleries/#davis-blevins", "name": "Davis & Blevins Gallery", "url": "https://davisandblevins.com",
    "telephone": "+1-940-995-2786",
    "address": {"@type": "PostalAddress", "streetAddress": "108 S Main St", "addressLocality": "Saint Jo", "addressRegion": "TX", "postalCode": "76265", "addressCountry": "US"},
}

WORKS = [
    dict(slug="guardian", title="Guardian", medium="Charcoal on canvas", form="Drawing", surface="Canvas",
         img="guardian-gallery", w=1316, h=784, sizes=[1316, 960, 640],
         alt="Guardian, a large charcoal drawing of a bald eagle in profile on a black ground, shown at gallery scale with a visitor standing before it",
         about="Bald eagle", note="Gallery scale"),
    dict(slug="bison", title="Bison", medium="Charcoal on canvas", form="Drawing", surface="Canvas",
         img="bison", w=319, h=380, sizes=[319],
         alt="Bison, charcoal drawing of an American bison standing in prairie grass, head turned toward the viewer",
         about="American bison", note=None),
    dict(slug="ride", title="Ride", medium="Graphite on canvas", form="Drawing", surface="Canvas",
         img="ride", w=533, h=380, sizes=[533],
         alt="Ride, graphite drawing of a young cowboy swinging a rope from the saddle of a galloping horse",
         about="Cowboy on horseback", note=None),
    dict(slug="madonna", title="Madonna", medium="Charcoal on canvas", form="Drawing", surface="Canvas",
         img="madonna", w=320, h=380, sizes=[320],
         alt="Madonna, charcoal study of a veiled marble face after Michelangelo's Pietà, lit from the left against darkness",
         about="Classical figure study", note=None),
    dict(slug="the-bear", title="The Bear", medium="Charcoal on canvas", form="Drawing", surface="Canvas",
         img="bear-gallery", w=1284, h=782, sizes=[1284, 960, 640],
         alt="The Bear, a framed charcoal drawing of a grizzly bear lowering its head, hung in a white gallery with a viewer beside it",
         about="Grizzly bear", note="Gallery scale"),
    dict(slug="the-horses", title="The Horses", medium="Charcoal on canvas, diptych", form="Drawing", surface="Canvas",
         img="horses-gallery", w=1204, h=868, sizes=[1204, 960, 640],
         alt="The Horses, two framed charcoal drawings of horses in motion, one rolling on dark ground and one rearing on light, viewed by a man in a gallery",
         about="Horses", note="Gallery scale"),
]
WORK_BY = {w["slug"]: w for w in WORKS}

def picture(work, cls="", loading="lazy", sizes_attr="(min-width: 960px) 50vw, 100vw", fetchpriority=None):
    """<picture> with webp + jpg, srcset when variants exist."""
    base = "/assets/img/" + work["img"]
    def srcset(ext):
        if len(work["sizes"]) == 1:
            return f"{base}.{ext}"
        parts = []
        for s in work["sizes"]:
            suf = "" if s == work["sizes"][0] else f"-{s}"
            parts.append(f"{base}{suf}.{ext} {s}w")
        return ", ".join(parts)
    ss = f' sizes="{sizes_attr}"' if len(work["sizes"]) > 1 else ""
    fp = f' fetchpriority="{fetchpriority}"' if fetchpriority else ""
    return (f'<picture><source type="image/webp" srcset="{srcset("webp")}"{ss}>'
            f'<img src="{base}.jpg" srcset="{srcset("jpg")}"{ss} width="{work["w"]}" height="{work["h"]}" '
            f'alt="{html.escape(work["alt"])}" loading="{loading}" decoding="async"{fp}{" class=" + chr(34) + cls + chr(34) if cls else ""}></picture>')

def nat(work):
    """Inline custom property that stops a figure scaling past its source pixels."""
    return f' style="--nat:{work["w"]}px"'

def artwork_schema(work):
    return {
        "@type": "VisualArtwork", "@id": f"{SITE}/works/#{work['slug']}", "name": work["title"],
        "creator": {"@id": SITE + "/#artist"}, "artform": work["form"], "artMedium": work["medium"].split(",")[0].split(" on ")[0],
        "artworkSurface": work["surface"], "image": f"{SITE}/assets/img/{work['img']}.jpg",
        "description": work["alt"], "about": work["about"], "inLanguage": "en-US",
    }

def faq_schema(items):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a_plain}}
        for q, a_plain, _ in items]}

def faq_html(items):
    out = ['<div class="faq">']
    for i, (q, _, a_html) in enumerate(items):
        out.append(f'<details{" open" if i == 0 else ""}><summary>{q}</summary><div class="answer">{a_html}</div></details>')
    out.append('</div>')
    return "\n".join(out)

def breadcrumbs(trail):
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"}]
    for i, (path, label) in enumerate(trail, start=2):
        items.append({"@type": "ListItem", "position": i, "name": label, "item": SITE + path})
    schema = {"@type": "BreadcrumbList", "itemListElement": items}
    lis = ['<li><a href="/">Home</a></li>'] + [
        (f'<li><a href="{p}">{l}</a></li>' if i < len(trail) - 1 else f'<li aria-current="page">{l}</li>')
        for i, (p, l) in enumerate(trail)]
    return schema, f'<ol class="crumbs" aria-label="Breadcrumb">{"".join(lis)}</ol>'

# ── Shell ──────────────────────────────────────────────────────────────────
def shell(*, path, title, description, body, schema, og_image=None, og_type="website"):
    url = SITE + path
    og_image = og_image or SITE + "/assets/img/og-image.jpg"
    graph = {"@context": "https://schema.org", "@graph": [WEBSITE, PERSON] + schema}
    nav = "".join(f'<a href="{h}">{l}</a>' for h, l in NAV)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="author" content="{NAME}">
<meta name="theme-color" content="#f3efe7">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Crystal Orlando Fine Art">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Guardian, a large charcoal drawing of a bald eagle by Crystal Orlando, shown at gallery scale">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(description)}">
<meta name="twitter:image" content="{og_image}">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="/assets/css/site.css">
<script>document.documentElement.classList.add('js')</script>
<script type="application/ld+json">{json.dumps(graph, ensure_ascii=False, separators=(",", ":"))}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="wordmark" href="/" aria-label="Crystal Orlando, home">Crystal Orlando<small>Charcoal &amp; Graphite</small></a>
    <nav class="site-nav" aria-label="Primary">{nav}<a class="nav-cta" href="/contact/">Contact</a></nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="footer__grid">
      <div class="footer__brand">
        <a class="wordmark" href="/">Crystal Orlando<small>Charcoal &amp; Graphite on Canvas</small></a>
        <p>Hyper-realistic drawings of horses, wildlife and the American West. Texas studio; shown in Jackson Hole, Wyoming and Saint Jo, Texas.</p>
      </div>
      <nav aria-labelledby="f-site"><h2 id="f-site">Site</h2>
        <ul><li><a href="/works/">Works</a></li><li><a href="/about/">About the artist</a></li><li><a href="/commissions/">Commissions</a></li><li><a href="/galleries/">Galleries</a></li><li><a href="/faq/">FAQ</a></li><li><a href="/contact/">Contact</a></li></ul>
      </nav>
      <div><h2>Galleries</h2>
        <ul><li><a href="https://amarangallery.com" rel="noopener">Amaran Gallery</a><br><span class="muted">Jackson Hole, WY · <a href="tel:+13072006757">307-200-6757</a></span></li>
        <li><a href="https://davisandblevins.com" rel="noopener">Davis &amp; Blevins</a><br><span class="muted">Saint Jo, TX · <a href="tel:+19409952786">940-995-2786</a></span></li></ul>
      </div>
      <div><h2>Studio</h2>
        <ul><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a href="https://www.instagram.com/orlandostudio/" rel="me noopener">Instagram</a></li><li><a href="https://www.facebook.com/crystalorlandoartist/" rel="me noopener">Facebook</a></li></ul>
      </div>
    </div>
    <div class="footer__bottom">
      <span>© {datetime.date.today().year} Crystal Orlando. All artwork and images are the property of the artist and may not be reproduced without written permission.</span>
      <span>Charcoal &amp; graphite · Texas · Wyoming</span>
    </div>
  </div>
</footer>
<script src="/assets/js/site.js" defer></script>
</body>
</html>
"""

# ── Content blocks reused across pages ────────────────────────────────────
def gallery_cards():
    return f"""
<div class="galleries">
  <article class="gallery-card" id="amaran">
    <h3>Amaran Gallery<span>Jackson Hole, Wyoming · since 2019</span></h3>
    <address>36 E Broadway Ave<br>Jackson, WY 83001<br><a href="tel:+13072006757">307-200-6757</a></address>
    <div class="links"><a class="textlink" href="https://amarangallery.com" rel="noopener">amarangallery.com</a><a class="textlink" href="https://www.google.com/maps/search/?api=1&amp;query=Amaran+Gallery+36+E+Broadway+Ave+Jackson+WY+83001" rel="noopener">Map</a></div>
  </article>
  <article class="gallery-card" id="davis-blevins">
    <h3>Davis &amp; Blevins Gallery<span>Saint Jo, Texas · since 2025</span></h3>
    <address>108 S Main St<br>Saint Jo, TX 76265<br><a href="tel:+19409952786">940-995-2786</a></address>
    <div class="links"><a class="textlink" href="https://davisandblevins.com" rel="noopener">davisandblevins.com</a><a class="textlink" href="https://www.google.com/maps/search/?api=1&amp;query=Davis+%26+Blevins+Gallery+108+S+Main+St+Saint+Jo+TX" rel="noopener">Map</a></div>
  </article>
</div>"""

def commission_band():
    return f"""
<section class="band" aria-labelledby="cta-h">
  <div class="wrap band__grid">
    <div class="band__text reveal">
      <p class="label">Commissions</p>
      <h2 id="cta-h">Your animal, drawn <em>once</em>, by hand.</h2>
      <p class="lede measure">Crystal draws a single original from your high-resolution photographs, or from a reference shoot she makes herself. A 50% deposit holds your place on the schedule.</p>
      <a class="btn btn--paper" href="/commissions/">How a commission works</a>
    </div>
    <figure class="band__figure reveal" data-delay="1">
      <picture><source type="image/webp" srcset="/assets/img/guardian-detail.webp"><img src="/assets/img/guardian-detail.jpg" width="746" height="880" alt="Detail of Guardian: the eye and beak of a bald eagle rendered in charcoal" loading="lazy" decoding="async"></picture>
      <figcaption>Guardian, detail. Charcoal on canvas.</figcaption>
    </figure>
  </div>
</section>"""

# ── FAQ content: (question, plain-text answer for schema, HTML answer) ─────
FAQ_MAIN = [
    ("Who is Crystal Orlando?",
     "Crystal Orlando is an American fine artist from Central Texas who draws horses, North American wildlife and figurative subjects in charcoal and graphite. She is largely self-taught, has sold her drawings since she was twelve, and is known for working at large scale directly on canvas and cradleboard. Her work is represented by Amaran Gallery in Jackson Hole, Wyoming, and Davis & Blevins Gallery in Saint Jo, Texas.",
     "<p>Crystal Orlando is an American fine artist from Central Texas who draws horses, North American wildlife and figurative subjects in charcoal and graphite. She is largely self-taught, has sold her drawings since she was twelve, and is known for working at large scale directly on canvas and cradleboard. Her work is represented by <a href=\"/galleries/#amaran\">Amaran Gallery</a> in Jackson Hole, Wyoming, and <a href=\"/galleries/#davis-blevins\">Davis &amp; Blevins Gallery</a> in Saint Jo, Texas.</p>"),
    ("What medium does Crystal Orlando use?",
     "Charcoal and graphite. Her signature technique combines powdered graphite with charcoal: graphite alone turns shiny at its darkest tones, and charcoal restores depth to those blacks. Since 2018 she has drawn large works directly on canvas and cradleboard rather than paper, so the pieces can hang unglazed at gallery scale.",
     "<p>Charcoal and graphite. Her signature technique combines powdered graphite with charcoal: graphite alone turns shiny at its darkest tones, and charcoal restores depth to those blacks. Since 2018 she has drawn large works directly on canvas and cradleboard rather than paper, so the pieces can hang unglazed at gallery scale.</p>"),
    ("Why is charcoal on canvas unusual?",
     "Charcoal is traditionally drawn on paper and framed under glass. Drawing it on primed canvas at wall scale is rare because there is almost no margin for error: charcoal cannot be painted over, and a serious mistake usually means starting the piece again. Orlando taught herself the method without a precedent to follow.",
     "<p>Charcoal is traditionally drawn on paper and framed under glass. Drawing it on primed canvas at wall scale is rare because there is almost no margin for error: charcoal cannot be painted over, and a serious mistake usually means starting the piece again. Orlando taught herself the method without a precedent to follow.</p>"),
    ("What does Crystal Orlando draw?",
     "Horses above all, then North American wildlife such as bison, grizzly bears, bald eagles and elk, and occasional figurative or classical studies. Most compositions show animals in motion, moving forward and out of the frame.",
     "<p>Horses above all, then North American wildlife such as bison, grizzly bears, bald eagles and elk, and occasional figurative or classical studies. Most compositions show animals in motion, moving forward and out of the frame.</p>"),
    ("Where can I see or buy Crystal Orlando's work?",
     "In person at Amaran Gallery, 36 E Broadway Ave, Jackson, Wyoming (307-200-6757) and at Davis & Blevins Gallery, 108 S Main St, Saint Jo, Texas (940-995-2786). For commissions and studio inquiries, email crystalorlando@gmail.com.",
     f"<p>In person at Amaran Gallery, 36 E Broadway Ave, Jackson, Wyoming (<a href=\"tel:+13072006757\">307-200-6757</a>) and at Davis &amp; Blevins Gallery, 108 S Main St, Saint Jo, Texas (<a href=\"tel:+19409952786\">940-995-2786</a>). For commissions and studio inquiries, email <a href=\"mailto:{EMAIL}\">{EMAIL}</a>.</p>"),
    ("Does Crystal Orlando accept commissions?",
     "Yes. She draws original commissions of horses, dogs, wildlife and other subjects from the client's high-resolution photographs, or from a reference shoot she makes herself (travel is billed separately). A 50% non-refundable deposit reserves a place on her schedule; the balance is due on completion. Timelines depend on size and the current queue and are confirmed before the deposit.",
     "<p>Yes. She draws original commissions of horses, dogs, wildlife and other subjects from the client's high-resolution photographs, or from a reference shoot she makes herself (travel is billed separately). A 50% non-refundable deposit reserves a place on her schedule; the balance is due on completion. Timelines depend on size and the current queue and are confirmed before the deposit. See <a href=\"/commissions/\">how a commission works</a>.</p>"),
    ("How much does a Crystal Orlando original cost?",
     "Prices depend on size, surface and complexity, and are quoted by the artist or her galleries for each piece. Small studies on paper are the most accessible entry point; large charcoal-on-canvas works are priced as gallery-scale originals. Contact the studio or either gallery for current availability and pricing.",
     f"<p>Prices depend on size, surface and complexity, and are quoted by the artist or her galleries for each piece. Small studies on paper are the most accessible entry point; large charcoal-on-canvas works are priced as gallery-scale originals. <a href=\"/contact/\">Contact the studio</a> or either gallery for current availability and pricing.</p>"),
    ("What awards has Crystal Orlando received?",
     "She was named Emerging Artist of the Year in 2013 by Art Galleries and Artists of the South Magazine and Artist of the Year in 2024 by Cowgirl Artists of America. She has been recognised by the Desert Caballeros Western Museum and the Lady Bird Johnson Wildflower Center at the University of Texas, and has exhibited with the Art Renewal Center's international ARC Salon.",
     "<p>She was named Emerging Artist of the Year in 2013 by Art Galleries and Artists of the South Magazine and Artist of the Year in 2024 by Cowgirl Artists of America. She has been recognised by the Desert Caballeros Western Museum and the Lady Bird Johnson Wildflower Center at the University of Texas, and has exhibited with the Art Renewal Center's international ARC Salon.</p>"),
    ("Are prints available?",
     "Yes. Fine art prints of selected wildlife drawings have been sold through the National Museum of Wildlife Art in Jackson, Wyoming, and can be requested from the studio. Originals remain one of a kind.",
     f"<p>Yes. Fine art prints of selected wildlife drawings have been sold through the National Museum of Wildlife Art in Jackson, Wyoming, and can be requested from the studio at <a href=\"mailto:{EMAIL}\">{EMAIL}</a>. Originals remain one of a kind.</p>"),
    ("How should a charcoal drawing on canvas be cared for?",
     "Hang it out of direct sunlight and away from humidity swings, and never touch or wipe the surface. The works are fixed by the artist and do not need glass; if you prefer glazing, use a spacer so the glass never rests on the drawing. Dust the frame, not the drawing.",
     "<p>Hang it out of direct sunlight and away from humidity swings, and never touch or wipe the surface. The works are fixed by the artist and do not need glass; if you prefer glazing, use a spacer so the glass never rests on the drawing. Dust the frame, not the drawing.</p>"),
]
FAQ_COMMISSION = [
    ("What can I commission?",
     "Any animal or subject you care about: a horse, a dog, a bull, wildlife you photographed, a family member on horseback. Crystal specialises in animals but has drawn figurative and classical subjects.",
     "<p>Any animal or subject you care about: a horse, a dog, a bull, wildlife you photographed, a family member on horseback. Crystal specialises in animals but has drawn figurative and classical subjects.</p>"),
    ("What photographs do you need?",
     "Sharp, high-resolution photographs taken in natural light, ideally several angles and one that shows the expression you want captured. Phone photos work if they are large and unedited. If your photos are not strong enough, Crystal can travel to shoot her own reference for a fee.",
     "<p>Sharp, high-resolution photographs taken in natural light, ideally several angles and one that shows the expression you want captured. Phone photos work if they are large and unedited. If your photos are not strong enough, Crystal can travel to shoot her own reference for a fee.</p>"),
    ("How does payment work?",
     "A 50% non-refundable deposit reserves your place on the schedule and covers materials. The remaining 50% is due when the finished drawing is approved and before shipping.",
     "<p>A 50% non-refundable deposit reserves your place on the schedule and covers materials. The remaining 50% is due when the finished drawing is approved and before shipping.</p>"),
    ("How long does a commission take?",
     "It depends on the size and the current queue. Small works on paper are quickest; large charcoal-on-canvas pieces take considerably longer because the medium cannot be corrected and each area is built up slowly. You receive a realistic timeline before paying the deposit.",
     "<p>It depends on the size and the current queue. Small works on paper are quickest; large charcoal-on-canvas pieces take considerably longer because the medium cannot be corrected and each area is built up slowly. You receive a realistic timeline before paying the deposit.</p>"),
    ("Can I choose canvas or paper?",
     "Yes. Paper suits smaller, intimate portraits and is framed under glass. Canvas or cradleboard suits larger pieces and hangs without glass, the way a painting does.",
     "<p>Yes. Paper suits smaller, intimate portraits and is framed under glass. Canvas or cradleboard suits larger pieces and hangs without glass, the way a painting does.</p>"),
]

# ── Pages ──────────────────────────────────────────────────────────────────
def page_home():
    hero = WORK_BY["guardian"]
    works_html = "\n".join([
        f'<figure class="work work--a reveal"{nat(WORK_BY["bison"])}>{picture(WORK_BY["bison"])}<figcaption><span class="work__title">Bison</span><span class="work__no">I</span><span class="work__medium">Charcoal on canvas</span></figcaption></figure>',
        f'<figure class="work work--b reveal" data-delay="1"{nat(WORK_BY["ride"])}>{picture(WORK_BY["ride"])}<figcaption><span class="work__title">Ride</span><span class="work__no">II</span><span class="work__medium">Graphite on canvas</span></figcaption></figure>',
        f'<figure class="work work--c reveal"{nat(WORK_BY["madonna"])}>{picture(WORK_BY["madonna"])}<figcaption><span class="work__title">Madonna</span><span class="work__no">III</span><span class="work__medium">Charcoal on canvas</span></figcaption></figure>',
        f'<figure class="work work--d reveal" data-delay="1"{nat(WORK_BY["the-horses"])}>{picture(WORK_BY["the-horses"], sizes_attr="(min-width: 960px) 44vw, 100vw")}<figcaption><span class="work__title">The Horses</span><span class="work__no">IV</span><span class="work__medium">Charcoal on canvas, diptych · gallery scale</span></figcaption></figure>',
    ])
    body = f"""
<section class="hero" aria-labelledby="hero-h">
  <div class="wrap">
    <div class="hero__grid">
      <div class="hero__text">
        <p class="label rise">Crystal Orlando · Charcoal &amp; graphite fine art</p>
        <h1 id="hero-h" class="hero__title rise">Charcoal, at the <em>scale</em> of a wall.</h1>
        <p class="lede hero__lede rise">Hyper-realistic drawings of horses and North American wildlife, worked in charcoal and graphite directly on canvas. A medium that cannot be corrected, chosen on purpose.</p>
        <div class="hero__actions rise">
          <a class="btn" href="/works/">See the work</a>
          <a class="textlink" href="/commissions/">Commission an original</a>
        </div>
        <div class="hero__meta rise">
          <span class="label label--ink">Texas studio</span>
          <span class="label">Amaran Gallery, Jackson Hole</span>
          <span class="label">Davis &amp; Blevins, Saint Jo</span>
        </div>
      </div>
      <figure class="hero__figure">
        {picture(hero, loading="eager", sizes_attr="(min-width: 960px) 55vw, 100vw", fetchpriority="high")}
        <figcaption><span><i>Guardian</i>, charcoal on canvas</span><span>Gallery scale</span></figcaption>
      </figure>
    </div>
  </div>
  <div class="strip" aria-hidden="true"><div class="strip__track">
    <span>Horses</span><span>Bison</span><span>Grizzly</span><span>Bald eagle</span><span>Charcoal on canvas</span><span>Powdered graphite</span><span>Jackson Hole</span><span>Saint Jo, Texas</span><span>Artist of the Year 2024</span><span>Commissions open</span>
    <span>Horses</span><span>Bison</span><span>Grizzly</span><span>Bald eagle</span><span>Charcoal on canvas</span><span>Powdered graphite</span><span>Jackson Hole</span><span>Saint Jo, Texas</span><span>Artist of the Year 2024</span><span>Commissions open</span>
  </div></div>
</section>

<section class="section" aria-labelledby="intro-h">
  <div class="wrap split">
    <div class="split__aside reveal">
      <div class="sticky">
        <p class="label">The artist</p>
        <h2 id="intro-h" class="display">Self-taught. Ranch-raised. <em>Unapologetically bold.</em></h2>
      </div>
    </div>
    <div class="split__main prose reveal" data-delay="1">
      <p class="lede">Crystal Orlando is an American fine artist from the ranchlands of Central Texas who draws horses, wildlife and figurative subjects in charcoal and graphite, often at gallery scale directly on canvas.</p>
      <p class="dropcap">She grew up homeschooled and largely alone with animals: horses, rescued strays, the wild things that came to the fence line. She sold her first drawings at twelve, trained cutting horses professionally, earned a degree in equine science, and came back to the pencil because it was the one thing she could always afford and always pick up. Since 2018 she has worked mostly on canvas and cradleboard, a surface almost nobody uses for charcoal because a mistake cannot be painted out.</p>
      <p>Cowgirl Artists of America named her Artist of the Year in 2024. Her drawings have hung from Kensington Palace in London to the National Museum of Wildlife Art in Jackson, Wyoming, which sells prints of her work.</p>
      <p><a class="textlink" href="/about/">Read the full biography</a></p>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="works-h">
  <div class="wrap">
    <div class="eyebrow reveal"><span class="num">01</span><h2 id="works-h" class="label label--ink" style="font-size:var(--step--1)">Selected works</h2></div>
    <div class="works">
      {works_html}
    </div>
    <div class="works-cta reveal">
      <p class="lede measure" style="max-width:40ch">Every piece is drawn by hand in the Texas studio. Originals are one of a kind.</p>
      <a class="btn" href="/works/">All selected works</a>
    </div>
  </div>
</section>

<section class="section" aria-label="Quotation from the artist">
  <div class="wrap">
    <blockquote class="quote reveal">
      <p>There is very little room for error. You cannot just paint over it. If done right, the drama and contrast of the black and white is like no other.</p>
      <footer class="label">Crystal Orlando, on charcoal</footer>
    </blockquote>
  </div>
</section>

<section class="section" aria-labelledby="facts-h">
  <div class="wrap">
    <h2 id="facts-h" class="visually-hidden">At a glance</h2>
    <div class="facts reveal">
      <div class="fact"><strong>25<sup>+</sup></strong><span class="label">Years drawing professionally</span></div>
      <div class="fact"><strong>60<sup>+</sup></strong><span class="label">Exhibitions</span></div>
      <div class="fact"><strong>2</strong><span class="label">Gallery representations</span></div>
      <div class="fact"><strong>2024</strong><span class="label">Artist of the Year, Cowgirl Artists of America</span></div>
    </div>
  </div>
</section>

{commission_band()}

<section class="section" aria-labelledby="where-h">
  <div class="wrap">
    <div class="eyebrow reveal"><span class="num">02</span><h2 id="where-h" class="label label--ink" style="font-size:var(--step--1)">Where to find the work</h2></div>
    <div class="reveal">{gallery_cards()}</div>
  </div>
</section>
"""
    schema = [
        {"@type": "WebPage", "@id": SITE + "/#webpage", "url": SITE + "/", "name": "Crystal Orlando | Charcoal & Graphite Fine Art",
         "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": SITE + "/#artist"},
         "primaryImageOfPage": {"@type": "ImageObject", "url": SITE + "/assets/img/guardian-gallery.jpg", "width": 1316, "height": 784},
         "dateModified": TODAY, "inLanguage": "en-US"},
        {"@type": "ItemList", "name": "Selected works", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "url": f"{SITE}/works/#{w['slug']}", "name": w["title"]} for i, w in enumerate(WORKS)]},
        AMARAN, DAVIS,
    ]
    return shell(path="/", title="Crystal Orlando | Charcoal & Graphite Fine Art, Horses & Wildlife on Canvas",
                 description="Crystal Orlando draws hyper-realistic horses and North American wildlife in charcoal and graphite at gallery scale on canvas. Texas studio; represented in Jackson Hole, WY and Saint Jo, TX. Commissions open.",
                 body=body, schema=schema, og_type="profile")

def page_works():
    crumbs_schema, crumbs = breadcrumbs([("/works/", "Works")])
    figs = []
    layout = ["work--wide", "work--third", "work--third", "work--third", "work--half", "work--half"]
    order = ["guardian", "bison", "ride", "madonna", "the-bear", "the-horses"]
    # each cell's share of a 12-column grid inside a 92vw wrap, so the browser
    # picks a variant at least as wide as the box it will actually fill
    cell_sizes = {"work--wide": "(min-width: 960px) 92vw, 100vw",
                  "work--half": "(min-width: 960px) 44vw, 100vw",
                  "work--third": "(min-width: 960px) 30vw, 100vw"}
    for i, (slug, cls) in enumerate(zip(order, layout)):
        w = WORK_BY[slug]
        note = f" · {w['note'].lower()}" if w["note"] else ""
        figs.append(f'<figure class="work {cls} reveal" id="{slug}"{nat(w)}>{picture(w, sizes_attr=cell_sizes[cls])}'
                    f'<figcaption><span class="work__title">{w["title"]}</span><span class="work__no">{["I","II","III","IV","V","VI"][i]}</span>'
                    f'<span class="work__medium">{w["medium"]}{note}</span></figcaption></figure>')
    body = f"""
<section class="page-head"><div class="wrap">
  {crumbs}
  <p class="label">Selected works</p>
  <h1>Drawn in <em>charcoal</em>, hung without glass.</h1>
  <p class="lede answer-box">Crystal Orlando's selected works are charcoal and graphite drawings of horses, bison, bears and eagles, most of them executed directly on canvas so they can hang at wall scale like paintings. Originals are one of a kind; prints of selected wildlife pieces are available on request.</p>
</div></section>
<section class="section--tight"><div class="wrap">
  <div class="works">{''.join(figs)}</div>
  <div class="works-cta reveal">
    <p class="lede" style="max-width:44ch">Availability changes as pieces sell. For current inventory and pricing, ask the studio or either gallery.</p>
    <div style="display:flex;gap:1rem 1.5rem;flex-wrap:wrap"><a class="btn" href="/contact/">Ask about availability</a><a class="btn btn--ember" href="/commissions/">Commission a piece</a></div>
  </div>
</div></section>
<section class="section"><div class="wrap split">
  <div class="split__aside reveal"><div class="sticky"><p class="label">On the medium</p><h2 class="display">Why the blacks look <em>the way they do</em></h2></div></div>
  <div class="split__main prose reveal" data-delay="1">
    <p>Graphite on its own goes glossy in the deepest shadows and throws back light. Orlando's answer, worked out over years without a teacher, is to lay powdered graphite for the mid-tones and bring charcoal into the darks, so the blacks stay matte and the whites of the canvas carry the light. Blending the two is unforgiving; they take to the surface differently and neither can be lifted cleanly once it is down.</p>
    <p>That is also why the work reads from across a room. Her stated aim is a drawing that is "instantly recognizable from across a crowded room," that catches the eye and pulls it back around the composition several times before the viewer moves on. Nearly every subject is in motion and moving forward, out of the frame.</p>
    <p><a class="textlink" href="/faq/">More questions answered</a></p>
  </div>
</div></section>
{commission_band()}
"""
    schema = [crumbs_schema,
              {"@type": "CollectionPage", "@id": SITE + "/works/#webpage", "url": SITE + "/works/", "name": "Selected works by Crystal Orlando",
               "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": SITE + "/#artist"}, "dateModified": TODAY, "inLanguage": "en-US",
               "hasPart": [{"@id": f"{SITE}/works/#{w['slug']}"} for w in WORKS]}] + [artwork_schema(w) for w in WORKS]
    return shell(path="/works/", title="Selected Works | Charcoal & Graphite Drawings by Crystal Orlando",
                 description="Selected charcoal and graphite drawings by Crystal Orlando: Guardian (bald eagle), Bison, Ride, Madonna, The Bear and The Horses. Large-scale originals on canvas; prints on request.",
                 body=body, schema=schema)

def page_about():
    crumbs_schema, crumbs = breadcrumbs([("/about/", "About the artist")])
    timeline = [
        ("Childhood", "Raised homeschooled on Central Texas ranchland among horses and rescued animals. Begins working at a horse barn at twelve in exchange for riding lessons, and sells her first drawings the same year."),
        ("Equine years", "Earns an A.A.S. in Equine Science from North Central Texas College in Gainesville, Texas. Works as a professional horse trainer, including at Leroy Ashcraft World Champion Cutting Horses and with USPA umpire Joe Bishop."),
        ("2012", "First gallery representation in the United States. Retires from horse training to draw full time."),
        ("2013", "Named Emerging Artist of the Year by Art Galleries and Artists of the South Magazine."),
        ("2018", "Begins drawing large works directly on canvas and cradleboard, leaving paper and glass behind for gallery-scale pieces."),
        ("2019", "Joins Amaran Gallery, Jackson Hole, Wyoming. The National Museum of Wildlife Art in Jackson carries prints of her wildlife drawings."),
        ("2020", "Diagnosed with breast cancer. Continues to draw through treatment and surgery; the animals in her work turn more decisively toward motion and forward movement."),
        ("2024", "Named Artist of the Year by Cowgirl Artists of America. Exhibits with the Art Renewal Center's international ARC Salon."),
        ("2025", "Joins Davis &amp; Blevins Gallery, Saint Jo, Texas."),
    ]
    tl = "".join(f'<li><span class="yr">{y}</span><p>{t}</p></li>' for y, t in timeline)
    body = f"""
<section class="page-head"><div class="wrap">
  {crumbs}
  <p class="label">About the artist</p>
  <h1>Crystal <em>Orlando</em></h1>
  <p class="lede answer-box">Crystal Orlando is a self-taught American artist from Central Texas who draws horses, wildlife and figurative subjects in charcoal and graphite. A former professional horse trainer with a degree in equine science, she is known for large-scale charcoal drawings made directly on canvas, and was named Artist of the Year by Cowgirl Artists of America in 2024.</p>
</div></section>

<section class="section--tight"><div class="wrap duo">
  <figure class="duo__fig reveal">
    <picture><source type="image/webp" srcset="/assets/img/horse-detail-2.webp"><img src="/assets/img/horse-detail-2.jpg" width="627" height="837" alt="Detail from The Horses: a charcoal drawing of a horse rolling, its neck and jaw filling the frame against black" loading="lazy" decoding="async"></picture>
    <figcaption>The Horses, detail. Charcoal on canvas.</figcaption>
  </figure>
  <div class="duo__body prose reveal" data-delay="1">
    <h2 style="font-size:var(--step-2);margin-bottom:1em">The wild classroom</h2>
    <p>"I was an isolated, homeschooled child in rural Texas," Orlando says. "My fondest memories are of wild animal friends, horses and rescued animals." Before charcoal there were the animals, and they remain the subject she has never left. Horses in particular taught her the thing her drawings are built on: attention. "The power of a horse, an animal that can kill you in a second, and the complexity of learning to communicate with them. When a horse loves you, his energy pulls negative out of you."</p>
    <p>She sold drawings from the age of twelve, then spent years in the saddle rather than the studio. She studied equine science at North Central Texas College, trained cutting horses professionally, and returned to drawing full time only after the horse work ended. The pencil was the one medium she could always afford and pick up in a spare hour. "Life situations kept happening," she says, "and it continued to be the easiest medium to pick up and put down quickly."</p>
  </div>
</div></section>

<section class="section"><div class="wrap duo duo--flip">
  <figure class="duo__fig reveal">
    <picture><source type="image/webp" srcset="/assets/img/bear-detail.webp"><img src="/assets/img/bear-detail.jpg" width="552" height="720" alt="Detail from The Bear: the face and shoulders of a grizzly bear in charcoal, fur catching light against a black ground" loading="lazy" decoding="async"></picture>
    <figcaption>The Bear, detail. Charcoal on canvas.</figcaption>
  </figure>
  <div class="duo__body prose reveal" data-delay="1">
    <h2 style="font-size:var(--step-2);margin-bottom:1em">The hardest surface</h2>
    <p>In 2018 she started drawing on canvas and cradleboard. "I didn't see anyone else doing this, so I had to figure it out on my own. I love the idea that I can work large and not have to be under glass." The trade is severe. Charcoal on a primed surface cannot be painted over; a real mistake means scrapping the piece. "If done right," she says, "the drama and contrast of the black and white is like no other."</p>
    <p>Her method pairs powdered graphite with charcoal. Graphite alone goes shiny in the darkest passages; charcoal brings the depth back. She describes seeing "patterns and depth easier than some people. Not just a subject, but all the shapes that form the subject." The flow, she adds, comes from joy; she finds it hard to work when she is sad.</p>
    <h3>Rising through fire</h3>
    <p>A breast cancer diagnosis in 2020 slowed the studio but did not close it. Treatment and surgery became, in her words, "a distraction and time to rethink my skills, and practice." The animals in her compositions since then are almost always moving forward, leaving the past behind. "The story of being unapologetically bold. Continuing to rise above the ashes over and over."</p>
    <p>Asked how she wants to be remembered: "As one of the great charcoal artists. That I helped pave the way for the medium to be recognized in the fine art world. And that I also helped break the glass ceiling for women artists to be recognized as great."</p>
  </div>
</div></section>

<section class="section"><div class="wrap split">
  <div class="split__aside reveal"><div class="sticky"><p class="label">Chronology</p><h2 class="display">A life in <em>graphite</em></h2></div></div>
  <div class="split__main reveal" data-delay="1"><ol class="timeline">{tl}</ol></div>
</div></section>

<section class="section"><div class="wrap split">
  <div class="split__aside reveal"><div class="sticky"><p class="label">Recognition</p><h2 class="display">Awards, museums, <em>salons</em></h2></div></div>
  <div class="split__main prose reveal" data-delay="1">
    <ul>
      <li><strong>Artist of the Year, 2024</strong>, Cowgirl Artists of America.</li>
      <li><strong>Emerging Artist of the Year, 2013</strong>, Art Galleries and Artists of the South Magazine.</li>
      <li>Recognition from the <strong>Desert Caballeros Western Museum</strong>, Wickenburg, Arizona, and the <strong>Lady Bird Johnson Wildflower Center</strong>, University of Texas at Austin.</li>
      <li>Exhibitor, <strong>Art Renewal Center International ARC Salon</strong> (14th and 16th Salons).</li>
      <li>Prints carried by the <strong>National Museum of Wildlife Art</strong>, Jackson, Wyoming.</li>
      <li>Work exhibited internationally, including at <strong>Kensington Palace</strong>, London.</li>
      <li>More than sixty exhibitions since 2012; represented by <a href="/galleries/#amaran">Amaran Gallery</a> (2019 to present) and <a href="/galleries/#davis-blevins">Davis &amp; Blevins Gallery</a> (2025 to present).</li>
    </ul>
    <p class="muted" style="margin-top:2rem"><small>Press and gallery inquiries: <a href="mailto:{EMAIL}">{EMAIL}</a>. High-resolution images and a current CV are available on request.</small></p>
  </div>
</div></section>
{commission_band()}
"""
    schema = [crumbs_schema,
              {"@type": "ProfilePage", "@id": SITE + "/about/#webpage", "url": SITE + "/about/", "name": "About Crystal Orlando",
               "isPartOf": {"@id": SITE + "/#website"}, "mainEntity": {"@id": SITE + "/#artist"}, "dateModified": TODAY, "inLanguage": "en-US"}]
    return shell(path="/about/", title="About Crystal Orlando | Self-Taught Charcoal Artist from Texas",
                 description="Biography of Crystal Orlando: Central Texas ranch upbringing, equine science degree, former horse trainer, self-taught charcoal and graphite artist, Cowgirl Artists of America Artist of the Year 2024. Timeline, awards and technique.",
                 body=body, schema=schema, og_type="profile")

def page_commissions():
    crumbs_schema, crumbs = breadcrumbs([("/commissions/", "Commissions")])
    body = f"""
<section class="page-head"><div class="wrap">
  {crumbs}
  <p class="label">Commissions</p>
  <h1>A drawing of <em>your</em> animal, made once.</h1>
  <p class="lede answer-box">Crystal Orlando accepts commissions for original charcoal and graphite drawings of horses, dogs, wildlife and other subjects. She works from your high-resolution photographs or from a reference shoot she makes herself. A 50% non-refundable deposit reserves your place on the schedule; the balance is due on completion.</p>
  <a class="btn btn--ember" href="mailto:{EMAIL}?subject=Commission%20inquiry">Start a commission by email</a>
</div></section>

<section class="section--tight"><div class="wrap">
  <div class="eyebrow reveal"><span class="num">01</span><h2 class="label label--ink" style="font-size:var(--step--1)">How it works</h2></div>
  <ol class="steps reveal">
    <li><h3>Tell her the subject</h3><p>Email a few words about the animal or scene, the size you have in mind, and where the piece will hang. Attach your best photographs or ask about a reference shoot.</p></li>
    <li><h3>Agree the piece</h3><p>Crystal proposes a surface (paper, canvas or cradleboard), a size, a price and a realistic timeline. Nothing is booked until you are happy with all four.</p></li>
    <li><h3>Reserve your place</h3><p>A 50% non-refundable deposit holds your slot on the schedule and covers materials. Large canvas pieces are booked in order of deposit.</p></li>
    <li><h3>The drawing</h3><p>Progress photos are shared at milestones. Because charcoal cannot be corrected, the work is slow and deliberate; the timeline you were given already accounts for that.</p></li>
    <li><h3>Approval and delivery</h3><p>You approve the finished drawing from photographs. The balance is paid, the piece is fixed and packed, and it ships insured or is collected from the studio or a gallery.</p></li>
  </ol>
</div></section>

<section class="section"><div class="wrap duo">
  <figure class="duo__fig reveal">
    <picture><source type="image/webp" srcset="/assets/img/horse-detail.webp"><img src="/assets/img/horse-detail.jpg" width="626" height="841" alt="Detail from The Horses: a charcoal drawing of a horse rearing, mane flying, on a light ground" loading="lazy" decoding="async"></picture>
    <figcaption>The Horses, detail. Charcoal on canvas.</figcaption>
  </figure>
  <div class="duo__body prose reveal" data-delay="1">
    <h2 style="font-size:var(--step-2);margin-bottom:1em">What makes a good commission</h2>
    <p>The strongest portraits come from photographs that show the animal as you know it: ears forward, weight shifting, the look it gives you at the gate. Several sharp images in natural light, taken at the animal's eye level, give Crystal the structure she needs. She sees "not just a subject, but all the shapes that form the subject," and a good reference lets those shapes come through.</p>
    <p>Where photographs fall short, she can travel to make her own reference for a fee. That is how the bison drawings began: a herd in Wyoming she was able to approach within a few yards, photographed once, and drawn many times since.</p>
    <h3>Surfaces and sizes</h3>
    <p>Paper suits intimate portraits and is framed under glass. Canvas and cradleboard suit large pieces and hang unglazed, the way a painting does. Both are fixed by the artist before delivery.</p>
  </div>
</div></section>

<section class="section"><div class="wrap split">
  <div class="split__aside reveal"><div class="sticky"><p class="label">Commission questions</p><h2 class="display">Before you <em>write</em></h2></div></div>
  <div class="split__main reveal" data-delay="1">{faq_html(FAQ_COMMISSION)}
    <p style="margin-top:2.5rem"><a class="btn" href="mailto:{EMAIL}?subject=Commission%20inquiry">Email {EMAIL}</a></p>
  </div>
</div></section>
"""
    schema = [crumbs_schema,
              {"@type": "WebPage", "@id": SITE + "/commissions/#webpage", "url": SITE + "/commissions/", "name": "Commission an original drawing",
               "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": SITE + "/#artist"}, "dateModified": TODAY, "inLanguage": "en-US"},
              {"@type": "Service", "name": "Commissioned charcoal and graphite drawing", "serviceType": "Fine art commission",
               "provider": {"@id": SITE + "/#artist"}, "areaServed": "US",
               "description": "Original charcoal and graphite drawings of horses, dogs, wildlife and other subjects, drawn from client photographs or an artist reference shoot. 50% non-refundable deposit to reserve a place on the schedule.",
               "url": SITE + "/commissions/"},
              faq_schema(FAQ_COMMISSION)]
    return shell(path="/commissions/", title="Commission a Charcoal Drawing | Crystal Orlando",
                 description="Commission an original charcoal or graphite drawing of your horse, dog or wildlife subject by Crystal Orlando. Drawn from your photographs; 50% deposit reserves your place. Process, surfaces, timeline and FAQ.",
                 body=body, schema=schema)

def page_galleries():
    crumbs_schema, crumbs = breadcrumbs([("/galleries/", "Galleries")])
    body = f"""
<section class="page-head"><div class="wrap">
  {crumbs}
  <p class="label">Galleries</p>
  <h1>Where to <em>see</em> the work</h1>
  <p class="lede answer-box">Crystal Orlando's drawings are shown and sold by Amaran Gallery at 36 E Broadway Ave in Jackson Hole, Wyoming, and by Davis &amp; Blevins Gallery at 108 S Main St in Saint Jo, Texas. Both galleries handle sales of available originals; commissions go through the studio.</p>
</div></section>
<section class="section--tight"><div class="wrap reveal">{gallery_cards()}</div></section>
<section class="section"><div class="wrap split">
  <div class="split__aside reveal"><div class="sticky"><p class="label">Also</p><h2 class="display">Museums and <em>prints</em></h2></div></div>
  <div class="split__main prose reveal" data-delay="1">
    <p>The <strong>National Museum of Wildlife Art</strong> in Jackson, Wyoming, has carried fine art prints of Crystal Orlando's wildlife drawings in its museum store. Prints of selected pieces can also be requested directly from the studio.</p>
    <p>Her work has been exhibited internationally, including at Kensington Palace in London, and with the Art Renewal Center's ARC Salon. For a current exhibition list, or to arrange a studio visit in Texas, email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
    <h3>Buying an original</h3>
    <p>Available originals are priced by the galleries and change as pieces sell. Call either gallery for what is on the wall today, or <a href="/contact/">contact the studio</a> to be told when new work is released. If nothing available fits, <a href="/commissions/">a commission</a> is drawn to your subject and size.</p>
  </div>
</div></section>
"""
    schema = [crumbs_schema,
              {"@type": "WebPage", "@id": SITE + "/galleries/#webpage", "url": SITE + "/galleries/", "name": "Galleries representing Crystal Orlando",
               "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": SITE + "/#artist"}, "dateModified": TODAY, "inLanguage": "en-US"},
              AMARAN, DAVIS]
    return shell(path="/galleries/", title="Galleries | Where to See & Buy Crystal Orlando's Drawings",
                 description="See Crystal Orlando's charcoal drawings at Amaran Gallery, 36 E Broadway Ave, Jackson Hole, WY (307-200-6757) and Davis & Blevins Gallery, 108 S Main St, Saint Jo, TX (940-995-2786). Prints via the National Museum of Wildlife Art.",
                 body=body, schema=schema)

def page_faq():
    crumbs_schema, crumbs = breadcrumbs([("/faq/", "FAQ")])
    body = f"""
<section class="page-head"><div class="wrap">
  {crumbs}
  <p class="label">Questions</p>
  <h1>Straight <em>answers</em></h1>
  <p class="lede answer-box">Direct answers about Crystal Orlando, her charcoal-on-canvas medium, where to buy the work, commissions, pricing, prints and care. Each answer stands on its own.</p>
</div></section>
<section class="section--tight"><div class="wrap split">
  <div class="split__aside reveal"><div class="sticky"><p class="label">Index</p><h2 class="display">The artist, the medium, <em>the buying</em></h2><p class="muted" style="margin-top:1.5rem">Something not covered? <a class="textlink" href="mailto:{EMAIL}">Email the studio</a>.</p></div></div>
  <div class="split__main reveal" data-delay="1">{faq_html(FAQ_MAIN)}</div>
</div></section>
{commission_band()}
"""
    schema = [crumbs_schema,
              {"@type": "WebPage", "@id": SITE + "/faq/#webpage", "url": SITE + "/faq/", "name": "Crystal Orlando FAQ",
               "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": SITE + "/#artist"}, "dateModified": TODAY, "inLanguage": "en-US"},
              faq_schema(FAQ_MAIN)]
    return shell(path="/faq/", title="FAQ | Crystal Orlando, Charcoal Artist: Medium, Buying, Commissions",
                 description="Answers about Crystal Orlando: who she is, why she draws charcoal on canvas, what she draws, where to buy originals and prints, commission terms, pricing and how to care for a charcoal drawing.",
                 body=body, schema=schema)

def page_contact():
    crumbs_schema, crumbs = breadcrumbs([("/contact/", "Contact")])
    body = f"""
<section class="page-head"><div class="wrap">
  {crumbs}
  <p class="label">Contact</p>
  <h1>Begin the <em>conversation</em></h1>
  <p class="lede answer-box">For commissions, prints, press and studio visits, email Crystal Orlando at <a href="mailto:{EMAIL}">{EMAIL}</a>. For available originals, call Amaran Gallery in Jackson Hole at 307-200-6757 or Davis &amp; Blevins Gallery in Saint Jo at 940-995-2786.</p>
</div></section>
<section class="section--tight"><div class="wrap split">
  <div class="split__aside reveal"><div class="sticky"><p class="label">Studio</p><h2 class="display">Texas</h2>
    <p style="margin-top:1.5rem"><a class="btn btn--ember" href="mailto:{EMAIL}?subject=Inquiry">Email the studio</a></p>
    <p class="muted" style="margin-top:1.5rem"><small>Please include your name, what you are interested in (commission, print, gallery information or general inquiry) and, for commissions, a sentence about the subject and size you have in mind.</small></p>
    <ul style="list-style:none;padding:0;margin:2rem 0 0;display:grid;gap:.5rem"><li><a class="textlink" href="https://www.instagram.com/orlandostudio/" rel="me noopener">Instagram, @orlandostudio</a></li><li><a class="textlink" href="https://www.facebook.com/crystalorlandoartist/" rel="me noopener">Facebook</a></li></ul>
  </div></div>
  <div class="split__main reveal" data-delay="1">
    <p class="label" style="margin-bottom:1.5rem">Galleries</p>
    {gallery_cards()}
  </div>
</div></section>
"""
    schema = [crumbs_schema,
              {"@type": "ContactPage", "@id": SITE + "/contact/#webpage", "url": SITE + "/contact/", "name": "Contact Crystal Orlando",
               "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": SITE + "/#artist"}, "dateModified": TODAY, "inLanguage": "en-US"},
              AMARAN, DAVIS]
    return shell(path="/contact/", title="Contact Crystal Orlando | Commissions, Prints & Gallery Inquiries",
                 description="Contact charcoal artist Crystal Orlando for commissions, prints and press at crystalorlando@gmail.com, or reach Amaran Gallery (Jackson Hole, WY) and Davis & Blevins Gallery (Saint Jo, TX) for available originals.",
                 body=body, schema=schema)

def page_404():
    body = """
<section class="lost wrap">
  <p class="label">404</p>
  <h1>Nothing on <em>this</em> wall.</h1>
  <p class="lede" style="margin-top:1.5rem">The page you asked for is not here. The work is.</p>
  <p style="margin-top:2rem"><a class="btn" href="/works/">See the work</a></p>
</section>"""
    out = shell(path="/404.html", title="Page not found | Crystal Orlando", description="This page does not exist.", body=body, schema=[])
    return out.replace('<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">', '<meta name="robots" content="noindex">')

PAGES = {
    "index.html": page_home,
    "works/index.html": page_works,
    "about/index.html": page_about,
    "commissions/index.html": page_commissions,
    "galleries/index.html": page_galleries,
    "faq/index.html": page_faq,
    "contact/index.html": page_contact,
    "404.html": page_404,
}

def sitemap():
    entries = [("/", "1.0"), ("/works/", "0.9"), ("/about/", "0.8"), ("/commissions/", "0.9"), ("/galleries/", "0.7"), ("/faq/", "0.7"), ("/contact/", "0.6")]
    imgs = "".join(f'<image:image><image:loc>{SITE}/assets/img/{w["img"]}.jpg</image:loc><image:title>{html.escape(w["title"])}</image:title></image:image>' for w in WORKS)
    urls = []
    for p, pr in entries:
        extra = imgs if p in ("/", "/works/") else ""
        urls.append(f"<url><loc>{SITE}{p}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority>{extra}</url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n' + "\n".join(urls) + "\n</urlset>\n")

def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for rel, fn in PAGES.items():
        path = os.path.join(root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(fn())
        print("wrote", rel)
    with open(os.path.join(root, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap())
    print("wrote sitemap.xml")

if __name__ == "__main__":
    main()
