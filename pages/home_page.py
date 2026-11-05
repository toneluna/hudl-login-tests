import re

from playwright.sync_api import Locator, Page, expect


class HomePage:
    """Page object for the logged-in Hudl home page."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.global_nav = page.get_by_role("navigation", name="Global navigation")
        # The account menu (avatar + display name, top right) opens on hover.
        self.account_menu = page.locator(".hui-globaluseritem").first
        self.log_out_link = page.get_by_role("link", name="Log Out")

    def account_email(self, username: str) -> Locator:
        # The email lives in the collapsed user menu, so it is attached but not visible.
        return self.page.get_by_text(username, exact=True).first

    def expect_loaded(self, username: str) -> None:
        expect(self.page).to_have_url(re.compile(r"hudl\.com/home"))
        expect(self.global_nav).to_be_visible()
        expect(self.account_email(username)).to_be_attached()

    def log_out(self) -> None:
        self.account_menu.hover()
        expect(self.log_out_link).to_be_visible()
        self.log_out_link.click()
