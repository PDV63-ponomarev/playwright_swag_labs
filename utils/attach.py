import allure
from allure_commons.types import AttachmentType
from playwright.sync_api import Page

def add_screenshot(page: Page):
    """Добавление скриншота"""
    png = page.screenshot(full_page=True)
    allure.attach(
        body=png,
        name='screenshot',
        attachment_type=AttachmentType.PNG,
        extension='.png'
    )

def add_logs(page: Page):
    """Добавление логов браузера"""
    logs = []
    # Собираем консольные сообщения
    def handle_console(msg):
        logs.append(f"[{msg.type}] {msg.text}")
    # Временно подписываемся на события
    page.on("console", handle_console)
    page.evaluate("console.log('Playwright log capture started')")
    # Небольшая задержка для сбора логов
    page.wait_for_timeout(100)
    # Отписываемся
    page.remove_listener("console", handle_console)

    if logs:
        log_text = "\n".join(logs)
        allure.attach(
            log_text,
            name='browser_logs',
            attachment_type=AttachmentType.TEXT,
            extension='.log'
        )

def add_html(page: Page):
    """Добавление HTML страницы"""
    html = page.content()
    allure.attach(
        html,
        name='page_source',
        attachment_type=AttachmentType.HTML,
        extension='.html'
    )
