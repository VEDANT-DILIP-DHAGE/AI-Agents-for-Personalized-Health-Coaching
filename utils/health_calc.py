"""
Health Calculation Utilities for Personalized Health Coaching.
Uses standard evidence-based medical formulas:
- Body Mass Index (BMI)
- Mifflin-St Jeor Equation for Basal Metabolic Rate (BMR)
- Total Daily Energy Expenditure (TDEE) based on activity multipliers
- Goal-based caloric shift & macro estimation
- Daily hydration requirements
"""

def calculate_bmi(weight_kg: float, height_cm: float) -> dict:
    """Calculate BMI and return value, category, and visual metadata."""
    if height_cm <= 0 or weight_kg <= 0:
        return {"bmi": 0.0, "category": "Invalid Input", "color": "#9E9E9E", "desc": "Please provide valid height and weight."}
    
    height_m = height_cm / 100.0
    bmi = weight_kg / (height_m ** 2)
    bmi_rounded = round(bmi, 1)

    if bmi < 18.5:
        category = "Underweight"
        color = "#3B82F6"  # Blue
        desc = "Below standard weight range. Focus on nutrient-dense calorie intake."
    elif 18.5 <= bmi < 25.0:
        category = "Normal Weight"
        color = "#10B981"  # Green
        desc = "Healthy weight range! Focus on balanced nutrition and maintenance."
    elif 25.0 <= bmi < 30.0:
        category = "Overweight"
        color = "#F59E0B"  # Amber
        desc = "Above standard weight range. A slight caloric deficit & exercise is recommended."
    else:
        category = "Obese"
        color = "#EF4444"  # Red
        desc = "Significantly above standard range. Focus on structured fitness & lifestyle changes."

    return {
        "bmi": bmi_rounded,
        "category": category,
        "color": color,
        "desc": desc
    }

def calculate_bmr(weight_kg: float, height_cm: float, age: int, gender: str) -> float:
    """
    Calculate BMR using the Mifflin-St Jeor Equation.
    Men: BMR = (10 * weight) + (6.25 * height) - (5 * age) + 5
    Women: BMR = (10 * weight) + (6.25 * height) - (5 * age) - 161
    """
    if weight_kg <= 0 or height_cm <= 0 or age <= 0:
        return 1600.0

    bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age)
    if gender.lower() == "male":
        bmr += 5
    else:
        bmr -= 161
    return round(bmr, 0)

def calculate_tdee(bmr: float, activity_level: str) -> float:
    """Calculate TDEE using physical activity level multipliers."""
    multipliers = {
        "Sedentary (Little/no exercise)": 1.2,
        "Lightly Active (1-3 days/week)": 1.375,
        "Moderately Active (3-5 days/week)": 1.55,
        "Very Active (6-7 days/week)": 1.725,
        "Extra Active (Physical job or 2x workout)": 1.9
    }
    
    # Matching fallback if key is formatted slightly differently
    multiplier = 1.375
    for key, val in multipliers.items():
        if activity_level.lower() in key.lower() or key.lower() in activity_level.lower():
            multiplier = val
            break
            
    return round(bmr * multiplier, 0)

def calculate_targets(tdee: float, goal: str) -> dict:
    """
    Calculate target daily calories and macronutrient distribution based on goal.
    """
    goal_lower = goal.lower()
    
    if "lose" in goal_lower or "loss" in goal_lower:
        target_calories = tdee - 400.0  # Safe ~0.4kg/week deficit
        protein_ratio, carb_ratio, fat_ratio = 0.35, 0.40, 0.25
        goal_type = "Caloric Deficit (Weight Loss)"
    elif "gain" in goal_lower or "muscle" in goal_lower:
        target_calories = tdee + 300.0  # Clean surplus for hypertrophy
        protein_ratio, carb_ratio, fat_ratio = 0.30, 0.45, 0.25
        goal_type = "Caloric Surplus (Muscle Gain)"
    else:
        target_calories = tdee
        protein_ratio, carb_ratio, fat_ratio = 0.25, 0.50, 0.25
        goal_type = "Maintenance"

    target_calories = max(1200.0, round(target_calories, 0))  # Safety minimum

    # 1g Protein = 4 kcal, 1g Carb = 4 kcal, 1g Fat = 9 kcal
    protein_g = round((target_calories * protein_ratio) / 4, 1)
    carb_g = round((target_calories * carb_ratio) / 4, 1)
    fat_g = round((target_calories * fat_ratio) / 9, 1)

    return {
        "target_calories": int(target_calories),
        "goal_type": goal_type,
        "protein_g": protein_g,
        "carb_g": carb_g,
        "fat_g": fat_g,
        "protein_ratio_pct": int(protein_ratio * 100),
        "carb_ratio_pct": int(carb_ratio * 100),
        "fat_ratio_pct": int(fat_ratio * 100)
    }

def calculate_water_intake(weight_kg: float, activity_level: str) -> float:
    """
    Calculate baseline recommended daily water intake in Liters.
    Formula: ~35ml per kg bodyweight + activity bonus.
    """
    if weight_kg <= 0:
        return 2.5
    
    base_liters = (weight_kg * 35) / 1000.0
    
    if "very" in activity_level.lower() or "extra" in activity_level.lower():
        base_liters += 0.75
    elif "moderately" in activity_level.lower():
        base_liters += 0.5
    elif "lightly" in activity_level.lower():
        base_liters += 0.25

    return round(base_liters, 1)
