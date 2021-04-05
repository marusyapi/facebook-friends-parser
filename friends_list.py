import os
import time
import getpass

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from constants import *
from csv_functions import CSVFile


class FacebookFriends:
    url = LOGIN_URL

    def __init__(self, login, password):
        chromedriver = './resources/chromedriver.exe'
        os.environ["webdriver.chrome.driver"] = chromedriver

        options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        options.add_experimental_option("prefs", prefs)

        self.driver = webdriver.Chrome(executable_path=chromedriver, options=options)
        self.wait = WebDriverWait(self.driver, 10)

        self.login(login, password)

    def login(self, login, password):
        self.driver.get(self.url)

        self.driver.find_element_by_name('email').send_keys(login)
        self.driver.find_element_by_name('pass').send_keys(password)
        self.driver.find_element_by_name('login').click()

    def go_to_facebook_profile(self):
        try:
            self.wait.until(EC.visibility_of_element_located((By.XPATH, BOOKMARKS_URL)))
            self.driver.find_element_by_xpath(BOOKMARKS_URL).click()

            self.wait.until(EC.visibility_of_element_located((By.XPATH, BOOKMARKS_PROFILE_URL)))
        except TimeoutException:
            self.driver.find_element_by_xpath(PROFILE_URL).click()

        self.driver.find_element_by_xpath(BOOKMARKS_PROFILE_URL).click()
        time.sleep(3)

    def go_to_facebook_friends(self):
        self.go_to_facebook_profile()
        self.driver.find_element_by_xpath(A_HREF + self.driver.current_url + FRIENDS_URL).click()
        time.sleep(3)

    def get_web_elements_of_friends(self):
        return self.driver.find_elements_by_xpath(FRIENDS_WEB_ELEMENTS)

    def get_links_of_friends(self):
        return self.driver.find_elements_by_xpath(FRIENDS_WEB_ELEMENTS_LINKS)

    def get_facebook_friends_list(self):
        self.go_to_facebook_friends()

        count_of_loaded_friends = len(self.get_web_elements_of_friends())

        while True:
            self.driver.execute_script(SCROLL_SCRIPT)

            try:
                self.wait.until(lambda driver: len(self.get_web_elements_of_friends()) > count_of_loaded_friends)

                count_of_loaded_friends = len(self.get_web_elements_of_friends())
            except TimeoutException:
                break

        names = [friend_name.text for friend_name in self.get_web_elements_of_friends()]
        links = [friend_link.get_attribute('href') for friend_link in self.get_links_of_friends()]

        list_of_all = []
        for i in range(0, count_of_loaded_friends):
            list_of_all.append(names[i] + "\n" + links[i])

        self.driver.quit()

        return list_of_all


if __name__ == '__main__':
    login = input('Please input login: ')
    password = getpass.getpass(prompt="Please insert your password: ")

    friends = FacebookFriends(login=login, password=password)
    csv_file = CSVFile(CSV_PATH, friends.get_facebook_friends_list())
    csv_file.write_to_csv()
