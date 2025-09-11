import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
import time
import json

class LinkedInProfile:
    def __init__(self, url: str, cookie_file: str = "cookie.json"):
        self.url = url
        self.cookie_file = cookie_file
        self.driver = uc.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 30)

    def load(self):
        self.driver.get(self.url)
        with open(self.cookie_file, "r") as f:
            cookies = json.load(f)
        for cookie in cookies:
            cookie.pop("sameSite", None) 
            try:
                self.driver.add_cookie(cookie)
            except Exception:
                continue
        self.driver.refresh()
        return f"accepted {self.url}"

    def close(self):
        self.driver.quit()
