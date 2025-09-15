from flask import Flask,request,jsonify,Response
from flask_cors import CORS
from linkedin_scraper import LinkedInScraper
from celery_worker import scrape_task, celery
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

        task = scrape_task.delay(url, feed, total, cookie_file)
        return jsonify({"task_id": task.id}), 202

    except Exception as e:
        return jsonify({"status": "failure", "message": str(e)})

@app.route("/status/<task_id>")
def status(task_id):
    task = celery.AsyncResult(task_id)

    if task.state == "PENDING":
        response = {
            "task_id": task.id,
            "state": task.state,
            "status": "pending",
            "message": "Task is still waiting in the queue..."
        }
    elif task.state == "STARTED":
        response = {
            "task_id": task.id,
            "state": task.state,
            "status": "running",
            "message": "Task is currently being processed..."
        }
    elif task.state == "SUCCESS":
        # Here, task.result will contain your return value
        response = {
            "task_id": task.id,
            "state": task.state,
            **task.result  # merges {"status": "...", "message": "..."}
        }
    elif task.state == "FAILURE":
        response = {
            "task_id": task.id,
            "state": task.state,
            "status": "failure",
            "message": str(task.info)  # exception info
        }
    else:
        response = {
            "task_id": task.id,
            "state": task.state,
            "status": "unknown",
            "message": str(task.info)
        }

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)