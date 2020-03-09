import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from makecsv import createcsv


def scrollDown(driver, numberOfScrollDowns):
    body = driver.find_element_by_tag_name("body")
    while numberOfScrollDowns >= 0:
        body.send_keys(Keys.PAGE_DOWN)
        numberOfScrollDowns -= 1
    return driver


def lookForDates(dates, driver):
    looking = True
    while looking:
        try:
            date = driver.find_element_by_xpath("//td[@data-date={}]".format(dates))
            driver.execute_script("arguments[0].click();", date)
            looking = False
        except:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.bui-calendar__control--next')))
            driver.find_element_by_css_selector(".bui-calendar__control--next").click()


def manDatepicker(driver, indates, outdates):
    indates = "\"" + indates + "\" "
    outdates = "\"" + outdates + "\" "
    driver.find_element_by_css_selector(".sb-date-field__icon.sb-date-field__icon-btn.bk-svg-wrapper.calendar-restructure-sb").click()
    lookForDates(indates, driver)
    lookForDates(outdates, driver)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button.sb-searchbox__button")))

    driver.find_element_by_css_selector("button.sb-searchbox__button").click()


def generateBookingUrl(driver, location, indates, outdates):
    time.sleep(2)
    locbox = driver.find_element_by_xpath("//input[@name='ss' and @id='ss']")
    locbox.send_keys(location)
    manDatepicker(driver, indates, outdates)
    time.sleep(4)
    return location


def booking(location, indates, outdates):
    url = "https://www.booking.com"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % "1920,1080")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    classnameHotel = "sr-hotel__name"
    classnamePrice = "bui-u-sr-only"
    pages_remaining = True
    generateBookingUrl(driver, location, indates, outdates)
    hotelList = []
    priceList = []
    originalPrice = []
    boolmore = True
    rating = []
    csvArr = []
    numofelements = driver.find_element_by_class_name("sr_header").text.strip('\n').split(' ')[1]
    try:
        while pages_remaining and boolmore:
            scrollDown(driver, 10)
            elemhotelList = driver.find_elements_by_class_name(classnameHotel)
            for element in elemhotelList:
                hotelList.append(element.get_attribute('innerHTML').strip("\n").replace("&amp;", "&"))

            rawelempriceList = driver.find_elements_by_class_name(classnamePrice)
            priceListtemp = []
            for i, element in enumerate(rawelempriceList):
                rawelempriceList[i] = element.get_attribute('innerHTML')
                rawelempriceList[i] = rawelempriceList[i].replace("€&nbsp;", "").strip("\n")
                if not ("Max persons:" in rawelempriceList[i] or "Max people:" in rawelempriceList[i]):
                    if ("Current price" in rawelempriceList[i]):
                        modprice = rawelempriceList[i].splitlines()
                        priceListtemp.append(int(modprice[3].replace(",", "")))
                        originalPrice.append(int(modprice[1].replace(",", "")))
                    else:
                        modprice = rawelempriceList[i].splitlines()
                        priceListtemp.append(int(modprice[1].replace(",", "")))

            rawsoldOut = driver.find_elements_by_css_selector(".sr_item_default")
            for element in rawsoldOut:
                rating.append(element.get_attribute('data-score').strip("\n").strip())
            soldOut = []
            rawsoldOut = driver.find_elements_by_css_selector(".sr_item_default")
            count = 0
            for i, element in enumerate(rawsoldOut):
                count += 1
                rawsoldOut[i] = element.get_attribute('innerHTML')
                if any(x in rawsoldOut[i] for x in ["You missed it", "sold out on our site"]):
                    soldOut.append(i)
            for i in soldOut:
                priceListtemp.insert(i, "")
            priceList.extend(priceListtemp)
            nomore = driver.find_element_by_class_name("bui-alert__text").text
            if "No properties left" in nomore:
                print("No more properties left")
                boolmore = False
                continue
            try:
                next_link = driver.find_element_by_css_selector(".bui-pagination__link.paging-next")
                driver.execute_script("arguments[0].click();", next_link)
                time.sleep(3)

            except:
                pages_remaining = False
                # driver.quit()
        csvArr = zip(hotelList, priceList, rating)
        fig = createcsv(csvArr, location, "booking", 1)
        driver.close()
        return fig

    except KeyboardInterrupt:
        driver.quit()


#if __name__ == '__main__':
#    booking("carcabuey", "2020-03-26", "2020-03-29")

