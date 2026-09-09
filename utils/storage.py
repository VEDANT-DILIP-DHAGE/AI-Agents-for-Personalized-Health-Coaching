"""
JSON Storage Utilities for User Profile and Chat Memory Persistence.
"""

import json
import os

PROFILE_FILE = "user_profile.json"
CHAT_FILE = "chat_history.json"

DEFAULT_PROFILE = {
    "name": "Alex",
    "age": 22,
    "gender": "Male",
    "height_cm": 175.0,
    "weight_kg": 70.0,
    "goal": "Gain muscle",
    "diet_pref": "Vegetarian",
    "activity_level": "Moderately Active (3-5 days/week)",
    "api_key": ""
}

def load_user_profile(filepath: str = PROFILE_FILE) -> dict:
    """Load user profile from JSON file. Returns default profile if file doesn't exist."""
    if not os.path.exists(filepath):
        save_user_profile(DEFAULT_PROFILE, filepath)
        return DEFAULT_PROFILE.copy()
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            profile = json.load(f)
            # Ensure all keys are present
            merged = DEFAULT_PROFILE.copy()
            merged.update(profile)
            return merged
    except Exception as e:
        print(f"Error loading profile JSON: {e}")
        return DEFAULT_PROFILE.copy()

def save_user_profile(profile_data: dict, filepath: str = PROFILE_FILE) -> bool:
    """Save user profile to JSON file."""
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(profile_data, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving profile JSON: {e}")
        return False

def load_chat_history(filepath: str = CHAT_FILE) -> list:
    """Load stored chat messages from JSON file."""
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading chat history JSON: {e}")
        return []

def save_chat_history(messages: list, filepath: str = CHAT_FILE) -> bool:
    """Save chat messages to JSON file."""
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(messages, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving chat history JSON: {e}")
        return False

def clear_chat_history(filepath: str = CHAT_FILE) -> bool:
    """Reset chat history file."""
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
        return True
    except Exception as e:
        print(f"Error resetting chat history: {e}")
        return False
