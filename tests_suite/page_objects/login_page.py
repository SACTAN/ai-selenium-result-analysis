from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class login_page:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        
    def navigate(self):
        self.driver.get("http://the-internet.herokuapp.com/login")
        self.wait.until(EC.presence_of_element_located((By.ID, "username")))
        
    def enter_credentials(self, username, password):
        self.driver.find_element(By.ID, "username").send_keys(username)
        self.driver.find_element(By.ID, "password").send_keys(password)
        
    def submit(self):
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        self.wait.until(EC.url_contains("/secure"))

    def error_username_invalid(self):
        try:
            self.wait.until(EC.visibility_of_element_located((By.ID, "flash")))
            return self.driver.find_element(By.XPATH, "//div[@id='flash']").text
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return ""

    def error_password_invalid(self):
        try:
            self.wait.until(EC.visibility_of_element_located((By.ID, "flash")))
            return self.driver.find_element(By.XPATH, "//div[@id='flash']").text
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return ""
