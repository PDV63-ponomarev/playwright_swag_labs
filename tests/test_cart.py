from playwright.sync_api import expect

def test_button_add_to_cart_and_remove(login_page):
    page = login_page.login()

    page.locator('.btn_primary').first.click()
    expect(page.locator('.shopping_cart_badge')).to_contain_text('1')

    page.locator('.btn_secondary ').first.click()
    expect(page.locator('.shopping_cart_badge')).to_have_count(0)

def test_check_item_in_cart(login_page):
    page = login_page.login()

    page.locator('.btn_primary').first.click()
    expect(page.locator('.shopping_cart_badge')).to_contain_text('1')

    page.locator('.shopping_cart_link').click()
    expect(page).to_have_url('https://www.saucedemo.com/cart.html')

    expect(page.locator('.cart_item')).not_to_be_empty()
    expect(page.locator('.inventory_item_name')).to_be_visible()
    expect(page.locator('.inventory_item_desc')).to_be_visible()
    expect(page.locator('.inventory_item_price')).to_be_visible()

def test_delete_item_in_cart(login_page):
    page = login_page.login()

    page.locator('.btn_primary').first.click()
    expect(page.locator('.shopping_cart_badge')).to_contain_text('1')

    page.locator('.shopping_cart_link').click()
    expect(page).to_have_url('https://www.saucedemo.com/cart.html')

    page.locator('.btn_secondary').first.click()
    expect(page.locator('.cart_item')).to_have_count(0)


def test_purchase_item(login_page):
    page = login_page.login()

    page.locator('.btn_primary').first.click()
    expect(page.locator('.shopping_cart_badge')).to_contain_text('1')
    page.locator('.shopping_cart_link').click()
    expect(page).to_have_url('https://www.saucedemo.com/cart.html')

    page.locator('#checkout').click()
    expect(page).to_have_url('https://www.saucedemo.com/checkout-step-one.html')
    page.locator('#first-name').fill('Oleg')
    page.locator('#last-name').fill('Popov')
    page.locator('#postal-code').fill('123-456')
    page.locator('#continue').click()
    expect(page).to_have_url('https://www.saucedemo.com/checkout-step-two.html')
    expect(page.locator('.cart_item')).not_to_be_empty()
    expect(page.locator('.inventory_item_name')).to_be_visible()
    expect(page.locator('.inventory_item_desc')).to_be_visible()
    expect(page.locator('.inventory_item_price')).to_be_visible()

    page.locator('#finish').click()
    expect(page).to_have_url('https://www.saucedemo.com/checkout-complete.html')

    expect(page.locator('.complete-header')).to_contain_text('Thank you for your order!')
    page.locator('#back-to-products').click()
    expect(page).to_have_url('https://www.saucedemo.com/inventory.html')