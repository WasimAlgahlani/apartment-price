from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import lxml
from time import sleep

ZILLOW_URL = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"
FORM_URL = "https://forms.gle/SzzR3EijxH2u5YvF6"
PATH = "C:/Development/chromedriver.exe"
FORM_REPLIES = "https://docs.google.com/forms/d/1pBY0CWDuA93UYc1jhDfgLor34xHPd7BXPUiO5K-ynWM/edit#responses"


class ApartmentsRent:
    def __init__(self):
        response = requests.get(ZILLOW_URL, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9,ar;q=0.8"}, timeout=10000)
        zillow_webpage = response.text
        self.addresses = []
        self.prices = []
        self.links = []
        self.soup = BeautifulSoup(zillow_webpage, "lxml")

    def get_addresses(self):
        addresses_tag = self.soup.find_all(name="address", class_="list-card-addr")
        for address in addresses_tag:
            self.addresses.append(address.getText())

    def get_prices(self):
        prices_tag = self.soup.find_all(name="div", class_="list-card-price")
        for price in prices_tag:
            price_text = price.getText()
            self.prices.append(price_text.split('+')[0])

    def get_links(self):
        links_tags = self.soup.find_all(name="a", class_="list-card-link")
        for link in links_tags:
            href = link.get("href")
            if "http" not in href:
                self.links.append(f"https://www.zillow.com{href}")
            else:
                self.links.append(href)

    def fill_form(self):
        driver = webdriver.Chrome(executable_path=PATH)
        driver.get(FORM_URL)
        sleep(30)
        ques1 = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
        ques2 = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
        ques3 = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
        send = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span')
        for ques in range(len(self.prices)):
            ques1.send_keys(self.addresses[ques])
            ques2.send_keys(self.prices[ques])
            ques3.send_keys(self.links[ques])
            send.click()
            sleep(10)
            send_another = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
            send_another.click()
            sleep(10)
        driver.get(FORM_REPLIES)
        sleep(15)
        spreadsheet = driver.find_element_by_xpath('//*[@id="ResponsesView"]/div/div[1]/div[1]/div[2]/div[1]/div/div')
        spreadsheet.click()
        sleep(5)
        create = driver.find_element_by_xpath('//*[@id="wizViewportRootId"]/div[10]/div/div[2]/div[3]/div[2]/span/span')
        create.click()
