from flask import Flask,request,jsonify,Response
from flask_cors import CORS
from linkedin_scraper import LinkedInScraper
from dotenv import load_dotenv
import os
import json

load_dotenv() 

app = Flask(__name__)
CORS(app)

@app.route('/',methods=['GET'])
def temp():
    return jsonify({"message":"hellooo!"})

@app.route('/scrape',methods=['POST'])
def scrape_data():
    try:
        data = request.get_json()
        url = data.get("url")
        feed = data.get("feed")
        total = data.get("total")
        #print(url,feed,total)
        cookie_str = os.environ.get("COOKIE_JSON")
        cookie_file = json.loads(cookie_str)
        #cookie_file = data.get("cookie_file")

        scraper = LinkedInScraper(url,feed,total,cookie_file)
        load_result = scraper.load()
        if load_result.get("status") == "success":
            print(load_result.get("message"))
            search_feed_result = scraper.search_feed()
            if search_feed_result.get("status") == "success":
                print(search_feed_result.get("message"))
                search_by_posts_result = scraper.search_by_posts()
                if search_by_posts_result.get("status") == 'success':
                    print(search_by_posts_result.get("message"))
                    click_date_posted_result = scraper.click_date_posted()
                    if click_date_posted_result.get("status") == 'success':
                        print(click_date_posted_result.get("message"))
                        get_data_result = scraper.get_data()
                        if get_data_result.get("status") == 'success':
                            #print(get_data_result.get("message"))
                            return jsonify({"status":"success","message":get_data_result.get("message")})
                        return jsonify({"status":"failure","message":click_date_posted_result.get("message")})
                    return jsonify({"status":"failure","message":search_by_posts_result.get("message")})
                return jsonify({"status":"failure","message":search_feed_result.get("message")})    
            return jsonify({"status":"failure","message": load_result.get("message")})
        scraper.close()

    except Exception:
        return jsonify({"status":"failure","message":str(Exception)})

if __name__ == "__main__":
    app.run(debug=True)