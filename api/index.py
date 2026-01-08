import os
from datetime import datetime
import requests
from flask import Blueprint, render_template, jsonify, request
from api.db import get_top_rankings, get_user_ranking


BOT_TOKEN = os.getenv("BOT_TOKEN")
BASE_API = os.getenv("BASE_API")

uptime = Blueprint("status", __name__)
@uptime.route("/api/status")
def status_api():
    try:
        response = requests.get(
            f"{BASE_API}/api/status"
        )
        if response.status_code == 200:
            data = response.json()
        else:
            data = {
                "facebook": {
                    "endpoint": "Outage",
                    "errorLog": [
                        {
                            "level": "error",
                            "message": "Server down!",
                            "timestamp": str(datetime.now())
                        },
                    ],
                    "latency": 9999,
                    "name": "outage",
                    "status": "down"
                },
            }
    except Exception:
        data = {
            "facebook": {
                "endpoint": "Outage",
                "errorLog": [
                    {
                        "level": "error",
                        "message": "Server down!",
                        "timestamp": str(datetime.now())
                    },
                ],
                "latency": 9999,
                "name": "outage",
                "status": "down"
            },
        }
    return jsonify(data)

uptime_web = Blueprint("status_web", __name__)
@uptime_web.route("/downloader/uptime")
def status_web():
    return render_template("api_monitor.html")

home_ = Blueprint("home", __name__)
@home_.route('/')
def home():
    return render_template("charts.html")

api_ = Blueprint("api", __name__)
@api_.route('/api')
def home():
    data_list = []
    id_user = request.args.get("id")
    if not id_user:
        res = get_top_rankings()
        for data in res:
            user = requests.get(
                f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMember?chat_id={data['user_id']}&user_id={data['user_id']}"
            ).json()
            tele_user = "Telegram User"
            if user["ok"]:
                tele_user = user["result"]["user"]["first_name"]
            data_list.append(
                {
                    "rank": data["rank"],
                    "user_id": data["user_id"],
                    "name": tele_user,
                    "timestamp": data["last_updated"],
                    "downloads": data["total_actions"]
                }
            )
    else:
        data = get_user_ranking(id_user)
        user = requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMember?chat_id={data['user_id']}&user_id={data['user_id']}"
        ).json()
        tele_user = "Telegram User"
        if user["ok"]:
            tele_user = user["result"]["user"]["first_name"]
        data_list.append(
                {
                    "rank": data["rank"],
                    "user_id": data["user_id"],
                    "name": tele_user,
                    "timestamp": data["last_updated"],
                    "downloads": data["total_actions"]
                }
        )
    return jsonify({"users": data_list})

downloader_web = Blueprint("downloader_web", __name__)
@downloader_web.route("/downloader")
def dl_web():
    return render_template("downloader.html")

dl_api = Blueprint("dl_api", __name__)
@dl_api.route('/api/dl')
def dl_api_():
    url = request.args.get("url")
    if url:
        response = requests.get(
            f"{BASE_API}/api?url={url}"
        )
        if response.status_code == 200:
            data = response.json()
            return jsonify(data)
        return jsonify({"error": response.text})
    else:
        return jsonify({"error": "input not found!"})
