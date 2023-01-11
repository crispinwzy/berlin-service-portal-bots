from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support import select
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from os.path import dirname, abspath, join
from webdriver_manager.chrome import ChromeDriverManager

import time


class WebDriver:
  def __init__(self, headless, timeout):
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {
        "download.default_directory": join(dirname(dirname(abspath(__file__))), "/downloads/"),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    if headless:
      options.add_argument("--headless")

    options.add_argument("--incognito")

    self.web_driver = webdriver.Chrome(options=options, service=service)
    self.web_driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
      "source": """
      Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
      })
      """
    })

    self.timeout = timeout

  def page(self, url):
    self.web_driver.get(url)

  def __get(self, xpath):
    return WebDriverWait(self.web_driver, self.timeout).until(
        expected_conditions.element_to_be_clickable((By.XPATH, xpath))
    )

  def click(self, xpath):
    self.__get(xpath).click()
    time.sleep(1)

  def select_by_text(self, xpath, text):
    select = Select(self.__get(xpath))
    time.sleep(1)
    select.select_by_visible_text(text)
    time.sleep(1)

  def select_by_index(self, xpath, index):
    select = Select(self.__get(xpath))
    time.sleep(1)
    select.select_by_index(index)
    time.sleep(1)

  def get_select_options_contents(self, xpath):
    select = self.__get(xpath)
    time.sleep(1)
    options = select.find_elements(By.TAG_NAME, "option")
    return list(map(lambda option: option.text, options))

  def get_attribute_content(self, xpath, attribute):
    return WebDriverWait(self.web_driver, self.timeout).until(
        expected_conditions.visibility_of_element_located((By.XPATH, xpath))
    ).get_attribute(attribute)

  def get_content(self, xpath):
    return WebDriverWait(self.web_driver, self.timeout).until(
        expected_conditions.visibility_of_element_located((By.XPATH, xpath))
    ).text

  def get_contents(self, xpath):
    elements = WebDriverWait(self.web_driver, self.timeout).until(
        expected_conditions.visibility_of_all_elements_located(
            (By.XPATH, xpath))
    )
    return list(map(lambda element: element.text, elements))

  def fill(self, xpath, text):
    WebDriverWait(self.web_driver, self.timeout).until(
        expected_conditions.visibility_of_element_located((By.XPATH, xpath))
    ).send_keys(text)

  def wait_visibility(self, xpath):
    WebDriverWait(self.web_driver, self.timeout).until(
        expected_conditions.visibility_of_element_located((By.XPATH, xpath))
    )

  def has_element(self, xpath):
    try:
      self.web_driver.find_element(By.XPATH, xpath)
      return 1
    except:
      return 0

  def refresh(self):
    self.web_driver.refresh()

  def current_url(self):
    return self.web_driver.current_url

  def save_page_screenshot(self):
    screenshot_path = datetime.now().strftime("%Y-%m-%d--%H-%M-%S.png")
    scroll_width = self.web_driver.execute_script(
        "return document.body.parentNode.scrollWidth")
    scroll_height = self.web_driver.execute_script(
        "return document.body.parentNode.scrollHeight")
    body = self.web_driver.find_element(By.TAG_NAME, "body")

    if all([scroll_width, scroll_height]):
      previous_size = self.web_driver.get_window_size()
      self.web_driver.set_window_size(scroll_width, scroll_height)
      body.screenshot(screenshot_path)
      self.web_driver.set_window_size(
          previous_size["width"], previous_size["height"])
    else:
      body.screenshot(screenshot_path)

    return screenshot_path

  def save_page_source(self):
    page_source_path = datetime.now().strftime("%Y-%m-%d--%H-%M-%S.html")

    with open(page_source_path, "w") as stream:
      stream.write(self.web_driver.page_source)

    return page_source_path
