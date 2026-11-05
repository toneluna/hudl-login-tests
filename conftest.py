import pytest
from playwright.sync_api import Page, expect

from config.settings import Credentials, get_credentials
from pages.home_page import HomePage
from pages.login_page import LoginPage


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    login = LoginPage(page)
    login.open()
    return login


@pytest.fixture
def password_step(login_page: LoginPage) -> LoginPage:
    """Login page advanced to the password step using a non-existent account."""
    login_page.submit_email("no.such.user.12345@example.com")
    expect(login_page.password_input).to_be_visible()
    return login_page


@pytest.fixture(scope="session")
def credentials() -> Credentials:
    creds = get_credentials()
    if creds is None:
        pytest.skip("Set HUDL_USERNAME and HUDL_PASSWORD in .env to run credentialed tests")
    return creds


@pytest.fixture
def home_page(page: Page, login_page: LoginPage, credentials: Credentials) -> HomePage:
    """Logs in with the real test account and returns the home page."""
    login_page.login(credentials.username, credentials.password)
    home = HomePage(page)
    home.expect_loaded(credentials.username)
    return home
