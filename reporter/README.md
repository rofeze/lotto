# Reporter

A simple Python module to report execution progress and results to various channels (Console, Discord, Telegram).

## JSON Format

```json
{
  "host": "hostname",
  "stage": "COMPLETE",
  "status": "SUCCESS",
  "duration": "1s",
  "detail": { ... }
}
```

## Configuration

To enable notifications, set the following environment variables:
- **Discord**: `REPORTER_WEBHOOK`
- **Telegram**: `REPORTER_TELEGRAM_TOKEN` and `REPORTER_TELEGRAM_CHAT_ID`

## Usage

The `Reporter` is designed to be drop-in ready while providing flexibility for complex notifications.

### 1. Simple Usage (Automatic)

When initialized without arguments, the `Reporter` automatically includes the `ConsoleAdapter` and checks for environment variables to add `DiscordAdapter` and `TelegramAdapter`.

```python
from reporter import Reporter
import traceback

# Initialize (auto-detects REPORTER_WEBHOOK, etc.)
rep = Reporter()

try:
    # 1. Start a stage
    rep.stage("SCRAPING")
    
    # ... your logic ...
    
    # 2. Update stage as you progress
    rep.stage("PURCHASING")
    
    # 3. Report success with optional detail dictionary
    rep.success({"processed_count": 5})

except Exception:
    # 4. Report failure with traceback
    rep.fail(traceback.format_exc())
```

### 2. Advanced Usage (Manual Config)

You can manually specify which adapters to use, bypassing environment variable auto-detection. This is useful for sending to multiple webhooks or specific bot accounts.

```python
from reporter import Reporter, ConsoleAdapter, DiscordAdapter, TelegramAdapter

# Configuration with explicit adapters
adapters = [
    ConsoleAdapter(), # Always recommended for systemd logs
    DiscordAdapter(webhook_url="https://discord.com/api/webhooks/..."),
    TelegramAdapter(token="BOT_TOKEN", chat_id="CHAT_ID")
]

rep = Reporter(adapters=adapters)
rep.success({"msg": "Manual report sent!"})
```

### 3. Key Concepts

- **Stages**: Use `rep.stage("NAME")` to track where an error occurred. If `rep.fail()` is called, it will include the last set stage.
- **Duration Tracking**: The `Reporter` calculates duration since its initialization. `success()` and `fail()` both include this in their reports.
- **JSON Format**: The `ConsoleAdapter` outputs a standardized line starting with `__RESULT__`, making it easy for systemd observers or external scripts to parse log files.
