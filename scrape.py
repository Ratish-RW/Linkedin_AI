import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from flask import Flask,request,jsonify
from flask_cors import CORS
import pandas as pd
import time
import json


# options = uc.ChromeOptions()
# options.add_argument("--headless=new")  
# options.add_argument("--disable-gpu")    
# options.add_argument("--no-sandbox")    
# options.add_argument("--disable-dev-shm-usage")

url = "https://www.linkedin.com/"
driver = uc.Chrome()
# driver.maximize_window()
driver.get(url)
wait = WebDriverWait(driver,30)
feed = "artificial intelligence AI machine learning deep learning generative AI LLM AI research AI tools Chatgpt Gemini Llama Openai new AI technologies"

time.sleep(2)

with open("cookie.json", "r") as f:
    cookies = json.load(f)


for cookie in cookies:
    cookie.pop("sameSite", None) 
    try:
        driver.add_cookie(cookie)
    except Exception as e:
        print(f"Skipping cookie {cookie.get('name')} due to: {e}")

driver.refresh()

print("Cookies added successfully\n")

try:
    search_feed_input_xpath = '//*[@id="global-nav-typeahead"]/input'
    elements_xpath = '//*[@id="search-reusables__filters-bar"]/ul'
    posts_xpath = elements_xpath
    posts_feed_classname = 'scaffold-finite-scroll__content'
    date_posted_btn_id = 'searchFilter_datePosted'
    date_posted_form_id = 'hoverable-outlet-date-posted-filter-value'

    search_feed_input = wait.until(EC.presence_of_element_located((By.XPATH,search_feed_input_xpath)))
    search_feed_input.send_keys(feed)
    search_feed_input.send_keys(Keys.RETURN)
    print("Search feed done successfully\n")

    elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, elements_xpath)))

    items = elements[0].text.split("\n")

    for i, it in enumerate(items):
        if it == "Posts":
            posts_xpath = f"{posts_xpath}/li[{i+1}]/button"
            break

    posts_btn = wait.until(EC.presence_of_element_located((By.XPATH,posts_xpath)))
    posts_btn.click()
    print("Post button Clicked Successfully\n")

    date_posted_btn = wait.until(EC.element_to_be_clickable((By.ID,date_posted_btn_id)))
    date_posted_btn.click()

    date_posted_form = wait.until(EC.presence_of_all_elements_located((By.ID,date_posted_form_id)))
    date_posted_id = date_posted_form[0].find_elements(By.XPATH,"./div[@id]")[0].get_attribute("id")

    date_posted_past24hrs_xpath = f'//*[@id="{date_posted_id}"]/div[1]/div/form/fieldset/div[1]/ul/li[1]/label'
    date_posted_past24hrs_radio_btn = driver.find_element(By.XPATH,date_posted_past24hrs_xpath)
    date_posted_past24hrs_radio_btn.click()


    date_posted_form_btns_xpath = f'//*[@id="{date_posted_id}"]/div[1]/div/form/fieldset/div[2]'
    date_posted_form_btns = driver.find_elements(By.XPATH,date_posted_form_btns_xpath)
    for btns in date_posted_form_btns:
        btns = btns.find_elements(By.XPATH,"./button[@id]") 
        for btn in btns:
            btn_id = btn.get_attribute("id")
            btn_name_xpath = f'//*[@id="{btn_id}"]/span'
            btn_name = driver.find_element(By.XPATH,btn_name_xpath).text
            if btn_name == "Show results":
                show_results_btn_xpath = f'//*[@id="{btn_id}"]'
                show_results_btn = driver.find_element(By.XPATH,show_results_btn_xpath)
                show_results_btn.click()
                print("Show results button clicked successfully")

    seen_ids = set()
    profiles = []

    while len(profiles) < 30:
        feeds_list = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,posts_feed_classname)))
        for feeds in feeds_list:
            feeds_id_divs = feeds.find_elements(By.XPATH,"./div[@id]")
            for divs in feeds_id_divs:
                feeds_id = divs.get_attribute("id")
                if feeds_id in seen_ids:
                    continue
                seen_ids.add(feeds_id)
                feeds = wait.until(EC.presence_of_all_elements_located((By.XPATH,f'.//*[@id="{feeds_id}"]/div/ul/li')))
                try:
                    for feed in feeds:
                        ids_div1 = feed.find_element(By.XPATH,"./div[@id]")
                        ids1 = ids_div1.get_attribute("id")

                        feed_ids_div2 = driver.find_element(By.XPATH,f'.//*[@id="{ids1}"]/div/div')
                        ids_div2 = feed_ids_div2.find_element(By.XPATH,"./div[@id]")
                        ids2 = ids_div2.get_attribute("id")

                        try:
                            profile_xpath = f'//*[@id="{ids2}"]/div/div/div[1]/div[1]/div[1]/div/div/a[1]/span[1]/span[1]/span/span[1]'
                            profile_link_xpath = f'//*[@id="{ids2}"]/div/div/div[1]/div[1]/div[1]/div/div/a[1]'
                            posted_by_xpath = f'//*[@id="{ids2}"]/div/div/div[1]/div[1]/div[1]/div/div/span/span[1]' 
                            body_xpath = f'//*[@id="{ids2}"]/div/div/div[1]/div[2]/div/div/span//span'
                            full_body_xpath = f'//*[@id="{ids2}"]/div/div/div[1]'

                            full_body_div3 = driver.find_element(By.XPATH,full_body_xpath)
                            ids_div3 = full_body_div3.find_element(By.XPATH,"./div[@id]")
                            ids3 = ids_div3.get_attribute("id")

                            likes_xpath = f'//*[@id="{ids3}"]/div[1]/div/div/ul/li[1]/button/span'
                            comments_xpath = f'//*[@id="{ids3}"]/div[1]/div/div/ul/li[2]/ul/li[1]/button/span'
                            comments_count = 0
                            likes_count = 0
                            # //*[@id="ember525"]/div[1]/div/div/ul/li[2]/ul/li[1]/button/span
                            try:
                                comments_data = driver.find_element(By.XPATH,comments_xpath).text
                                comments_count = int(comments_data.split(" ")[0])
                                #print(f"Comments: {comments_count}")
                            except:
                                comments_xpath = f'//*[@id="{ids3}"]/div[1]/div/div/ul/li[2]/ul/li/button/span'
                                try:
                                    comments_data = driver.find_element(By.XPATH,comments_xpath).text
                                    comments_count = int(comments_data.split(" ")[0])
                                    #print(f"Comments: {comments_count}")
                                except:
                                    likes_xpath = f'//*[@id="{ids3}"]/div[1]/div/div/ul/li/button/span'
                            try:
                                likes_data = driver.find_element(By.XPATH,likes_xpath).text
                                likes_count = int(likes_data.split(" ")[0])
                                #print(f'Likes: {likes_count}')
                            except:
                                print(f"No likes and Comments")
                            

                            profile_name = driver.find_element(By.XPATH,profile_xpath).text
                            profile_link = driver.find_element(By.XPATH,profile_link_xpath).get_attribute("href")
                            posted_by = driver.find_element(By.XPATH,posted_by_xpath).text

                            body_datas = driver.find_elements(By.XPATH,body_xpath)
                            text = " ".join(body_data.text.strip() for body_data in body_datas if body_data.text.strip())
                            if (len(text) < 100):
                                continue
                            profiles.append({
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
            if len(profiles) < 30:
                driver.execute_script("window.scrollBy(0,1000);")
                time.sleep(2)

    df = pd.DataFrame(profiles)
    df.to_csv("ai_data1.csv",index=False,encoding="utf-8")
    print("CSV file saved successfully")
except:
    print("Main Error...!")

input("Enter to quit...")
driver.quit()
