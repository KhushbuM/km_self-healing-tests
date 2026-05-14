import requests
from healer.screenshot import check_screenshots
from healer.sim import create_sim
from healer.healer import create_healing_pr
from datetime import datetime
import subprocess

def check_api_health(url):
    """
    Step 1: Hit the UI URL as an API call
    Returns (status_code, is_healthy)
    """

    print(f"\n🔌 Step 1: Checking API health for {url}")
    try:
        # Add browser-like headers so server accepts our request
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
        response = requests.get(url, timeout=10, headers=headers)
        status_code = response.status_code

        if status_code == 200:
            print(f"✅ API healthy — got {status_code}")
            return status_code, True
        else:
            print(f"❌ API unhealthy — got {status_code}")
            return status_code, False
        
    except requests.exceptions.Timeout:
        print("❌ API check timed out")
        return 408, False
    except requests.exceptions.ConnectionError:
        print("❌ Connection error")
        return 503, False   
    

def run_single_test(test_path):
    """
    Runs a single pytest test
    Returns (passed, output)
    """    
    result = subprocess.run(
        ["pytest", test_path, "-v", "--tb=short"],
        capture_output=True,
        text=True
    )
    passed = result.returncode == 0
    output =result.stdout + result.stderr
    return passed, output

def triage_test(test_name, test_path, page_url, test_page_name):
    """
    Full triage for a single test:
    Step 1 → API check
    Step 2 → Screenshot comparison
    Step 3 → Self heal
    """

    print(f"\n{'='*60}")
    print(f"🔍 Triaging: {test_name}")
    print(f"{'='*60}")

    # ─────────────────────────────────
    # STEP 1: API Health Check
    # ─────────────────────────────────
    status_code, is_healthy = check_api_health(page_url)

    if not is_healthy:
        create_sim(
            title=f"API Down for {test_name}",
            body=f"""
**Test:** {test_name}
**File:** {test_path}
**URL checked:** {page_url}
**Status code:** {status_code}
**Time:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Page returned non-200 status code.
Skipping this test — no point analysing further.
            """,
            label="api-down"            
        )
        print(f"⏭️ Skipping {test_name} — moving to next test")
        return "skipped-api-down"
    
    # ─────────────────────────────────
    # STEP 2: Screenshot Comparison
    # ─────────────────────────────────
    print(f"\n📸 Step 2: Screenshot validation")
    similarity, is_match = check_screenshots(
        url=page_url,
        test_name=test_page_name
    )

    if not is_match:
        create_sim(
            title=f"Product Bug — UI changed for {test_name}",
            body=f"""
**Test:** {test_name}
**File:** {test_path}
**URL:** {page_url}
**Screenshot similarity:** {similarity}% (threshold: 95%)
**Time:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Screenshot comparison failed.
UI has changed from baseline — likely a product bug.
Please review:
- Baseline: screenshots/baseline/{test_page_name}.png
- Actual:   screenshots/actual/{test_page_name}.png
            """,
            label="product-bug"
        )
        print(f"⏭️ Skipping {test_name} — product bug, not automation issue")
        return "skipped-product-bug"
    
   # ─────────────────────────────────
    # STEP 3: Self Heal via PR
    # ─────────────────────────────────
    print(f"\n🤖 Step 3: Attempting self heal via PR")

    passed, output = run_single_test(test_path)

    if passed:
        print(f"✅ {test_name} passing — no healing needed!")
        return "passed"

    print(f"❌ Test failing — sending to Claude...")

    # Extract just the file path (remove ::test_name part)
    file_path = test_path.split("::")[0]

    # Create PR with Claude's fix
    pr = create_healing_pr(
        test_file_path=file_path,
        error_message=output,
        page_url=page_url,
        test_name=test_name
    )

    # Create SIM pointing to the PR
    create_sim(
        title=f"Healing PR opened — {test_name}",
        body=(
            f"**Test:** {test_name}\n"
            f"**File:** {file_path}\n"
            f"**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            "Claude has analyzed the failure and opened a PR with the fix.\n"
            "Please review and merge if correct.\n\n"
            f"**PR:** {pr.html_url}"
        ),
        label="healed"
    )

    print(f"⏳ PR ready for review: {pr.html_url}")
    return "pr-opened"