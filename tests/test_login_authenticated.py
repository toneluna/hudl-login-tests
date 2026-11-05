import re

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage

PUBLIC_SITE = re.compile(r"^https://www\.hudl\.com/?(\?.*)?$")


@pytest.mark.auth
@pytest.mark.smoke
def test_successful_login_lands_on_home(login_page, credentials):
    login_page.login(credentials.username, credentials.password)
    HomePage(login_page.page).expect_loaded(credentials.username)


@pytest.mark.auth
def test_logout_returns_to_public_site(home_page):
    home_page.log_out()
    expect(home_page.page).to_have_url(PUBLIC_SITE)


@pytest.mark.auth
def test_home_requires_login_after_logout(home_page):
    home_page.log_out()
    expect(home_page.page).to_have_url(PUBLIC_SITE)
    home_page.page.goto("/home")
    expect(home_page.page).to_have_url(re.compile(r"identity\.hudl\.com"))
