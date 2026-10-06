import pytest

from appium import webdriver
from appium.options.android import UiAutomator2Options


@pytest.fixture
def driver():
    options = UiAutomator2Options()

    options.platform_name = "Android"
    options.device_name = "Pixel_8"
    options.automation_name = "UiAutomator2"
    options.app_package = "com.csdroid.pkg"
    options.app_activity = "com.csdroid.pkg.MainActivity"

    driver = webdriver.Remote(
        "http://127.0.0.1:4723",
        options=options
    )

    yield driver

    driver.quit()