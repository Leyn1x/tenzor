from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MainPage:
    def __init__(self, driver):
        self.driver = driver

    def open(self, url):
        self.driver.get(url)

    def go_to_contacts(self):
        contacts_link = self.driver.find_element(By.LINK_TEXT, "Контакты")
        contacts_link.click()

    def get_selected_region(self):
        return self.driver.find_element(By.ID, "region-name").text

    def has_partner_list(self):
        return EC.presence_of_element_located((By.CLASS_NAME, "partners-list"))(self.driver)

    def change_region(self, region_name):
        region_dropdown = self.driver.find_element(By.ID, "region-selector")
        region_dropdown.click()
        region_option = self.driver.find_element(By.XPATH, f"//li[contains(text(), '{region_name}')]")
        region_option.click()
    
    def go_to_download_sbis(self):
        download_link = self.driver.find_element(By.LINK_TEXT, "Скачать СБИС")
        download_link.click()

class ContactsPage:
    def __init__(self, driver):
        self.driver = driver

    def find_tensor_banner(self):
        tensor_banner = self.driver.find_element(By.XPATH, "//img[@alt='Тензор']")
        tensor_banner.click()

class TensorPage:
    def __init__(self, driver):
        self.driver = driver

    def has_sila_v_lyudyah_block(self):
        return EC.presence_of_element_located((By.XPATH, "//div[@class='sila']"))(self.driver)

    def go_to_about(self):
        about_link = self.driver.find_element(By.XPATH, "//a[text()='Подробнее']")
        about_link.click()

    def has_about_url(self, url):
        return self.driver.current_url == url

    def check_photos_height_and_width(self):
        photos = self.driver.find_elements(By.XPATH, "//div[@class='photos']//img")
        dimensions = set()
        for photo in photos:
            dimensions.add((photo.size['height'], photo.size['width']))
        return len(dimensions) == 1