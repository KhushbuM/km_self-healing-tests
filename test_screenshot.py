from healer.screenshot import check_screenshots

similarity, is_match = check_screenshots(
    url="https://practicetestautomation.com/practice-test-login/",
    test_name="login_page"
)

print(f"Similarity: {similarity}%")
print(f"Match: {is_match}")