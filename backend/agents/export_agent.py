from pathlib import Path


class ExportAgent:
    def __init__(self):
        self.prompt_path = Path(__file__).resolve().parents[2] / "docs" / "prompts" / "agent5_export.txt"

    def _build_markdown(self, formatted_output: dict) -> str:
        po_section = formatted_output.get("formatted_po", []) if isinstance(formatted_output, dict) else []
        ba_section = formatted_output.get("formatted_ba", []) if isinstance(formatted_output, dict) else []
        technical_ba_section = (
            formatted_output.get("formatted_technical_ba", []) if isinstance(formatted_output, dict) else []
        )
        recommendations = formatted_output.get("final_recommendations", []) if isinstance(formatted_output, dict) else []

        markdown_lines = ["# Tailored Resume", "## Product Owner – Henry Schein"]
        markdown_lines.extend([f"- {item}" for item in po_section])

        markdown_lines.append("\n## Business Analyst – Henry Schein")
        markdown_lines.extend([f"- {item}" for item in ba_section])

        markdown_lines.append("\n## Technical BA – AXA XL (RPA)")
        markdown_lines.extend([f"- {item}" for item in technical_ba_section])

        if recommendations:
            markdown_lines.append("\n## Final Recommendations")
            markdown_lines.extend([f"- {item}" for item in recommendations])

        return "\n".join(markdown_lines)

    def run(self, formatted_output: dict) -> dict:
        markdown_content = self._build_markdown(formatted_output)

        return {
            "docx_structure": "DOCX export placeholder - populate in Step 9",
            "pdf_structure": "PDF export placeholder - populate in Step 9",
            "md_structure": markdown_content,
        }
