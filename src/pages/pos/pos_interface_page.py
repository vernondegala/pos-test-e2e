import logging

import allure

from src.core.config import config
from src.core.ui_utils import wait_for_no_modal
from src.pages.base_page import BasePage
from src.pages.pos.dashboard_page import DashboardPage

logger = logging.getLogger(__name__)


class PosInterfacePage(BasePage):
    SELECTORS = {
        "pos_container": "div.pos.dvh-100",
        "product_list": ".product-list",
        "product_item": "article.product",
        "product_name": ".product-name",
        "product_price": ".price-tag",
        "search_product_input": 'input[placeholder="Search products..."]',
        "order_pane": ".leftpane",
        "empty_order_message": ".leftpane h3",
        "payment_button": ".pay.validation.pay-order-button",
        "customer_button": ".set-partner",
        "refund_button": 'button.control-button:has-text("Refund")',
        "customer_note_button": 'button.control-button:has-text("Customer Note")',
        "numpad": ".numpad",
        "control_buttons": ".control-buttons",
        "cashier_name": ".cashier-name .username",
        "status_connected": ".oe_status .fa-wifi",
        "menu_button": ".menu-button",
        "category_button": ".category-button",
        "category_item": ".category-item",
        "pos_branding": ".pos-branding",
        "popup": ".popup",
        "opening_cash_control": ".modal-dialog",
        "opening_cash_input": ".modal-dialog input[type='text']",
        "open_session_button": '.modal-dialog button:has-text("Open Session")',
    }

    def navigate_to(self, pos_id: int = 1):
        self.navigate(f"{config.base_url}/pos/ui?config_id={pos_id}")
        if self.page.locator(self.SELECTORS["pos_container"]).is_visible():
            self.wait_for_timeout(2000)
            self.start_session()
            logger.info(f"Navigated to POS interface (config_id: {pos_id})")
            return self
        logger.info("POS UI did not load directly, starting session via dashboard")
        self.navigate(config.base_url)
        self.wait_for_page_load()
        dashboard = DashboardPage(self.page)
        dashboard.open_pos_module()
        self.wait_for_timeout(2000)
        session_btns = [
            '.o_kanban_record button:has-text("Session")',
            '.o_kanban_record a:has-text("Session")',
            '.o_kanban_record button:has-text("Open Session")',
            '.o_kanban_record a:has-text("Open Session")',
            '.o_kanban_record button:has-text("New Session")',
        ]
        start_btn = None
        for sel in session_btns:
            try:
                candidates = self.page.locator(sel)
                if candidates.count() > 0:
                    btn = candidates.first
                    if btn.is_visible():
                        start_btn = btn
                        break
            except Exception:
                pass
        if start_btn:
            with self.page.expect_navigation(wait_until='load', timeout=20000):
                start_btn.click()
            self.wait_for_element(self.SELECTORS["pos_container"], timeout=15000)
        else:
            raise Exception("Could not find Session/Open Session button")
        self.wait_for_timeout(2000)
        self.start_session()
        logger.info(f"Navigated to POS interface (config_id: {pos_id})")
        return self

    @allure.step("Start POS session with opening cash: {opening_cash}")
    def start_session(self, opening_cash: str = "100"):
        try:
            try:
                self.page.wait_for_selector(self.SELECTORS["opening_cash_control"], timeout=5_000)
            except Exception:
                pass
            if self.page.locator(self.SELECTORS["opening_cash_control"]).is_visible():
                self.page.locator(self.SELECTORS["opening_cash_input"]).fill(opening_cash)
                self.page.locator(self.SELECTORS["open_session_button"]).click()
                self.wait_for_element_disappear(self.SELECTORS["opening_cash_control"], timeout=15000)
                logger.info(f"POS session started with opening cash: {opening_cash}")
            else:
                logger.info("Session already started, skipping cash control")
        except Exception as e:
            logger.info(f"No cash control dialog, session already active: {e}")
        return self

    @allure.step("Search for product: {query}")
    def search_product(self, query: str):
        self.fill(self.SELECTORS["search_product_input"], query)
        self.page.keyboard.press("Enter")
        self.wait_for_timeout(500)
        return self

    @allure.step("Simulate barcode scan: {barcode}")
    def scan_barcode(self, barcode: str):
        self.fill(self.SELECTORS["search_product_input"], barcode)
        self.page.keyboard.press("Enter")
        self.wait_for_timeout(500)
        logger.info(f"Scanned barcode: {barcode}")
        return self

    @allure.step("Select product: {product_name}")
    def select_product(self, product_name: str):
        locator = f'article.product:has-text("{product_name}")'
        wait_for_no_modal(self.page)
        self.page.locator(locator).first.click()
        logger.info(f"Selected product: {product_name}")
        return self

    @allure.step("Select first product from results")
    def select_first_product(self):
        wait_for_no_modal(self.page)
        self.page.locator(self.SELECTORS["product_item"]).first.click()
        logger.info("Selected first product")
        return self

    @allure.step("Add product to order: {product_name} x{quantity}")
    def add_product_to_order(self, product_name: str, quantity: int = 1):
        self.search_product(product_name)
        for _ in range(quantity):
            self.select_product(product_name)
        return self

    @allure.step("Add product to order by barcode: {barcode}")
    def add_product_by_barcode(self, barcode: str):
        self.scan_barcode(barcode)
        return self

    @allure.step("Set customer: {customer_name}")
    def set_customer(self, customer_name: str):
        self.click(self.SELECTORS["customer_button"])
        self.wait_for_timeout(500)
        self.click(f'.set-partner-line:has-text("{customer_name}")')
        logger.info(f"Customer set: {customer_name}")
        return self

    @allure.step("Apply discount: {percentage}%")
    def apply_discount(self, percentage: float):
        self.click('% Disc')
        self.wait_for_timeout(300)
        self.click(self.SELECTORS["product_item"])
        self.fill('.popup input', str(percentage))
        self.page.keyboard.press("Enter")
        logger.info(f"Discount applied: {percentage}%")
        return self

    @allure.step("Set quantity: {qty}")
    def set_quantity(self, qty: float):
        self.click("Qty")
        self.wait_for_timeout(300)
        self.click(self.SELECTORS["product_item"])
        self.fill('.popup input', str(qty))
        self.page.keyboard.press("Enter")
        logger.info(f"Quantity set: {qty}")
        return self

    @allure.step("Open payment screen")
    def open_payment(self):
        self.click(self.SELECTORS["payment_button"])
        self.wait_for_timeout(1000)
        logger.info("Opened payment screen")
        return self

    @allure.step("Select payment method: {method}")
    def select_payment_method(self, method: str):
        self.click(f'.button.paymentmethod:has-text("{method}")')
        self.wait_for_timeout(500)
        logger.info(f"Selected payment method: {method}")
        return self

    @allure.step("Validate order")
    def validate_order(self):
        self.click('.button.next.validation')
        self.page.wait_for_selector('.receipt-screen', timeout=10000)
        logger.info("Order validated")
        return self

    @allure.step("Complete payment with method: {method}")
    def pay(self, method: str = "Cash"):
        self.open_payment()
        self.select_payment_method(method)
        self.validate_order()
        return self

    @allure.step("Split payment - Cash: {cash_amount}, Card: {card_amount}")
    def pay_split(self, cash_amount: float, card_amount: float):
        self.open_payment()
        self.select_payment_method("Cash")
        self.fill('.amount-input input', str(cash_amount))
        self.select_payment_method("Bank")
        self.fill('.amount-input input', str(card_amount))
        self.validate_order()
        logger.info(f"Split payment: Cash={cash_amount}, Card={card_amount}")
        return self

    @allure.step("Complete a full sale transaction")
    def complete_sale(self, products: list, payment_method: str = "Cash", customer: str = None):
        if customer:
            self.set_customer(customer)
        for product in products:
            qty = product.get("quantity", 1)
            name = product.get("name", product)
            self.add_product_to_order(name, qty)
        self.pay(payment_method)
        return self

    @allure.step("Get receipt item count")
    def get_receipt_item_count(self) -> int:
        items = self.page.query_selector_all('.orderline')
        return len(items)

    @allure.step("Get order line count")
    def get_order_item_count(self) -> int:
        items = self.page.query_selector_all('.orderline')
        return len(items)

    @allure.step("Get receipt total")
    def get_total(self) -> str:
        el = self.page.query_selector('.order-summary .total')
        if el:
            return el.inner_text()
        return ""

    @allure.step("Get receipt subtotal")
    def get_subtotal(self) -> str:
        el = self.page.query_selector('.order-summary .total')
        if el:
            return el.inner_text()
        return ""

    @allure.step("Get receipt tax amount")
    def get_tax(self) -> str:
        el = self.page.query_selector('.order-summary .tax')
        if el:
            return el.inner_text()
        return ""

    @allure.step("Get receipt product names")
    def get_receipt_product_names(self) -> list:
        items = self.page.query_selector_all('.orderline .product-name')
        return [i.inner_text() for i in items]

    @allure.step("Get available product count")
    def get_available_product_count(self) -> int:
        return len(self.page.query_selector_all(self.SELECTORS["product_item"]))

    @allure.step("Get product count for barcode search: {barcode}")
    def get_product_count_for_barcode(self, barcode: str) -> int:
        self.scan_barcode(barcode)
        self.wait_for_timeout(500)
        count = len(self.page.query_selector_all(self.SELECTORS["product_item"]))
        return count

    @allure.step("Start a new order")
    def new_order(self):
        self.click(self.SELECTORS["menu_button"])
        self.wait_for_timeout(500)
        self.click('button:has-text("New Order")')
        self.wait_for_page_load()
        return self

    @allure.step("Process refund")
    def process_refund(self):
        self.click(self.SELECTORS["refund_button"])
        self.handle_dialog(accept=True)
        self.wait_for_page_load()
        return self

    @allure.step("Send receipt by email: {email}")
    def email_receipt(self, email: str):
        self.click(self.SELECTORS["menu_button"])
        self.wait_for_timeout(300)
        self.click('button:has-text("Email Receipt")')
        self.fill('.popup input[type="email"]', email)
        self.click('button:has-text("Send")')
        return self

    @allure.step("Close POS session")
    def close_session(self):
        self.click(self.SELECTORS["menu_button"])
        self.wait_for_timeout(500)
        self.click('a:has-text("Close Session")')
        self.wait_for_timeout(500)
        self.click('.popup.close-pos-popup button:has-text("Close Session")')
        self.wait_for_timeout(1000)
        confirm = self.page.query_selector('.popup.popup-confirm')
        if confirm and confirm.is_visible():
            wait_for_no_modal(self.page)
            confirm.query_selector('.button.confirm').click()
            self.wait_for_timeout(2000)
        logger.info("POS session closed")
        return self

    @allure.step("Check if POS interface is loaded")
    def is_pos_loaded(self) -> bool:
        return self.is_visible(self.SELECTORS["pos_container"])

    @allure.step("Wait for element to disappear")
    def wait_for_element_disappear(self, selector: str, timeout: int = 10000):
        self.page.wait_for_selector(selector, state="hidden", timeout=timeout)
        return self

    def wait_for_timeout(self, ms: int):
        self.page.wait_for_timeout(ms)
        return self
