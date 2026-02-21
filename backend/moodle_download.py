"""
Moodle Auto-Downloader for HKBU

Usage:
    python moodle_download.py

1. Opens a browser window to HKBU Moodle
2. You log in manually (your password never touches this code)
3. Tell the assistant you've logged in -- it creates a trigger file
4. Script auto-discovers courses and downloads all materials
"""

import os
import re
import sys
import time
import logging
from pathlib import Path
from urllib.parse import urlparse, unquote

from playwright.sync_api import sync_playwright, Page, BrowserContext

MOODLE_URL = "https://buelearning.hkbu.edu.hk"
MATERIALS_DIR = Path(__file__).parent / "materials"
DATA_DIR = Path(__file__).parent / "data"
LOG_FILE = DATA_DIR / "moodle_download.log"
TRIGGER_FILE = DATA_DIR / "login_ready"

DATA_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.FileHandler(str(LOG_FILE), mode="w"),
        logging.StreamHandler(sys.stdout),
    ],
    force=True,
)
log = logging.getLogger("moodle")

COURSE_FOLDER_MAP = {
    "comp7045": "nlp",
    "nlp": "nlp",
    "natural language": "nlp",
    "language model": "nlp",
    "comp7055": "cvpr",
    "cvpr": "cvpr",
    "computer vision": "cvpr",
    "pattern recognition": "cvpr",
    "it forum": "it-forum",
    "comp7530": "it-forum",
}

DOWNLOADABLE_EXTENSIONS = {
    ".pdf", ".pptx", ".ppt", ".docx", ".doc", ".xlsx", ".xls",
    ".zip", ".rar", ".7z", ".tar", ".gz",
    ".py", ".ipynb", ".txt", ".csv",
    ".mp4", ".mp3", ".png", ".jpg", ".jpeg",
}


def flush():
    sys.stdout.flush()
    sys.stderr.flush()
    for h in log.handlers:
        h.flush()


def match_course_folder(course_name: str) -> str:
    name_lower = course_name.lower()
    for keyword, folder in COURSE_FOLDER_MAP.items():
        if keyword in name_lower:
            return folder
    safe = re.sub(r"[^a-z0-9]+", "-", name_lower).strip("-")[:50]
    return safe


def wait_for_login(timeout_seconds=300):
    if TRIGGER_FILE.exists():
        TRIGGER_FILE.unlink()
    log.info("Waiting for login signal...")
    log.info(f"  Trigger file: {TRIGGER_FILE}")
    flush()
    start = time.time()
    while time.time() - start < timeout_seconds:
        if TRIGGER_FILE.exists():
            TRIGGER_FILE.unlink()
            return True
        time.sleep(1)
    return False


def discover_courses(page: Page) -> list[dict]:
    page.goto(f"{MOODLE_URL}/my/", wait_until="networkidle", timeout=30000)
    courses = []
    seen_ids = set()

    for link in page.query_selector_all('a[href*="course/view.php"]'):
        href = link.get_attribute("href") or ""
        text = (link.inner_text() or "").strip()
        if not text or "course/view.php" not in href:
            continue
        match = re.search(r"id=(\d+)", href)
        if not match:
            continue
        course_id = match.group(1)
        if course_id in seen_ids:
            continue
        seen_ids.add(course_id)
        courses.append({
            "id": course_id,
            "name": text,
            "url": href if href.startswith("http") else f"{MOODLE_URL}/course/view.php?id={course_id}",
            "folder": match_course_folder(text),
        })

    return courses


def try_download_via_expect(page: Page, url: str, folder: Path) -> str | None:
    """Try Playwright expect_download approach."""
    try:
        with page.expect_download(timeout=10000) as dl_info:
            page.goto(url, timeout=10000)
        download = dl_info.value
        filename = download.suggested_filename
        if filename:
            target = folder / filename
            if target.exists():
                log.info(f"    Skip (exists): {filename}")
                flush()
                return filename
            download.save_as(str(target))
            log.info(f"    Downloaded: {filename}")
            flush()
            return filename
    except Exception:
        pass
    return None


def try_download_via_request(context: BrowserContext, url: str, folder: Path) -> str | None:
    """Use Playwright API request to directly fetch the file."""
    try:
        response = context.request.get(url, timeout=30000)
        if response.status != 200:
            return None

        content_disp = response.headers.get("content-disposition", "")
        content_type = response.headers.get("content-type", "")

        if "text/html" in content_type and not content_disp:
            return None

        filename = None
        if "filename=" in content_disp:
            match = re.search(r'filename[*]?=["\']?(?:UTF-8\'\')?([^"\';\r\n]+)', content_disp)
            if match:
                filename = unquote(match.group(1).strip())

        if not filename:
            parsed = urlparse(url)
            filename = unquote(parsed.path.split("/")[-1])

        if not filename or filename == "/" or "." not in filename:
            return None

        target = folder / filename
        if target.exists():
            log.info(f"    Skip (exists): {filename}")
            flush()
            return filename

        target.write_bytes(response.body())
        log.info(f"    Downloaded: {filename} ({len(response.body()) // 1024}KB)")
        flush()
        return filename
    except Exception as e:
        log.info(f"    Request failed: {e}")
        flush()
        return None


