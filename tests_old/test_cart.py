from playwright.sync_api import Page, expect

shop = "https://demowebshop.tricentis.com/"

def test_give_item_in_cart_simple(page: Page) -> None:
    page.goto(shop + 'books', wait_until="commit")
    expect(page.locator("#topcartlink")).to_contain_text("(0)")
    page.get_by_role("button", name="Add to cart").first.click()
    expect(page.get_by_role("paragraph")).to_contain_text("The product has been added to your shopping cart")
    expect(page.locator("#topcartlink")).to_contain_text("(1)")

def test_give_item_in_cart(page: Page) -> None:
    page.goto(shop + 'desktops', wait_until="commit")
    expect(page.locator("#topcartlink")).to_contain_text("(0)")
    page.get_by_role("button", name="Add to cart").first.click()
    page.get_by_role("radio", name="Fast [+100.00]").check()
    page.get_by_role("radio", name="GB [+60.00]").check()
    page.get_by_role("radio", name="GB [+100.00]").check()
    page.get_by_role("checkbox", name="Image Viever [+5.00]").check()
    page.get_by_role("textbox", name="Qty:").fill("10")
    page.locator("#add-to-cart-button-72").click()
    expect(page.locator("#topcartlink")).to_contain_text("(10)")

def test_change_item_in_cart(page: Page) -> None:
    page.goto(shop + '141-inch-laptop', wait_until="commit")
    expect(page.locator("#topcartlink")).to_contain_text("(0)")

    page.locator("#add-to-cart-button-31").click()
    expect(page.locator("#topcartlink")).to_contain_text("(1)")

    page.locator('.cart-label').first.click()
    expect(page.locator(".qty-input")).to_have_value("1")
    expect(page.locator('.product-subtotal')).to_contain_text('1590.00')
    page.locator(".qty-input").dblclick()
    page.locator(".qty-input").fill('2')
    page.locator(".qty-input").press("Enter")
    expect(page.locator('.product-subtotal')).to_contain_text('3180.00')


def test_delete_item_in_cart(page: Page) -> None:
    page.goto(shop + 'books', wait_until="commit")
    page.get_by_role("button", name="Add to cart").first.click()
    expect(page.locator("#topcartlink")).to_contain_text("(1)")
    page.locator('.cart-label').first.click()

    page.locator("input[name=\"removefromcart\"]").check()
    page.get_by_role("button", name="Update shopping cart").click()
    expect(page.locator("body")).to_contain_text("Your Shopping Cart is empty!")


def test_making_order(page: Page) -> None:
    page.goto(shop + 'books', wait_until="commit")

    page.get_by_role("link", name="Fiction", exact=True).click()
    expect(page).to_have_url('https://demowebshop.tricentis.com/fiction')
    expect(page.get_by_role("heading", name="Fiction")).to_be_visible()
    expect(page.get_by_text("24.00")).to_be_visible()

    page.get_by_role("button", name="Add to cart").click()
    page.locator('.cart-label').first.click()
    expect(page).to_have_url('https://demowebshop.tricentis.com/cart')

    page.locator("#termsofservice").check()
    page.get_by_role("button", name="Checkout").click()
    expect(page).to_have_url('https://demowebshop.tricentis.com/login/checkoutasguest?returnUrl=%2Fcart')

    page.locator(".email").fill('Bob@mail.ru')
    page.locator(".password").click()
    page.locator(".password").fill('some_pass')
    page.locator(".login-button").click()
    expect(page).to_have_url('https://demowebshop.tricentis.com/cart')

    page.get_by_role("button", name="Checkout").click()
    page.get_by_role("button", name="close").click()
    page.locator("#termsofservice").check()
    page.get_by_role("button", name="Checkout").click()
    page.get_by_label("Select a billing address from").select_option("4877649")
    page.get_by_role("button", name="Continue").click()
    page.get_by_label("Select a shipping address").select_option("4877649")
    page.get_by_role("button", name="Continue").click()
    page.get_by_role("radio", name="Next Day Air (40.00)").check()
    page.get_by_role("button", name="Continue").click()
    page.get_by_role("radio", name="Purchase Order Purchase Order").check()
    page.get_by_role("button", name="Continue").click()
    page.get_by_role("textbox", name="PO Number").click()
    page.get_by_role("textbox", name="PO Number").fill("20-3-000")
    page.get_by_role("button", name="Continue").click()
    page.get_by_role("button", name="Confirm").click()

    expect(page.locator('.page-body')).to_contain_text(
        "Your order has been successfully processed!",
        timeout=30000)
    expect(page.locator('.page-body')).to_contain_text("Order number:")
    page.get_by_role("button", name="Continue").click()

    expect(page).to_have_url('https://demowebshop.tricentis.com/')
    expect(page.locator("#topcartlink")).to_contain_text("(0)")