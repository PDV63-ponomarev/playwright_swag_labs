from playwright.sync_api import expect

def test_cards(login_page):
    page = login_page.login()

    for item in page.locator('.inventory_item').all():
        expect(item.locator('.inventory_item_img img')).to_be_visible()
        expect(item.locator('.inventory_item_name ')).to_be_visible()
        expect(item.locator('.inventory_item_desc')).to_be_visible()
        expect(item.locator('.inventory_item_price')).to_be_visible()

def test_sort(login_page):
    page = login_page.login()

    page.locator('.product_sort_container').select_option('az')
    name_a_z = []
    for item in page.locator('.inventory_item').all():
        title = item.locator('.inventory_item_name').text_content()
        name_a_z.append(title.strip())
    is_ascending = all(name_a_z[i] <= name_a_z[i + 1] for i in range(len(name_a_z) - 1))
    assert is_ascending

    page.locator('.product_sort_container').select_option('za')
    name_z_a = []
    for item in page.locator('.inventory_item').all():
        title = item.locator('.inventory_item_name').text_content()
        name_z_a.append(title.strip())
    is_descending = all(name_z_a[i] >= name_z_a[i + 1] for i in range(len(name_z_a) - 1))
    assert is_descending

    page.locator('.product_sort_container').select_option('lohi')
    price_low_high = []
    for item in page.locator('.inventory_item').all():
        title = item.locator('.inventory_item_price').text_content().replace('$', '')
        price_low_high.append(float(title.strip()))
    price_low_high = all(price_low_high[i] <= price_low_high[i + 1] for i in range(len(price_low_high) - 1))
    assert price_low_high

    page.locator('.product_sort_container').select_option('hilo')
    price_high_low = []
    for item in page.locator('.inventory_item').all():
        title = item.locator('.inventory_item_price').text_content().replace('$', '')
        price_high_low.append(float(title.strip()))
    price_high_low = all(price_high_low[i] >= price_high_low[i + 1] for i in range(len(price_high_low) - 1))
    assert price_high_low


# def test_product_card(page: Page) -> None:
#     page.goto(shop, wait_until="commit")
#
#     page.locator('.picture').first.click()
#     expect(page.locator('[itemprop="image"]')).to_be_visible()
#     expect(page.locator('.product-name')).to_be_visible()
#     expect(page.locator('.short-description')).to_be_visible()
#     expect(page.locator('.qty-input')).to_be_visible()
#     expect(page.locator('.add-to-cart-panel').locator('[value="Add to cart"]')).to_be_visible()