import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPEN_API_KEY: str=os.getenv("OPEAI_API_KEY","")
    EMBEDDING_PROVIDER: str=os.getenv("EMBEDDED_PROVIDER", "local").lower()
    CHROMA_PERSIST_DIR: str=os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")

settings=Settings()
