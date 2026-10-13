import allure
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait


def get_app_elements(driver):
    return driver.find_elements(
        AppiumBy.ID,
        "com.csdroid.pkg:id/tv_title"
    )


def swipe_up(driver, start_x, start_y, end_x, end_y):
    actions = ActionChains(driver)

    actions.w3c_actions.pointer_action.move_to_location(
        start_x,
        start_y
    )

    actions.w3c_actions.pointer_action.pointer_down()

    actions.w3c_actions.pointer_action.move_to_location(
        end_x,
        end_y
    )

    actions.w3c_actions.pointer_action.pointer_up()

    actions.perform()

def find_calendar(driver):
    window_size = driver.get_window_size()

    screen_width = window_size["width"]
    screen_height = window_size["height"]

    print("Window size:", window_size)

    previous_page_source = driver.page_source

    for swipe_number in range(50):
        elements = get_app_elements(driver)

        if len(elements) < 1:
            continue

        element_names = [element.text for element in elements]

        print(f"Свайп №{swipe_number}")
        print(element_names)

        allure.attach(
            "\n".join(element_names),
            name=f"Элементы после свайпа №{swipe_number}",
            attachment_type=allure.attachment_type.TEXT
        )

        # Ищем Calendar среди видимых элементов
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

        # Проверяем, изменился ли экран
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

    raise Exception(
        "Calendar не найден за максимальное количество свайпов"
    )

@allure.title("Поиск Calendar в списке приложений")
def test_find_calendar(driver):
    print("Current package:", driver.current_package)

    WebDriverWait(driver, 10).until(
        lambda driver: driver.find_elements(
            AppiumBy.ID,
            "com.csdroid.pkg:id/tv_title"
        )
    )

    with allure.step("Поиск элемента Calendar"):
        calendar = find_calendar(driver)

    print("Calendar найден:", calendar.text)

    calendar.click()