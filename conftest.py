from playwright.sync_api import Page
import pytest
from utils import attach

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

@pytest.fixture(scope='function')
def allure(page: Page, request):
    attach.add_screenshot(page, name=f"screenshot_{request.node.name}")
    attach.add_logs(page, name=f"logs_{request.node.name}")
    attach.add_html(page, name=f"html_{request.node.name}")