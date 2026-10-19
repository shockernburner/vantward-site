#!/usr/bin/env python3
"""Builds the inner pages of vantward.com (about, products, insights),
plus sitemap.xml, from the data below. The homepage (index.html) is
hand-written and not touched.

Run from the repository root:  python3 tools/build_pages.py
After the change is live, tell search engines:  python3 tools/build_pages.py --indexnow
"""
import html
import json
from pathlib import Path

SITE = "https://vantward.com"
ROOT = Path(__file__).resolve().parent.parent
UPDATED = "2026-10-19"

CHROME_URL = "https://chromewebstore.google.com/detail/eraseai-firewall/hckhbadbpkihjpooeljdocgidelcampp"
PLAY_RUBIKATION = "https://play.google.com/store/apps/details?id=com.rubikation.arena"
LI_COMPANY_POST = ("https://www.linkedin.com/posts/vantward-solutions-pte-ltd_aidatagovernance-aifirewall-"
                   "promptsecurity-activity-7453375075518611456-Zfh5")
LI_FOUNDER_POST = "https://lnkd.in/p/gcBD_wBn"
PLAY_ERASEAI = "https://play.google.com/store/apps/details?id=com.eraseai.firewall"
ITCH_HUSHCLAW = "https://firdousmahmood.itch.io/hushclaw"
MEDIUM_POST = "https://medium.com/@firdous.mahmood26/the-three-layers-between-a-citizen-and-an-ai-model-4712f1ceb952"

ORG_REF = {"@id": f"{SITE}/#org"}

NAV = [
    ("/eraseai-firewall/", "EraseAI Firewall"),
    ("/rubikation/", "Rubikation"),
    ("/cookhub/", "CookHub"),
    ("/hushclaw/", "Hushclaw"),
    ("/insights/", "Insights"),
    ("/about/", "About"),
]

PRODUCTS = [
    ("/eraseai-firewall/", "EraseAI Firewall", "Stops secrets and personal data reaching AI chats.", "#22d3ee"),
    ("/rubikation/", "Rubikation", "Live 1v1 cube arena with world and country ranks.", "#e8b23f"),
    ("/cookhub/", "CookHub", "Zero-commission home cooking from your neighbourhood.", "#ff6a1f"),
    ("/hushclaw/", "Hushclaw", "Co-op dinosaur survival. Alpha out now for PC and Mac.", "#8fdc5a"),
]


def faq_html(faq):
    items = "\n".join(
        f"      <details><summary>{html.escape(q)}</summary><p>{a}</p></details>" for q, a in faq
    )
    return f'<div class="faq">\n{items}\n    </div>'


def faq_schema(faq):
    import re
    strip = lambda s: re.sub(r"<[^>]+>", "", s)
    return {
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip(a)}}
            for q, a in faq
        ],
    }


