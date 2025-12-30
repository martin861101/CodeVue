import sqlite3
import time
import shutil
from pathlib import Path
from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from core.logger import sys_log

class MemoryManager:
    def __init__(self, db_path="neuroterm.db", chroma_path="neuroterm_chroma"):
        self.db_path = db_path
        
        sys_log.log("MEMORY", "Initializing Vector DB (nomic-embed-text)...")
        self.embedding_fn = OllamaEmbeddings(model="nomic-embed-text") 
        self.vector_store = Chroma(
            collection_name="chat_history",
            embedding_function=self.embedding_fn,
            persist_directory=chroma_path
        )
        
        self._init_sql()

    def _init_sql(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS logs 
                     (id INTEGER PRIMARY KEY, timestamp REAL, user_msg TEXT, ai_msg TEXT, context TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS backups
                     (id INTEGER PRIMARY KEY, timestamp REAL, original_path TEXT, backup_path TEXT)''')
        conn.commit()
        conn.close()

    def save_interaction(self, user_msg, ai_msg, context=""):
        # SQL
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("INSERT INTO logs (timestamp, user_msg, ai_msg, context) VALUES (?, ?, ?, ?)",
                  (time.time(), user_msg, ai_msg, context))
        conn.commit()
        conn.close()

        # Vector
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        text = f"User: {user_msg}\nAI: {ai_msg}"
        docs = splitter.create_documents([text])
        self.vector_store.add_documents(docs)
        sys_log.log("MEMORY", "Interaction saved to Long-Term Memory.")

    def retrieve_context(self, query, k=2):
        sys_log.log("MEMORY", f"Retrieving context for: '{query[:30]}...'")
        try:
            results = self.vector_store.similarity_search(query, k=k)
            if not results: return ""
            return "\n---\n".join([doc.page_content for doc in results])
        except Exception as e:
            sys_log.log("MEMORY", f"Retrieval Error: {e}", "ERROR")
            return ""

    def create_backup(self, file_path):
        src = Path(file_path)
        if not src.exists(): return None
        
        ts = int(time.time())
        dest = f"{file_path}.{ts}.bak"
        shutil.copy2(src, dest)
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("INSERT INTO backups (timestamp, original_path, backup_path) VALUES (?, ?, ?)",
                  (time.time(), str(src), dest))
        conn.commit()
        conn.close()
        sys_log.log("MEMORY", f"Backup created: {dest}")
        return dest
