import json
import os
import time
import urllib.request
from .base import BaseAdapter

class DiscordAdapter(BaseAdapter):
    def __init__(self, webhook_url=None):
        self.webhook_url = webhook_url or os.environ.get('REPORTER_WEBHOOK')

    def send(self, result):
        if not self.webhook_url:
            return
            
        status_emoji = "✅" if result['status'] == "SUCCESS" else "❌"
        
        embed = {
            "title": f"{status_emoji} Lotto Purchase Result: {result['status']}",
            "color": 0x00ff00 if result['status'] == "SUCCESS" else 0xff0000,
            "fields": [
                {"name": "Host", "value": result['host'], "inline": True},
                {"name": "Stage", "value": result['stage'], "inline": True},
                {"name": "Duration", "value": result['duration'], "inline": True},
            ],
            "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        }
        
        if result['status'] == "SUCCESS" and result.get('detail'):
            processed = result['detail'].get('processed_count', 0)
            embed["description"] = f"Purchased: **{processed}** games"
            
        if result['status'] == "FAIL" and result.get('trace'):
            trace = result['trace']
            if len(trace) > 1000:
                trace = trace[:1000] + "..."
            embed["fields"].append({"name": "Error Trace", "value": f"```python\n{trace}\n```"})

        data = json.dumps({"embeds": [embed]}).encode('utf-8')
        req = urllib.request.Request(self.webhook_url, data=data, headers={'Content-Type': 'application/json', 'User-Agent': 'Result-Bot'})
        
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                pass
        except Exception as e:
            print(f"Failed to send Discord notification: {e}")
