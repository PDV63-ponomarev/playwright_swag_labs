from playwright.sync_api import Page
import pytest

SITE = "https://www.saucedemo.com/"
VALID_USER = 'standard_user'
VALID_PASSWORD = 'secret_sauce'

@pytest.fixture()
def login_page(page: Page):
    page.goto(SITE)

    class LoginPage:
        def login(self, username: str = VALID_USER, password: str = VALID_PASSWORD):
            page.locator("#user-name").fill(username)
            page.locator("#password").fill(password)
            page.locator("#login-button").click()
            return page

        def goto(self):
            page.goto(SITE)
            return self

    return LoginPage()