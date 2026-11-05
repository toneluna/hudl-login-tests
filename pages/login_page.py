import re

from playwright.sync_api import Locator, Page, expect


class LoginPage:
    """Page object for Hudl's two-step login flow: email first, then password."""

    PATH = "/login"

    def __init__(self, page: Page) -> None:
        self.page = page

        # Step 1: email
        self.email_input = page.get_by_label(re.compile(r"^Email"))
        self.continue_button = page.get_by_role("button", name="Continue", exact=True)
        self.create_account_link = page.get_by_role("link", name="Create Account")
        self.google_button = page.get_by_role("button", name=re.compile("with Google", re.I))
        self.facebook_button = page.get_by_role("button", name=re.compile("with Facebook", re.I))
        self.apple_button = page.get_by_role("button", name=re.compile("with Apple", re.I))

        # Step 2: password
        self.password_input = page.get_by_label(re.compile(r"^Password"))
        self.forgot_password_link = page.get_by_role("link", name="Forgot Password?")
        self.edit_email_link = page.get_by_role("link", name="Edit")
        self.password_toggle = page.get_by_role(
            "button", name=re.compile(r"(show|hide).*password", re.I)
        )

    def open(self) -> None:
        self.page.goto(self.PATH)
        expect(self.page).to_have_url(re.compile(r"identity\.hudl\.com"))
        expect(self.email_input).to_be_visible()

    def submit_email(self, email: str) -> None:
        self.email_input.fill(email)
        self.continue_button.click()

    def error_message(self, text: str) -> Locator:
        return self.page.get_by_text(text, exact=True)

    def submit_password(self, password: str) -> None:
        self.password_input.fill(password)
        self.continue_button.click()

    def login(self, username: str, password: str) -> None:
        self.submit_email(username)
        expect(self.password_input).to_be_visible()
        self.submit_password(password)
