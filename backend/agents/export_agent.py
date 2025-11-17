import base64

from services.export_service import ExportService


class ExportAgent:
    def __init__(self):
        self.export_service = ExportService()

    def run(self, formatted_output: dict) -> dict:
        po_section = formatted_output.get("po", []) if isinstance(formatted_output, dict) else []
        ba_section = formatted_output.get("ba", []) if isinstance(formatted_output, dict) else []
        technical_ba_section = formatted_output.get("technical_ba", []) if isinstance(formatted_output, dict) else []

        markdown_output = self.export_service.generate_markdown(po_section, ba_section, technical_ba_section)
        docx_buffer = self.export_service.generate_docx(po_section, ba_section, technical_ba_section)
        pdf_buffer = self.export_service.generate_pdf(po_section, ba_section, technical_ba_section)

        docx_base64 = base64.b64encode(docx_buffer.getvalue()).decode("utf-8")
        pdf_base64 = base64.b64encode(pdf_buffer.getvalue()).decode("utf-8")

        return {
            "md": markdown_output,
            "docx": docx_base64,
            "pdf": pdf_base64,
        }
