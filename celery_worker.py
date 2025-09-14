from celery import Celery
from linkedin_scraper import LinkedInScraper
from dotenv import load_dotenv
import os

load_dotenv()

celery = Celery(
    "tasks",
    broker=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://localhost:6379/0")
)

@celery.task(bind=True)
def scrape_task(self, url, feed, total, cookie_file):
    scraper = LinkedInScraper(url, feed, total, cookie_file)

    load_result = scraper.load()
    if load_result.get("status") != "success":
        return {"status": "failure", "message": load_result.get("message")}

    search_feed_result = scraper.search_feed()
    if search_feed_result.get("status") != "success":
        return {"status": "failure", "message": search_feed_result.get("message")}

    search_by_posts_result = scraper.search_by_posts()
    if search_by_posts_result.get("status") != "success":
        return {"status": "failure", "message": search_by_posts_result.get("message")}

    click_date_posted_result = scraper.click_date_posted()
    if click_date_posted_result.get("status") != "success":
        return {"status": "failure", "message": click_date_posted_result.get("message")}

    get_data_result = scraper.get_data()
    if get_data_result.get("status") == "success":
        return {"status": "success", "message": get_data_result.get("message")}
    else:
        return {"status": "failure", "message": get_data_result.get("message")}
