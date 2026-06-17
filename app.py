from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

# إعدادات البوت
BOT_TOKEN = "8582141954:AAHIV2A5GukH7Kr1g_8ZJE4h0_74XcD4Rzs"
CHAT_ID = "158231042"
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

def send_telegram_message(text):
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(TELEGRAM_URL, json=payload, timeout=10)
        return response.json()
    except Exception as e:
        print(f"Error: {e}")
        return None

@app.route('/')
def home():
    return "✅ SPCX Bot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    
    action = data.get('action', 'UNKNOWN')
    price = data.get('price', 'N/A')
    time_str = data.get('time', datetime.utcnow().strftime('%H:%M:%S'))
    
    emoji = "🟢" if action == "BUY" else "🔴" if action == "SELL" else "⚪"
    
    message = f"""🚧 𝗟𝗜𝗩𝗘 𝗦𝗜𝗚𝗡𝗔𝗟
• العملات: SPCX
• الإطار الزمني: M1
• توقيت الدخول: {time_str} UTC
• نوع الصفقة: {action} {emoji}
• السعر: {price}
• نسبة الفوز المتوقعة: 💰 75%"""
    
    send_telegram_message(message)
    return jsonify({"status": "sent", "action": action})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
