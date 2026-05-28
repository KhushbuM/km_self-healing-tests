# 🤖 AI-Powered Self-Healing Test Framework

A smart test automation framework that uses **Claude AI** to automatically detect, triage, and heal failing tests — without human intervention.

Built with Python, Playwright, and Claude API. Integrated with GitHub and Jenkins for a complete CI/CD pipeline.

---

## 🧠 How It Works

When a test fails, the framework triages it in 3 steps:
Test Fails
     ↓
Step 1: API Health Check
     ↓ Non-200 → 🔴 GitHub Issue "API Down" → Skip test
     ↓ 200
Step 2: HTML Contract Validation
     ↓ Element missing → 🟡 GitHub Issue "Product Bug" → Skip test
     ↓ New element found → 🟡 PR to update contract + GitHub Issue
     ↓ Contract valid
Step 3: Self Heal
     → Claude inspects real page HTML
     → Finds correct selector
     → Opens a Pull Request with the fix
     → Human reviews and merges ✅

---

## 🔄 Smart Triage Flow
Test Fails
↓
Step 1: API Health Check
↓ Non-200 → 🔴 Create GitHub Issue "API Down" → Skip test
↓ 200
Step 2: Screenshot Comparison (95% threshold)
↓ Mismatch → 🟡 Create GitHub Issue "Product Bug" → Skip test
↓ Match
Step 3: Self Heal
→ Claude inspects real page HTML
→ Finds correct selector
→ Creates branch + Pull Request
→ 🟢 Human reviews and merges

---

## 🚀 Installation

```bash
# Clone the repo
git clone https://github.com/KhushbuM/km_self-healing-tests.git
cd km_self-healing-tests

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
playwright install
```

Create a `.env` file in the root:
ANTHROPIC_API_KEY=your-anthropic-api-key
GITHUB_TOKEN=your-github-token
GITHUB_REPO=KhushbuM/km_self-healing-tests

---

## 🧪 Running Tests

```bash
# Run all tests
pytest tests/ -v -s

# Run only API tests
pytest tests/api/ -v -s

# Run only UI tests
pytest tests/ui/ -v -s
```

---

## 🤖 Running the Self-Healing Framework

```bash
python -m healer.runner
```

---

## 👩‍💻 Author
**Khushbu Mehta**
*Built with ❤️ using Claude AI, Playwright and Python*