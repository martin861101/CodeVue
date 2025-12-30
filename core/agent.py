from core.providers import gemini, ollama, openrouter
from core.files import FileManager
from core.graph import NeuroGraph
from core.memory import MemoryManager
from core.logger import sys_log

PROVIDERS = {
    "gemini": gemini.GeminiProvider,
    "ollama": ollama.OllamaProvider,
    "openrouter": openrouter.OpenRouterProvider,
    "mistral": openrouter.OpenRouterProvider,
    "huggingface": openrouter.OpenRouterProvider,
}

class NeuroAgent:
    def __init__(self, provider_name="gemini", **kwargs):
        self.provider_name = provider_name
        self.kwargs = kwargs
        self.files = FileManager()
        self.memory = MemoryManager()
        self.graph = NeuroGraph()
        self._load_provider()

    def _load_provider(self):
        if self.provider_name not in PROVIDERS:
            raise ValueError(f"Provider {self.provider_name} not found.")
        provider_class = PROVIDERS[self.provider_name]
        self.provider = provider_class(**self.kwargs)
        self.graph.set_api_provider(self.provider)

    async def stream(self, prompt: str):
        sys_log.log("AGENT", "--- New Stream Request ---")
        
        # 1. RAG
        context = self.memory.retrieve_context(prompt)
        
        # 2. Routing
        complexity = await self.graph.route_request(prompt)
        
        # 3. Execution
        response_acc = ""
        if complexity == "simple":
            sys_log.log("AGENT", "Using Local Ollama (Simple)")
            yield "🚀 [Local]: Handling via Ollama...\n\n"
            streamer = self.graph.local_llm.stream(f"Context: {context}\n\nRequest: {prompt}")
        else:
            sys_log.log("AGENT", f"Using Cloud {self.provider_name} (Complex)")
            yield f"☁️ [Cloud]: Handling via {self.provider_name.capitalize()}...\n\n"
            full_prompt = f"RELEVANT MEMORY:\n{context}\n\nUSER REQUEST:\n{prompt}"
            streamer = self.provider.stream(full_prompt)

        async for token in streamer:
            response_acc += token
            yield token
            
        self.memory.save_interaction(prompt, response_acc, context)

    async def autonomous_fix(self, file_path, max_attempts=3):
        attempt = 1
        while attempt <= max_attempts:
            sys_log.log("AGENT", f"Auto-fix Attempt {attempt} for {file_path}")
            yield f"\n🔄 **Attempt {attempt}/{max_attempts}:** Executing `{file_path}`...\n"
            
            result = self.files.execute_script(file_path)
            
            if result["success"]:
                yield f"✅ **Success!** Script ran cleanly.\n"
                yield f"Output:\n```\n{result['output']}\n```\n"
                return
            
            yield f"❌ **Error Detected:**\n```text\n{result['error']}\n```\n"
            yield f"🧠 **Analyzing & Fixing...**\n"

            current_code = self.files.read_file(file_path)
            fix_prompt = (
                f"The python script `{file_path}` crashed.\n"
                f"ERROR:\n{result['error']}\n\n"
                f"CODE:\n{current_code}\n\n"
                "TASK: Return ONLY the fixed code."
            )
            
            fix_response = ""
            async for chunk in self.provider.stream(fix_prompt):
                fix_response += chunk
            
            fixed_code = fix_response.replace("```python", "").replace("```", "").strip()

            self.memory.create_backup(file_path)
            self.files.write_allowed = True
            self.files.write_file(file_path, fixed_code)
            
            yield f"🛠️ **Patch Applied.** Retrying...\n"
            attempt += 1

        yield f"⚠️ **Failed to fix script after {max_attempts} attempts.**\n"
