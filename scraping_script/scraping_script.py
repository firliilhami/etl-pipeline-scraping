# scraping barang dan harga tokopedia
# hasil scraping akan distore pada table landing.scraping
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from main import scraping 

# connect selenium 
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1420,1080')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"')
driver = webdriver.Chrome(options=chrome_options)

#website
list_URL = [
    "https://www.tokopedia.com/search?navsource=home&page=1&q=acer%20swift%203%20infinity%204&st=product",
    "https://www.tokopedia.com/search?navsource=home&page=1&q=lenovo%20ideapad%20slim%205&st=product",
    "https://www.tokopedia.com/search?st=product&q=asus&navsource=home",
    "https://www.tokopedia.com/search?navsource=home&page=1&q=laptop%20ROG&st=product",
    "https://www.tokopedia.com/search?navsource=home&page=2&q=macbook%20pro&st=product",
]


connection_string = 'postgresql+psycopg2://username:password@postgres-service:5432/database'

engine = create_engine(connection_string,echo=True)
# make local session to access database
Session = sessionmaker()
local_session = Session(bind=engine)
j
for URL in list_URL :
    driver.get(URL)
    driver.maximize_window()
    print(driver.title)
    # dapetin barang
    time.sleep(12)
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # time.sleep(7)
    list_barang = driver.find_elements(By.CLASS_NAME,'css-12sieg3')
    for barang in list_barang :
        try :
            product = barang.find_element(By.CLASS_NAME,'css-12fc2sy').text
            price = barang.find_element(By.CLASS_NAME,'css-a94u6c').text
            #insert data to table
            new_data=scraping(product=product,price=price)
            local_session.add(new_data)
            local_session.commit()
        
            print(product)
            print(price)
            print()

        except Exception as error:
            pass
            
driver.quit()