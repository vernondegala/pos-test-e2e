import allure
import pytest


@pytest.mark.skip(reason="Skipped all performance tests")
@allure.feature("Performance")
@allure.story("Page Load Metrics")
class TestPosPagePerformance:
    @allure.title("Login page loads within performance threshold")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_page_load_performance(self, browser_manager, page, navigate_to, performance_metrics):
        performance_metrics["start_recording"]()
        navigate_to("http://localhost:8069/web/login")
        page.wait_for_load_state("load")

        metrics = performance_metrics["assert_performance"]()
        allure.attach(str(metrics), name="Login Page Performance Metrics", attachment_type=allure.attachment_type.TEXT)

        lcp = metrics.get("lcp", 0)
        page_load = metrics.get("page_load", 0)
        assert lcp < 5000, f"LCP too high: {lcp}ms"
        assert page_load < 5000, f"Page load too high: {page_load}ms"

    @allure.title("POS interface loads within performance threshold")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_pos_interface_load_performance(self, logged_in_admin, dashboard_page, page, performance_metrics):
        performance_metrics["start_recording"]()
        dashboard_page.open_pos_module()
        page.wait_for_load_state("load")

        metrics = performance_metrics["assert_performance"]()
        allure.attach(str(metrics), name="POS Module Performance Metrics", attachment_type=allure.attachment_type.TEXT)

        page_load = metrics.get("page_load", 0)
        assert page_load < 5000, f"POS module page load too high: {page_load}ms"

    @allure.title("Order processing performance")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.skip(reason="Products not visible in POS grid (article.product timeout)")
    def test_order_processing_time(self, pos_session, pos_keywords, page):
        import time
        start = time.time()

        pos_keywords.quick_sale("Product A", quantity=1, payment_method="Cash")

        elapsed = (time.time() - start) * 1000
        allure.attach(f"{elapsed:.0f}ms", name="Order Processing Time", attachment_type=allure.attachment_type.TEXT)
        assert elapsed < 10000, f"Order processing too slow: {elapsed:.0f}ms"

    @allure.title("Multiple orders throughput performance")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.skip(reason="Products not visible in POS grid (article.product timeout)")
    def test_multiple_orders_throughput(self, pos_session, pos_keywords, page):
        import time

        order_times = []
        for i in range(5):
            start = time.time()
            pos_keywords.quick_sale("Product A", quantity=1, payment_method="Cash")
            elapsed = (time.time() - start) * 1000
            order_times.append(elapsed)
            pos_keywords.start_new_order()

        avg_time = sum(order_times) / len(order_times)
        max_time = max(order_times)
        min_time = min(order_times)

        summary = f"Orders: 5\nAvg: {avg_time:.0f}ms\nMax: {max_time:.0f}ms\nMin: {min_time:.0f}ms"
        allure.attach(summary, name="Throughput Summary", attachment_type=allure.attachment_type.TEXT)
        assert avg_time < 10000, f"Average order time too high: {avg_time:.0f}ms"

    @allure.title("Product search response time in POS")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.skip(reason="Products not visible in POS grid (article.product timeout)")
    def test_product_search_performance(self, pos_session, pos_keywords, page):
        import time

        start = time.time()
        pos_keywords.search_and_select_product("Product A")
        elapsed = (time.time() - start) * 1000

        allure.attach(f"{elapsed:.0f}ms", name="Search Response Time", attachment_type=allure.attachment_type.TEXT)
        assert elapsed < 3000, f"Product search too slow: {elapsed:.0f}ms"

    @allure.title("Concurrent POS operations timing")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.skip(reason="Products not visible in POS grid (article.product timeout)")
    def test_concurrent_operations_timing(self, pos_session, pos_keywords, page):
        import time

        times = {}
        start = time.time()
        pos_keywords.search_and_select_product("Product A")
        times["add_product"] = (time.time() - start) * 1000

        start = time.time()
        pos_keywords.apply_discount_to_order(15)
        times["apply_discount"] = (time.time() - start) * 1000

        start = time.time()
        pos_keywords.set_customer_on_order("Test Customer")
        times["set_customer"] = (time.time() - start) * 1000

        start = time.time()
        pos_keywords.pos_interface.set_quantity(3)
        times["set_quantity"] = (time.time() - start) * 1000

        start = time.time()
        pos_keywords.payment_keywords.pay_with_cash()
        times["payment"] = (time.time() - start) * 1000

        allure.attach(str(times), name="Operation Timing Breakdown", attachment_type=allure.attachment_type.TEXT)
        for op, t in times.items():
            assert t < 5000, f"{op} too slow: {t:.0f}ms"
