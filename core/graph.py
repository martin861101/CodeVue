from core.providers.ollama import OllamaProvider
from core.logger import sys_log

class NeuroGraph:
    def __init__(self):
        # Local Router Model
        self.local_llm = OllamaProvider(model="llama3.2") 
        self.api_llm = None 

    def set_api_provider(self, provider):
        self.api_llm = provider

    async def route_request(self, prompt):
        sys_log.log("GRAPH", f"Routing request: '{prompt[:30]}...'")
        
        routing_prompt = (
            f"Analyze this coding request: '{prompt}'\n"
            "If it is a simple code explanation, generic question, or local file retrieval, reply 'simple'.\n"
            "If it requires complex reasoning, refactoring, or external API knowledge, reply 'complex'.\n"
            "Reply ONLY with the word 'simple' or 'complex'."
        )
        
        try:
            response = ""
            async for token in self.local_llm.stream(routing_prompt):
                response += token
            
            decision = response.strip().lower()
            sys_log.log("GRAPH", f"Decision: {decision.upper()}", "DEBUG")
            
            if "simple" in decision:
                return "simple"
            return "complex"
        except Exception as e:
            sys_log.log("GRAPH", f"Routing Error: {e}. Defaulting to complex.", "ERROR")
            return "complex"
