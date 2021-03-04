from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import os
import time

PROMISED_DOWN = 150
PROMISED_UP = 10
CHROME_DRIVER_PATH = os.environ.get("CHROME_DRIVER_PATH")
TWITTER_EMAIL = "@Goona91"
TWITTER_PASSWORD = os.environ.get("EMAIL_PASSWORD")

class InternetSpeedTwitterBot:

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
        self.driver.maximize_window()
        self.up = 0
        self.down = 0

    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/")
        go_button = self.driver.find_element_by_xpath("//*[@id='container']/div/div[3]/div/div/div/div[2]/div[3]/div[1]/a")
        go_button.click()
        time.sleep(60)
        search_down = self.driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span').text
        self.down = float(search_down)
        search_up = self.driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[3]/div/div[2]/span').text
        self.up = float(search_up)

    def find_xpath_element(self, xpath):
        is_found = False
        element = None
        while not is_found:
            try:
                time.sleep(3)
                element = self.driver.find_element_by_xpath(xpath)
                is_found = True
            except NoSuchElementException:
                is_found = False
        return element

    def tweet_at_provider(self):
        self.driver.get("https://twitter.com/?lang=en")

        time.sleep(3)

        login_button = self.find_xpath_element(
            "//*[@id='react-root']/div/div/div/main/div/div/div/div[1]/div/div[3]/a[2]"
        )
        login_button.click()

        time.sleep(3)

        email = self.find_xpath_element('/html/body/div/div/div/div[2]/main/div/div/div[2]/form/div/div[1]/label')
        email.click()
        time.sleep(0.3)
        email.send_keys(TWITTER_EMAIL)

        password = self.find_xpath_element(
            '/html/body/div/div/div/div[2]/main/div/div/div[2]/form/div/div[2]/label')
        password.click()
        time.sleep(0.3)
        password.send_keys(TWITTER_PASSWORD)
        password.send_keys(Keys.ENTER)

        tweet_compose = self.find_xpath_element('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div[2]/div')
        tweet = f"Hey Internet Provider, why is my internet speed {self.down}down/{self.up}up when I pay for {PROMISED_DOWN}down/{PROMISED_UP}up?"
        tweet_compose.send_keys(tweet)
        time.sleep(3)

        tweet_button = self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[4]/div/div/div[2]/div[3]')
        tweet_button.click()


bot = InternetSpeedTwitterBot()
bot.get_internet_speed()
if bot.up < PROMISED_UP or bot.down < PROMISED_DOWN:
    bot.tweet_at_provider()

