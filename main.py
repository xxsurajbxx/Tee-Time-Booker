import settings
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import WebDriverException, ElementNotInteractableException, NoSuchElementException
from time import sleep

COURSES = [6318, 6319, 6323, 6324] # Mercer Oaks West, Mercer Oaks East, Princeton Country Club, Mountain View

bookingDate = (datetime.datetime.now() + datetime.timedelta(days=7)).strftime("%m-%d-%Y")

PATH = "C:\Program Files (x86)\chromedriver.exe"

try:
    ops = webdriver.chrome.options.Options()
    ops.add_argument("--headless")
    driver = webdriver.Chrome(executable_path=PATH, options=ops)
    driver.implicitly_wait(5)
except WebDriverException:
    print("error")
    driver.quit()
    exit()

driver.get(settings.LOGIN_PAGE)
driver.find_element_by_id("login_email").send_keys(settings.CREDENTIALS["username"])
driver.find_element_by_id("login_password").send_keys(settings.CREDENTIALS["password"])
driver.find_element_by_xpath("//div[@id=\"submit_button\"]/input").click()
driver.find_element_by_id("reservations-tab").click()
driver.find_element_by_xpath("//a[@class=\"btn btn-primary\"][@href=\"#/teetimes\"][text()=\"Reserve a time now.\"]").click()
coursesDropDown = driver.find_element_by_id("schedule_select")
for c in coursesDropDown.find_elements_by_tag_name("option"):
    if c.get_attribute("value") == str(COURSES[settings.course-1]):
        c.click()
        break
driver.find_element_by_xpath("//button[@class='btn btn-primary col-md-4 col-xs-12 col-md-offset-4'][text()=\"Resident Member\"]").click()
e = driver.find_element_by_id("date-field")
try:
    num = len(e.get_attribute("value"))
    for i in range(num):
        e.send_keys(Keys.BACKSPACE)
    e.send_keys(bookingDate)
except ElementNotInteractableException:
    try:
        e.find_element_by_xpath("//option[@value=\"{}\"]".format(bookingDate)).click()
    except NoSuchElementException:
        print("\n\n\ntee times aren't out yet\n\n\n")
        driver.quit()
        exit()
sleep(3)
try:
    driver.find_element_by_class_name("reserve-time").click()
    options = driver.find_element_by_xpath("//div[@class=\"btn-group btn-group-justified players\"]")
    for option in options.find_elements_by_tag_name("a"):
        if option.get_attribute("data-value") == str(settings.players) and option.get_attribute("class") != "btn btn-primary active":
            option.click()
            break
    options = driver.find_element_by_xpath("//div[@class=\"btn-group btn-group-justified carts\"]")
    for option in options.find_elements_by_tag_name("a"):
        if carting and option.get_attribute("data-value") == "yes" and option.get_attribute("class") == "btn btn-primary":
            option.click()
        elif not carting and opiton.get_attribute("data-value") == "no" and option.get_attribute("class") == "btn btn-primary":
            option.click()
except NoSuchElementException:
    print("No times available")
    driver.quit()
    exit()
driver.find_element_by_xpath("//button[@type=\"button\"][@class=\"btn btn-success book pull-left\"][text()=\"Book Time\"]").click()
driver.quit()