import pytest
from playwright.sync_api import expect


@pytest.mark.negative
def test_wrong_password_shows_generic_error(password_step):
    password_step.submit_password("not-the-password")
    expect(password_step.error_message("Incorrect username or password.")).to_be_visible()
    expect(password_step.password_input).to_be_visible()


@pytest.mark.ui
def test_password_is_masked_by_default(password_step):
    expect(password_step.password_input).to_have_attribute("type", "password")


@pytest.mark.ui
def test_password_toggle_reveals_and_hides_password(password_step):
    password_step.password_input.fill("example-password")
    password_step.password_toggle.click()
    expect(password_step.password_input).to_have_attribute("type", "text")
    password_step.password_toggle.click()
    expect(password_step.password_input).to_have_attribute("type", "password")


def test_forgot_password_link_goes_to_reset_page(password_step):
    password_step.forgot_password_link.click()
    expect(password_step.page.get_by_role("heading", name="Reset Password")).to_be_visible()
    expect(password_step.email_input).to_have_value("no.such.user.12345@example.com")


@pytest.mark.negative
def test_blank_password_shows_required_message(password_step):
    password_step.submit_password("")
    expect(password_step.error_message("Please enter your password")).to_be_visible()
