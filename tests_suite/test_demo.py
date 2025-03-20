import pytest

from tests_suite.logger import JSONLogger

logger = JSONLogger()
def test_example():
    assert 1 + 1 == 2
    print("test case passed")
    logger.log_test_step("PASS", "Successful login", "Verify_login_with_valid_credential")
