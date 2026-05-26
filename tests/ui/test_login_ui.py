import pytest
from playwright.sync_api import expect

BASE_URL = "https://practicetestautomation.com/practice-test-login"

def test_successful_login(page):
    """Test logging in with correct credentials"""
    page.goto(BASE_URL)

    # Find the username and password fields and fill them
    page.fill("#wrong-username", "student")
    page.fill("#password", "Password123")

    # Click the login button
    page.click("#submit")

    # Assert we got redirected and see a success message
    expect(page.locator(".post-title")).to_have_text("Logged In Successfully")
    print("✓ Login successful!")


def test_failed_login(page):
    """Test that wrong credentials show an error"""

    page.goto(BASE_URL)

    page.fill("#username", "wronguser")
    page.fill("#password", "wrongpassword")
    page.click("#submit")

    # We should see an error message
    expect(page.locator("#error")).to_be_visible()
    print("✓ Error message shown correctly")


def test_logout(page):
    """Test the full login -> logout flow"""

    page.goto(BASE_URL)
    page.fill("#username", "student")
    page.fill("#password", "Password123")
    page.click("#submit")

    #now log out
    page.click(".wp-block-button__link")

    # We should be back at the login page
    expect(page.locator("#username")).to_be_visible()
    print("✓ Logout successful!")