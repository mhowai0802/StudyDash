"""
Moodle Auto-Downloader for HKBU

Usage:
    python moodle_download.py

1. Opens a browser window to HKBU Moodle
2. You log in manually (your password never touches this code)
3. Press Enter in the terminal once logged in
4. The script auto-discovers your courses and downloads all materials
"""

import os
import re
import sys
from pathlib import Path
from urllib.parse import urlparse, unquote

from playwright.sync_api import sync_playwright, Page

MOODLE_URL = "https://buelearning.hkbu.edu.hk"
MATERIALS_DIR = Path(__file__).parent / "materials"

COURSE_FOLDER_MAP = {
    "comp7045": "nlp",
    "nlp": "nlp",
    "natural language": "nlp",
    "language model": "nlp",
    "cvpr": "cvpr",
    "computer vision": "cvpr",
    "pattern recognition": "cvpr",
    "it forum": "it-forum",
    "itforum": "it-forum",
}

DOWNLOADABLE_EXTENSIONS = {
    ".pdf", ".pptx", ".ppt", ".docx", ".doc", ".xlsx", ".xls",
    ".zip", ".rar", ".7z", ".tar", ".gz",
    ".py", ".ipynb", ".txt", ".csv", ".json",
    ".mp4", ".mp3", ".png", ".jpg", ".jpeg",
}


def match_course_folder(course_name: str) -> str:
    """Map a Moodle course name to a local folder name."""
    name_lower = course_name.lower()
    for keyword, folder in COURSE_FOLDER_MAP.items():
        if keyword in name_lower:
            return folder
    safe = re.sub(r"[^a-z0-9]+", "-", name_lower).strip("-")[:50]
    return safe


def discover_courses(page: Page) -> list[dict]:
    """Find all enrolled courses from the Moodle dashboard."""
    page.goto(f"{MOODLE_URL}/my/", wait_until="networkidle")

    courses = []
    course_links = page.query_selector_all('a[href*="course/view.php"]')
    seen_ids = set()

    for link in course_links:
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


def download_course_materials(page: Page, course: dict, download_dir: Path):
    """Download all materials from a single course page."""
    folder = download_dir / course["folder"]
    folder.mkdir(parents=True, exist_ok=True)

    print(f"\n  Scanning: {course['name']}")
    page.goto(course["url"], wait_until="networkidle")

    resource_links = []

    # Find resource links (files directly linked)
    for link in page.query_selector_all('a[href*="/mod/resource/"], a[href*="/mod/folder/"], a[href*="/pluginfile.php/"]'):
        href = link.get_attribute("href") or ""
        text = (link.inner_text() or "").strip()
        if href and href not in [r["url"] for r in resource_links]:
            resource_links.append({"url": href, "title": text})

    # Also find any direct file links on the page
    for link in page.query_selector_all("a[href]"):
        href = link.get_attribute("href") or ""
        parsed = urlparse(href)
        path_lower = parsed.path.lower()
        if any(path_lower.endswith(ext) for ext in DOWNLOADABLE_EXTENSIONS):
            text = (link.inner_text() or "").strip()
            if href not in [r["url"] for r in resource_links]:
                resource_links.append({"url": href, "title": text})

    if not resource_links:
        print(f"    No downloadable resources found.")
        return 0

    downloaded = 0
    for res in resource_links:
        try:
            downloaded += download_single_resource(page, res, folder)
        except Exception as e:
            print(f"    Error downloading {res['title']}: {e}")

    return downloaded


def download_single_resource(page: Page, resource: dict, folder: Path) -> int:
    """Download a single resource, handling Moodle redirects."""
    url = resource["url"]

    # For /mod/resource/ links, navigate to get the actual file
    if "/mod/resource/" in url:
        try:
            with page.expect_download(timeout=15000) as download_info:
                page.goto(url)
            download = download_info.value
            filename = download.suggested_filename
            target = folder / filename

            if target.exists():
                print(f"    Skip (exists): {filename}")
                return 0

            download.save_as(str(target))
            print(f"    Downloaded: {filename}")
            return 1
        except Exception:
            pass

    # For /mod/folder/ links, navigate and find files within
    if "/mod/folder/" in url:
        page.goto(url, wait_until="networkidle")
        inner_count = 0
        for file_link in page.query_selector_all('a[href*="pluginfile.php"]'):
            file_href = file_link.get_attribute("href") or ""
            file_text = (file_link.inner_text() or "").strip()
            if file_href:
                inner_count += download_single_resource(
                    page, {"url": file_href, "title": file_text}, folder
                )
        return inner_count

    # For direct file links (pluginfile.php or extension-matched)
    try:
        with page.expect_download(timeout=15000) as download_info:
            page.evaluate(f'() => {{ window.location.href = "{url}"; }}')
        download = download_info.value
        filename = download.suggested_filename

        if not filename:
            parsed = urlparse(url)
            filename = unquote(parsed.path.split("/")[-1]) or "unknown_file"

        target = folder / filename
        if target.exists():
            print(f"    Skip (exists): {filename}")
            return 0

        download.save_as(str(target))
        print(f"    Downloaded: {filename}")
        return 1
    except Exception:
        # Not a downloadable link, skip silently
        return 0


def main():
    MATERIALS_DIR.mkdir(exist_ok=True)

    print("=" * 60)
    print("  HKBU Moodle Auto-Downloader")
    print("=" * 60)
    print()
    print("A browser window will open to HKBU Moodle.")
    print("Please log in with your credentials in the browser.")
    print()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        page.goto(f"{MOODLE_URL}/login/index.php")
        print("Browser opened. Please log in now.")
        print()
        input(">>> Press ENTER here after you have logged in successfully... ")

        # Verify login
        page.goto(f"{MOODLE_URL}/my/", wait_until="networkidle")
        if "login" in page.url.lower():
            print("Error: Still on login page. Please try again.")
            browser.close()
            return

        print("\nLogin confirmed! Discovering courses...")
        courses = discover_courses(page)

        if not courses:
            print("No courses found. Check if you're enrolled in any courses.")
            browser.close()
            return

        print(f"\nFound {len(courses)} course(s):")
        for i, c in enumerate(courses, 1):
            print(f"  {i}. {c['name']}  ->  materials/{c['folder']}/")

        print("\nStarting downloads...")
        total = 0
        for course in courses:
            count = download_course_materials(page, course, MATERIALS_DIR)
            total += count

        browser.close()

    print()
    print("=" * 60)
    print(f"  Done! Downloaded {total} file(s)")
    print(f"  Files saved to: {MATERIALS_DIR}")
    print()
    print("  Next: In StudyDash, use 'Scan & Import' to add")
    print("  these files to your study tracker.")
    print("=" * 60)


if __name__ == "__main__":
    main()