def page(p):
    url = f"{SITE}{p['path']}"
    image = f"{SITE}/assets/og/{p['og']}"
    crumbs = [("Home", f"{SITE}/"), (p["crumb"], url)]
    graph = [
        {
            "@type": "WebPage",
            "@id": f"{url}#page",
            "url": url,
            "name": p["title"],
            "description": p["desc"],
            "isPartOf": {"@id": f"{SITE}/#website"},
            "publisher": ORG_REF,
            "primaryImageOfPage": image,
            "dateModified": UPDATED,
            "inLanguage": "en",
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)
            ],
        },
        *p.get("schema", []),
    ]
    if p.get("faq"):
        graph.append(faq_schema(p["faq"]))
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=2, ensure_ascii=False)

    current = ' aria-current="page"'
    nav = "\n".join(
        f'        <a href="{h}"{current if h == p["path"] else ""}>{t}</a>' for h, t in NAV
    )
    ctas = "\n".join(f"        {c}" for c in p["ctas"])
    others = "\n".join(
        f'      <a class="other" href="{h}" style="--c:{c}"><b>{t}</b><span>{d}</span></a>'
        for h, t, d, c in PRODUCTS
        if h != p["path"]
    )
    faq_block = ""
    if p.get("faq"):
        faq_block = f"""
  <section class="block" id="faq">
    <div class="wrap">
      <h2>Questions</h2>
    {faq_html(p["faq"])}
    </div>
  </section>
"""
    tag = f'\n      <p class="tag">{p["tag"]}</p>' if p.get("tag") else ""
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#0a0c45">
  <title>{html.escape(p["title"])}</title>
  <meta name="description" content="{html.escape(p["desc"])}">
  <meta name="robots" content="index,follow,max-image-preview:large">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Vantward Solutions">
  <meta property="og:locale" content="en_SG">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{html.escape(p["title"])}">
  <meta property="og:description" content="{html.escape(p["desc"])}">
  <meta property="og:image" content="{image}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{html.escape(p["alt"])}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(p["title"])}">
  <meta name="twitter:description" content="{html.escape(p["desc"])}">
  <meta name="twitter:image" content="{image}">
  <link rel="icon" type="image/png" href="/assets/favicon.png">
  <link rel="apple-touch-icon" href="/assets/icon-192.png">
  <link rel="manifest" href="/site.webmanifest">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=Sora:wght@700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/site.css">
  <style>:root {{ --acc: {p["acc"]}; }}</style>
  <script type="application/ld+json">
{ld}
  </script>
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
  <header class="top">
    <div class="wrap">
      <a class="brand" href="/"><span><img src="/assets/logo-mark-96.png" alt="" width="30" height="30"></span>Vantward</a>
      <nav aria-label="Primary">
{nav}
        <a class="cta" href="/about/#contact">Contact</a>
      </nav>
    </div>
  </header>

  <main id="main">
    <div class="wrap">
      <ol class="crumbs" aria-label="Breadcrumb"><li><a href="/">Home</a></li><li aria-current="page">{p["crumb"]}</li></ol>
      <div class="hero">
        <div>
          <span class="eyebrow">{p["eyebrow"]}</span>
          <h1>{p["h1"]}</h1>{tag}
          <p class="lead">{p["lead"]}</p>
          <div class="btns">
{ctas}
          </div>
        </div>
        <figure><img src="/assets/og/{p["og"]}" alt="{html.escape(p["alt"])}" width="1200" height="630" fetchpriority="high"></figure>
      </div>
    </div>
{p["body"]}{faq_block}
    <section class="block">
      <div class="wrap">
        <h2>More from Vantward</h2>
        <div class="others">
{others}
        </div>
      </div>
    </section>
  </main>

  <footer>
    <div class="wrap">
      <div>
        <b style="color:#fff">Vantward Solutions Pte. Ltd.</b><br>
        68 Circular Road #02-01, Singapore 049422<br>
        <a href="mailto:director@vantward.com">director@vantward.com</a> · <a href="https://wa.me/6582430739">+65 8243 0739</a><br>
        <span class="note">© 2026 Vantward Solutions</span>
      </div>
      <nav aria-label="Footer">
        <a href="/">Home</a>
{chr(10).join(f'        <a href="{h}">{t}</a>' for h, t in NAV)}
      </nav>
    </div>
  </footer>
</body>
</html>
"""


def section(title, inner, anchor=""):
    a = f' id="{anchor}"' if anchor else ""
    return f"""
  <section class="block"{a}>
    <div class="wrap">
      <h2>{title}</h2>
{inner}
    </div>
  </section>
