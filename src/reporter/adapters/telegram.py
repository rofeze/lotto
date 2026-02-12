import json
import os
import urllib.request
from .base import BaseAdapter

class TelegramAdapter(BaseAdapter):
    def __init__(self, token=None, chat_id=None):
        self.token = token or os.environ.get('REPORTER_TELEGRAM_TOKEN')
        self.chat_id = chat_id or os.environ.get('REPORTER_TELEGRAM_CHAT_ID')

    def send(self, result):
        if not self.token or not self.chat_id:
            return
            
        status_emoji = ""  # Removed noisy emojis
        title = result.get('title', 'Execution')
        text = f"*{title} Result: {result['status']}*\n\n"
        text += f"- *Host:* {result['host']}\n"
        text += f"- *Stage:* {result['stage']}\n"
        text += f"- *Duration:* {result['duration']}\n"
        
        if result.get('detail'):
            for key, value in result['detail'].items():
                label = key.replace('_', ' ').title()
                text += f"- *{label}:* {value}\n"
            
        if result['status'] == "FAIL" and result.get('trace'):
            trace = result['trace']
            if len(trace) > 500:
                trace = trace[:500] + "..."
            text += f"\n*Error Trace:*\n`{trace}`"

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        data = json.dumps({
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": "Markdown"
        }).encode('utf-8')
        
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                pass
        except Exception as e:
            print(f"Failed to send Telegram notification: {e}")
