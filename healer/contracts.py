# Page contracts — defines what elements must exist on each page
# If any element is missing → product bug
# If new element appears → change alert

PAGE_CONTRACTS = {
    "login_page": {
        "url": "https://practicetestautomation.com/practice-test-login/",
        "required_elements": [
            "#username",
            "#password",
            "#submit",
        ],
        "required_text": [
            "Username",
            "Password",
        ],
        "page_title": "Practice Test Login"
    }
}