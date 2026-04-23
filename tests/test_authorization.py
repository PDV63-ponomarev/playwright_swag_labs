from playwright.sync_api import expect

def test_login(login_page):
    page = login_page.login()
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

def test_logout(login_page):
    page = login_page.login()
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

    page.locator('#react-burger-menu-btn').click()
    page.locator("#logout_sidebar_link").click()
    expect(page).to_have_url('https://www.saucedemo.com/')

def test_login_bad_username(login_page):
    page = login_page.login(username="invalid_user")

    expect(page).to_have_url('https://www.saucedemo.com/')
    (expect(page.locator('[data-test=\"error\"]'))
     .to_contain_text("Username and password do not match any user in this service"))

def test_login_empty_username(login_page):
    page = login_page.login(username="")

    expect(page).to_have_url('https://www.saucedemo.com/')
    (expect(page.locator('[data-test=\"error\"]'))
     .to_contain_text("Username is required"))

def test_login_empty_password(login_page):
    page = login_page.login(password="")

    expect(page).to_have_url('https://www.saucedemo.com/')
    (expect(page.locator('[data-test=\"error\"]'))
     .to_contain_text("Password is required"))

def test_login_locked_user(login_page):
    page = login_page.login(username='locked_out_user')

    expect(page).to_have_url('https://www.saucedemo.com/')
    (expect(page.locator('[data-test=\"error\"]'))
     .to_contain_text("Sorry, this user has been locked out"))