# llm_agent.py
# -----------------------------
# This file contains the main LLMCoreAgent class.
# It coordinates the strategy selection, invokes appropriate tools,
# enriches the context using a Knowledge Base (RAG), and generates
# a final response using the OpenAI GPT model.

from openai import OpenAI
from config import OPENAI_API_KEY
from rag.knowledge_base import KnowledgeBase

# Initialize OpenAI client using new API format (v1+)
client = OpenAI(api_key=OPENAI_API_KEY)

class LLMCoreAgent:
    def __init__(self, strategy_selector, tools):
        # StrategySelector decides which path to follow
        # Tools is a dictionary with ImagingAI and ClinicalModel
        self.strategy_selector = strategy_selector
        self.tools = tools

        # Knowledge base initialized with preprocessed clinical documents
        self.kb = KnowledgeBase()

    def handle_case(self, case_data):
        """
        Main entry point: Given a case, select strategy, run tools,
        enrich with knowledge base, and produce final answer.
        """
        # Step 1: Select the appropriate strategy
        strategy = self.strategy_selector.select(case_data)

        # Step 2: Run the selected strategy with the appropriate tools
        tool_results = strategy.execute(case_data, self.tools)

        # Step 3: Query Knowledge Base for relevant clinical info
        user_question = case_data.get("question", "")
        kb_docs = self.kb.query(user_question)
        kb_context = "\n\n".join([doc if isinstance(doc, str) else doc.get("text", "") for doc in kb_docs])


        # Step 4: Compose final answer using OpenAI GPT
        return self.compose_response(tool_results, kb_context)

    def compose_response(self, tool_results, kb_text):
        """
        Use OpenAI GPT to generate a personalized, clinically relevant answer.
        The context includes both tool outputs and relevant knowledge.
        """
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # Use gpt-4 if enabled in your account
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a clinical assistant specialized in pediatric leukemia. "
                            "Use both tool outputs and evidence from clinical guidelines to help doctors."
                        )
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Tool Output:\n{tool_results}\n\n"
                            f"Relevant Knowledge Base Documents:\n{kb_text}"
                        )
                    }
                ],
                max_tokens=700,
                temperature=0.4
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ Error generating response from GPT: {str(e)}"
