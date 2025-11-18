from agents.ats_formatter import ATSFormatterAgent
from agents.export_agent import ExportAgent
from agents.jd_analyzer import JdAnalyzerAgent
from agents.rag_retriever import RagRetrieverAgent
from agents.tailoring_engine import TailoringEngineAgent
from backend.services.logging_service import LoggingService


class AgentOrchestrator:
    def __init__(self):
        self.jd_analyzer = JdAnalyzerAgent()
        self.rag_retriever = RagRetrieverAgent()
        self.tailoring_engine = TailoringEngineAgent()
        self.ats_formatter = ATSFormatterAgent()
        self.export_agent = ExportAgent()
        self.logger = LoggingService()

    def run_pipeline(self, jd_text: str) -> dict:
        try:
            self.logger.log_info("Running JD Analyzer...")
            jd_analysis = self.jd_analyzer.run(jd_text)
            self.logger.log_debug(f"JD analysis result: {jd_analysis}")
            self.logger.log_info("JD Analyzer completed")

            self.logger.log_info("Running RAG Retriever...")
            retrieved_seeds = self.rag_retriever.run(jd_analysis)
            self.logger.log_debug(f"RAG retriever result: {retrieved_seeds}")
            self.logger.log_info("RAG Retriever completed")

            self.logger.log_info("Running Tailoring Engine...")
            tailored_bullets = self.tailoring_engine.run(jd_analysis, retrieved_seeds)
            self.logger.log_debug(f"Tailoring engine result: {tailored_bullets}")
            self.logger.log_info("Tailoring Engine completed")

            self.logger.log_info("Running ATS Formatter...")
            formatted_output = self.ats_formatter.run(tailored_bullets)
            self.logger.log_debug(f"ATS formatter result: {formatted_output}")
            self.logger.log_info("ATS Formatter completed")

            self.logger.log_info("Running Export Agent...")
            exports = self.export_agent.run(formatted_output)
            self.logger.log_debug(f"Export agent result: {exports}")
            self.logger.log_info("Export Agent completed")

            self.logger.log_info("Pipeline run complete.")

            return {
                "jd_analysis": jd_analysis,
                "retrieved_seeds": retrieved_seeds,
                "tailored_bullets": tailored_bullets,
                "formatted_output": formatted_output,
                "exports": exports,
            }
        except Exception as e:
            self.logger.log_error(f"Pipeline failed: {str(e)}")
            return {
                "error": True,
                "message": "Pipeline failed internally.",
                "details": str(e)
            }
