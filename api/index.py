import requests
from telebot import TeleBot
from flask import Blueprint, render_template, jsonify
from api.db import get_top_rankings


BOT_TOKEN = os.getenv("BOT_TOKEN")




home_ = Blueprint("home", __name__)
@home_.route('/')
def home():
    return render_template("charts.html")

api_ = Blueprint("api", __name__)
@api_.route('/api')
def home():
    data_list = []
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
    return jsonify({"users": data_list})
