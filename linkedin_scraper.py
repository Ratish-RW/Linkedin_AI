import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import json

class LinkedInScraper:
    def __init__(self,url:str,feed: str,total: int,cookie_file: str = "cookie.json"):
        self.url = url
        self.cookie_file = cookie_file
        self.options = uc.ChromeOptions()
        self.options.add_argument("--headless=new")  
        self.options.add_argument("--disable-gpu")    
        self.options.add_argument("--no-sandbox")    
        self.options.add_argument("--disable-dev-shm-usage")
        self.driver = uc.Chrome(options=self.options)
        self.wait = WebDriverWait(self.driver,30)
        self.feed = feed
        self.seen_ids = set()
        self.profiles = []
        self.total = total


    def load(self):
        self.driver.get(self.url)
        time.sleep(2)
        try:
            with open(self.cookie_file, "r") as f:
                cookies = json.load(f)
            for cookie in cookies:
                cookie.pop("sameSite", None) 
                try:
                    self.driver.add_cookie(cookie)
                except Exception as e:
                    print(f"Skipping cookie {cookie.get('name')} due to: {e}")
            self.driver.refresh()
            #print("Cookies added Successfully\n")
            return {"status":"success","message":"cookies added successfully"}
        except Exception:
            #print("Error in Cookies\n")
            return {"status":"failure","message":f"error in cookies\n {str(Exception)}"}   

    def search_feed(self):
        try:
            self.search_feed_input_xpath = '//*[@id="global-nav-typeahead"]/input'
            self.elements_xpath = '//*[@id="search-reusables__filters-bar"]/ul'
            self.posts_xpath = self.elements_xpath
            self.posts_feed_classname = 'scaffold-finite-scroll__content'
            self.date_posted_btn_id = 'searchFilter_datePosted'
            self.date_posted_form_id = 'hoverable-outlet-date-posted-filter-value'

            self.search_feed_input = self.wait.until(EC.presence_of_element_located((By.XPATH,self.search_feed_input_xpath)))
            self.search_feed_input.send_keys(self.feed)
            self.search_feed_input.send_keys(Keys.RETURN)
            #print("Feed Search Done Successfully\n")
            return {"status": "success","message":"feed search done successfully"}
        except Exception:
            #print("Error in Feed Search\n")
            return {"status":"failure","error":f"error in feed search \n{str(Exception)}"}

    def search_by_posts(self):
        try:
            elements = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, self.elements_xpath)))
            items = elements[0].text.split("\n")
            for i, it in enumerate(items):
                if it == "Posts":
                    self.posts_xpath = f"{self.posts_xpath}/li[{i+1}]/button"
                    break
            posts_btn = self.wait.until(EC.presence_of_element_located((By.XPATH,self.posts_xpath)))
            posts_btn.click()
            #print("Post button Clicked Successfully\n")
            return {"status":"success","message":"post button clicked successfully"}
        except Exception:
            #print("Error in Post button")
            return {"status":"failure","error":f"error in post button \n{str(Exception)}"}
    
    def click_date_posted(self):
        try:
            date_posted_btn = self.wait.until(EC.element_to_be_clickable((By.ID,self.date_posted_btn_id)))
            date_posted_btn.click()

            date_posted_form = self.wait.until(EC.presence_of_all_elements_located((By.ID,self.date_posted_form_id)))
            date_posted_id = date_posted_form[0].find_elements(By.XPATH,"./div[@id]")[0].get_attribute("id")

            date_posted_past24hrs_xpath = f'//*[@id="{date_posted_id}"]/div[1]/div/form/fieldset/div[1]/ul/li[1]/label'
            date_posted_past24hrs_radio_btn = self.driver.find_element(By.XPATH,date_posted_past24hrs_xpath)
            date_posted_past24hrs_radio_btn.click()

            date_posted_form_btns_xpath = f'//*[@id="{date_posted_id}"]/div[1]/div/form/fieldset/div[2]'
            date_posted_form_btns = self.driver.find_elements(By.XPATH,date_posted_form_btns_xpath)
            for btns in date_posted_form_btns:
                btns = btns.find_elements(By.XPATH,"./button[@id]") 
                for btn in btns:
                    btn_id = btn.get_attribute("id")
                    btn_name_xpath = f'//*[@id="{btn_id}"]/span'
                    btn_name = self.driver.find_element(By.XPATH,btn_name_xpath).text
                    if btn_name == "Show results":
                        show_results_btn_xpath = f'//*[@id="{btn_id}"]'
                        show_results_btn = self.driver.find_element(By.XPATH,show_results_btn_xpath)
                        show_results_btn.click()
                        #print("Show results button clicked successfully")
                        return {"status":"success","message":"show results filter button clicked successfully"}
        except Exception:
            #print("Error in Date Posted")
            return {"status":"failure","error":f"error in date posted filter\n{str(Exception)}"}
    
    def get_data(self):
        try:
            while len(self.profiles) < self.total:
                feeds_list = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,self.posts_feed_classname)))
                for feeds in feeds_list:
                    feeds_id_divs = feeds.find_elements(By.XPATH,"./div[@id]")
                    for divs in feeds_id_divs:
                        feeds_id = divs.get_attribute("id")
                        if feeds_id in self.seen_ids:
                            continue
                        self.seen_ids.add(feeds_id)
                        feeds = self.wait.until(EC.presence_of_all_elements_located((By.XPATH,f'.//*[@id="{feeds_id}"]/div/ul/li')))
                        try:
                            for feed in feeds:
                                ids_div1 = feed.find_element(By.XPATH,"./div[@id]")
                                ids1 = ids_div1.get_attribute("id")

                                feed_ids_div2 = self.driver.find_element(By.XPATH,f'.//*[@id="{ids1}"]/div/div')
                                ids_div2 = feed_ids_div2.find_element(By.XPATH,"./div[@id]")
                                ids2 = ids_div2.get_attribute("id")

                                try:
                                    profile_xpath = f'//*[@id="{ids2}"]/div/div/div[1]/div[1]/div[1]/div/div/a[1]/span[1]/span[1]/span/span[1]'
                                    profile_link_xpath = f'//*[@id="{ids2}"]/div/div/div[1]/div[1]/div[1]/div/div/a[1]'
                                    posted_by_xpath = f'//*[@id="{ids2}"]/div/div/div[1]/div[1]/div[1]/div/div/span/span[1]' 
                                    body_xpath = f'//*[@id="{ids2}"]/div/div/div[1]/div[2]/div/div/span//span'
                                    full_body_xpath = f'//*[@id="{ids2}"]/div/div/div[1]'

                                    full_body_div3 = self.driver.find_element(By.XPATH,full_body_xpath)
                                    ids_div3 = full_body_div3.find_element(By.XPATH,"./div[@id]")
                                    ids3 = ids_div3.get_attribute("id")

                                    likes_xpath = f'//*[@id="{ids3}"]/div[1]/div/div/ul/li[1]/button/span'
                                    comments_xpath = f'//*[@id="{ids3}"]/div[1]/div/div/ul/li[2]/ul/li[1]/button/span'
                                    comments_count = 0
                                    likes_count = 0
                                    # //*[@id="ember525"]/div[1]/div/div/ul/li[2]/ul/li[1]/button/span
                                    try:
                                        comments_data = self.driver.find_element(By.XPATH,comments_xpath).text
                                        comments_count = int(comments_data.split(" ")[0])
                                        #print(f"Comments: {comments_count}")
                                    except:
                                        comments_xpath = f'//*[@id="{ids3}"]/div[1]/div/div/ul/li[2]/ul/li/button/span'
                                        try:
                                            comments_data = self.driver.find_element(By.XPATH,comments_xpath).text
                                            comments_count = int(comments_data.split(" ")[0])
                                            #print(f"Comments: {comments_count}")
                                        except:
                                            likes_xpath = f'//*[@id="{ids3}"]/div[1]/div/div/ul/li/button/span'
                                    try:
                                        likes_data = self.driver.find_element(By.XPATH,likes_xpath).text
                                        likes_count = int(likes_data.split(" ")[0])
                                        #print(f'Likes: {likes_count}')
                                    except:
                                        print(f"No likes and Comments")                                

                                    profile_name = self.driver.find_element(By.XPATH,profile_xpath).text
                                    profile_link = self.driver.find_element(By.XPATH,profile_link_xpath).get_attribute("href")
                                    posted_by = self.driver.find_element(By.XPATH,posted_by_xpath).text

                                    body_datas = self.driver.find_elements(By.XPATH,body_xpath)
                                    text = " ".join(body_data.text.strip() for body_data in body_datas if body_data.text.strip())
                                    if (len(text) < 100):
                                        continue
                                    self.profiles.append({
                                        "name": profile_name,
                                        "link": profile_link,
                                        "likes": likes_count,
                                        "comments": comments_count,
                                        "data": text   
                                    })
                                    print(profile_name)
                                    
                                except:
                                    print(f"Skipping feed")
                                    continue
                        except:
                            print(f"Skipping Feed List")
                            continue
                    if len(self.profiles) < self.total:
                        self.driver.execute_script("window.scrollBy(0,1000);")
                        time.sleep(2)

            # df = pd.DataFrame(self.profiles)
            # df.to_csv("ai_data2.csv",index=False,encoding="utf-8")
            #print("CSV file saved successfully")
            return {"status":"success","message":{self.profiles}}
        except Exception:
            #print("Error in getting data")
            return {"status":"failure","error":f"error in getting data\n{str(Exception)}"}

    def close(self):
        self.driver.close()

