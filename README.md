# Hudl Login Test Automation

Automated UI tests for the Hudl login flow (https://www.hudl.com/login), built with
Playwright and Python using pytest and the Page Object Model.

## Prerequisites

- Python 3 (developed with Python 3.14)
- Git
- A Hudl test account (credentials are supplied separately and never committed)

## Setup

1. Clone the repository and move into it:

   ```
   git clone https://github.com/toneluna/hudl-login-tests.git
   cd hudl-login-tests
   ```

2. Create and activate a virtual environment.g

   Windows (PowerShell):
   ```
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   macOS/Linux:
   ```
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies and the Playwright browser:

   ```
   pip install -r requirements.txt
   playwright install chromium
   ```

4. Configure credentials (needed only for tests that use a real account):

   ```
   copy .env.example .env      # Windows
   cp .env.example .env        # macOS/Linux
   ```

   Then open `.env` and fill in `HUDL_USERNAME` and `HUDL_PASSWORD`.
   The `.env` file is listed in `.gitignore` and must never be committed.

## Running the tests

| Goal | Command |
|---|---|
| Run everything (headless) | `pytest` |
| Watch the browser | `pytest --headed` |
| Smoke tests only | `pytest -m smoke` |
| Negative tests only | `pytest -m negative` |
| UI/element checks only | `pytest -m ui` |
| Tests that log in with the real account | `pytest -m auth` |
| Everything except real-account tests | `pytest -m "not auth"` |

On failure, screenshots and Playwright traces are saved to `test-results/`.
View a trace with `playwright show-trace <path-to-trace.zip>`.

## Linting and formatting

This project uses [Ruff](https://docs.astral.sh/ruff/).

```
ruff check .
ruff format .
```

## Project structure

```
config/       Loads test credentials from .env
pages/        Page objects: login_page.py (login flow), home_page.py (logged-in home)
tests/        Test files grouped by area of the flow
conftest.py   Shared fixtures
pytest.ini    Pytest configuration and markers
pyproject.toml Ruff configuration
.env.example  Names of the required environment variables (no values)
```

## Design decisions

- **Page Object Model:** locators and actions live in page objects:
  `pages/login_page.py` (email and password steps) and `pages/home_page.py`
  (the logged-in home page and account menu). Tests hold the assertions, so a
  UI change means updating one page object, not every test.
- **Accessible locators:** elements are found by label and role instead of
  CSS or XPath, which keeps tests readable and resilient to markup changes.
  The one exception is the account menu on the home page, which has no accessible role or name, so it is located by its CSS class (.hui-globaluseritem).
  Credentialed tests skip cleanly: if HUDL_USERNAME/HUDL_PASSWORD are not set, tests marked auth are skipped with a message instead of failing. The password is excluded from the Credentials object’s string form so it never appears in logs or test output.
- **No hard waits:** Playwright's auto-waiting and web-first assertions
  handle timing.
- **Fixtures:** `login_page` opens the page and `password_step` advances to the
  second step, so tests start from a known state.
- **Markers:** tests are tagged `smoke`, `negative`, and `ui` so subsets can run.
- **Secrets:** credentials are read from environment variables, never from code.

## Observed behavior of the login flow

The login is a two-step flow (email, then password) hosted on `identity.hudl.com`.
Findings from exploring the page, which the tests document:

- An empty email shows "Please enter your email address".
- An invalid email format shows "Enter a valid email."
- An email with no matching account still advances to the password step.
- A wrong password shows the generic "Incorrect username or password."
  Together with the previous point, the flow does not reveal whether an
  account exists.
- The Edit link returns to the email step with the email field cleared.
- The password field is masked and has a show/hide control.
- The Forgot Password page pre-fills the email entered on the previous step.
- The show/hide password control changes its label to match its state, so the
  locator matches either "Show password" or "Hide password".
  (Noted as an observation only.)
  - After logging in, the user lands on `hudl.com/home`.
- The account menu (top right) opens on hover, not click; Log Out is inside it.
- Logging out returns the user to the public site, `www.hudl.com`.
- After logging out, visiting `/home` redirects back to the login page.

## Scope and limitations

- **Not automated on purpose:** third-party sign-in flows (Google, Facebook,
  Apple) are only checked for presence, since they hand off to external sites.
  Account creation is not exercised.
- **No lockout or brute-force testing:** the tests run against a live
  production site and use a made-up address for negative cases, to avoid
  locking real accounts and to keep request volume low.
- **Bot protection:** [note here if you ever encounter CAPTCHA or rate limiting].
- **Known warning:** pytest may print a deprecation warning about a `base_url`
  fixture. It comes from a plugin interacting with a newer pytest, not from
  this project's code.
- **Credentialed tests:** successful login, logout, and “home requires login after logout” run against the supplied test account. They need .env to be filled in.

## Possible next steps

- Run the suite in CI (GitHub Actions) on every push.
- Add cross-browser runs (Firefox and WebKit).
- Add accessibility checks.