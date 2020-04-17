#coding:utf-8
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select,WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import chromedriver_binary
import sys
import re
import csv
import time

def get_urls(args):
    """
    
    """
    urls = []
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome() 
    wait = WebDriverWait(driver,10)
    URL = "https://db.netkeiba.com/?pid=race_search_detail"
    driver.get(URL)
    time.sleep(1)
    wait.until(EC.presence_of_all_elements_located)

    #?????

    start_year = args[1]
    start_mon = args[2]
    end_year = args[3]
    end_mon = args[4]

    start_year_element = driver.find_element_by_name('start_year')
    start_year_select = Select(start_year_element)
    start_year_select.select_by_value(str(start_year))
    start_mon_element = driver.find_element_by_name('start_mon')
    start_mon_select = Select(start_mon_element)
    start_mon_select.select_by_value(str(start_mon))
    end_year_element = driver.find_element_by_name('end_year')
    end_year_select = Select(end_year_element)
    end_year_select.select_by_value(str(end_year))
    end_mon_element = driver.find_element_by_name('end_mon')
    end_mon_select = Select(end_mon_element)
    end_mon_select.select_by_value(str(end_mon))

    for i in range(1,11):
        terms = driver.find_element_by_id("check_Jyo_"+ str(i).zfill(2))
        terms.click()
    #???????????100????
    list_element = driver.find_element_by_name('list')
    list_select = Select(list_element)
    list_select.select_by_value("100")

    frm = driver.find_element_by_css_selector("#db_search_detail_form > form")
    frm.submit()
    time.sleep(10)
    wait.until(EC.presence_of_all_elements_located)
    while True:
        time.sleep(10)
        wait.until(EC.presence_of_all_elements_located)
        all_rows = driver.find_element_by_class_name('race_table_01').find_elements_by_tag_name("tr")
        for row in range(1, len(all_rows)):
            race_href=all_rows[row].find_elements_by_tag_name("td")[4].find_element_by_tag_name("a").get_attribute("href")
            urls.append(race_href)
        try:
            target = driver.find_elements_by_link_text("次")[0]
            time.sleep(4)
            driver.execute_script("arguments[0].click();", target)
        except IndexError:
            break
    return urls
