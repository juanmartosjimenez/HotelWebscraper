import time
import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, expected_conditions
from makecsv import createcsv


def scrollDown(driver, numberOfScrollDowns):
    body = driver.find_element_by_tag_name("body")
    while numberOfScrollDowns >= 0:
        body.send_keys(Keys.PAGE_DOWN)
        numberOfScrollDowns -= 1
    return driver


def selectdates(driver, indate):
    notAvailable = True
    while notAvailable:
        dateo = datetime.datetime.strptime(indate, '%Y-%m-%d')
        date = dateo.strftime("%a %b %d %Y")
        time.sleep(0.5)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, '_1HphCM4i')))
        time.sleep(2)
        try:
            driver.find_element_by_xpath("//div[@aria-label=\"{}\"]".format(date)).click()
            notAvailable = False
        except:
            driver.find_element_by_css_selector(
                '.hotels-calendar-calendar__navButton--21dqp.hotels-calendar-calendar__next--1svjm').click()
    return dateo


def entersearch(driver, location):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, '.ui_icon.hotels.brand-quick-links-QuickLinkTileItem__icon--2iguo')))
    time.sleep(4)
    driver.find_element_by_css_selector('.ui_icon.hotels.brand-quick-links-QuickLinkTileItem__icon--2iguo').click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'Smftgery')))
    time.sleep(2)
    element = driver.find_element_by_class_name('Smftgery')
    element.send_keys(location)
    time.sleep(2)
    element.send_keys(Keys.RETURN)
    time.sleep(2)


def tripadvisor(location, indate, outdate):
    pages_remaining = True
    fullhotelname = []
    fullhotelprice = []
    fullhotelrating = []
    url = "https://www.tripadvisor.com"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % "1920,1080")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    entersearch(driver, location)
    firstdate = selectdates(driver, indate)
    time.sleep(5)
    seconddate = selectdates(driver, outdate)
    datediff = (seconddate - firstdate).days
    moreprice = True
    while pages_remaining:
        time.sleep(5)
        scrollDown(driver, 50)
        time.sleep(8)
        hotelprice = []
        if moreprice:
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.price")))
                elemhotelprice = driver.find_elements_by_css_selector("div.price-wrap")
                print(elemhotelprice[0].text)
                hotelprice.extend([float(element.text.split("\n")[-1].replace("€", "")) for element in elemhotelprice])  # *datediff
            except Exception as e:
                print(e)
                moreprice = False
        try:
            elemhotelprice = driver.find_elements_by_css_selector("div.note")
            for i in elemhotelprice:
                hotelprice.append("")
        except Exception as e:
            print(e)
            pass

        print(hotelprice, "hotelprice")
        fullhotelprice.extend(hotelprice)
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'listing_title')))
        elemhotelname = driver.find_elements_by_css_selector("a.property_title")
        # ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
        # your_element = WebDriverWait(driver, 3, ignored_exceptions=ignored_exceptions).until(expected_conditions.presence_of_element_located((By.ID, my_element_id)))
        hotelname = []
        for element in elemhotelname:
            hotelname.append(element.text)
        print(hotelname, "hotelname")
        fullhotelname.extend(hotelname)
        rawallreviews = driver.find_elements_by_css_selector('a[data-clicksource="ReviewCount"]')
        totalreviews = [element.text.strip("\n").split(' ')[0].replace(",", "") for element in rawallreviews]
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
                (By.XPATH, '//*[contains(@class, "ui_bubble_rating") and contains(@class, "bubble_")]')))
            elemhotelrating = driver.find_elements_by_xpath(
                '//*[contains(@class, "ui_bubble_rating") and contains(@class, "bubble_")]')
            rawhotelrating = [element.get_attribute('alt') for element in elemhotelrating]
            rawhotelrating = list(filter(lambda x: x != None, rawhotelrating))
            rawhotelrating = [float(x.split(' ')[0]) * 2 for x in rawhotelrating]
        except Exception as e:
            pages_remaining=False
            print(e)
            pass
        hotelrating = []
        counter = 0
        for i, reviews in enumerate(totalreviews):
            if int(reviews) > 0:
                hotelrating.append(rawhotelrating[counter])
                counter += 1
            else:
                hotelrating.append("")
        print(hotelrating, "hotel rating")
        fullhotelrating.extend(hotelrating)
        try:
            nextbutton = driver.find_element_by_css_selector(".nav.next.ui_button.primary")
            driver.execute_script("arguments[0].click();", nextbutton)
            if len(driver.find_elements_by_css_selector(".nav.next.ui_button.primary.disabled")) == 1:
                pages_remaining = False
                continue
            print("next page")
        except Exception as e:
            print(e)
            print("Driver shutdown")
            pages_remaining = False
    csvArr = zip(fullhotelname, fullhotelprice, fullhotelrating)
    fig = createcsv(csvArr, location, "tripadvisor", 2)
    driver.close()
    print("driver shutdown")
    return fig


if __name__ == '__main__':
    tripadvisor("carcabuey", "2020-03-26", "2020-03-29")

