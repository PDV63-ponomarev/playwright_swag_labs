from playwright.sync_api import expect
import allure

@allure.title("Тест авторизации")
def test_login(login_page):
    with allure.step('Авторизация'):
        page = login_page.login()
    with allure.step('Проверка перехода на страницу магазина'):
        expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

@allure.title("Тест выход из аккаунта")
def test_logout(login_page):
    with allure.step('Авторизация'):
        page = login_page.login()
    with allure.step('Проверка перехода на страницу магазина'):
        expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

    with allure.step('Нажатие лог-оут'):
        page.locator('#react-burger-menu-btn').click()
        page.locator("#logout_sidebar_link").click()
    with allure.step('Проверка перехода на страницу авторизации'):
        expect(page).to_have_url('https://www.saucedemo.com/')

@allure.title("Тест авторизации с неверным именем")
def test_login_bad_username(login_page):
    with allure.step('Авторизация с неверным логином'):
        page = login_page.login(username="invalid_user")

    with allure.step('Остается на странице авторизации'):
        expect(page).to_have_url('https://www.saucedemo.com/')
    with allure.step('Проверка появления сообщения о неверном имени'):
        (expect(page.locator('[data-test=\"error\"]'))
         .to_contain_text("Username and password do not match any user in this service"))

@allure.title("Тест авторизации с пустым именем")
def test_login_empty_username(login_page):
    with allure.step('Авторизация с пустым логином'):
        page = login_page.login(username="")

    with allure.step('Остается на странице авторизации'):
        expect(page).to_have_url('https://www.saucedemo.com/')
    with allure.step('Проверка появления сообщения о пустом имени'):
        (expect(page.locator('[data-test=\"error\"]'))
         .to_contain_text("Username is required"))

@allure.title("Тест авторизации с пустым паролем")
def test_login_empty_password(login_page):
    with allure.step('Авторизация с пустым паролем'):
        page = login_page.login(password="")

    with allure.step('Остается на странице авторизации'):
        expect(page).to_have_url('https://www.saucedemo.com/')
    with allure.step('Проверка появления сообщения о пустом пароле'):
        (expect(page.locator('[data-test=\"error\"]'))
        .to_contain_text("Password is required"))

@allure.title("Тест авторизации с заблокированным аккаунтом")
def test_login_locked_user(login_page):
    with allure.step('Авторизация с заблокированным аккаунтом'):
        page = login_page.login(username='locked_out_user')

    with allure.step('Остается на странице авторизации'):
        expect(page).to_have_url('https://www.saucedemo.com/')
    with allure.step('Проверка появления сообщения о заблокированном аккаунте'):
        (expect(page.locator('[data-test=\"error\"]'))
         .to_contain_text("Sorry, this user has been locked out"))