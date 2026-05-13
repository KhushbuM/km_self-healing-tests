import subprocess
import sys
from healer import heal_test, save_healed_test

def run_tests(test_path):
    """
    Runs pytest on a test file and returns
    whether it passed and any error output
    """

    result = subprocess.run(
        ["pytest", test_path, "-v", "--tb=short"],
        capture_output=True,
        text=True
    )

    passed = result.returncode == 0
    output = result.stdout + result.stderr
    return passed, output

def run_with_healing(test_path):
    """
    Runs a test - if it fails, heals it and runs again
    """

    print(f"\n Running: {test_path}")

    #First run
    passed, output = run_tests(test_path)

    if passed:
        print("✅ Tests passed - no healing needed !")
        return
    
    # Tests failed - time to heal
    print("❌ Tests failed -- calling Claude to fix ...")
    print(f"Error: {output[-500]}") # shows last 500 chars of error

    # Send to Claude
    fixed_code = heal_test(test_path, output)

    # Save the fix
    save_healed_test(test_path, fixed_code)

    # Run again with the fix
    print("\n 🔄 Rerunning healed test ...")
    passed, output = run_tests(test_path)

    if passed:
        print("✅ Self healing worked! Tests passing now!")
    else:
        print("⚠️ Healing attempt did not fix it — may need manual review")
        print(output)


if __name__ == "__main__":
    # Default to UI test if no argument given
    test_path = sys.argv[1] if len(sys.argv) > 1 else "tests/ui/test_login_ui.py"
    run_with_healing(test_path)

    



