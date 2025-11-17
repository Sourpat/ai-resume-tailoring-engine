import json
from pathlib import Path

from openai import OpenAI


class TailoringEngineAgent:
    def __init__(self):
        self.client = OpenAI()
        self.prompt_path = Path(__file__).resolve().parents[2] / "docs" / "prompts" / "agent3_tailor.txt"

    def _load_prompt(self) -> str:
        return self.prompt_path.read_text()

    def _fallback_response(self) -> dict:
        return {
            "product_owner_section": [],
            "business_analyst_section": [],
            "technical_ba_section": [],
        }

    def run(self, jd_analysis: dict, retrieved_seeds: dict) -> dict:
        prompt = self._load_prompt()
        analysis_text = json.dumps(jd_analysis or {}, indent=2)
        seeds_text = json.dumps(retrieved_seeds.get("retrieved_seeds", []), indent=2)

        user_prompt = (
            f"{prompt}\n\nJob Description Analysis:\n{analysis_text}\n\n"
            f"Retrieved Seeds:\n{seeds_text}\n\nReturn JSON only."
        )

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
