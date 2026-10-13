import allure
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def get_app_elements(driver):
    return driver.find_elements(
        AppiumBy.ID,
        "com.csdroid.pkg:id/tv_title"
    )


def swipe_up(driver, start_x, start_y, end_x, end_y):
    touch_input = PointerInput(interaction.POINTER_TOUCH, "touch")
    actions = ActionBuilder(driver, mouse=touch_input)

    actions.pointer_action.move_to_location(start_x, start_y)
    actions.pointer_action.pointer_down()
    actions.pointer_action.move_to_location(end_x, end_y)
    actions.pointer_action.release()

    actions.perform()


def find_calendar(driver):
    max_swipes = 50
    swipe_number = 0

    window_size = driver.get_window_size()
    screen_width = window_size["width"]
    screen_height = window_size["height"]

    print("Window size:", window_size)

    previous_page_source = driver.page_source

    while swipe_number < max_swipes:
        elements = get_app_elements(driver)

        if not elements:
            swipe_number += 1
            continue

        element_names = [element.text for element in elements]

        print(f"Экран №{swipe_number}")
        print(element_names)

        allure.attach(
            "\n".join(element_names),
            name=f"Элементы на экране №{swipe_number}",
            attachment_type=allure.attachment_type.TEXT
        )

        # Ищем Calendar среди видимых элементов.
        for element in elements:
            if element.text == "Calendar":
                return element

        with allure.step(f"Свайп №{swipe_number}"):
            swipe_up(
                driver,
                screen_width // 2,
                int(screen_height * 0.80),
                screen_width // 2,
                int(screen_height * 0.25)
            )

        current_page_source = driver.page_source
        print(
            "Экран изменился:",
            current_page_source != previous_page_source
        )

        if current_page_source == previous_page_source:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Последний экран",
                attachment_type=allure.attachment_type.PNG
            )
            allure.attach(
                current_page_source,
                name="Page source последнего экрана",
                attachment_type=allure.attachment_type.XML
            )
            raise Exception(
                "Достигнут конец списка. Calendar не найден"
            )

        previous_page_source = current_page_source
        swipe_number += 1

    raise Exception(
        "Calendar не найден за максимальное количество свайпов"
    )


@allure.title("Поиск Calendar в списке приложений")
def test_find_calendar(driver):
    print("Current package:", driver.current_package)

    WebDriverWait(driver, 30).until(
        lambda driver: len(get_app_elements(driver)) >= 5
    )

    with allure.step("Поиск элемента Calendar"):
        calendar = find_calendar(driver)

    print("Calendar найден:", calendar.text)

    with allure.step("Открытие сведений о Calendar"):
        calendar.click()

    with allure.step("Проверка окна со сведениями о Calendar"):
        package_info = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().textContains("com.google.android.calendar")'
                )
            )
        )

        assert package_info.text.splitlines()[0] == "com.google.android.calendar", (
            "Окно сведений о Calendar не появилось или пакет не совпадает"
        )

        allure.attach(
            driver.get_screenshot_as_png(),
            name="Окно сведений о Calendar",
            attachment_type=allure.attachment_type.PNG
        )
