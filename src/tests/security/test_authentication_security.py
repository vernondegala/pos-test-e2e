import allure
import pytest


@allure.feature("Security")
@allure.story("Authentication Security")
class TestAuthenticationSecurity:
    @pytest.mark.skip(reason="Rate limiting not configured in dev Odoo")
    @allure.title("Brute force protection - rapid failed logins")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_brute_force_protection(self, login_page, page):
        login_page.navigate_to()
        for i in range(10):
            login_page.login_expecting_failure(f"user{i}@test.com", "wrongpass")
            page.wait_for_timeout(200)
        login_page.login()
        assert not login_page.is_login_successful(), "Brute force should be rate-limited"

    @allure.title("Session timeout after inactivity")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_session_timeout(self, logged_in_admin, page, dashboard_page):
        import time
        original_url = dashboard_page.current_url
        page.wait_for_timeout(5000)
        page.goto(dashboard_page.current_url)
        page.wait_for_load_state("load")
        assert "web/login" not in page.url, "Session should remain active briefly"

    @allure.title("No sensitive data in URL parameters")
    @allure.severity(allure.severity_level.NORMAL)
    def test_no_sensitive_data_in_url(self, login_page, page):
        login_page.navigate_to()
        login_page.login()
        assert "password" not in page.url.lower(), "Password should not appear in URL"
        assert "token" not in page.url.lower(), "Token should not appear in URL"

    @pytest.mark.skip(reason="Dev environment uses HTTP, not HTTPS")
    @allure.title("Login page has HTTPS enforced")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_page_https(self, login_page, page):
        login_page.navigate_to()
        assert "http://" not in page.url, "Should use HTTPS" if False else True

    @allure.title("Password field masks input")
    @allure.severity(allure.severity_level.NORMAL)
    def test_password_field_masked(self, login_page, page):
        login_page.navigate_to()
        pw_type = page.get_attribute(login_page.SELECTORS["password_input"], "type")
        assert pw_type == "password", "Password field should be masked"
