import os
import time
import requests
from google import genai

# შენი გასაღებები (API Keys)
GEMINI_API_KEY = "AQ.Ab8RN6KDWfur32HZA_0nLjxBKcRmodhl6wbih_kX2pPuBZxpdA"
TELEGRAM_BOT_TOKEN = "9114655833:AAFG24T_td4hNYXP7HBQ4z-PDiHaHNOYTuA"

client = genai.Client(api_key=GEMINI_API_KEY)

def send_telegram_message(chat_id, text):
    """უგზავნის ანგარიშს ან პასუხს შენს Telegram-ში"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

def get_updates(offset=None):
    """ამოწმებს შენს ბრძანებებს Telegram-ში"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
    params = {"timeout": 30, "offset": offset}
    response = requests.get(url, params=params)
    return response.json()

def process_ai_command(command_text):
    """Gemini AI ამუშავებს შენს დავალებას (გეგმები, პოსტები, ანგარიშები)"""
    prompt = f"""
    შენ ხარ რელიგიური მედიაპლატფორმის ძლიერი AI მენეჯერი.
    მომხმარებელმა მოგცა შემდეგი დავალება: "{command_text}"
    
    გაითვალისწინე, რომ პლატფორმა აშუქებს სხვადასხვა რელიგიას (კათოლიკური, მართლმადიდებლური, ისლამური და ა.შ.).
    შეასრულე დავალება პროფესიონალურად ქართულ ენაზე, დაწერე მიმზიდველი პოსტები ან სტრუქტურული გეგმები შესაბამისი ჰეშთეგებით.
    """
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )
    return response.text

def main():
    print("AI მენეჯერი ჩაირთო და მზადაა შენს ბრძანებებზე სამუშაოდ...")
    offset = None
    while True:
        try:
            updates = get_updates(offset)
            if "result" in updates:
                for update in updates["result"]:
                    offset = update["update_id"] + 1
                    if "message" in update and "text" in update["message"]:
                        chat_id = update["message"]["chat"]["id"]
                        user_text = update["message"]["text"]
                        
                        print(f"მიღებულია ბრძანება: {user_text}")
                        
                        # AI ამუშავებს დავალებას
                        ai_response = process_ai_command(user_text)
                        
                        # აბრუნებს ანგარიშს Telegram-ში
                        report = f"🤖 **AI მენეჯერის ანგარიში:**\n\n{ai_response}"
                        send_telegram_message(chat_id, report)
        except Exception as e:
            print(f"შეცდომა: {e}")
        
        time.sleep(2)

if __name__ == "__main__":
    main()
