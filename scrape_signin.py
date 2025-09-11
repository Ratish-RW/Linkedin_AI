import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time
import json

url = "https://www.linkedin.com/"
driver = uc.Chrome()
driver.maximize_window()
driver.get(url)
wait = WebDriverWait(driver,30)

# email = "rwtemp9@gmail.com"
# password = "tempo@04"
feed = "ai"


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


# signin1_xpath = '/html/body/nav/div/a[1]'
# email_input_xpath = '//*[@id="username"]'
# passowrd_input_xpath = '//*[@id="password"]'
# signin2_xpath = '//*[@id="organic-div"]/form/div[4]/button'
search_feed_input_xpath = '//*[@id="global-nav-typeahead"]/input'
elements_xpath = '//*[@id="search-reusables__filters-bar"]/ul'
posts_xpath = elements_xpath
posts_feed_classname = 'scaffold-finite-scroll__content'
date_posted_btn_id = 'searchFilter_datePosted'
date_posted_past24hours_xpath = '//*[@id="artdeco-hoverable-artdeco-gen-51"]/div[1]/div/form/fieldset/div[1]/ul/li[1]/label'
date_posted_form_btns_xpath = '//*[@id="artdeco-hoverable-artdeco-gen-51"]/div[1]/div/form/fieldset/div[2]'


# check_signin_btn1 = wait.until(EC.presence_of_element_located((By.XPATH,signin1_xpath)))
# if check_signin_btn1.text != "Sign in":
#     signin1_xpath = signin1_xpath[:-2] + "2" + signin1_xpath[-1:]

# signin_btn1 = wait.until(EC.element_to_be_clickable((By.XPATH,signin1_xpath)))
# signin_btn1.click()

# email_input = wait.until(EC.presence_of_element_located((By.XPATH,email_input_xpath)))
# email_input.send_keys(email)

# password_input = wait.until(EC.presence_of_element_located((By.XPATH,passowrd_input_xpath)))
# password_input.send_keys(password)

# signin_btn2 = wait.until(EC.element_to_be_clickable((By.XPATH,signin2_xpath)))
# signin_btn2.click()

search_feed_input = wait.until(EC.presence_of_element_located((By.XPATH,search_feed_input_xpath)))
search_feed_input.send_keys(feed)
search_feed_input.send_keys(Keys.RETURN)

elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, elements_xpath)))

items = elements[0].text.split("\n")

for i, it in enumerate(items):
    if it == "Posts":
        posts_xpath = f"{posts_xpath}/li[{i+1}]/button"
        break

posts_btn = wait.until(EC.presence_of_element_located((By.XPATH,posts_xpath)))
posts_btn.click()

date_posted_btn = wait.until(EC.element_to_be_clickable((By.ID,date_posted_btn_id)))
date_posted_btn.click()

past24hours_checkbox = wait.until(EC.element_to_be_clickable((By.XPATH,date_posted_past24hours_xpath)))
past24hours_checkbox.click()

date_posted_form_btns = wait.until(EC.presence_of_all_elements_located((By.XPATH,date_posted_form_btns_xpath)))

btns = date_posted_form_btns[0]
divs = btns.find_elements(By.XPATH,'./button[@id]')
print(divs)

feeds = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,posts_feed_classname)))


# //*[@id="4DSdiPpFTjO9ka3HVcQ2Uw=="]/div/ul/li[1]

feeds_id = feeds[0].find_elements(By.XPATH,"./div[@id]")[0].get_attribute("id")

