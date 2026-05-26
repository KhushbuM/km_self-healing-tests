import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True) # headless false so that you can see the browser
        yield browser
        browser.close()



@pytest.fixture
def page(browser):
    # Create fresh page for each test
    context = browser.new_context()
    page = context.new_page() # 1. SETUP - runs first
    yield page                # 2. PAUSE - hands 'page' to your test, waits here
    page.close()              # 3. TEARDOWN - runs after test finishes
