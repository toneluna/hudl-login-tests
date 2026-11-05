import re

import pytest
from playwright.sync_api import expect

from config.test_data import UNKNOWN_EMAIL


@pytest.mark.negative
@pytest.mark.parametrize(
    ("email", "expected_error"),
    [
        ("", "Please enter your email address"),
        ("abc", "Enter a valid email."),
    ],
    ids=["empty-email", "invalid-format"],
)
def test_email_validation_errors(login_page, email, expected_error):
    login_page.submit_email(email)
    expect(login_page.error_message(expected_error)).to_be_visible()
    expect(login_page.password_input).to_have_count(0)


@pytest.mark.smoke
def test_unknown_email_advances_to_password_step(login_page):
    login_page.submit_email(UNKNOWN_EMAIL)
    expect(login_page.password_input).to_be_visible()
    expect(login_page.forgot_password_link).to_be_visible()
    expect(login_page.edit_email_link).to_be_visible()


def test_edit_link_returns_to_empty_email_step(login_page):
    login_page.submit_email(UNKNOWN_EMAIL)
    login_page.edit_email_link.click()
    expect(login_page.email_input).to_be_editable()
    expect(login_page.email_input).to_have_value("")


def test_create_account_link_goes_to_signup(login_page):
    login_page.create_account_link.click()
    expect(login_page.page).to_have_url(re.compile(r"/u/signup"))


def test_enter_key_submits_email(login_page):
    login_page.email_input.fill(UNKNOWN_EMAIL)
    login_page.email_input.press("Enter")
    expect(login_page.password_input).to_be_visible()
