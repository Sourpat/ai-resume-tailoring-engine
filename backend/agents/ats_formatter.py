import json
from pathlib import Path

from openai import OpenAI


class ATSFormatterAgent:
    def __init__(self):
        self.client = OpenAI()
        self.prompt_path = Path(__file__).resolve().parents[2] / "docs" / "prompts" / "agent4_ats_formatter.txt"

    def _load_prompt(self) -> str:
        return self.prompt_path.read_text()

    def _fallback_response(self) -> dict:
        return {
            "formatted_po": [],
            "formatted_ba": [],
            "formatted_technical_ba": [],
            "keyword_density_score": "",
            "final_recommendations": [],
        }

    def run(self, tailored_bullets: dict) -> dict:
        prompt = self._load_prompt()
        bullets_text = json.dumps(tailored_bullets or {}, indent=2)
        user_prompt = f"{prompt}\n\nTailored Bullets:\n{bullets_text}\n\nReturn JSON only."

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
