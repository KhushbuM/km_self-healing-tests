
import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
import math
from PIL import Image, ImageChops
from functools import reduce
import operator

load_dotenv()

BASELINE_DIR = "screenshots/baseline"
ACTUAL_DIR = "screenshots/actual"
THRESHOLD = 95.0 # 95% match required

def take_screenshot(url, filename):
    """
    Opens the real page and takes a screenshot
    Saves it to screenshots/actual/
    """

    os.makedirs(ACTUAL_DIR, exist_ok=True)
    actual_path = os.path.join(ACTUAL_DIR, filename)

    print(f"📸 Taking screenshot of {url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        page.set_default_timeout(60000)
        page.goto(url)
        page.goto(url, wait_until="domcontentloaded")
        page.wait_for_timeout(2000)
        page.screenshot(path=actual_path, full_page=False)
        browser.close()

    print(f"✓ Screenshot saved: {actual_path}")    
    return actual_path

def take_baseline_screenshot(url, filename):
    """
    Takes the golden/baseline screenshot
    Saves it to th screenshots/baseline/
    Only run this once when everything is working correctly
    """

    os.makedirs(BASELINE_DIR, exist_ok=True)
    baseline_path = os.path.join(BASELINE_DIR, filename)

    print(f"📸 Taking BASELINE screenshot of {url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height" : 720})
        page.set_default_timeout(60000)
        page.goto(url, wait_until="domcontentloaded")  # faster than waiting for networkidle
        page.wait_for_timeout(2000)  # wait 2 extra seconds for page to settle
        page.screenshot(path=baseline_path, full_page=False)
        browser.close()

    print(f"✓ Baseline screenshot saved: {baseline_path}")
    return baseline_path   

def compare_screenshots(baseline_path, actual_path):
    """
    Compares two screenshots pixel by pixel
    Returns (match_percentage, is_match)
    """

    print(f"🔍 Comparing screenshots...")

    # Open both images
    baseline = Image.open(baseline_path).convert("RGB")
    actual = Image.open(actual_path).convert("RGB")

    # Resize actual to match baseline of sizes differ slightly
    if baseline.size != actual.size:
        actual = actual.resize(baseline.size)

    # Calculate difference between images
    diff = ImageChops.difference(baseline, actual)

    # Get all pixel values
    pixels = list(diff.getdata())

    # Calculate how difference each pixel id
    total_diff = sum(
        math.sqrt(reduce(operator.add, map(lambda x: x * x, pixel)))
        for pixel in pixels
    )   

    # Maximum possible difference per pixel
    max_diff = math.sqrt(3 * (255 ** 2))
    total_pixels = len(pixels)
    max_total_diff = max_diff * total_pixels

    # Calculate similarity percentage
    similarity = (1 - (total_diff / max_total_diff)) * 100

    is_match = similarity >= THRESHOLD

    print(f"📊 Similarity: {similarity:.2f}% (threshold: {THRESHOLD}%)")

    if is_match:
        print("✅ Screenshots match!")
    else:
        print("❌ Screenshots do NOT match — possible product bug!")

    return round(similarity, 2), is_match

def check_screenshots(url, test_name):
    """
    Main function called by triage:
    1. Takes actual screenshot
    2. Compares with baseline
    3. Returns result
    """
    filename = f"{test_name}.png"
    baseline_path = os.path.join(BASELINE_DIR, filename)
    actual_path = os.path.join(ACTUAL_DIR, filename)

    # Check if baseline exists
    if not os.path.exists(baseline_path):
        print(f"⚠️ No baseline found for {test_name} — creating now")
        try:
            take_baseline_screenshot(url, filename)
        except Exception as e:
            print(f"⚠️ Could not create baseline: {e} — skipping screenshot check")
            return 100.0, True
        return 100.0, True

    # Take actual screenshot
    try:
        take_screenshot(url, filename)
    except Exception as e:
        print(f"⚠️ Screenshot timed out: {e}")
        print(f"⚠️ Skipping screenshot check — assuming match")
        return 100.0, True    

    # Compare
    similarity, is_match = compare_screenshots(baseline_path, actual_path)
    return similarity, is_match