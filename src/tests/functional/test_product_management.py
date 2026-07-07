import allure
import pytest


@pytest.mark.skip(reason="Product creation is broken in CI (fill timeout on product form)")
@allure.feature("Product Management")
@allure.story("CRUD Operations")
class TestProductManagement:
    @allure.title("Create a new product")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_product(self, logged_in_admin, dashboard_page, product_keywords, data_generator):
        dashboard_page.open_products()
        product_data = data_generator.product_data()
        product_keywords.create_product(**product_data)
        assert product_keywords.verify_product_exists(product_data["name"])

    @allure.title("Edit an existing product")
    @allure.severity(allure.severity_level.NORMAL)
    def test_edit_product(self, logged_in_admin, dashboard_page, product_keywords, data_generator):
        dashboard_page.open_products()
        prod = data_generator.product_data()
        product_keywords.create_product(**prod)
        new_name = f"Updated {prod['name']}"
        product_keywords.update_product(prod["name"], {"name": new_name, "price": 99.99})
        assert product_keywords.verify_product_exists(new_name)

    @allure.title("Delete a product")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_product(self, logged_in_admin, dashboard_page, product_keywords, data_generator):
        dashboard_page.open_products()
        prod = data_generator.product_data()
        product_keywords.create_product(**prod)
        product_keywords.delete_product(prod["name"])
        assert not product_keywords.verify_product_exists(prod["name"])

    @allure.title("Create multiple products in bulk")
    @allure.severity(allure.severity_level.NORMAL)
    def test_bulk_product_creation(self, logged_in_admin, dashboard_page, product_keywords, data_generator):
        dashboard_page.open_products()
        count_before = product_keywords.get_product_count()
        products = data_generator.bulk_product_data(5)
        product_keywords.create_multiple_products(products)
        count_after = product_keywords.get_product_count()
        assert count_after >= count_before + 5, "Bulk products should be created"

    @allure.title("Search for a product")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_product(self, logged_in_admin, dashboard_page, product_keywords, data_generator):
        dashboard_page.open_products()
        prod = data_generator.product_data()
        product_keywords.create_product(**prod)
        product_keywords.search_product(prod["name"])
        assert product_keywords.verify_product_exists(prod["name"])

    @allure.title("Create product with barcode")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_product_with_barcode(self, logged_in_admin, dashboard_page, product_keywords, data_generator):
        dashboard_page.open_products()
        prod = data_generator.product_data(barcode=f"BAR{data_generator.random_string(9)}")
        product_keywords.create_product(**prod)
        assert product_keywords.verify_product_exists(prod["name"])
