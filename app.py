from flask import Flask, request, jsonify
from urllib.parse import parse_qs
import requests
import os

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = os.environ.get("CHANNEL_ACCESS_TOKEN")
RICH_MENU_TH = os.environ.get("RICH_MENU_TH")
RICH_MENU_EN = os.environ.get("RICH_MENU_EN")

@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.get_json()
    events = body.get("events", [])

    for event in events:
        if event["type"] == "postback":
            data = parse_qs(event["postback"]["data"])
            action = data.get("action", [None])[0]
            lang = data.get("lang", [None])[0]
            user_id = event["source"]["userId"]

            if action == "switchLang":
                menu_id = RICH_MENU_EN if lang == "en" else RICH_MENU_TH
                link_rich_menu(user_id, menu_id)

    return jsonify({"status": "ok"}), 200

def link_rich_menu(user_id, rich_menu_id):
    url = f"https://api.line.me/v2/bot/user/{user_id}/richmenu/{rich_menu_id}"
    headers = {"Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}"}
    requests.post(url, headers=headers)

if __name__ == "__main__":
    app.run(port=3000)