def download_course_materials(page: Page, context: BrowserContext, course: dict, download_dir: Path) -> int:
    folder = download_dir / course["folder"]
    folder.mkdir(parents=True, exist_ok=True)

    log.info(f"Scanning: {course['name']}")
    flush()
    page.goto(course["url"], wait_until="networkidle", timeout=30000)

    resource_urls = []
    seen_urls = set()

    for link in page.query_selector_all('a[href*="/mod/resource/"], a[href*="/mod/folder/"], a[href*="/pluginfile.php/"]'):
        href = link.get_attribute("href") or ""
        if href and href not in seen_urls:
            seen_urls.add(href)
            text = (link.inner_text() or "").strip()
            resource_urls.append({"url": href, "title": text, "type": "moodle"})

    for link in page.query_selector_all("a[href]"):
        href = link.get_attribute("href") or ""
        if href in seen_urls:
            continue
        parsed = urlparse(href)
        if any(parsed.path.lower().endswith(ext) for ext in DOWNLOADABLE_EXTENSIONS):
            seen_urls.add(href)
            text = (link.inner_text() or "").strip()
            resource_urls.append({"url": href, "title": text, "type": "direct"})

    if not resource_urls:
        log.info("  No downloadable resources found.")
        flush()
        return 0

    log.info(f"  Found {len(resource_urls)} resource links")
    flush()

    downloaded = 0
    for i, res in enumerate(resource_urls, 1):
        url = res["url"]
        title = res["title"] or url.split("/")[-1]
        log.info(f"  [{i}/{len(resource_urls)}] {title[:60]}")
        flush()

        try:
            # Handle folder links: navigate and collect inner files
            if "/mod/folder/" in url:
                page.goto(url, wait_until="networkidle", timeout=15000)
                for file_link in page.query_selector_all('a[href*="pluginfile.php"]'):
                    file_href = file_link.get_attribute("href") or ""
                    if file_href:
                        result = try_download_via_request(context, file_href, folder)
                        if result:
                            downloaded += 1
                continue

            # For resource/pluginfile links, try request-based download first
            result = try_download_via_request(context, url, folder)
            if result:
                downloaded += 1
                continue

            # For /mod/resource/ links that redirect, try navigating
            if "/mod/resource/" in url:
                result = try_download_via_expect(page, url, folder)
                if result:
                    downloaded += 1
                    continue

            log.info(f"    Skipped (not downloadable)")
            flush()

        except Exception as e:
            log.info(f"    Error: {e}")
            flush()

    return downloaded


def main():
    MATERIALS_DIR.mkdir(exist_ok=True)

    log.info("=" * 50)
    log.info("HKBU Moodle Auto-Downloader")
    log.info("=" * 50)
    log.info("A browser will open to HKBU Moodle.")
    log.info("Log in, then tell the assistant you're done.")
    flush()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, channel="chromium")
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        page.goto(f"{MOODLE_URL}/login/index.php", timeout=30000)
        log.info("Browser opened. Please log in now...")
        flush()

        if not wait_for_login(timeout_seconds=300):
            log.info("Timed out (5 min). Exiting.")
            browser.close()
            return

        log.info("Signal received! Proceeding...")
        flush()
        page.goto(f"{MOODLE_URL}/my/", wait_until="networkidle", timeout=30000)

        log.info("Discovering courses...")
        flush()
        courses = discover_courses(page)

        if not courses:
            log.info("No courses found.")
            browser.close()
            return

        log.info(f"Found {len(courses)} course(s):")
        for i, c in enumerate(courses, 1):
            log.info(f"  {i}. {c['name']}  ->  materials/{c['folder']}/")
        flush()

        log.info("Starting downloads...")
        flush()
        total = 0
        for course in courses:
            count = download_course_materials(page, context, course, MATERIALS_DIR)
            total += count
            log.info(f"  => {count} files from this course")
            flush()

        browser.close()

    log.info("=" * 50)
    log.info(f"Done! Downloaded {total} file(s)")
    log.info(f"Files saved to: {MATERIALS_DIR}")
    log.info("=" * 50)
    flush()


if __name__ == "__main__":
    main()
