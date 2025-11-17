import json
from pathlib import Path

from openai import OpenAI


class JdAnalyzerAgent:
    def __init__(self):
        self.client = OpenAI()
        self.prompt_path = Path(__file__).resolve().parents[2] / "docs" / "prompts" / "agent1_jd_analyzer.txt"

    def _load_prompt(self) -> str:
        return self.prompt_path.read_text()

    def _fallback_response(self) -> dict:
        return {
            "role_title": "",
            "primary_responsibilities": [],
            "required_skills": [],
            "preferred_skills": [],
            "tools_mentioned": [],
            "soft_skills": [],
            "seniority_level": "",
            "JD_summary": "",
        }

    def run(self, jd_text: str) -> dict:
        prompt = self._load_prompt()
        user_prompt = f"{prompt}\n\nJob Description:\n{jd_text}\n\nReturn JSON only."

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": user_prompt}],
            )
            content = response.choices[0].message.content or ""
            parsed = json.loads(content)
            if isinstance(parsed, dict):
                return parsed
        except Exception:
            pass

        return self._fallback_response()