feeds = wait.until(EC.presence_of_all_elements_located((By.XPATH,f'//*[@id="{feeds_id}"]/div/ul/li')))
for feed in feeds:
    ids_div1 = feed.find_element(By.XPATH,"./div[@id]")
    ids1 = ids_div1.get_attribute("id")

    feed_ids_div2 = driver.find_element(By.XPATH,f'//*[@id="{ids1}"]/div/div')
    ids_div2 = feed_ids_div2.find_element(By.XPATH,"./div[@id]")
    ids2 = ids_div2.get_attribute("id")
    #print(f"ids2 ----> {ids2}")

    profile_xpath = f'//*[@id="{ids2}"]/div/div/div[1]/div[1]/div[1]/div/div/a[1]/span[1]/span[1]/span/span[1]'
    profile_link = f'//*[@id="{ids2}"]/div/div/div[1]/div[1]/div[1]/div/div/a[1]'
    posted_by = f'//*[@id="{ids2}"]/div/div/div[1]/div[1]/div[1]/div/div/span/span[1]' 

    profile_name = driver.find_element(By.XPATH,profile_xpath).text
    profile_link = driver.find_element(By.XPATH,profile_link).get_attribute("href")
    posted_by = driver.find_element(By.XPATH,posted_by).text

    print(profile_name,profile_link,posted_by)

    #profile_name = //*[@id="ember292"]/div/div/div[1]/div[1]/div[1]/div/div/a[1]/span[1]/span[1]/span/span[1]
    # profile_link = //*[@id="ember292"]/div/div/div[1]/div[1]/div[1]/div/div/a[1]
    # date_posted = //*[@id="ember292"]/div/div/div[1]/div[1]/div[1]/div/div/span/span[1]

    

# //*[@id="ember283"]/div/div

# //*[@id="ember295"]/div/div/div[1]/div[1]/div[1]/div/div/a[1]/span[1]/span[1]/span/span[1]

# ids_div_classname = 'full-height'

# for feed in feeds:
#     ids_div = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,ids_div_classname)))
#     ids = ids_div[0].find_elements(By.XPATH,)


# for i,feed in enumerate(feeds):
#     inner_divs = feeds[0].find_elements(By.XPATH, "./div[@id]")
#     for div in inner_divs:
#         div_id = div.get_attribute("id")
#         print(f"{div_id}")
# # Give time for the new window to open
# time.sleep(2)

# # Switch to the new window (Google login popup)
# windows = driver.window_handles
# driver.switch_to.window(windows[-1]) 

input("Enter to quit...")
driver.quit()



#--------------------------------------------------
# feeds_list = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,posts_feed_classname)))
# for feeds in feeds_list:
#     feeds_id = feeds.find_elements(By.XPATH,"./div[@id]")[0].get_attribute("id")
#     feeds = wait.until(EC.presence_of_all_elements_located((By.XPATH,f'//*[@id="{feeds_id}"]/div/ul/li')))
#     try:
#         for feed in feeds:
#             ids_div1 = feed.find_element(By.XPATH,"./div[@id]")
#             ids1 = ids_div1.get_attribute("id")

#             feed_ids_div2 = driver.find_element(By.XPATH,f'//*[@id="{ids1}"]/div/div')
#             ids_div2 = feed_ids_div2.find_element(By.XPATH,"./div[@id]")
#             ids2 = ids_div2.get_attribute("id")
#             print(ids2)

#             try:
#                 profile_xpath = f'//*[@id="{ids2}"]/div/div/div[1]/div[1]/div[1]/div/div/a[1]/span[1]/span[1]/span/span[1]'
#                 profile_link = f'//*[@id="{ids2}"]/div/div/div[1]/div[1]/div[1]/div/div/a[1]'
#                 posted_by = f'//*[@id="{ids2}"]/div/div/div[1]/div[1]/div[1]/div/div/span/span[1]' 

#                 profile_name = driver.find_element(By.XPATH,profile_xpath).text
#                 profile_link = driver.find_element(By.XPATH,profile_link).get_attribute("href")
#                 posted_by = driver.find_element(By.XPATH,posted_by).text

#                 print(profile_name,profile_link,posted_by)
#             except:
#                 print(f"Skipping Feed")
#                 continue
#     except:
#         print(f"Skipping Feed List")
#         continue