# Project Summary — AI Self-Healing Test Framework

## What is this?

This project is an automated testing framework that can **fix itself when something breaks** — using AI.

In simple terms:
- It runs automated tests on a website
- If a test fails, it figures out **why** it failed
- It then asks Claude AI to **fix the broken test automatically**
- The fix is raised as a Pull Request for a human to review and approve

---

## The Problem It Solves

When a website changes (for example a button moves or a field gets renamed), automated tests break. 

Normally a developer or tester has to:
1. Notice the test failed
2. Figure out what changed
3. Manually fix the test code
4. Re-run the tests

This takes time and is repetitive work.

---

## How This Framework Fixes It

Instead of a human doing all that work, this framework does it automatically:

1. **Is the website even up?**
   If the website is down, there is no point investigating further.
   A ticket is raised automatically and the test is skipped.

2. **Did the page structure change?**
   The framework checks if all required elements still exist on the page 
   using an HTML contract — a simple list of elements that must be present.

   If an element is **missing** → product bug → ticket raised → stop
   If a **new element** is found → PR raised to update the contract → 
   human reviews whether it was intentional
   If everything looks correct → move to Step 3

3. **Is it just a broken test selector?**
   If the website is up and looks correct, the test itself is broken.
   Claude AI looks at the real website HTML, finds the correct element,
   and fixes the test code automatically.
   A Pull Request is opened for a human to review and merge.

---

## What Makes This Special

Most test frameworks just tell you something broke.
This one tells you **why** it broke and **fixes it for you**.

- No more manually hunting for broken selectors
- No more wasted time investigating infrastructure issues
- AI does the repetitive fixing work
- Humans only review the final fix — not debug it

---

## Technologies Used

- **Python + Playwright** — runs the automated tests
- **Claude AI** — analyses failures and suggests fixes
- **GitHub** — stores code, raises Pull Requests and Issues automatically
- **Jenkins** — runs the tests automatically on every code push

---

*This project was built as a portfolio piece to demonstrate 
AI-powered test automation using modern tools.*