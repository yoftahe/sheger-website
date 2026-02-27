#!/usr/bin/env python3
"""
download-images.py — Download vehicle, team, and showcase images from menamotors.com
and save them into the images/ directory for the Sheger International website.

Usage:
    python3 scripts/download-images.py

Requirements:
    pip install requests beautifulsoup4

Directories created:
    images/vehicles/     — vehicle inventory photos
    images/team/         — team member portraits
    images/services/     — service section imagery
    images/              — general (showroom, about page)

Run this script from the repository root.
"""

import os
import re
import sys
import time
import urllib.parse
from pathlib import Path

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Missing dependencies. Install them with:")
    print("    pip install requests beautifulsoup4")
    sys.exit(1)

BASE_URL = "https://menamotors.com"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": BASE_URL,
}

# Images directory relative to this script's parent (repo root)
REPO_ROOT = Path(__file__).resolve().parent.parent
IMAGES_DIR = REPO_ROOT / "images"

# ─────────────────────────────────────────────────────────
# Target image destinations on the Sheger website
# ─────────────────────────────────────────────────────────
VEHICLE_TARGETS = {
    "toyota-land-cruiser-300.jpg": ["land cruiser 300", "landcruiser 300", "lc300"],
    "toyota-land-cruiser-76.jpg":  ["land cruiser 76", "lc76", "land cruiser hardtop"],
    "toyota-hilux-double-cab.jpg": ["hilux", "hi-lux", "hilux double"],
    "nissan-patrol-v8.jpg":        ["patrol", "nissan patrol", "patrol v8"],
    "toyota-land-cruiser-prado.jpg": ["prado", "land cruiser prado", "lc prado"],
    "mitsubishi-l200-triton.jpg":  ["l200", "triton", "mitsubishi l200"],
    "toyota-hiace-high-roof.jpg":  ["hiace", "hi-ace", "hiace high"],
    "toyota-camry-grande.jpg":     ["camry", "toyota camry"],
    "lexus-lx-600.jpg":            ["lexus lx", "lx 600", "lx600"],
    "land-rover-defender-110.jpg": ["defender", "land rover defender"],
    "isuzu-dmax.jpg":              ["d-max", "dmax", "isuzu d-max"],
    "mercedes-e-class-300.jpg":    ["e-class", "e class", "mercedes e"],
}

TEAM_TARGETS = {
    "yoftahe-fisseha.jpg":  ["yoftahe", "fisseha"],
    "kal-solomon.jpg":      ["kal", "solomon"],
    "nebiyat-dereje.jpg":   ["nebiyat", "dereje"],
    "tesfahun-hailu.jpg":   ["tesfahun", "hailu"],
}


