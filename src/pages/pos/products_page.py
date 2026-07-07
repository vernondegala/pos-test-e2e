import logging

import allure

from src.pages.base_page import BasePage

logger = logging.getLogger(__name__)


class ProductsPage(BasePage):
    SELECTORS = {
        "create_button": 'button:has-text("New")',
        "import_button": '.o_button_import',
        "search_input": '.o_searchview_input',
        "list_view": '.o_list_view',
        "kanban_view": '.o_kanban_view',
        "kanban_record": '.o_kanban_record',
        "form_view": '.o_form_view',
        "name_input": '[name="name"] .o_input',
        "price_input": '[name="list_price"] .o_input',
        "cost_input": '[name="standard_price"] .o_input',
        "barcode_input": '[name="barcode"] .o_input',
        "category_select": '[name="categ_id"] .o_input',
        "tax_select": '[name="taxes_id"] .o_input',
        "save_button": '.o_form_button_save',
        "discard_button": '.o_form_button_discard',
        "edit_button": '.o_form_button_edit',
        "delete_button": '.o_form_button_delete',
        "action_dropdown": '.o_dropdown_button',
        "delete_confirm": '.modal .btn-primary',
        "product_row": '.o_data_row',
        "product_name_cell": '.o_field_char',
        "product_price_cell": '.o_field_monetary',
        "pager_info": '.o_pager',
        "list_item": '.o_data_row',
        "view_switcher_kanban": 'button[data-view-type="kanban"]',
        "view_switcher_list": 'button[data-view-type="list"]',
    }

    @allure.step("Click Create Product")
    def click_create(self):
        self.wait_for_no_modal()
        create_selectors = [
            self.SELECTORS["create_button"],
            '.o_list_button_add',
            '.o-kanban-button-new',
            'button:has-text("New")',
            'a:has-text("New")',
            '.o_control_panel button:first-child',
        ]
        clicked = False
        for sel in create_selectors:
            try:
                btn = self.page.locator(sel).first
                if btn.is_visible():
                    btn.click()
                    clicked = True
                    break
            except Exception:
                pass
        if not clicked:
            try:
                btn = self.page.get_by_text("New", exact=True).first
                if btn.is_visible():
                    btn.click()
                    clicked = True
            except Exception:
                pass
        if clicked:
            self.wait_for_element(self.SELECTORS["form_view"])
        return self

    @allure.step("Fill product form: {product_data}")
    def fill_product_form(self, product_data: dict):
        if "name" in product_data:
            self.fill(self.SELECTORS["name_input"], product_data["name"])
        if "price" in product_data:
            self.fill(self.SELECTORS["price_input"], str(product_data["price"]))
        if "cost" in product_data:
            self.fill(self.SELECTORS["cost_input"], str(product_data["cost"]))
        if "barcode" in product_data:
            self.fill(self.SELECTORS["barcode_input"], product_data["barcode"])
        if "category" in product_data:
            self.select_option(self.SELECTORS["category_select"], product_data["category"])
        return self

    @allure.step("Save product form")
    def save(self):
        self.click(self.SELECTORS["save_button"])
        self.wait_for_page_load()
        return self

    @allure.step("Discard product form")
    def discard(self):
        self.click(self.SELECTORS["discard_button"])
        return self

    @allure.step("Edit product: {product_name}")
    def edit_product(self, product_name: str, updates: dict):
        self.search_product(product_name)
        self.click(f'.o_data_row:has-text("{product_name}")')
        self.wait_for_element(self.SELECTORS["form_view"])
        self.click(self.SELECTORS["edit_button"])
        self.fill_product_form(updates)
        self.save()
        return self

    @allure.step("Delete product: {product_name}")
    def delete_product(self, product_name: str):
        self.search_product(product_name)
        self.click(f'.o_data_row:has-text("{product_name}")')
        self.wait_for_element(self.SELECTORS["form_view"])
        self.click(self.SELECTORS["action_dropdown"])
        self.click(self.SELECTORS["delete_button"])
        self.click(self.SELECTORS["delete_confirm"])
        self.wait_for_page_load()
        return self

    @allure.step("Search product: {query}")
    def search_product(self, query: str):
        self.fill(self.SELECTORS["search_input"], query)
        self.page.keyboard.press("Enter")
        self.wait_for_page_load()
        return self

    @allure.step("Create a new product")
    def create_product(self, product_data: dict):
        self.click_create()
        self.fill_product_form(product_data)
        self.save()
        return self

    @allure.step("Get product list")
    def get_product_list(self) -> list:
        rows = self.page.locator(self.SELECTORS["list_item"]).all()
        products = []
        for row in rows:
            products.append({
                "name": row.locator(self.SELECTORS["product_name_cell"]).inner_text(),
                "price": row.locator(self.SELECTORS["product_price_cell"]).inner_text(),
            })
        return products

    @allure.step("Check if product exists: {product_name}")
    def product_exists(self, product_name: str) -> bool:
        return self.is_visible(f'.o_data_row:has-text("{product_name}")')

    @allure.step("Get product count")
    def get_product_count(self) -> int:
        items = self.page.query_selector_all(self.SELECTORS["list_item"])
        if items:
            return len(items)
        kanban_records = self.page.query_selector_all(self.SELECTORS["kanban_record"])
        if kanban_records:
            return len(kanban_records)
        money_fields = self.page.query_selector_all(self.SELECTORS["product_price_cell"])
        return len(money_fields)
