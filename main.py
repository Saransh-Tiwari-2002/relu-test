from time import sleep, time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from json import dumps, load
from os.path import join, dirname, join
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import threading
import csv
from compile_json import compile_json
from mysql_upload import mysql_upload

with open('C:\Python\\relu-test\Amazon Scraping - Sheet1.csv', 'r') as file:
    spamreader=list(csv.reader(file))[1:]           #reading the initial csv file containing asin, country combos

def start_driver():
    chrome_options=uc.ChromeOptions()
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"
    #chrome_options.binary_location = os_environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument(f'user-agent={UserAgent().random}')
    #launching a webdriver instance
    driver = uc.Chrome(options=chrome_options, use_subprocess=True, desired_capabilities=caps,version_main=102)
    return driver
    
def fix_json(temp_dict, filename):
    try:
        with open(f'C:\Python\\relu-test\\{filename}.json', 'r') as a:
            json_data = load(a)         #loading the thread specific json file into a dict variable
    except:
        json_data={}
    json_data.update({len(json_data):temp_dict})
    with open(join(dirname(__file__), f'{filename}.json'), 'w') as f:
        f.write(dumps(json_data, indent=4))    #dumping the upadated info into the thread specific json file

def scrape(asin, country, driver, filename):
    driver.get(f'https://www.amazon.{country}/dp/{asin}')       
    sleep(5)            #inducing a 5 second delay to let the page load
    if(len(driver.find_elements(by=By.XPATH, value='//a[@href="/ref=cs_404_logo/"]'))):
        print(f'https://www.amazon.{country}/dp/{asin}')
        return False   #returning False in case of 404 error
    try:
        try: 
            #accepting all cookies
            driver.find_element(by=By.XPATH, value='//input[@class="a-button-input celwidget"]').click()
            sleep(3)
        except: pass
        #fetching the relevant product info
        ptitle=driver.find_element(by=By.XPATH, value='//span[@id="productTitle"]').text
        #using error handling to adjust for different page layouts
        try: pimageurl=driver.find_element(by=By.XPATH, value='//img[@id="imgBlkFront"]').get_attribute('src')
        except: pimageurl=driver.find_element(by=By.XPATH, value='//img[@id="landingImage"]').get_attribute('src')
        try: pprice=driver.find_element(by=By.XPATH, value='//span[@class="a-price aok-align-center reinventPricePriceToPayMargin priceToPay"]').text
        except: pprice=driver.find_element(by=By.XPATH, value='//span[@class="a-color-base"]').text
        temp={'Title': ptitle,'Image URL':pimageurl, 'Price':pprice}
        try:        #using error handling to adjust for different page layouts
            ul_from_xpath=driver.find_element(by=By.XPATH, value='//ul[@class="a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list"]')
            all_li = ul_from_xpath.find_elements(by=By.TAG_NAME, value='li')
            for li in all_li:
                field_name=li.find_element(by=By.XPATH, value='.//span[@class="a-text-bold"]').text
                field_value=li.find_element(by=By.XPATH, value='.//span[@class="a-text-bold"]/following-sibling::span').text
                temp.update({field_name:field_value})
        except:
            for x in driver.find_element(by=By.XPATH, value='//table[@id="productDetails_techSpec_section_1"]').find_elements(by=By.XPATH, value='.//th[@class="a-color-secondary a-size-base prodDetSectionEntry"]'):
                field_name=x.text
                field_value=x.find_element(by=By.XPATH, value='.//following-sibling::td').text
                temp.update({field_name:field_value})
        fix_json(temp, filename)        #updating the thread specific json file
        return True
    except: 
        return False                    #returning False in case of any error

def main(filename, start=0, end=1000):
    driver=start_driver()                               #staring a webdriver instance
    for x in spamreader[start:end]:
        if(scrape(x[2], x[3], driver, filename)):       #condition is True upon successful product info extraction
            pass
        else:                                           #closing and restarting the webdriver instance in case of failure
            driver.close()
            driver=start_driver()
    driver.close()

start_count=0
end_count=50
threads = [] 

start_time=time()
for link in range(20): # each thread could be like a new 'click' 

    random_file_name=f'filenumber{link}'
    th = threading.Thread(target=main, args=(random_file_name,start_count, end_count,))    
    start_count+=50
    end_count+=50
    th.start() # could `time.sleep` between 'clicks' to see whats'up without headless option
    threads.append(th)        
for th in threads:
    th.join() # Main thread wait for threads finish
print('FINAL TIME: ', time()-start_time)
compile_json('new')
print('JSON FILE CREATED')
mysql_upload()
print('DATA DUMPED TO SQL')