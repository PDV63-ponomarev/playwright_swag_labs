from playwright.sync_api import Page, expect
from faker import Faker

shop = "https://demowebshop.tricentis.com/"
email = 'Bob@mail.ru'
password = 'some_pass'

fake = Faker()

def log_in(page: Page, email: email, password: password) -> None:
    page.locator(".email").click()
    page.locator(".email").fill(email)
    page.locator(".password").click()
    page.locator(".password").fill(password)
    page.locator(".login-button").click()

def _test_register(page: Page) -> None:
    page.goto(shop, wait_until="commit")

    fake_email = fake.email()
    page.locator(".ico-register").click()

    page.locator('#gender-male').click()
    page.locator('#FirstName').click()
    page.locator('#FirstName').fill(fake.name())
    page.locator('#LastName').click()
    page.locator('#LastName').fill(fake.last_name())
    page.locator('#Email').click()
    page.locator('#Email').fill(fake_email)
    page.locator('#Password').click()
    page.locator('#Password').fill(password)
    page.locator('#ConfirmPassword').click()
    page.locator('#ConfirmPassword').fill(password)

    page.locator('#register-button').click()

    expect(page.locator("body")).to_contain_text(fake_email)

def test_login(page: Page) -> None:
    page.goto(shop, wait_until="commit")
    page.locator(".ico-login").click()

    log_in(page,email,password)

    expect(page.locator("body")).to_contain_text(email)

def test_login_fail(page: Page) -> None:
    page.goto(shop, wait_until="commit")
    page.locator(".ico-login").click()

    log_in(page,email,'111')

    expect(page.locator("body")).to_contain_text("Login was unsuccessful.")

def test_forgot_password(page: Page) -> None:
    page.goto(shop + 'login', wait_until="commit")
    page.locator('.forgot-password').click()
    page.get_by_role("link", name="Forgot password?").click()
    expect(page).to_have_url(shop + 'passwordrecovery')

    page.locator(".email").click()
    page.locator(".email").fill(email)
    page.get_by_role("button", name="Recover").click()

    expect(page.locator("body")).to_contain_text("Email with instructions has been sent to you.")

def test_logout(page: Page) -> None:
    page.goto(shop, wait_until="commit")
    page.locator(".ico-login").click()

    log_in(page, email, password)

    expect(page.locator("body")).to_contain_text(email)

    page.locator('.ico-logout').click()
    expect(page.get_by_role("link", name="Log in")).to_be_visible()
