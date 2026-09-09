"""
Coordinator Master Agent.
Routes user query to specialist agents (Nutrition, Fitness, Lifestyle), orchestrates their responses,
and synthesizes a unified personalized health coaching plan.
"""

from typing import Dict, Any, List, Tuple
from agents.base_agent import BaseAgent
from agents.nutrition_agent import NutritionAgent
from agents.fitness_agent import FitnessAgent
from agents.lifestyle_agent import LifestyleAgent

COORDINATOR_SYSTEM_PROMPT = """You are the Lead Coordinator AI Health Coach.
Your task is to analyze the user's inquiry and profile, select the appropriate specialist agent(s) (Nutrition, Fitness, Lifestyle), and synthesize their recommendations into a clear, unified, friendly response.
"""

class CoordinatorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Coordinator Agent",
            role="Lead Health Orchestrator",
            system_prompt=COORDINATOR_SYSTEM_PROMPT
        )
        self.nutrition_agent = NutritionAgent()
        self.fitness_agent = FitnessAgent()
        self.lifestyle_agent = LifestyleAgent()

    def determine_active_agents(self, prompt: str) -> List[str]:
        """Analyze user query to decide which agent(s) should respond."""
        p_lower = prompt.lower()
        active = []

        is_nutrition = any(w in p_lower for w in ["diet", "food", "meal", "nutrit", "eat", "protein", "calorie", "carb", "fat", "snack", "breakfast", "lunch", "dinner", "recipe", "veg"])
        is_fitness = any(w in p_lower for w in ["workout", "exercise", "gym", "train", "pushup", "squat", "cardio", "run", "lift", "weight", "home workout", "sets", "reps", "routine"])
        is_lifestyle = any(w in p_lower for w in ["sleep", "water", "drink", "stress", "habit", "lifestyle", "recover", "walk", "fatigue", "tired", "mind", "focus"])

        if is_nutrition:
            active.append("nutrition")
        if is_fitness:
            active.append("fitness")
        if is_lifestyle:
            active.append("lifestyle")

        # If general request or none explicitly matched, activate all 3 for a full holistic plan
        if not active or "plan" in p_lower or "overall" in p_lower or "today" in p_lower or "help" in p_lower:
            active = ["nutrition", "fitness", "lifestyle"]

        return active

    def process_query(self, prompt: str, user_profile: Dict[str, Any], api_key: str = "") -> Tuple[str, List[str]]:
        """
        Processes query:
        1. Identifies active sub-agents.
        2. Solicits responses from active agents.
        3. Merges and formats response with agent badges.
        """
        active_agents = self.determine_active_agents(prompt)
        agent_names = []
        sections = []

        # Header summary from Coordinator
        name = user_profile.get("name", "User")
        goal = user_profile.get("goal", "Stay Fit")
        
        intro = f"👋 **Hello {name}!** Here is your personalized recommendation from your AI Health Coaching Team tailored for your goal: **{goal}**.\n"
        sections.append(intro)

        if "nutrition" in active_agents:
            agent_names.append("Nutrition Agent")
            nut_response = self.nutrition_agent.generate_response(prompt, user_profile, api_key)
            sections.append(f"--- \n#### 🏷️ Contribution from **Nutrition Agent**\n{nut_response}")

        if "fitness" in active_agents:
            agent_names.append("Fitness Agent")
            fit_response = self.fitness_agent.generate_response(prompt, user_profile, api_key)
            sections.append(f"--- \n#### 🏷️ Contribution from **Fitness Agent**\n{fit_response}")

        if "lifestyle" in active_agents:
            agent_names.append("Lifestyle Agent")
            life_response = self.lifestyle_agent.generate_response(prompt, user_profile, api_key)
            sections.append(f"--- \n#### 🏷️ Contribution from **Lifestyle Agent**\n{life_response}")

        # Add mandatory medical disclaimer
        disclaimer = "\n\n> ⚠️ **Safety Disclaimer**: *This application provides general educational health & fitness suggestions powered by AI agents. It is NOT medical advice or diagnosis. Always consult a physician or healthcare professional for health issues.*"
        sections.append(disclaimer)

        final_text = "\n\n".join(sections)
        return final_text, agent_names
