import json
import socket
import time
import os
from .adapters import ConsoleAdapter, DiscordAdapter, TelegramAdapter

class Reporter:
    def __init__(self, title="Task", adapters=None):
        self.title = title
        self.host = socket.gethostname()
        self.start_time = time.time()
        self.current_stage = "INIT"
        
        if adapters is None:
            # Default adapters: Console always
            self.adapters = [ConsoleAdapter()]
            
            # Auto-detect Discord
            if os.environ.get('REPORTER_WEBHOOK'):
                self.adapters.append(DiscordAdapter())
                
            # Auto-detect Telegram
            if os.environ.get('REPORTER_TELEGRAM_TOKEN') and os.environ.get('REPORTER_TELEGRAM_CHAT_ID'):
                self.adapters.append(TelegramAdapter())
        else:
            self.adapters = adapters
        
    def stage(self, stage_name):
        self.current_stage = stage_name
        
    def _get_duration(self):
        duration_sec = time.time() - self.start_time
        if duration_sec < 60:
            return f"{int(duration_sec)}s"
        else:
            minutes = int(duration_sec // 60)
            seconds = int(duration_sec % 60)
            return f"{minutes}m {seconds}s"

    def _notify(self, result_data):
        for adapter in self.adapters:
            try:
                adapter.send(result_data)
            except Exception as e:
                print(f"Adapter {adapter.__class__.__name__} failed: {e}")

    def success(self, detail=None):
        result_data = {
            "title": self.title,
            "host": self.host,
            "stage": "COMPLETE",
            "status": "SUCCESS",
            "duration": self._get_duration(),
            "detail": detail or {}
        }
        self._notify(result_data)
        
    def fail(self, error_trace):
        result_data = {
            "title": self.title,
            "host": self.host,
            "stage": self.current_stage,
            "status": "FAIL",
            "duration": self._get_duration(),
            "trace": error_trace
        }
        self._notify(result_data)
