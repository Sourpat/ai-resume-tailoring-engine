from backend.agents.ats_formatter import ATSFormatterAgent
from backend.agents.export_agent import ExportAgent
from backend.agents.jd_analyzer import JdAnalyzerAgent
from backend.agents.rag_retriever import RagRetrieverAgent
from backend.agents.tailoring_engine import TailoringEngineAgent


class AgentOrchestrator:
    def __init__(self):
        self.jd_analyzer = JdAnalyzerAgent()
        self.rag_retriever = RagRetrieverAgent()
        self.tailoring_engine = TailoringEngineAgent()
        self.ats_formatter = ATSFormatterAgent()
        self.export_agent = ExportAgent()

    def run_pipeline(self, jd_text: str) -> dict:
        jd_analysis = self.jd_analyzer.run(jd_text)
        retrieved_seeds = self.rag_retriever.run(jd_analysis)
        tailored_bullets = self.tailoring_engine.run(jd_analysis, retrieved_seeds)
        formatted_output = self.ats_formatter.run(tailored_bullets)
        exports = self.export_agent.run(formatted_output)

        return {
            "jd_analysis": jd_analysis,
            "retrieved_seeds": retrieved_seeds,
            "tailored_bullets": tailored_bullets,
            "formatted_output": formatted_output,
            "exports": exports,
        }
