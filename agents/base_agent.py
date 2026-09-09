"""
Base Agent Abstract Class for Specialized AI Health Agents.
Supports LLM integration (Google Gemini / Groq) with smart fallback rule engine.
"""

import os
import requests
from typing import Dict, Any, Optional

class BaseAgent:
    def __init__(self, name: str, role: str, system_prompt: str):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt

    def _call_gemini_api(self, prompt: str, api_key: str) -> Optional[str]:
        """Call Google Gemini API using SDK or direct HTTP request."""
        # Try google.genai SDK first
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            # Use gemini-2.5-flash or gemini-1.5-flash
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=f"{self.system_prompt}\n\nUser Question/Context:\n{prompt}"
            )
            if response and hasattr(response, 'text') and response.text:
                return response.text.strip()
        except Exception as e:
            pass

        # Fallback to direct HTTP endpoint for Gemini API
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [{"text": f"{self.system_prompt}\n\n{prompt}"}]
                    }
                ]
            }
            res = requests.post(url, json=payload, headers=headers, timeout=12)
            if res.status_code == 200:
                data = res.json()
                text = data['candidates'][0]['content']['parts'][0]['text']
                return text.strip()
        except Exception as err:
            print(f"Gemini API request error: {err}")
            
        return None

    def _call_groq_api(self, prompt: str, api_key: str) -> Optional[str]:
        """Call Groq API (free high-speed LLM endpoint)."""
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "llama3-8b-8192",
                "messages": [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7
            }
            res = requests.post(url, json=payload, headers=headers, timeout=12)
            if res.status_code == 200:
                data = res.json()
                return data['choices'][0]['message']['content'].strip()
        except Exception as err:
            print(f"Groq API error: {err}")
        return None

    def generate_response(self, prompt: str, user_profile: Dict[str, Any], api_key: Optional[str] = None) -> str:
        """
        Generate response using available LLM API key, or fall back to
        the specialized rule-based generator.
        """
        effective_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GROQ_API_KEY") or user_profile.get("api_key", "")

        if effective_key:
            # Check if key looks like Groq key (starts with gsk_) or Gemini key
            if effective_key.startswith("gsk_"):
                response = self._call_groq_api(prompt, effective_key)
            else:
                response = self._call_gemini_api(prompt, effective_key)
            
            if response:
                return response

        # Fallback generator if no key or API failed
        return self.fallback_rule_response(prompt, user_profile)

    def fallback_rule_response(self, prompt: str, user_profile: Dict[str, Any]) -> str:
        """Override in child agent classes to provide smart offline responses."""
        return f"**[{self.name}]**: Standard recommendation for {user_profile.get('name', 'User')} based on goal '{user_profile.get('goal')}'."
