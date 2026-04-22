from playwright.sync_api import Page, expect

shop = "https://demowebshop.tricentis.com/"

def test_cards_books(page: Page) -> None:
    page.goto(shop + 'books', wait_until="commit")
    for item in page.locator('.item-box').all():
        expect(item.locator(".picture")).to_be_visible()
        expect(item.locator(".product-title")).to_be_visible()
        expect(item.locator(".rating")).to_be_visible()
        expect(item.locator(".prices")).to_be_visible()

def test_sort(page: Page) -> None:
    page.goto(shop + 'books', wait_until="commit")

    page.locator('#products-orderby').select_option(label="Name: A to Z")
    expect(page.locator('#products-orderby')).to_contain_text("Name: A to Z")
    name_a_z = []
    for item in page.locator('.item-box').all():
        title = item.locator(".product-title").text_content()
        name_a_z.append(title.strip())
    is_ascending = all(name_a_z[i] <= name_a_z[i + 1] for i in range(len(name_a_z) - 1))
    assert is_ascending

    page.locator('#products-orderby').select_option(label="Name: Z to A")
    expect(page.locator('#products-orderby')).to_contain_text("Name: Z to A")
    name_z_a = []
    for item in page.locator('.item-box').all():
        title = item.locator(".product-title").text_content()
        name_z_a.append(title.strip())
    is_descending = all(name_z_a[i] >= name_z_a[i + 1] for i in range(len(name_z_a) - 1))
    assert is_descending

    page.locator('#products-orderby').select_option(label="Price: Low to High")
    expect(page.locator('#products-orderby')).to_contain_text("Price: Low to High")
    price_low_high = []
    for item in page.locator('.item-box').all():
        title = item.locator(".actual-price").text_content()
        price_low_high.append(title.strip())
    is_price_low = all(price_low_high[i] <= price_low_high[i + 1] for i in range(len(price_low_high) - 1))
    assert is_price_low

    page.locator('#products-orderby').select_option(label="Price: High to Low")
    expect(page.locator('#products-orderby')).to_contain_text("Price: High to Low")
    price_high_low = []
    for item in page.locator('.item-box').all():
        title = item.locator(".actual-price").text_content()
        price_high_low.append(title.strip())
    price_high_low = all(price_high_low[i] >= price_high_low[i + 1] for i in range(len(price_high_low) - 1))
    assert price_high_low

    page.locator('#products-orderby').select_option(label="Created on")
    expect(page.locator('#products-orderby')).to_contain_text("Created on")

    page.locator('#products-orderby').select_option(label="Position")
    expect(page.locator('#products-orderby')).to_contain_text("Position")
    position = []
    for item in page.locator('.item-box').all():
        title = item.locator(".product-title").text_content()
        position.append(title.strip())
    is_ascending = all(position[i] <= position[i + 1] for i in range(len(position) - 1))
    assert is_ascending

def test_filters(page: Page) -> None:
    page.goto(shop + 'desktops', wait_until="commit")

    page.get_by_role("link", name="Under").click()
    for item in page.locator('.item-box').all():
        price = float(item.locator(".actual-price").text_content())
        assert price <= 1000

    page.get_by_role("link", name="Remove Filter").click()
    page.get_by_role("link", name="- 1200.00").click()
    for item in page.locator('.item-box').all():
        price = float(item.locator(".actual-price").text_content())
        assert 1000 <= price <= 1200

    page.get_by_role("link", name="Remove Filter").click()
    page.get_by_role("link", name="Over").click()
    for item in page.locator('.item-box').all():
        price = float(item.locator(".actual-price").text_content())
        assert price >= 1200

def test_product_card(page: Page) -> None:
    page.goto(shop, wait_until="commit")

    page.locator('.picture').first.click()
    expect(page.locator('[itemprop="image"]')).to_be_visible()
    expect(page.locator('.product-name')).to_be_visible()
    expect(page.locator('.short-description')).to_be_visible()
    expect(page.locator('.qty-input')).to_be_visible()
    expect(page.locator('.add-to-cart-panel').locator('[value="Add to cart"]')).to_be_visible()