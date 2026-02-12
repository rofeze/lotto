from .base import BaseAdapter

class ConsoleAdapter(BaseAdapter):
    def send(self, data):
        import json
        print(f"{json.dumps(data, ensure_ascii=False)}")
