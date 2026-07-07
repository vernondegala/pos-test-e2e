import logging
from typing import Optional

from playwright.sync_api import Locator, Page

from src.core.config import config
from src.core.self_healing.locator_manager import HealerLocator, LocatorManager
from src.core.self_healing.retry_handler import RetryHandler, retry_on_failure
from src.core.ui_utils import wait_for_no_modal

logger = logging.getLogger(__name__)


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.lm = LocatorManager(page)
        self.retry = RetryHandler()
        self.timeout = config.timeout

    @property
    def current_url(self) -> str:
        return self.page.url

    def navigate(self, url: str):
        try:
            self.page.goto(url, wait_until="load")
        except Exception as e:
            if "ERR_ABORTED" in str(e):
                logger.warning(f"Navigation aborted to {url}, retrying with domcontentloaded")
                self.page.goto(url, wait_until="domcontentloaded")
            else:
                raise
        logger.info(f"Navigated to: {url}")

    def wait_for_page_load(self):
        self.page.wait_for_load_state("load")
        return self

    @retry_on_failure()
    def click(self, locator: str, *, by_role: bool = False, **kwargs):
        wait_for_no_modal(self.page, timeout=5_000)
        if by_role:
            role = kwargs.pop("role", "button")
            name = kwargs.pop("name", locator)
            self.page.get_by_role(role, name=name).click(**kwargs)
        else:
            self.page.locator(locator).click(**kwargs)
        return self

    def force_click(self, locator: str, *, by_role: bool = False, **kwargs):
        kwargs.setdefault("force", True)
        return self.click(locator, by_role=by_role, **kwargs)

    @retry_on_failure()
    def fill(self, locator: str, value: str, **kwargs):
        wait_for_no_modal(self.page, timeout=3_000)
        self.page.locator(locator).fill(value, **kwargs)
        return self

    @retry_on_failure()
    def type_text(self, locator: str, text: str, **kwargs):
        self.page.locator(locator).type(text, **kwargs)
        return self

    @retry_on_failure()
    def select_option(self, locator: str, value: str, **kwargs):
        self.page.locator(locator).select_option(value, **kwargs)
        return self

    @retry_on_failure()
    def get_text(self, locator: str) -> str:
        return self.page.locator(locator).inner_text()

    @retry_on_failure()
    def is_visible(self, locator: str) -> bool:
        return self.page.locator(locator).is_visible()

    @retry_on_failure()
    def is_enabled(self, locator: str) -> bool:
        return self.page.locator(locator).is_enabled()

    @retry_on_failure()
    def wait_for_element(self, locator: str, state: str = "visible", timeout: int = None):
        self.page.locator(locator).wait_for(state=state, timeout=timeout or self.timeout)
        return self

    @retry_on_failure()
    def wait_for_text(self, text: str, timeout: int = None):
        self.page.locator(f"text={text}").wait_for(timeout=timeout or self.timeout)
        return self

    def wait_for_navigation(self):
        self.page.wait_for_load_state("load")
        return self

    def reload(self):
        self.page.reload(wait_until="load")
        return self

    def get_by_testid(self, test_id: str) -> HealerLocator:
        return self.lm.by_testid(test_id)

    def get_by_role(self, role: str, name: str = "") -> HealerLocator:
        return self.lm.by_role(role, name)

    def get_by_text(self, text: str, exact: bool = False) -> HealerLocator:
        return self.lm.by_text(text, exact)

    def get_by_placeholder(self, placeholder: str) -> HealerLocator:
        return self.lm.by_placeholder(placeholder)

    def get_by_label(self, label: str) -> HealerLocator:
        return self.lm.by_label(label)

    def get_by_css(self, css: str) -> HealerLocator:
        return self.lm.by_css(css)

    def get_by_xpath(self, xpath: str) -> HealerLocator:
        return self.lm.by_xpath(xpath)

    def handle_dialog(self, accept: bool = True):
        self.page.once("dialog", lambda dialog: dialog.accept() if accept else dialog.dismiss())
        return self

    def evaluate(self, expression: str, **kwargs):
        return self.page.evaluate(expression, **kwargs)

    def screenshot(self, name: str) -> str:
        path = f"screenshots/{name}.png"
        self.page.screenshot(path=path, full_page=True)
        return path

    def hover(self, locator: str, **kwargs):
        self.page.locator(locator).hover(**kwargs)
        return self

    def press_key(self, locator: str, key: str):
        self.page.locator(locator).press(key)
        return self

    def wait_for_no_modal(self, timeout: int = 5_000):
        wait_for_no_modal(self.page, timeout=timeout)
        return self
