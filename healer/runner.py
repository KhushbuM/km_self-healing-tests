from healer.triage import triage_test

# Track pages already checked for contract changes
# So we don't create duplicate PRs for the same page
checked_contracts = set()

TESTS = [
    {
        "test_name":      "test_successful_login",
        "test_path":      "tests/ui/test_login_ui.py::test_successful_login",
        "page_url":       "https://practicetestautomation.com/practice-test-login/",
        "test_page_name": "login_page"
    },
    {
        "test_name":      "test_failed_login",
        "test_path":      "tests/ui/test_login_ui.py::test_failed_login",
        "page_url":       "https://practicetestautomation.com/practice-test-login/",
        "test_page_name": "login_page"
    },
    {
        "test_name":      "test_logout",
        "test_path":      "tests/ui/test_login_ui.py::test_logout",
        "page_url":       "https://practicetestautomation.com/practice-test-login/",
        "test_page_name": "login_page"
    }
]


def run_all():
    print("\n🚀 Starting Self Healing Test Framework")
    print(f"📋 Running triage for {len(TESTS)} tests\n")

    results = {
        "passed":              0,
        "pr-opened":           0,
        "skipped-api-down":    0,
        "skipped-product-bug": 0,
        "healing-failed":      0
    }

    for test in TESTS:
        result = triage_test(
            test_name=      test["test_name"],
            test_path=      test["test_path"],
            page_url=       test["page_url"],
            test_page_name= test["test_page_name"],
            checked_contracts=checked_contracts  # ← pass it in
        )
        results[result] = results.get(result, 0) + 1

    print(f"\n{'='*60}")
    print(f"📊 FINAL SUMMARY")
    print(f"{'='*60}")
    print(f"✅ Passed:           {results['passed']}")
    print(f"📬 PRs Opened:       {results['pr-opened']}")
    print(f"🔴 API Down:         {results['skipped-api-down']}")
    print(f"🟡 Product Bugs:     {results['skipped-product-bug']}")
    print(f"🔵 Healing Failed:   {results['healing-failed']}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    run_all()