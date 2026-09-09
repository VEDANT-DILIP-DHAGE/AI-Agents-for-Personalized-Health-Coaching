"""
Lifestyle & Well-being Specialist Agent.
Provides recommendations for sleep optimization, hydration schedule, stress reduction, and healthy daily habits.
"""

from typing import Dict, Any
from agents.base_agent import BaseAgent
from utils.health_calc import calculate_water_intake

LIFESTYLE_SYSTEM_PROMPT = """You are a Holistic Health & Wellness Coach AI Agent.
Your role is to guide users on sleep hygiene, hydration protocols, stress management techniques, circadian rhythm alignment, and daily habit stacking.

Rules:
1. Provide practical, daily lifestyle habits (not vague advice).
2. Give clear hydration targets in Liters.
3. Offer concrete sleep optimization steps (blue light reduction, sleep environment).
4. Keep tone calming, encouraging, and supportive.
"""

class LifestyleAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Lifestyle Agent",
            role="Holistic Wellness Specialist",
            system_prompt=LIFESTYLE_SYSTEM_PROMPT
        )

    def fallback_rule_response(self, prompt: str, user_profile: Dict[str, Any]) -> str:
        name = user_profile.get("name", "Friend")
        weight = user_profile.get("weight_kg", 70.0)
        activity = user_profile.get("activity_level", "Moderately Active")
        goal = user_profile.get("goal", "Stay fit")

        water_liters = calculate_water_intake(weight, activity)
        glasses = int(water_liters * 4)  # ~250ml per glass

        return f"""### 🌿 Lifestyle & Recovery Guide for {name}

#### 💧 Hydration Target:
- **Daily Requirement**: **~{water_liters} Liters** (approx. {glasses} glasses of water/day).
- **Pro Tip**: Drink 500ml (2 glasses) immediately upon waking up to kickstart metabolism and rehydrate after sleep.

#### 😴 Sleep Hygiene Protocol (Target: 7.5 - 8.5 Hours):
- **Blue Light Cutoff**: Turn off screens (phone, laptop, TV) 45 minutes before sleep or use night-shift mode.
- **Sleep Environment**: Keep room dark, cool (~18-21°C / 65-70°F), and quiet.
- **Consistency**: Go to bed and wake up within the same 30-minute window every day to lock in your circadian rhythm.

#### 🧘 Stress Reduction & Habit Stacking:
- **Box Breathing (4-4-4-4)**: Inhale 4s, Hold 4s, Exhale 4s, Hold 4s (perform 5 cycles whenever feeling stressed).
- **Daily Movement**: Take a 10-minute walk after lunch or dinner to assist digestion and steady blood sugar.
- **Sunlight Exposure**: Get 10-15 minutes of natural morning sunlight within 1 hour of waking up.

💡 *Wellness Tip*: Recovery is where progress happens! High stress raises cortisol, which can slow down {goal.lower()} progress.
"""
