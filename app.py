from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, RichLog
from textual.binding import Binding
from rich.markdown import Markdown
import asyncio
from pathlib import Path

from core.agent import NeuroAgent
from core.providers.gemini import GeminiProvider
from core.providers.ollama import OllamaProvider
from core.providers.openrouter import OpenRouterProvider


class NeuroTermApp(App):
    CSS = """
    RichLog {
        border: solid $primary;
        height: 1fr;
    }
    Input {
        dock: bottom;
    }
    """

    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit"),
        Binding("ctrl+l", "clear", "Clear"),
    ]

    def __init__(self):
        super().__init__()
        # Default to Gemini, but easily switchable
        api_key = os.getenv("GEMINI_API_KEY", "")
        self.agent = NeuroAgent("gemini", api_key=api_key)
        self.current_provider = "gemini"

    def compose(self) -> ComposeResult:
        yield Header()
        yield RichLog(id="chat")
        yield Input(placeholder="Enter message or /command...")
        yield Footer()

    async def on_mount(self):
        self.log_widget = self.query_one(RichLog)
        self.input = self.query_one(Input)
        self.log_widget.write(Markdown("# Neuroterm\nType `/help` for commands"))

    async def on_input_submitted(self, event: Input.Submitted):
        msg = event.value.strip()
        if not msg:
            return

        self.input.value = ""

        # Handle commands
        if msg.startswith("/"):
            await self.handle_command(msg)
            return

        # Show user message
        self.log_widget.write(Markdown(f"**You:** {msg}"))

        # Stream AI response
        response = ""
        async for token in self.agent.stream(msg):
            response += token
        self.log_widget.write(Markdown(f"**Neuroterm:** {response}"))

    async def handle_command(self, cmd: str):
        parts = cmd.split(maxsplit=1)
        base = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        try:
            if base == "/help":
                help_text = """
**Commands:**
- `/provider <name>` - Switch provider (gemini, ollama, openrouter)
- `/model <name>` - Switch model
- `/scan [path]` - List directory files
- `/read <file>` - Read file contents
- `/tree [path]` - Show directory tree
- `/exec <file>` - Execute Python file
- `/new project <name>` - Create new project
- `/allow write` - Enable file writing
- `/deny write` - Disable file writing
- `/open <file>` - Set active file for context
- `/clear` - Clear chat
"""
                self.log_widget.write(Markdown(help_text))

            elif base == "/provider":
                await self.switch_provider(arg)

            elif base == "/scan":
                files = self.agent.files.scan_directory(arg or ".")
                output = "\n".join(
                    f"{'📁' if f['type'] == 'dir' else '📄'} {f['path']}" for f in files
                )
                self.log_widget.write(output)

            elif base == "/read":
                content = self.agent.files.read_file(arg)
                self.log_widget.write(Markdown(f"```\n{content}\n```"))

            elif base == "/tree":
                tree = self.agent.files.tree(arg or ".")
                self.log_widget.write(tree)

            elif base == "/exec":
                output = self.agent.files.execute_python(arg)
                self.log_widget.write(Markdown(f"```\n{output}\n```"))

            elif base == "/new":
                if arg.startswith("project "):
                    name = arg.replace("project ", "").strip()
                    path = self.agent.files.create_project(name)
                    self.log_widget.write(f"✅ Created project: {path}")

            elif base == "/allow":
                if arg == "write":
                    self.agent.files.write_allowed = True
                    self.log_widget.write("✅ Write permissions enabled")

            elif base == "/deny":
                if arg == "write":
                    self.agent.files.write_allowed = False
                    self.log_widget.write("🔒 Write permissions disabled")

            elif base == "/open":
                self.agent.files.active_file = arg
                self.log_widget.write(f"📂 Active file: {arg}")

            elif base == "/clear":
                self.log_widget.clear()

        except Exception as e:
            self.log_widget.write(f"❌ Error: {str(e)}")

    async def switch_provider(self, provider_name: str):
        if provider_name == "gemini":
            api_key = os.getenv("GEMINI_API_KEY", "")
            self.agent.provider = GeminiProvider(api_key)
        elif provider_name == "ollama":
            self.agent.provider = OllamaProvider()
        elif provider_name == "openrouter":
            api_key = os.getenv("OPENROUTER_API_KEY", "")
            self.agent.provider = OpenRouterProvider(api_key)
        else:
            self.log_widget.write(f"❌ Unknown provider: {provider_name}")
            return

        self.current_provider = provider_name
        self.log_widget.write(f"✅ Switched to {provider_name}")

    def action_clear(self):
        self.log_widget.clear()

    def action_quit(self):
        self.exit()


if __name__ == "__main__":
    import os

    app = NeuroTermApp()
    app.run()
