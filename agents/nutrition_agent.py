"""
Nutrition Specialist Agent.
Provides personalized meal plans, macro target breakdowns, and diet advice.
"""

from typing import Dict, Any
from agents.base_agent import BaseAgent
from utils.health_calc import calculate_bmr, calculate_tdee, calculate_targets

NUTRITION_SYSTEM_PROMPT = """You are an expert Clinical Nutritionist AI Agent.
Your role is to provide safe, highly actionable, evidence-based meal recommendations, macro breakdowns, and dietary tips.

Rules:
1. Always tailor advice strictly to the user's diet preference (Vegetarian, Non-Vegetarian, Vegan, Keto, etc.).
2. Respect calorie goals (Deficit for weight loss, Surplus for muscle gain, Maintenance for staying fit).
3. Include specific food examples with high protein and micronutrients.
4. Keep tone encouraging, structured, and easy to follow.
5. End with a reminder: "Consult a nutritionist or physician for customized clinical diets."
"""

class NutritionAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Nutrition Agent",
            role="Nutritionist Specialist",
            system_prompt=NUTRITION_SYSTEM_PROMPT
        )

    def fallback_rule_response(self, prompt: str, user_profile: Dict[str, Any]) -> str:
        name = user_profile.get("name", "Friend")
        goal = user_profile.get("goal", "Stay fit")
        diet = user_profile.get("diet_pref", "Vegetarian")
        weight = user_profile.get("weight_kg", 70.0)
        height = user_profile.get("height_cm", 175.0)
        age = user_profile.get("age", 22)
        gender = user_profile.get("gender", "Male")
        activity = user_profile.get("activity_level", "Moderately Active")

        bmr = calculate_bmr(weight, height, age, gender)
        tdee = calculate_tdee(bmr, activity)
        targets = calculate_targets(tdee, goal)

        # Diet-specific protein and food suggestions
        if "veg" in diet.lower() and "non" not in diet.lower():
            protein_sources = "Paneer/Tofu, Lentils (Dal), Greek Yogurt/Curd, Chickpeas, Sprouts, and Whey Protein"
            breakfast = "Oatmeal cooked in milk topped with almonds & chia seeds, plus 2 boil eggs or paneer scramble."
            lunch = "Brown rice or 2 Whole Wheat Rotis, 1 bowl Paneer/Tofu Curry, Mixed Veggies, and Curd."
            dinner = "Grilled Tofu/Paneer salad or Lentil Soup (Dal Tadka) with sautéed veggies & quinoa."
        elif "vegan" in diet.lower():
            protein_sources = "Tofu, Tempeh, Edamame, Chickpeas, Lentils, Hemp seeds, and Plant Protein Powder"
            breakfast = "Overnight oats with soy/almond milk, chia seeds, peanut butter & berries."
            lunch = "Quinoa bowl with black beans, roasted tofu, avocado & spinach."
            dinner = "Lentil stew with broccoli, sweet potato, and hemp seed garnish."
        else:
            protein_sources = "Chicken Breast, Eggs, Fish (Salmon/Tuna), Greek Yogurt, and Cottage Cheese"
            breakfast = "3 Whole Eggs (scrambled/boiled), 2 slices Whole Wheat Toast & avocado."
            lunch = "Grilled Chicken Breast (200g) with Brown Rice, Steamed Broccoli & olive oil."
            dinner = "Pan-seared Fish or Chicken Breast with grilled asparagus & baked sweet potato."

        return f"""### 🥗 Nutrition Coach Recommendation for {name}

**Target Goal**: {targets['goal_type']} ({targets['target_calories']} kcal/day)
**Diet Preference**: {diet}

#### 📊 Recommended Daily Macronutrient Breakdown:
- **Protein**: ~{targets['protein_g']}g ({targets['protein_ratio_pct']}% of daily intake)
- **Carbohydrates**: ~{targets['carb_g']}g ({targets['carb_ratio_pct']}%)
- **Healthy Fats**: ~{targets['fat_g']}g ({targets['fat_ratio_pct']}%)

#### 🍽️ Sample 1-Day Meal Plan tailored for {goal}:
- 🌅 **Breakfast**: {breakfast}
- ☀️ **Lunch**: {lunch}
- ☕ **Snack**: Handful of mixed nuts (Walnuts & Almonds) + Green Tea or Protein Shake.
- 🌙 **Dinner**: {dinner}

💡 *Top Nutrition Tip*: Prioritize **{protein_sources}** to hit your daily protein goal cleanly! Ensure you eat within 45 minutes after workouts for optimal recovery.
"""
