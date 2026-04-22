from playwright.sync_api import Page, expect

shop = "https://demowebshop.tricentis.com/"
word = 'comput'
fall_word = 'some'

def test_search_for_word(page: Page) -> None:
    page.goto(shop, wait_until="commit")
    page.locator('.search-box-text').fill(word)
    page.get_by_role("button", name="Search").click()

    expect(page.locator('.item-box').first).to_be_visible()

    for item in page.locator('.item-box').all():
        title_text = item.locator('.product-title').text_content()
        assert word.lower() in title_text.lower()

def test_search_for_fall_word(page: Page) -> None:
    page.goto(shop, wait_until="commit")
    page.locator('.search-box-text').fill(fall_word)
    page.get_by_role("button", name="Search").click()

    expect(page.locator('.result')).to_contain_text('No products were found that matched your criteria.')

def test_search_for_help_word(page: Page) -> None:
    page.goto(shop, wait_until="commit")
    page.locator('.search-box-text').fill(word)
    page.locator("#ui-id-2").click()

    title_text = page.locator('#product-details-form').text_content()
    assert word.lower() in title_text.lower()

def test_search_for_empty(page: Page) -> None:
    page.goto(shop, wait_until="commit")

    def handle_dialog(dialog):
        assert 'Please enter some search keyword' in dialog.message  # Сохраняем сообщение
        dialog.accept()
    page.on("dialog", handle_dialog)
    page.get_by_role("button", name="Search").click()

