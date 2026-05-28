import pytest
from playwright.sync_api import expect

BASE_URL = "https://practicetestautomation.com/practice-test-login"


def wait_for_page_ready(page, max_retries=3):
    """Retry loading the page if we get rate-limited (429)."""
    for attempt in range(max_retries):
        page.goto(BASE_URL)
        # Check if we got the real page or a 429 error
        if page.locator("#username").count() > 0:
            return
        # We likely got rate-limited; wait and retry
        page.wait_for_timeout(5000 * (attempt + 1))
    # One final attempt
    page.goto(BASE_URL)
    expect(page.locator("#username")).to_be_visible(timeout=15000)


def test_successful_login(page):
    """Test logging in with correct credentials"""
    wait_for_page_ready(page)

    # Find the username and password fields and fill them
    page.fill("#wron-username", "student")
    page.fill("#password", "Password123")

    # Click the login button
    page.click("#submit")

    # Assert we got redirected and see a success message
    expect(page.locator(".post-title")).to_have_text("Logged In Successfully")
    print("✓ Login successful!")


def test_failed_login(page):
    """Test that wrong credentials show an error"""
    wait_for_page_ready(page)

    page.fill("#username", "wronguser")
    page.fill("#password", "wrongpassword")
    page.click("#submit")

    # We should see an error message
    expect(page.locator("#error")).to_be_visible()
    print("✓ Error message shown correctly")


def test_logout(page):
    """Test the full login -> logout flow"""
    wait_for_page_ready(page)

    page.fill("#username", "student")
    page.fill("#password", "Password123")
    page.click("#submit")

    # now log out
    page.click(".wp-block-button__link")

    # We should be back at the login page
    expect(page.locator("#username")).to_be_visible()
    print("✓ Logout successful!")