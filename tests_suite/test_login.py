import pytest
from tests_suite.browser_factory import browser_factory
from tests_suite.logger import JSONLogger
from tests_suite.page_objects.login_page import login_page
from tests_suite.screenshot_utils import ScreenshotManager

logger = JSONLogger()

class TestLogin:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.driver = browser_factory.get_driver()
        self.login_page = login_page(self.driver)
        yield
        self.driver.quit()

    def test_valid_login(self):
        screenshot = ScreenshotManager(self.driver)
        try:
            self.login_page.navigate()
            self.login_page.enter_credentials("tomsmith", "SuperSecretPassword!")
            self.login_page.submit()
            
            assert "The Home Page" in self.driver.title
            logger.log_test_step("PASS", "Successful login", "verify_home_page_title")
            
        except Exception as e:
            logger.log_test_step("FAIL", "Login failed","verify_home_page_title", error=e)
            path = screenshot.capture_and_log(context=f"Error: {str(e)}")
            pytest.fail(f"Test failed. See screenshot: {path}")
            pytest.fail(str(e))

    def test_invalid_username(self):
        screenshot = ScreenshotManager(self.driver)
        try:
            self.login_page.navigate()
            self.login_page.enter_credentials("sachin", "invalidPassword!")
            self.login_page.submit()

            error_message = self.login_page.error_username_invalid()
            assert "Your username is invalid!" in error_message.text
            logger.log_test_step("PASS", "Successful login", "verify_login_with_invalid_username")

        except Exception as e:
            logger.log_test_step("FAIL", "Login failed", "verify_login_with_invalid_username", error=e)
            path = screenshot.capture_and_log(context=f"Error: {str(e)}")
            pytest.fail(f"Test failed. See screenshot: {path}")
            pytest.fail(str(e))

    def test_with_login(self):
        screenshot = ScreenshotManager(self.driver)
        try:
            self.login_page.navigate()
            self.login_page.enter_credentials("tomsmith", "SuperSecretPassword!")
            self.login_page.submit()

            assert "The Internet" in self.driver.title
            logger.log_test_step("PASS", "Successful login", "verify_login_with_valid_credential")

        except Exception as e:
            logger.log_test_step("FAIL", "Login failed", "verify_login_with_valid_credential", error=e)
            path = screenshot.capture_and_log(context=f"Error: {str(e)}")
            pytest.fail(f"Test failed. See screenshot: {path}")
            pytest.fail(str(e))

    def test_invalid_password(self):
        screenshot = ScreenshotManager(self.driver)
        try:
            self.login_page.navigate()
            self.login_page.enter_credentials("tomsmith", "invalidPassword!")
            self.login_page.submit()

            error_message = self.login_page.error_password_invalid()
            assert "Your password is invalid!" in error_message.text
            logger.log_test_step("PASS", "Successful login", "verify_login_with_invalid_password")

        except Exception as e:
            logger.log_test_step("FAIL", "Login failed", "verify_login_with_invalid_password", error=e)
            path = screenshot.capture_and_log(context=f"Error: {str(e)}")
            pytest.fail(f"Test failed. See screenshot: {path}")
            pytest.fail(str(e))