"""


def tiles(items):
    return '      <div class="grid">\n' + "\n".join(
        f'        <div class="tile"><h3>{h}</h3><p>{t}</p></div>' for h, t in items
    ) + "\n      </div>"


def steps(items):
    return '      <ol class="steps">\n' + "\n".join(f"        <li>{t}</li>" for t in items) + "\n      </ol>"


def prose(*paras):
    return "\n".join(f"      <p>{t}</p>" for t in paras)


# --------------------------------------------------------------------------
# Pages
# --------------------------------------------------------------------------

PAGES = []

# EraseAI Firewall ----------------------------------------------------------
eraseai_faq = [
    ("Is EraseAI Firewall free?",
     "Yes. The Chrome extension is free, with no limit and no account: every message is checked on your device. "
     "EraseAI Personal, $5 a month or $54 a year, adds one-click Sanitize &amp; Send, attachment and screenshot "
     "scanning and scan history."),
    ("Does EraseAI send my prompts anywhere?",
     "Without an account, no. Every check happens in your browser and nothing is sent anywhere. With an account, "
     "message text is checked by the EraseAI API over HTTPS, and your scan history keeps a short excerpt with secrets "
     "masked. Your data is never sold or used to train models."),
    ("Which AI tools does it work with?",
     "ChatGPT, Claude, Gemini and Replit, in your browser. The extension only runs on those sites."),
    ("What does it detect?",
     "Common access key and token formats, passwords written into a message, and personal information such as "
     "contact details and payment card numbers."),
    ("Does it check files I attach?",
     "Yes. Attached files are checked too, and text inside images is read on your device, so the image itself is "
     "never uploaded."),
    ("Is there an Android app?",
     f'Yes. Get EraseAI Firewall for Android on <a href="{PLAY_ERASEAI}">Google Play</a>. It also runs as a '
     'Chrome extension and as a web app at <a href="https://eraseai.ai">eraseai.ai</a>.'),
    ("Who makes EraseAI Firewall?",
     'Vantward Solutions Pte. Ltd., a software studio in Singapore. <a href="/about/">About us</a>.'),
]
PAGES.append({
    "path": "/eraseai-firewall/",
    "slug": "eraseai-firewall",
    "crumb": "EraseAI Firewall",
    "title": "EraseAI Firewall: Stop Secrets Reaching ChatGPT and Claude",
    "desc": "Free Chrome extension and Android app that checks prompts and files before they reach ChatGPT, Claude, "
            "Gemini or Replit, and redacts API keys, passwords, card numbers and personal data.",
    "acc": "#22d3ee",
    "og": "eraseai.jpg",
    "alt": "EraseAI Firewall stopping a message with a password and an API key before it is sent to an AI chat",
    "eyebrow": "AI security · Chrome, Android and web",
    "h1": "EraseAI Firewall: an AI firewall in your browser",
    "lead": "EraseAI Firewall checks what you are about to send to an AI chat and stops secrets and personal data "
            "before they leave your browser. When it finds something sensitive, you decide whether to redact it, "
            "send anyway, or cancel.",
    "ctas": [
        f'<a class="btn primary" href="{CHROME_URL}?utm_source=site&amp;utm_medium=web&amp;utm_campaign=vantward" rel="noopener">Add to Chrome, free</a>',
        '<a class="btn" href="https://eraseai.ai" rel="noopener">Open the web app</a>',
        f'<a class="btn" href="{PLAY_ERASEAI}&amp;hl=en" rel="noopener">Get it on Google Play</a>',
    ],
    "body": section("Why an AI firewall", prose(
        "Pasting a log, a config file or a customer email into an AI chat is an easy way to leak a credential or "
        "someone's personal details. Once it is sent, you cannot take it back.",
        "EraseAI Firewall checks each message at the moment you press Send, so a mistake gets caught instead of "
        "shipped. Messages with nothing sensitive go through without interruption.")) +
        section("What it looks for", tiles([
            ("Keys and tokens", "Common access key and token formats, the kind that sit in config files and logs."),
            ("Passwords", "Passwords written into a message, such as a connection string or a copied .env line."),
            ("Personal data", "Contact details, payment card numbers and other personal information."),
            ("Attachments", "Files you attach are checked too. Text in images is read on your device."),
        ])) +
        section("How it works", steps([
            "<b>Write or paste</b> your message as usual in ChatGPT, Claude, Gemini or Replit.",
            "<b>Press Send.</b> EraseAI Firewall checks the message and any attached files first.",
            "<b>Decide.</b> If something sensitive is found, it shows you what and where. Choose Sanitize &amp; Send "
            "to replace it with placeholders, Send Anyway, or Cancel.",
        ])) +
        section("Your data", prose(
            "The extension runs only on the AI sites it protects. Without an account, every check happens on your "
            "device and nothing is sent anywhere. With an account, message text is checked by the EraseAI API over "
            "HTTPS, and your scan history keeps a short excerpt of each scan, with secrets masked, so you can review "
            "it in your dashboard.",
            'We never sell your data or use it to train models. Read the <a href="https://eraseai.ai/privacy">'
            "EraseAI privacy policy</a>.")) +
        section("Pricing", """      <div class="prices">
        <div class="price"><h3>EraseAI Firewall</h3><div class="amt">Free</div><ul><li>Every message checked on your device</li><li>No limit, no account</li><li>ChatGPT, Claude, Gemini, Replit</li></ul></div>
        <div class="price"><h3>EraseAI Personal</h3><div class="amt">$5<small style="font-size:.9rem;color:#b6bddc"> / month</small></div><ul><li>Or $54 a year</li><li>One-click Sanitize &amp; Send</li><li>Attachment and screenshot scanning</li><li>Scan history in your dashboard</li></ul></div>
      </div>
      <p style="margin-top:18px">Security and IT teams use EraseAI Firewall to reduce data leaks to AI tools without banning them. Team plans are at <a href="https://eraseai.ai">eraseai.ai</a>.</p>"""),
    "faq": eraseai_faq,
    "schema": [{
        "@type": "SoftwareApplication",
        "@id": f"{SITE}/eraseai-firewall/#app",
        "name": "EraseAI Firewall",
        "alternateName": "EraseAI",
        "applicationCategory": "SecurityApplication",
        "applicationSubCategory": "AI data loss prevention",
        "operatingSystem": "Chrome, Android, Web",
        "sameAs": [CHROME_URL, PLAY_ERASEAI],
        "url": "https://eraseai.ai",
        "downloadUrl": CHROME_URL,
        "installUrl": CHROME_URL,
        "description": "Browser extension that stops API keys, passwords, card numbers and personal data before "
                       "they reach ChatGPT, Claude, Gemini or Replit, in prompts and attached files.",
        "featureList": ["Secret and PII detection in prompts", "Attachment scanning", "On-device image text reading",
                        "Sanitize & Send with placeholders", "Works in ChatGPT, Claude, Gemini and Replit"],
        "offers": [
            {"@type": "Offer", "name": "EraseAI Firewall", "price": "0", "priceCurrency": "USD"},
            {"@type": "Offer", "name": "EraseAI Personal (monthly)", "price": "5", "priceCurrency": "USD"},
            {"@type": "Offer", "name": "EraseAI Personal (yearly)", "price": "54", "priceCurrency": "USD"},
        ],
        "publisher": ORG_REF,
        "image": f"{SITE}/assets/og/eraseai.jpg",
    }],
})

# Rubikation --------------------------------------------------------------
rubik_faq = [
    ("Can I play Rubikation in a browser?",
     'Yes. Play on the web at <a href="https://rubikation.com">rubikation.com</a>, or install the Android app from '
     f'<a href="{PLAY_RUBIKATION}">Google Play</a>.'),
    ("Is it really live 1v1?",
     "Yes. You face a real opponent in real time and see their cube race beside yours. It is not a ghost replay "
     "and not a solo timer."),
    ("How do the rankings work?",
     "Every serious solve can move you up the worldwide leaderboard and your country's leaderboard. Weekly and "
     "monthly arenas add qualifiers and seasonal competition."),
    ("Can a beginner learn to solve the cube here?",
     "Yes. Training goes step by step from the cross and first layers into CFOP (Cross, F2L, OLL, PLL), and smart "
     "hints read your cube and suggest a real next move."),
    ("Is Rubikation affiliated with Rubik's?",
     "No. Rubikation is an independent project and is not affiliated with, endorsed by, or sponsored by the owner "
     "of the RUBIK'S trademark."),
]
PAGES.append({
    "path": "/rubikation/",
    "slug": "rubikation",
    "crumb": "Rubikation",
    "title": "Rubikation: Live 1v1 Cube Arena with World and Country Ranks",
    "desc": "Race another cuber head-to-head in real time, climb worldwide and country leaderboards, join weekly "
            "arenas and learn from layers to CFOP. Play on the web or on Android.",
    "acc": "#e8b23f",
    "og": "rubikation.jpg",
    "alt": "Vee the robot racing a live 1v1 cube battle in Rubikation, with both timers on screen",
    "eyebrow": "Game · Web and Android",
    "h1": "Rubikation: Cube Arena",
    "tag": "Race. Rank. Represent.",
    "lead": "The live 1v1 cube arena with real global competition. Race another cuber head-to-head, climb the "
            "worldwide and country leaderboards, fight weekly and monthly arenas, and train your skill.",
    "ctas": [
        '<a class="btn primary" href="https://rubikation.com" rel="noopener">Play on the web</a>',
        f'<a class="btn" href="{PLAY_RUBIKATION}" rel="noopener">Get it on Google Play</a>',
    ],
    "body": section("What you get", tiles([
        ("Live 1v1 battles", "Face a real opponent in real time and feel every second of the duel."),
        ("Global and country ranks", "Climb the worldwide board and represent your country on the national one."),
        ("Weekly and monthly arenas", "Qualifiers and seasonal competition give you something beyond a personal best."),
        ("A real 3x3", "Turn a fully simulated cube with notation (U, R, F, L, D, B) or swipe. Reorient with x, y, z."),
        ("Train for skill", "Step-by-step learning from the cross and layers into CFOP: Cross, F2L, OLL, PLL."),
        ("Smart hints", "Stuck mid-solve? Hints read your cube and suggest a real next move."),
    ])) + section("Who it's for", prose(
        "Beginners who want a patient path to solving, and speedcubers who want somewhere to prove it. Earn points "
        "by solving and training, unlock cube skins for every arena, and race without ads interrupting.",
        '<span class="note">Rubikation is an independent project and is not affiliated with, endorsed by, or '
        "sponsored by the owner of the RUBIK'S trademark.</span>")),
    "faq": rubik_faq,
    "schema": [{
        "@type": "VideoGame",
        "@id": f"{SITE}/rubikation/#game",
        "name": "Rubikation: Cube Arena",
        "alternateName": "Rubikation",
        "url": "https://rubikation.com",
        "sameAs": [PLAY_RUBIKATION],
        "genre": ["Puzzle", "Competitive"],
        "gamePlatform": ["Web browser", "Android"],
        "playMode": ["MultiPlayer", "SinglePlayer"],
        "applicationCategory": "GameApplication",
        "operatingSystem": "Android, Web",
        "description": "Live 1v1 cube battles with worldwide and country leaderboards, weekly and monthly arenas, "
                       "CFOP training and smart hints.",
        "publisher": ORG_REF,
        "image": f"{SITE}/assets/og/rubikation.jpg",
    }],
})

# CookHub -----------------------------------------------------------------
cook_faq = [
    ("Does CookHub take a commission?",
     "No. Chefs keep 100% of every meal. There is zero commission on neighbourhood pre-orders."),
    ("What does it cost a chef?",
     "A one-time $49 lifetime chef licence. Publishing recipes and building an audience is free."),
    ("Do diners pay a service fee?",
     "No. Diners pay no platform service fees."),
    ("How do I get my food?",
     "Rider-powered delivery or pickup from the home kitchen."),
    ("Where can I try it?",
     'At <a href="https://cookhub.live">cookhub.live</a>.'),
]
PAGES.append({
    "path": "/cookhub/",
    "slug": "cookhub",
    "crumb": "CookHub",
    "title": "CookHub: Zero-Commission Home Cooking Marketplace",
    "desc": "CookHub connects home chefs with diners nearby. Chefs keep 100% of every meal for a $49 lifetime "
            "licence, diners pay no service fees, with pickup or rider delivery. Made by Vantward Solutions.",
    "acc": "#ff6a1f",
    "og": "cookhub.jpg",
    "alt": "Vee the robot ordering biryani from a nearby home kitchen in the CookHub app",
    "eyebrow": "Food · Neighbourhood marketplace",
    "h1": "CookHub: real home cooking, zero corporate cut",
    "lead": "A neighbourhood food marketplace that connects home chefs with local diners. Chefs keep 100% of their "
            "earnings and diners pay no platform service fees.",
    "ctas": ['<a class="btn primary" href="https://cookhub.live" rel="noopener">Find a home kitchen</a>',
             '<a class="btn" href="https://cookhub.live" rel="noopener">Start selling</a>'],
    "body": section("For diners", tiles([
        ("Eat local", "Find fresh dishes from home kitchens nearby."),
        ("No service fees", "Diners pay no platform service fees."),
        ("Pickup or delivery", "Collect from the kitchen or have a rider bring it."),
        ("Community recipes", "Browse recipes shared by cooks in your neighbourhood."),
    ])) + section("For chefs", tiles([
        ("Keep 100% of every meal", "Zero commission, ever, on neighbourhood pre-orders."),
        ("$49 lifetime licence", "One payment. No monthly plan and no cut of your sales."),
        ("Publish recipes free", "Build an audience before and between orders."),
        ("Run the business, not just the menu", "Turn views, DMs and repeat clients into paid work."),
    ])),
    "faq": cook_faq,
    "schema": [{
        "@type": "WebApplication",
        "@id": f"{SITE}/cookhub/#app",
        "name": "CookHub",
        "url": "https://cookhub.live",
        "applicationCategory": "LifestyleApplication",
        "operatingSystem": "Web",
        "description": "Neighbourhood marketplace for home cooking: chefs keep 100% of every meal, diners pay no "
                       "service fees, pickup or rider delivery.",
        "offers": {"@type": "Offer", "name": "Lifetime chef licence", "price": "49", "priceCurrency": "USD"},
        "publisher": ORG_REF,
        "image": f"{SITE}/assets/og/cookhub.jpg",
    }],
})

# Hushclaw (formerly announced as TETHER: Primal) ---------------------------
hush_faq = [
    ("Can I play Hushclaw now?",
     f'Yes. The alpha (version 0.3.0) is on <a href="{ITCH_HUSHCLAW}">itch.io</a> for Windows and macOS, '
     "and you name your own price."),
    ("How many people can play together?",
     "Play solo, or co-op with up to four players using a join code. Teammates hear each other through proximity "
     "voice chat."),
    ("Can I play solo?",
     "Yes. Solo has Easy, Medium and Hard difficulty. Co-op always plays on Hard."),
    ("Is it pay-to-win?",
     "No. Everything you buy during a match is paid for with coins earned in that match, and nothing is sold for power."),
    ("Is Hushclaw the game that was called TETHER: Primal?",
     "Yes. Hushclaw is the new name of the co-op dinosaur survival game we first announced as TETHER: Primal."),
    ("Who makes Hushclaw?",
     'Vantward Games, the games label of <a href="/about/">Vantward Solutions</a> in Singapore.'),
]
PAGES.append({
    "path": "/hushclaw/",
    "slug": "hushclaw",
    "crumb": "Hushclaw",
    "title": "Hushclaw: Co-op Dinosaur Survival Game for PC and Mac",
    "desc": "In some parallel universe, the dinosaurs never died out. Solo or co-op for up to four: recover black "
            "boxes on a new island every match and reach the helicopter. Alpha on itch.io.",
    "acc": "#8fdc5a",
    "og": "hushclaw.jpg",
    "alt": "Hushclaw teaser: a dinosaur crossing a volcanic island while a team of four stays close together",
    "eyebrow": "Game · Alpha out now",
    "h1": "Hushclaw",
    "tag": "Stay quiet. Stay close. Leave no one.",
    "lead": "In some parallel universe, the dinosaurs never died out. Hushclaw is a first-person co-op survival "
            "game: drop onto a new island every match, recover what was left at dead outposts, and get everyone to "
            "the helicopter.",
    "ctas": [f'<a class="btn primary" href="{ITCH_HUSHCLAW}" rel="noopener">Play on itch.io</a>',
             '<span class="btn soon">Windows · macOS · Name your own price</span>'],
    "body": section("How a match works", steps([
        "<b>Drop in.</b> Every match is a new procedurally generated island of jungle, plains, swamps, rivers and ruins.",
        "<b>Recover.</b> Search dead outposts. Black boxes beep, and the beeping draws dinosaurs to you.",
        "<b>Deliver.</b> Bring what you found to the landing pad and fire a flare.",
        "<b>Hold.</b> Survive 45 seconds until the helicopter arrives. Teammates who go down can be revived.",
    ])) + section("The island", tiles([
        ("Dinosaurs that listen", "They hear you, track your scent, growl before they charge, pounce, swing their tails and knock you down."),
        ("Night and weather", "Night matches with night vision goggles, plus storms, fog and rain."),
        ("The Field Archive", "Recovered items are sealed files that hold a contract, a story page, a perk or an outfit."),
        ("Tools to stay alive", "Heal, throw a noise lure, light a hand flare, and shop between fights."),
    ])) + section("Play together", tiles([
        ("Co-op for up to four", "Join with a code and talk through proximity voice chat."),
        ("Daily Island and Weekly Contract", "Shared by every player, with a daily streak."),
        ("Leaderboards", "Worldwide boards for survivors and for teams, with custom team emblems."),
        ("Fair by design", "In-match purchases use in-match coins only. Nothing is sold for power."),
    ])) + section("Details", """      <div class="grid">
        <div class="tile"><h3>Platforms</h3><p>Windows and macOS</p></div>
        <div class="tile"><h3>Players</h3><p>Solo, or co-op for 1 to 4</p></div>
        <div class="tile"><h3>Status</h3><p>Alpha, version 0.3.0</p></div>
        <div class="tile"><h3>Price</h3><p>Name your own price on itch.io</p></div>
        <div class="tile"><h3>A match</h3><p>About half an hour</p></div>
        <div class="tile"><h3>Controls</h3><p>Keyboard and mouse, rebindable</p></div>
      </div>
      <p class="note" style="margin-top:16px">Hushclaw was first announced as TETHER: Primal.</p>"""),
    "faq": hush_faq,
    "schema": [{
        "@type": "VideoGame",
        "@id": f"{SITE}/hushclaw/#game",
        "name": "Hushclaw",
        "alternateName": "TETHER: Primal",
        "url": f"{SITE}/hushclaw/",
        "sameAs": [ITCH_HUSHCLAW],
        "description": "First-person co-op dinosaur survival game for one to four players on a procedurally "
                       "generated island, with stealth, proximity voice chat and extraction by helicopter.",
        "genre": ["Survival", "Co-op", "Stealth", "Horror"],
        "gamePlatform": ["Windows", "macOS"],
        "operatingSystem": "Windows, macOS",
        "applicationCategory": "GameApplication",
        "softwareVersion": "0.3.0",
        "playMode": ["CoOp", "MultiPlayer", "SinglePlayer"],
        "numberOfPlayers": {"@type": "QuantitativeValue", "minValue": 1, "maxValue": 4},
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD", "url": ITCH_HUSHCLAW,
                   "description": "Name your own price"},
        "author": {"@type": "Organization", "name": "Vantward Games", "parentOrganization": ORG_REF},
        "publisher": ORG_REF,
        "image": f"{SITE}/assets/og/hushclaw.jpg",
    }],
})

# Insights ----------------------------------------------------------------
PAGES.append({
    "path": "/insights/",
    "slug": "insights",
    "crumb": "Insights",
    "title": "Insights: AI Security, Data Leaks and a Firewall the User Owns",
    "desc": "Articles by Firdous Mahmood, founder of Vantward Solutions, on AI data leaks, prompt security and why "
            "people need an AI firewall that sits outside the model.",
    "acc": "#a5b4fc",
    "og": "insights.jpg",
    "alt": "Vee the robot reading by lamplight, with three article pages floating up",
    "eyebrow": "Insights · AI security",
    "h1": "Insights on AI security and data leaks",
    "lead": "Notes from our founder, Firdous Mahmood, on how secrets leak into AI tools, why alignment on the "
            "server is not the same as trust on the user's side, and what an AI firewall should be.",
    "ctas": [f'<a class="btn primary" href="{LI_FOUNDER_POST}" rel="noopener">Read the latest</a>',
             '<a class="btn" href="/eraseai-firewall/">See EraseAI Firewall</a>'],
    "body": section("Articles", f"""      <div class="posts">
        <a class="post" href="{LI_FOUNDER_POST}" rel="noopener"><small>LinkedIn · 1 October 2026</small><h3>Your team is already pasting secrets into AI chats. Here's the seatbelt we built.</h3><p>Smart people paste secrets into ChatGPT every day. Not carelessly, just fast: a config file with a cloud key, a customer export. Why that happens, and how EraseAI Firewall catches it at the Send button.</p></a>
        <a class="post" href="{LI_COMPANY_POST}" rel="noopener"><small>LinkedIn · 24 April 2026</small><h3>The Missing Layer in AI: A Firewall the User Owns</h3><p>Everyone is teaching their AI agents to behave. Nobody is giving the user a comfort zone. Why server-side alignment isn't the same thing as user-side trust, and why the firewall should be independent of the model it protects.</p></a>
        <a class="post" href="{MEDIUM_POST}" rel="noopener"><small>Medium</small><h3>The Three Layers Between a Citizen and an AI Model</h3><p>A long-form look at the layers of protection, governance and control that should sit between a person and the AI systems they use.</p></a>
      </div>"""),
    "schema": [{
        "@type": "ItemList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "item": {
                "@type": "Article", "headline": "Your team is already pasting secrets into AI chats. Here's the seatbelt we built.",
                "url": LI_FOUNDER_POST, "datePublished": "2026-10-01", "author": {"@id": f"{SITE}/#founder"}}},
            {"@type": "ListItem", "position": 2, "item": {
                "@type": "Article", "headline": "The Missing Layer in AI: A Firewall the User Owns",
                "url": LI_COMPANY_POST, "datePublished": "2026-04-24", "publisher": ORG_REF}},
            {"@type": "ListItem", "position": 3, "item": {
                "@type": "Article", "headline": "The Three Layers Between a Citizen and an AI Model",
                "url": MEDIUM_POST, "author": {"@id": f"{SITE}/#founder"}}},
        ],
    }],
})

# About -------------------------------------------------------------------
PAGES.append({
    "path": "/about/",
    "slug": "about",
    "crumb": "About",
    "title": "About Vantward Solutions | Software Studio in Singapore",
    "desc": "Vantward Solutions Pte. Ltd. is a Singapore software studio founded by Firdous Mahmood. We make EraseAI "
            "Firewall, Rubikation, CookHub and, under Vantward Games, Hushclaw.",
    "acc": "#02c8df",
    "og": "home.jpg",
    "alt": "Vee the robot in a room at dawn, the opening scene of vantward.com",
    "eyebrow": "About · Singapore",
    "h1": "About Vantward Solutions",
    "lead": "Vantward Solutions is a software studio in Singapore. We build products for the calm parts of a loud "
            "day: privacy for people who use AI, fair play for cubers, fair pay for home cooks, and a game you play "
            "with friends.",
    "ctas": ['<a class="btn primary" href="#contact">Contact us</a>', '<a class="btn" href="/">Watch Vee\'s day</a>'],
    "body": section("What we make", tiles([
        ('<a href="/eraseai-firewall/">EraseAI Firewall</a>', "A free Chrome extension and Android app that stops secrets and personal data reaching ChatGPT, Claude, Gemini and Replit."),
        ('<a href="/rubikation/">Rubikation</a>', "A live 1v1 cube arena with world and country ranks, on the web and Android."),
        ('<a href="/cookhub/">CookHub</a>', "A zero-commission marketplace for home cooking in your neighbourhood."),
        ('<a href="/hushclaw/">Hushclaw</a>', "A co-op dinosaur survival game from Vantward Games, in alpha for Windows and macOS."),
    ])) + section("Company", """      <div class="grid">
        <div class="tile"><h3>Legal name</h3><p>Vantward Solutions Pte. Ltd.<br>Registration No. 202606980C</p></div>
        <div class="tile"><h3>Based in</h3><p>68 Circular Road #02-01, Singapore 049422</p></div>
        <div class="tile"><h3>Founder</h3><p>Firdous Mahmood, founder. Writes on AI security and data leaks in <a href="/insights/">Insights</a>.</p></div>
        <div class="tile"><h3>Labels</h3><p>Vantward Solutions for software, Vantward Games for games.</p></div>
      </div>""") + section("Contact", """      <p>Partnering, investing, or building something we should know about? Write to us.</p>
      <div class="btns">
        <a class="btn primary" href="mailto:director@vantward.com?subject=Hello%20Vantward">director@vantward.com</a>
        <a class="btn" href="https://wa.me/6582430739" rel="noopener">WhatsApp +65 8243 0739</a>
        <a class="btn" href="https://www.linkedin.com/company/vantward-solutions-pte-ltd" rel="noopener">LinkedIn</a>
      </div>""", anchor="contact"),
    "schema": [{
        "@type": "AboutPage",
        "url": f"{SITE}/about/",
        "mainEntity": ORG_REF,
    }],
})


def main():
    for p in PAGES:
        out = ROOT / p["slug"] / "index.html"
        out.parent.mkdir(exist_ok=True)
        out.write_text(page(p))
        print("wrote", out.relative_to(ROOT))

    # The game was renamed; keep the old address working and point search engines at the new one.
    (ROOT / "tether-primal").mkdir(exist_ok=True)
    (ROOT / "tether-primal" / "index.html").write_text(f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Hushclaw (formerly TETHER: Primal) | Vantward</title>
  <link rel="canonical" href="{SITE}/hushclaw/">
  <meta name="robots" content="noindex,follow">
  <meta http-equiv="refresh" content="0; url=/hushclaw/">
</head>
<body>
  <p>TETHER: Primal is now called Hushclaw. <a href="/hushclaw/">Go to Hushclaw</a>.</p>
</body>
</html>
""")
    print("wrote tether-primal/index.html (redirect)")

    urls = [("/", "1.0")] + [(p["path"], "0.8") for p in PAGES]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, pr in urls:
        sm.append(f"  <url><loc>{SITE}{path}</loc><lastmod>{UPDATED}</lastmod><priority>{pr}</priority></url>")
    sm.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(sm) + "\n")
    print("wrote sitemap.xml")


INDEXNOW_KEY = "5bea7fa8e979cc425cba68f9329a0a2e"  # served from /5bea7fa8e979cc425cba68f9329a0a2e.txt


def ping_indexnow():
    """Tell IndexNow search engines (Bing, Yandex, Seznam, Naver) that every page changed."""
    import urllib.request
    urls = [f"{SITE}/"] + [f"{SITE}{p['path']}" for p in PAGES]
    body = json.dumps({"host": "vantward.com", "key": INDEXNOW_KEY,
                       "keyLocation": f"{SITE}/{INDEXNOW_KEY}.txt", "urlList": urls}).encode()
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body,
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(req, timeout=30) as r:
        print("IndexNow:", r.status, len(urls), "URLs")


if __name__ == "__main__":
    import sys
    if "--indexnow" in sys.argv:
        ping_indexnow()
        sys.exit()
    main()
