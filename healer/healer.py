import os
import anthropic
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# Load the API key from .env file
load_dotenv()

# Create the Anthropic client - this is what talks to Claude
client = anthropic.Anthropic(api_keys=os.getenv("ANTHROPIC_API_KEY"))

def get_page_html(url):
    """
    Opens the actual webpage using Playwright
    and returns its real HTML content
    """
    print(f"🌐 Opening page to inspect real HTML: {url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url)

        # Wait for the page to fully load
        page.wait_for_load_state("networkidle")

        # Grab the actual HTML of the page
        html = page.content()

        browser.close()
        return html


def heal_test(test_file_path, error_message, page_url):
    """
    Takes a broken test file and its error message,
    end both to Claude, gets back a fixed version
    """

    # Read the broken test file
    with open(test_file_path, "r") as f:
        brokentest_code = f.read()

    # Get the Real HTML from the actual webpage
    real_html = get_page_html(page_url)    

    # Build the prompt - this is what we send to Claude
    prompt = f""" 
    You are a test automation expert
    A playwright/pytest test is failing

    Here is the broken test code:
```python
    {brokentest_code}
```

    Here is the error message:
    {error_message}

    Here is the REAL HTML of the page the test is running against:
```html
    {real_html}
```    

    Instructions :
    - Look at the real HTNL above
    - Find the correct selectors that actually exists in the HTML
    - Fix the broken test code using ONLY selectors that exist in the real HTML
    - Do not guess - use what you can see in the HTML
    - Return ONLY the fixed python code, no explanations.
    """

    print("🤖 Sending real HTML to Claude for analysis...")

    # Send to claude and get response
    message = client.message.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # Extract the fixed code from Claude's response
    fixed_code = message.content[0].text

    #Clean up the response - Claude sometimes wraps code in ```python blocks`
    if "```python" in fixed_code:
        fixed_code = fixed_code.split("```python")[1].split("```")[0].strip()

    return fixed_code    


def save_healed_test(test_file_path, fixed_code):
    """
    Save the fixed code back to the same test file,
    overwritting the broken version 
    """

    with open(test_file_path, "w") as f:
        f.write(fixed_code)

    print(f"✓ Healed test saved to {test_file_path}")


