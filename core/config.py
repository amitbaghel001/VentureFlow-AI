import json
import os

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "..", "config.json")

DEFAULT_CONFIG = {
    "active_model": "gpt-4o",  # or "gemini-1.5-pro"
}

def load_config() -> dict:
    if not os.path.exists(CONFIG_FILE):
        return DEFAULT_CONFIG.copy()
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Merge with defaults in case of missing keys
            for k, v in DEFAULT_CONFIG.items():
                if k not in data:
                    data[k] = v
            return data
    except Exception:
        return DEFAULT_CONFIG.copy()

def save_config(config_data: dict) -> None:
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config_data, f, indent=4)
