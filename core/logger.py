import logging
import time
from pathlib import Path

class SystemLogger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SystemLogger, cls).__new__(cls)
            cls._instance._setup()
        return cls._instance

    def _setup(self):
        self.log_file = Path("system.log")
        
        # Setup standard python logging
        self.logger = logging.getLogger("NeuroTerm")
        self.logger.setLevel(logging.DEBUG)
        
        # File Handler (Persistent logs)
        fh = logging.FileHandler(self.log_file, mode='a', encoding='utf-8')
        fh.setFormatter(logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s'))
        self.logger.addHandler(fh)

    def log(self, component: str, message: str, level="INFO"):
        formatted_msg = f"[{component.upper()}] {message}"
        
        if level == "INFO":
            self.logger.info(formatted_msg)
        elif level == "DEBUG":
            self.logger.debug(formatted_msg)
        elif level == "ERROR":
            self.logger.error(formatted_msg)
            
        return formatted_msg

    def get_recent_logs(self, n=20):
        if not self.log_file.exists():
            return ["No logs yet."]
        
        with open(self.log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            return [line.strip() for line in lines[-n:]]

sys_log = SystemLogger()
