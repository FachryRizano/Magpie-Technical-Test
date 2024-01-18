import pandas as pd

import time
import json
from selenium import webdriver
import undetected_chromedriver as uc
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC

# import chromedriver_autoinstaller


# chromedriver_autoinstaller.install()

class TokopediaScraper:
    def __init__(self):
        
        firefox_options = Options()
        firefox_options.add_argument("--window-size=1920,1080")
        firefox_options.add_argument("--disable-extensions")
        firefox_options.add_argument("--proxy-server='direct://'")
        firefox_options.add_argument("--proxy-bypass-list=*")
        firefox_options.add_argument("--start-maximized")
        firefox_options.add_argument('--headless')
        firefox_options.add_argument('--disable-gpu')
        firefox_options.add_argument('--disable-dev-shm-usage')
        firefox_options.add_argument('--no-sandbox')
        firefox_options.add_argument('--ignore-certificate-errors')
        firefox_options.add_argument('--allow-running-insecure-content')
        firefox_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
        firefox_options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
        
        #Chrome
        # self.driver = uc.Chrome(service=Service(), options=chrome_options)
        
        service = Service(executable_path='geckodriver.exe')
        self.driver = webdriver.Firefox(options=firefox_options,service=service)
        # self.driver.maximize_window()
        self.driver.get("https://www.tokopedia.com/")
        # time.sleep(1000)
    def search_product(self,keyword):
        # self.driver.get_screenshot_as_file("screenshot.png")
        wait = WebDriverWait(self.driver, 10)
        search_bar = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[1]/div/div/div[2]/div[2]/div/div/div/div/input")))
        search_bar.send_keys(keyword)
        search_bar.send_keys(Keys.RETURN)
    
    def scroll_on(self):
        i = 1
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom smoothly
            for i in range(0, last_height, 100):  # Scroll step is set to 100 pixels
                self.driver.execute_script(f"window.scrollTo(0, {i});")
                time.sleep(0.05)  # Small delay to mimic smooth scrolling
                # Check next page button exist or not, if exist it will stop scrolling
                try:
                    next_btn = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div/div[2]/div/div[2]/div[5]/nav/ul/li[11]/button')
                    if next_btn:
                        break
                except:
                    next_btn = None
                    pass
            # Wait to load page
            time.sleep(2)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height or next_btn != None:
                break
            last_height = new_height
    
    def scrape_page(self,page):
        product_data = []
        # print(f"==========PAGE {page}==============")
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, f'/html/body/div[1]/div/div[2]/div/div[2]/div[4]')))
        
        all_batch_product_parent= self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div[2]')
        all_batch_product= all_batch_product_parent.find_elements(By.XPATH, f'./div[@data-ssr="contentProductsSRPSSR"]/div')
        for batch_product in all_batch_product:
            products = batch_product.find_elements(By.XPATH,"./div")
            # print(len(products))
            for product in products:
                # print(product.text)
                #Search product
                try:
                    parent_metadata = product.find_element(By.XPATH,"./div/div/div/div/div/div[2]/a")
                except:
                    #Shop nearby
                    parent_metadata = product.find_element(By.XPATH,"./div[2]/div[1]/div/div/div/div/div/div[2]/a")
                sku_name = parent_metadata.find_element(By.XPATH,"./div[contains(@class, 'prd_link-product-name')]").text
                price = parent_metadata.find_element(By.XPATH,"./div[@class='']/div[@class='']/div[contains(@class, 'prd_link-product-price')]").text
                # If element is empty, that means sold is 0
                try:
                    sold = parent_metadata.find_element(By.XPATH,"./div[@data-productinfo='true']/div[2]/span[3]").text
                except:
                    sold = 0
                product_data.append({
                    "sku_name": sku_name,
                    "price": price,
                    "sold": sold,
                    "page": page  
                })
        return pd.DataFrame(product_data)
    def next_page(self):
        stop_flag = False
        wait = WebDriverWait(self.driver, 10)
        try:
            parent_next_btn = wait.until(EC.presence_of_element_located((By.XPATH, f'/html/body/div[1]/div/div[2]/div/div[2]/div[5]'))).find_element(By.XPATH,"./nav/ul")
        except:
            parent_next_btn = wait.until(EC.presence_of_element_located((By.XPATH, f'/html/body/div[1]/div/div[2]/div/div[2]/div[4]'))).find_element(By.XPATH,"./nav/ul")
        next_btn = parent_next_btn.find_elements(By.XPATH,"./li")[-1].find_element(By.XPATH,"./button")
        if next_btn.is_enabled():
            self.driver.execute_script("arguments[0].scrollIntoView();",next_btn)
            self.driver.execute_script("arguments[0].click();",next_btn)
        else:
            stop_flag = True
        return stop_flag
        # self.driver.quit()
    def close_browser(self):
        self.driver.quit()
        
def post_processing(df):
    # Harga
    # Jumlah penjualan
    # Estimasi GMV (harga * jumlah penjualan)
    df["sold"] = df["sold"].apply(lambda x: int(x.split()[0].replace("+","").replace("rb","000")) if x!=0 else x)
    df['price'] = df['price'].apply(lambda x:int(x.replace(".","").replace("Rp","")))
    df['gmv_estimation'] = df['price'] * df['sold']
    return df
    


# Scraping
df = pd.read_csv("input.csv")
temp = pd.DataFrame(columns=["sku_name","price","sold",'page',"keyword"])
for i,row in df.iterrows():
    print(f"{'='*8}Scraping {row['keyword']}{'='*8}")
    t = TokopediaScraper()
    pages = int(row['pages'])
    # t.search_product(row['keyword'])
    t.search_product(row['keyword'])
    for i in range(pages):
        stop_flag = False
        t.scroll_on()
        result_df = t.scrape_page(i+1)
        result_df['keyword'] = row['keyword']
        temp = pd.concat([result_df,temp])
        if pages != 1 and i < pages - 1:
            stop_flag = t.next_page()
            if stop_flag:
                break
    t.close_browser()
temp.to_csv(f"scrape_result.csv",index=False,sep=";")
print("Scraping done")
#Post Processing
final_postprocess = post_processing(temp)
final_postprocess.to_csv("post_process.csv",index=False,sep=";")
print("Post Processing done")
# t.scrape_products_in_page()
