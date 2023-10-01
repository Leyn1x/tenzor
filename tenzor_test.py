import pytest
from selenium import webdriver
import os
import requests
import shutil
from page_objects import MainPage, ContactsPage, TensorPage

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_scenario_1(driver):
    main_page = MainPage(driver)
    main_page.open("https://sbis.ru/")
    main_page.go_to_contacts()

    contacts_page = ContactsPage(driver)
    contacts_page.find_tensor_banner()

    tensor_page = TensorPage(driver)
    assert tensor_page.has_sila_v_lyudyah_block()

    tensor_page.go_to_about()
    assert tensor_page.has_about_url("https://tensor.ru/about")

def test_scenario_2(driver):
    main_page = MainPage(driver)
    main_page.open("https://sbis.ru/")
    main_page.go_to_contacts()

    contacts_page = ContactsPage(driver)
    contacts_page.find_tensor_banner()

    tensor_page = TensorPage(driver)
    assert tensor_page.has_sila_v_lyudyah_block()

    tensor_page.go_to_about()
    assert tensor_page.check_photos_height_and_width()

def test_scenario_3(driver):
    main_page = MainPage(driver)
    main_page.open("https://sbis.ru/")
    main_page.go_to_contacts()

    selected_region = main_page.get_selected_region()
    assert selected_region == "Ярославская обл.", "Неправильно выбран регион"
    assert main_page.has_partner_list(), "Отсутствует список партнеров"

    main_page.change_region("Камчатский край")

    selected_region = main_page.get_selected_region()
    assert selected_region == "Камчатский край", "Регион не изменился"
    assert main_page.has_partner_list(), "Отсутствует список партнеров"

    # Проверка URL и title содержат информацию о выбранном регионе
    current_url = driver.current_url
    assert "Камчатский край" in current_url, f"Неправильный URL: {current_url}"
    assert "Камчатский край" in driver.title, f"Неправильный title: {driver.title}"

def test_scenario_4(driver):
    main_page = MainPage(driver)
    main_page.open("https://sbis.ru/")
    
    main_page.go_to_download_sbis()

    # Определите путь для сохранения файла (папка с данным тестом)
    download_folder = os.path.dirname('C:\tests')
    file_path = os.path.join(download_folder, "sbis_installer.exe")

    # Ожидайте, пока файл скачается
    timeout = 60  # Установите тайм-аут на скачивание файла (в секундах)
    download_link = "https://update.sbis.ru/Sbis3Plugin/master/win32/sbisplugin-setup-web.exe"  # Замените на фактическую ссылку
    with requests.get(download_link, stream=True) as response:
        with open(file_path, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
    del response

    # Проверьте, что файл скачался
    assert os.path.exists(file_path), "Файл не был скачан"

    # Проверьте размер скачанного файла
    expected_size = 3.64 * 1024 * 1024  # Размер файла в байтах (3.64 МБ)
    actual_size = os.path.getsize(file_path)
    assert actual_size == expected_size, "Размер скачанного файла не совпадает с ожидаемым"
