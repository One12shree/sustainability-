"""Download and localize the pages linked from The Sustainabilist's main menu."""

from concurrent.futures import ThreadPoolExecutor
from html import escape, unescape
from pathlib import Path
import hashlib
import json
import re
from urllib.parse import urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "static" / "assets"
LIB = ROOT / "src" / "lib"
ROUTES = ROOT / "src" / "routes"
PAGES = {
    "about-us": "https://thesustainabilist.ae/about-us/",
    "our-editor-in-chief": "https://thesustainabilist.ae/our-editor-in-chief/",
    "green-economists-note": "https://thesustainabilist.ae/green-economists-note/",
    "media-kit": "https://thesustainabilist.ae/media-kit/",
    "editorial-calendar": "https://thesustainabilist.ae/editorial-calendar/",
    "editorial-calendar-2019": "https://thesustainabilist.ae/editorial-calendar-2019/",
    "editorial-calendar-2020": "https://thesustainabilist.ae/editorial-calendar-2020/",
    "trending-articles": "https://thesustainabilist.ae/trending-articles/",
    "themes": "https://thesustainabilist.ae/themes/",
    "partners": "https://thesustainabilist.ae/partners/",
    "green-jobs": "https://thesustainabilist.ae/green-jobs/",
    "advertise-with-us": "https://thesustainabilist.ae/advertise-with-us/",
    "contact-us": "https://thesustainabilist.ae/contact-us/",
}
LOCAL_LINKS = {url: f"/{slug}/" for slug, url in PAGES.items()}
LOCAL_LINKS.update({"https://thesustainabilist.ae/": "/", "https://thesustainabilist.ae/ramadan/": "/ramadan/", "https://thesustainabilist.ae/contribute/": "/contribute/", "https://thesustainabilist.ae/our-issues/": "/our-issues/"})


def get(url):
    return urlopen(Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=25).read()


def asset_name(url):
    base = Path(urlparse(url).path).name or "asset"
    return f"menu-{hashlib.sha256(url.encode()).hexdigest()[:12]}-{base}"


def localize_asset(url):
    if not url.startswith("http"):
        return url
    filename = asset_name(url)
    destination = ASSETS / filename
    if not destination.exists():
        try:
            destination.write_bytes(get(url))
        except Exception:
            return url
    return f"/assets/{filename}"


def extract_urls(html):
    image_urls = re.findall(r'<img[^>]*?src=["\']([^"\']+)', html, flags=re.I)
    style_urls = [match for tag in re.findall(r'<link[^>]*>', html, flags=re.I) if "stylesheet" in tag.lower() for match in re.findall(r'href=["\']([^"\']+)', tag, flags=re.I)]
    return {unescape(url) for url in image_urls + style_urls if url.startswith("http")}


def clean_body(html, replacements):
    body = re.search(r"<body[^>]*>(.*)</body>", html, flags=re.I | re.S).group(1)
    body = re.sub(r"<script\b[^>]*>.*?</script>|<link\b[^>]*>", "", body, flags=re.I | re.S)
    body = re.sub(r"\s+on\w+=(?:\"[^\"]*\"|'[^']*')", "", body)
    body = re.sub(r"<iframe\b[^>]*>.*?</iframe>", "", body, flags=re.I | re.S)
    body = re.sub(r"<textarea([^>]*)>.*?</textarea>", r"<textarea\1></textarea>", body, flags=re.I | re.S)
    for source, local in replacements.items():
        body = body.replace(source, local).replace(escape(source, quote=False), local)
    for source, local in LOCAL_LINKS.items():
        body = body.replace(source, local)
    return body


def main():
    ASSETS.mkdir(parents=True, exist_ok=True)
    html_by_slug = {slug: get(url).decode("utf-8", errors="replace") for slug, url in PAGES.items()}
    urls = set().union(*(extract_urls(html) for html in html_by_slug.values()))
    with ThreadPoolExecutor(max_workers=8) as pool:
        replacements = dict(zip(urls, pool.map(localize_asset, urls)))
    for slug, html in html_by_slug.items():
        styles = []
        for tag in re.findall(r"<link[^>]*>", html, flags=re.I):
            if "stylesheet" in tag.lower():
                match = re.search(r'href=["\']([^"\']+)', tag, flags=re.I)
                if match:
                    style = replacements.get(unescape(match.group(1)), unescape(match.group(1)))
                    if style not in styles:
                        styles.append(style)
        (LIB / f"{slug}.json").write_text(json.dumps({"styles": styles, "body": clean_body(html, replacements)}, ensure_ascii=False), encoding="utf-8")
        route = ROUTES / slug
        route.mkdir(exist_ok=True)
        title = slug.replace("-", " ").title()
        (route / "+page.svelte").write_text(f'<script>\n  import Replica from "$lib/Replica.svelte";\n  import homepage from "$lib/{slug}.json";\n</script>\n\n<Replica {{homepage}} title="{title} | The Sustainabilist" frontendOnly />\n', encoding="utf-8")


if __name__ == "__main__":
    main()