def get_page(url: str) -> BeautifulSoup | None:
    """Fetch a page and return a BeautifulSoup object."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        return BeautifulSoup(resp.text, "html.parser")
    except requests.RequestException as e:
        print(f"  ✗ Failed to fetch {url}: {e}")
        return None


def download_image(url: str, dest: Path) -> bool:
    """Download a single image to dest. Returns True on success."""
    if dest.exists():
        print(f"  → Already exists: {dest.name}")
        return True
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30, stream=True)
        resp.raise_for_status()
        dest.parent.mkdir(parents=True, exist_ok=True)
        with open(dest, "wb") as f:
            for chunk in resp.iter_content(8192):
                f.write(chunk)
        print(f"  ✓ Downloaded: {dest.name}")
        return True
    except requests.RequestException as e:
        print(f"  ✗ Download failed ({dest.name}): {e}")
        return False


def absolute_url(href: str) -> str:
    """Convert a relative URL to absolute."""
    if href.startswith("http"):
        return href
    return urllib.parse.urljoin(BASE_URL, href)


def scrape_vehicle_images():
    """Scrape vehicle inventory pages and download matching images."""
    print("\n── Scraping vehicle inventory ──────────────────────────────")
    inventory_urls = [
        f"{BASE_URL}/cars/category-2-PASSENGER+VEHICLES",
        f"{BASE_URL}/cars/category-14-BUSSES",
        f"{BASE_URL}/cars",
        f"{BASE_URL}/inventory",
    ]

    # Collect all vehicle page links
    vehicle_pages: list[str] = []
    for url in inventory_urls:
        soup = get_page(url)
        if not soup:
            continue
        # Look for vehicle detail links
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if re.search(r"/cars?/\d+|/vehicle/|/inventory/\d+", href):
                vehicle_pages.append(absolute_url(href))
        # Also grab all images directly from inventory page
        _download_page_images(soup, url, IMAGES_DIR / "vehicles", VEHICLE_TARGETS)
        time.sleep(0.5)

    # Visit each vehicle detail page
    seen = set()
    for page_url in vehicle_pages:
        if page_url in seen:
            continue
        seen.add(page_url)
        soup = get_page(page_url)
        if not soup:
            continue
        _download_page_images(soup, page_url, IMAGES_DIR / "vehicles", VEHICLE_TARGETS)
        time.sleep(0.3)


def scrape_team_images():
    """Scrape the team page and download portrait images."""
    print("\n── Scraping team photos ─────────────────────────────────────")
    team_urls = [
        f"{BASE_URL}/team",
        f"{BASE_URL}/about",
        f"{BASE_URL}/about-us",
    ]
    for url in team_urls:
        soup = get_page(url)
        if not soup:
            continue
        _download_page_images(soup, url, IMAGES_DIR / "team", TEAM_TARGETS)
        time.sleep(0.5)


def scrape_general_images():
    """Grab hero/showroom images for the homepage and about page."""
    print("\n── Scraping general/hero images ─────────────────────────────")
    homepage = get_page(BASE_URL)
    if not homepage:
        return

    # Grab the first large image on the homepage as the showroom image
    for img in homepage.find_all("img"):
        src = img.get("src") or img.get("data-src") or ""
        if not src:
            continue
        url = absolute_url(src)
        # Prefer large hero/banner images
        alt = (img.get("alt") or "").lower()
        if any(k in alt for k in ["showroom", "hero", "banner", "fleet", "car", "vehicle"]):
            dest = IMAGES_DIR / "showroom.jpg"
            if download_image(url, dest):
                # Also use as about.jpg if not already present
                about_dest = IMAGES_DIR / "about.jpg"
                if not about_dest.exists():
                    import shutil
                    shutil.copy(dest, about_dest)
                    print(f"  ✓ Copied showroom.jpg → about.jpg")
                break


def _download_page_images(
    soup: BeautifulSoup,
    page_url: str,
    dest_dir: Path,
    targets: dict[str, list[str]],
):
    """Find images on a parsed page and save them to dest_dir if they match targets."""
    # Collect all img src values
    imgs: list[tuple[str, str]] = []  # (src, alt)
    for img in soup.find_all("img"):
        src = img.get("src") or img.get("data-src") or img.get("data-lazy-src") or ""
        alt = (img.get("alt") or "").lower()
        if src and not src.startswith("data:"):
            imgs.append((absolute_url(src), alt))

    # Match each target filename to an image
    for filename, keywords in targets.items():
        dest = dest_dir / filename
        if dest.exists():
            continue
        for src, alt in imgs:
            src_lower = src.lower()
            if any(kw in alt or kw in src_lower for kw in keywords):
                if download_image(src, dest):
                    break


def main():
    print("Sheger International — Image Download Script")
    print(f"Repository root : {REPO_ROOT}")
    print(f"Images directory: {IMAGES_DIR}\n")

    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    (IMAGES_DIR / "vehicles").mkdir(exist_ok=True)
    (IMAGES_DIR / "team").mkdir(exist_ok=True)
    (IMAGES_DIR / "services").mkdir(exist_ok=True)

    scrape_general_images()
    scrape_vehicle_images()
    scrape_team_images()

    print("\n── Summary ──────────────────────────────────────────────────")
    for subdir in ["", "vehicles", "team", "services"]:
        d = IMAGES_DIR / subdir if subdir else IMAGES_DIR
        files = [f for f in d.iterdir() if f.is_file() and not f.name.startswith(".")]
        print(f"  {d.relative_to(REPO_ROOT)}/  → {len(files)} image(s)")

    print("\nDone. Refresh your browser to see the images on the website.")
    print("If some images are missing, check menamotors.com manually and")
    print("save them to the appropriate images/ subdirectory.")


if __name__ == "__main__":
    main()
