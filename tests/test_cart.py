from playwright.sync_api import expect
import allure

@allure.title("Тест добавления и удаление товара из корзины")
def test_button_add_to_cart_and_remove(login_page):
    with allure.step('Авторизация'):
        page = login_page.login()

    with allure.step('Добавление товара в корзину'):
        page.locator('.btn_primary').first.click()
    with allure.step('Увеличения товара в корзине'):
        expect(page.locator('.shopping_cart_badge')).to_contain_text('1')

    with allure.step('Удаление товара из корзины'):
        page.locator('.btn_secondary ').first.click()
    with allure.step('Уменьшения товара в корзине'):
        expect(page.locator('.shopping_cart_badge')).to_have_count(0)

@allure.title("Проверка заполнения карточки товара в корзине")
def test_check_item_in_cart(login_page):
    with allure.step('Авторизация'):
        page = login_page.login()

    with allure.step('Добавление товара в корзину'):
        page.locator('.btn_primary').first.click()
    with allure.step('Увеличения товара в корзине'):
        expect(page.locator('.shopping_cart_badge')).to_contain_text('1')

    with allure.step('Переход в корзину'):
        page.locator('.shopping_cart_link').click()
        expect(page).to_have_url('https://www.saucedemo.com/cart.html')

    with allure.step('Корзина не пустая'):
        expect(page.locator('.cart_item')).not_to_be_empty()
    with allure.step('В карточке товара есть наименование, описание, цена'):
        expect(page.locator('.inventory_item_name')).to_be_visible()
        expect(page.locator('.inventory_item_desc')).to_be_visible()
        expect(page.locator('.inventory_item_price')).to_be_visible()

@allure.title("Тест удаления товара из внутри корзины")
def test_delete_item_in_cart(login_page):
    with allure.step('Авторизация'):
        page = login_page.login()

    with allure.step('Добавление товара в корзину'):
        page.locator('.btn_primary').first.click()
        expect(page.locator('.shopping_cart_badge')).to_contain_text('1')

    with allure.step('Переход в корзину'):
        page.locator('.shopping_cart_link').click()
        expect(page).to_have_url('https://www.saucedemo.com/cart.html')

    with allure.step('Удаление товара из корзины'):
        page.locator('.btn_secondary').first.click()
        expect(page.locator('.cart_item')).to_have_count(0)

@allure.title("Тест оформления заказа")
def test_purchase_item(login_page):
    with allure.step('Авторизация'):
        page = login_page.login()

    with allure.step('Добавление товара в корзину'):
        page.locator('.btn_primary').first.click()
        expect(page.locator('.shopping_cart_badge')).to_contain_text('1')

    with allure.step('Переход в корзину'):
        page.locator('.shopping_cart_link').click()
        expect(page).to_have_url('https://www.saucedemo.com/cart.html')

    with allure.step('Первый этап оформления'):
        page.locator('#checkout').click()
        expect(page).to_have_url('https://www.saucedemo.com/checkout-step-one.html')
        page.locator('#first-name').fill('Oleg')
        page.locator('#last-name').fill('Popov')
        page.locator('#postal-code').fill('123-456')

    with allure.step('Второй этап оформления'):
        page.locator('#continue').click()
        expect(page).to_have_url('https://www.saucedemo.com/checkout-step-two.html')
        expect(page.locator('.cart_item')).not_to_be_empty()
        expect(page.locator('.inventory_item_name')).to_be_visible()
        expect(page.locator('.inventory_item_desc')).to_be_visible()
        expect(page.locator('.inventory_item_price')).to_be_visible()

    with allure.step('Подтверждение заказа'):
        page.locator('#finish').click()
        expect(page).to_have_url('https://www.saucedemo.com/checkout-complete.html')
        expect(page.locator('.complete-header')).to_contain_text('Thank you for your order!')

    with allure.step('Переход в магазин по завершению покупки'):
        page.locator('#back-to-products').click()
        expect(page).to_have_url('https://www.saucedemo.com/inventory.html')