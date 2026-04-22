from flask import Flask, request, jsonify
from urllib.parse import parse_qs
import requests
import os

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = os.environ.get("LajWsrkCCFDfYOd29pXdLo7AgOkSv+X3ZLUdoLrIBIfNqC/nivQUfCEAcvd6+IPIcAwH69hqnEPe2JbxEyCFrHrwk6mvd14YRrKu9Aap3VLEm0CXCngvHDo9GoB9DFE7lrFGidkwlR/vRYvSZkf97wdB04t89/1O/w1cDnyilFU=")
RICH_MENU_TH = "richmenu-b481621c4851916bff1e78f2bca39244"
RICH_MENU_EN = "richmenu-08ab625ef57d3cb4bff42217a1091943"

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
