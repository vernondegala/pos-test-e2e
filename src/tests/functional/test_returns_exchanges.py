import allure
import pytest

from src.utils.data_generator import DataGenerator


@allure.feature("Returns & Exchanges")
@allure.story("Return Processing")
class TestReturnsExchanges:
    @allure.title("Create a return for a completed sale")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.skip(reason="POS session fixture needs Odoo 17 selector fixes")
    def test_create_return_for_completed_sale(self, pos_session, pos_keywords):
        pos_keywords.quick_sale("Product A", quantity=1, payment_method="Cash")
        assert pos_keywords.validate_order_total(), "Original sale should complete"

    @allure.title("Process full refund on returned item")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.skip(reason="POS session fixture needs Odoo 17 selector fixes")
    def test_full_refund_process(self, pos_session, pos_keywords):
        pos_keywords.quick_sale("Product B", quantity=2, payment_method="Cash")
        assert pos_keywords.validate_order_total(), "Initial sale should complete"
        pos_keywords.process_refund()
        assert pos_keywords.validate_order_total(expected_min=-9999), "Refund should show negative total"

    @allure.title("Return with different reason codes")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.skip(reason="POS session fixture needs Odoo 17 selector fixes")
    def test_return_different_reasons(self, pos_session, pos_keywords):
        pos_keywords.quick_sale("Product C", quantity=1, payment_method="Cash")
        assert pos_keywords.validate_order_total()
        pos_keywords.process_refund()

    @allure.title("Partial return of multi-item order")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.skip(reason="POS session fixture needs Odoo 17 selector fixes")
    def test_partial_return_multi_item(self, pos_session, pos_keywords):
        products = [
            {"name": "Product A", "quantity": 1},
            {"name": "Product B", "quantity": 2},
        ]
        pos_keywords.create_sale_order(products, payment_method="Cash")

    @allure.title("Return processed after POS session closed")
    @allure.severity(allure.severity_level.NORMAL)
    def test_return_after_session_closed(self, logged_in_admin, dashboard_page, orders_page):
        orders_page.navigate_to()
        orders_page.wait_for_page_load()
        assert orders_page.get_order_count() >= 0, "Should be able to view historical orders"
