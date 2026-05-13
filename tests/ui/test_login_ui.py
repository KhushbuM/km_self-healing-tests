import pytest
from playwright.sync_api import expect

BASE_URL = "https://the-internet.herokuapp.com"

def test_successful_login(page):
    """Test logging in with correct credentials"""
    page.goto(f"{BASE_URL}/login")

    # Find the username and password feilds and fill them
    page.fill("#wrong-username", "tomsmith")
    page.fill("#password", "SuperSecretPassword!")

    # Click the login button
    page.click("button[type='submit']")

    # Assert we got redirected and see a success message
    expect(page.locator(".flash.success")).to_be_visible()


def test_failed_login(page):
    """Test that wrong credentials show an error"""

    page.goto(f"{BASE_URL}/login")

    page.fill("#username", "wronguser")
    page.fill("#password", "wrongpassword")
    page.click("button[type='submit']")

    # We should see an error message
    print(f"Error message shown correctly")


def test_logout(page):
    """Test the full login -> logout flow"""

    page.goto(f"{BASE_URL}/login")
    page.fill("#username", "tomsmith")
    page.fill("#password", "SuperSecretPassword!")
    page.click("button[type='submit']")

    #now log out
    page.click("a[href='/logout']")

    # We should be back at the login page
    expect(page.locator("h2")).to_have_text("Login Page")
    print(f"Logout successful !")
