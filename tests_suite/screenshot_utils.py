# utilities/screenshot_utils.py
import os
import logging
import uuid
from datetime import datetime
from PIL import Image, ImageDraw
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from typing import Optional, Tuple
from configparser import ConfigParser

logger = logging.getLogger(__name__)


class ScreenshotManager:
    """Advanced screenshot utility with annotation and error handling"""

    def __init__(self, driver: WebDriver, test_id: Optional[str] = None):
        self.driver = driver
        self.test_id = test_id or str(uuid.uuid4())
        self.config = ConfigParser()
        self.config.read('config/config.ini')

        # Setup directories
        self.base_dir = self.config.get('PATHS', 'SCREENSHOT_DIR', fallback='reports/screenshots')
        os.makedirs(self.base_dir, exist_ok=True)

    def _generate_filename(self, prefix: str = 'failure') -> str:
        """Generate unique screenshot filename"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{self.test_id}_{prefix}_{timestamp}.png"

    def capture_full_screenshot(self) -> Optional[str]:
        """Capture full-page screenshot (works for Chrome/Firefox)"""
        try:
            original_size = self.driver.get_window_size()

            if self.driver.name.lower() == 'chrome':
                total_height = self.driver.execute_script(
                    "return document.body.parentNode.scrollHeight")
                self.driver.set_window_size(1920, total_height)

            filename = os.path.join(self.base_dir, self._generate_filename('full'))
            self.driver.save_screenshot(filename)

            # Restore original window size
            self.driver.set_window_size(
                original_size['width'],
                original_size['height']
            )
            return filename

        except Exception as e:
            logger.error(f"Failed to capture full screenshot: {str(e)}")
            return None

    def capture_element_screenshot(self, element, padding: int = 10) -> Optional[str]:
        """Capture screenshot of specific element with padding"""
        try:
            location = element.location_once_scrolled_into_view
            size = element.size

            filename = os.path.join(self.base_dir, self._generate_filename('element'))
            self.driver.save_screenshot(filename)

            # Crop to element coordinates
            img = Image.open(filename)
            left = location['x'] - padding
            top = location['y'] - padding
            right = location['x'] + size['width'] + padding
            bottom = location['y'] + size['height'] + padding

            img = img.crop((left, top, right, bottom))
            img.save(filename)
            return filename

        except Exception as e:
            logger.error(f"Failed to capture element screenshot: {str(e)}")
            return None

    def annotate_screenshot(self, image_path: str, text: str,
                            position: Tuple[int, int] = (10, 10)) -> str:
        """Add annotations to existing screenshot"""
        try:
            with Image.open(image_path) as img:
                draw = ImageDraw.Draw(img)
                draw.text(position, text, fill='red')

                annotated_path = image_path.replace('.png', '_annotated.png')
                img.save(annotated_path)
                return annotated_path

        except Exception as e:
            logger.error(f"Failed to annotate screenshot: {str(e)}")
            return image_path

    def capture_and_log(self, context: str = '') -> Optional[str]:
        """Full workflow: capture, annotate, and return path"""
        try:
            path = self.capture_full_screenshot()
            if path and self.config.getboolean('SCREENSHOTS', 'ANNOTATE', fallback=True):
                annotation = f"Test ID: {self.test_id}\nContext: {context}"
                path = self.annotate_screenshot(path, annotation)

            logger.info(f"Screenshot captured: {path}")
            return path

        except Exception as e:
            logger.error(f"Screenshot capture failed: {str(e)}")
            return None


# Example usage in tests:
if __name__ == "__main__":
    from selenium import webdriver

    driver = webdriver.Chrome()
    driver.get("https://example.com")

    screenshot_manager = ScreenshotManager(driver, "test_123")

    # Capture full page
    full_screen = screenshot_manager.capture_full_screenshot()

    # Capture element screenshot
    #element = driver.find_element_by_tag_name('h1')
    element = driver.find_element(By.TAG_NAME, 'h1')
    element_screen = screenshot_manager.capture_element_screenshot(element)

    # Annotate and save
    annotated = screenshot_manager.annotate_screenshot(full_screen, "Homepage Test")

    driver.quit()