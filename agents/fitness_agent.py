"""
Fitness Specialist Agent.
Provides personalized exercise routines, home/gym workouts, and recovery guidelines.
"""

from typing import Dict, Any
from agents.base_agent import BaseAgent

FITNESS_SYSTEM_PROMPT = """You are a certified Personal Trainer AI Agent.
Your role is to design safe, progressive workout programs (bodyweight or gym) tailored to the user's age, physical condition, and specific fitness goal.

Rules:
1. Specify exercise names, sets, reps, and rest periods clearly.
2. Adapt intensity based on user goal (Muscle Gain: Hypertrophy 8-12 reps; Weight Loss: HIIT/Circuit + Strength; Stay Fit: Balanced Full Body).
3. Include warm-up and cool-down steps.
4. Emphasize proper exercise technique to prevent injury.
"""

class FitnessAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Fitness Agent",
            role="Certified Personal Trainer",
            system_prompt=FITNESS_SYSTEM_PROMPT
        )

    def fallback_rule_response(self, prompt: str, user_profile: Dict[str, Any]) -> str:
        name = user_profile.get("name", "Friend")
        goal = user_profile.get("goal", "Stay fit")
        age = user_profile.get("age", 22)
        activity = user_profile.get("activity_level", "Moderately Active")
        goal_lower = goal.lower()

        if "muscle" in goal_lower or "gain" in goal_lower:
            workout_type = "Hypertrophy & Strength (Resistance Training)"
            focus = "Progressive Overload with compound movements"
            exercises = [
                ("Push-ups / Bench Press", "4 Sets x 8-12 Reps", "90 sec rest"),
                ("Bodyweight Squats / Barbell Squats", "4 Sets x 10-12 Reps", "90 sec rest"),
                ("Inverted Rows / Lat Pulldown", "3 Sets x 10-12 Reps", "60 sec rest"),
                ("Dumbbell / Resistance Band Shoulder Press", "3 Sets x 10-12 Reps", "60 sec rest"),
                ("Plank Hold", "3 Sets x 45-60 seconds", "45 sec rest")
            ]
        elif "lose" in goal_lower or "loss" in goal_lower:
            workout_type = "Metabolic Fat-Loss & Conditioning Circuit"
            focus = "High heart rate + strength preservation"
            exercises = [
                ("Jumping Jacks / Mountain Climbers", "3 Sets x 45 seconds", "30 sec rest"),
                ("Bodyweight Squats into Jump", "4 Sets x 15 Reps", "45 sec rest"),
                ("Push-ups (Incline or Regular)", "3 Sets x 12-15 Reps", "45 sec rest"),
                ("Walking Lunges", "3 Sets x 12 Reps/leg", "45 sec rest"),
                ("Bicycle Crunches", "3 Sets x 20 Reps", "30 sec rest")
            ]
        else:
            workout_type = "Full Body Functional Fitness & Mobility"
            focus = "General strength, posture, and cardiovascular endurance"
            exercises = [
                ("Bodyweight Squats", "3 Sets x 12 Reps", "60 sec rest"),
                ("Standard Push-ups", "3 Sets x 10 Reps", "60 sec rest"),
                ("Glute Bridges", "3 Sets x 15 Reps", "45 sec rest"),
                ("Doorway or Dumbbell Rows", "3 Sets x 12 Reps", "60 sec rest"),
                ("Bird-Dog & Cat-Cow Mobility", "3 Sets x 10 Reps/side", "30 sec rest")
            ]

        ex_formatted = "\n".join([f"- **{ex[0]}**: {ex[1]} *(Rest: {ex[2]})*" for ex in exercises])

        return f"""### 🏋️ Fitness Coach Routine for {name}

**Primary Goal**: {goal} | **Program Type**: {workout_type}
**User Activity Profile**: {activity} (Age: {age})

#### ⏱️ Warm-Up (5 Minutes):
- 2 mins Arm circles & torso twists
- 3 mins Dynamic leg swings & light jumping jacks

#### 💪 Recommended Routine ({focus}):
{ex_formatted}

#### 🧘 Cool-Down & Recovery (3 Minutes):
- Hamstring stretch (30s hold per leg)
- Chest opener stretch (30s hold)
- Deep diaphragmatic breathing

💡 *Trainer's Tip*: Focus on controlled form over heavy weight. Take at least 1-2 rest days per week for optimal muscle repair!
"""
