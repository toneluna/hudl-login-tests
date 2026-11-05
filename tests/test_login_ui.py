import pytest
from playwright.sync_api import expect


@pytest.mark.ui
@pytest.mark.smoke
def test_login_page_shows_email_step(login_page):
    expect(login_page.email_input).to_be_visible()
    expect(login_page.continue_button).to_be_enabled()
    expect(login_page.create_account_link).to_be_visible()


@pytest.mark.ui
def test_social_login_options_are_present(login_page):
    expect(login_page.google_button).to_be_visible()
    expect(login_page.facebook_button).to_be_visible()
    expect(login_page.apple_button).to_be_visible()
