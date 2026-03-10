import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FollowEvent

app = Flask(__name__)

# 設定你的金鑰 (建議之後用環境變數管理)
LINE_CHANNEL_ACCESS_TOKEN = '你的_CHANNEL_ACCESS_TOKEN'
LINE_CHANNEL_SECRET = 'ea9dc6d429fcb9b1debbe0b9a44676ae'

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 當有人加好友時觸發
@handler.add(FollowEvent)
def handle_follow(event):
    welcome_msg = "✨ 歡迎來到 LIN SHOP！\n\n感謝您的關注 🫧\n這裡將不定期更新最新商品與優惠資訊。\n如有任何問題，歡迎直接留言詢問唷！"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=welcome_msg)
    )

if __name__ == "__main__":
    app.run(port=5000)
