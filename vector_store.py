import os
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional
from schemas import SearchResultItem
from config import settings

class VectorStoreService:
    def __init__(self, collection_name: str="enterprise_rag_docs"):
        api_key = os.getenv("OPEAI_API_KEY")

        self.provider=settings.EMBEDDED_PROVIDER
        #persistant storage locally inside chromadb folder
        self.chroma_client = chromadb.PersistentClient(path="./chromadb")

        #factory method to reolve embedding provider and isolated collection
        self.embedding_fn, self.collection_name=self._resolve_embedding_provider()

        #initialize or get chroma collection
        self.collection=self.chroma_client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=self.embedding_fn,
            metadata={"hnsw:space":"cosine"},
        )

    def add_chunks(self,chunks: List[Dict[str,Any]])-> int :
        """
        Adds text chunks and metadata to ChromaDB collection
        """
        if not chunks:
            return 0

        ids=[c["chunk_id"] for c in chunks]
        documents=[c["text"] for c in chunks]
        metadatas=[c["metadata"] for c in chunks]

        self.collection.add(
            ids= ids,
            documents=documents,
            metadatas=metadatas
        )
        return len(chunks)

    def search(self, query:str, top_k: int =3, filter_metadata: Optional[Dict[str,Any]]= None)-> List[SearchResultItem]:
        """
        Queries the vector index using cosine similarity
        """
        where_clause= filter_metadata if filter_metadata else None

        results=self.collection.query(
            query_texts=[query],
            n_results=top_k,
            where=where_clause,
            include=["documents","metadata","distances"]
        )
        search_items=[]
        if results and results["ids"] and len(results["ids"][0])>0:
            for i in range(len(results["ids"][0])):
                search_items.append(SearchResultItem(
                    chunk_id=results["ids"][0][i],
                    document_id=results["metadatas"][0][i].get("document_id",""),
                    text=results["documents"][0][i],
                    score=round(results["distances"][0][i],4),
                    metadata=results["metadatas"][0][i]
                ))
        return search_items

    def count(self) -> int:
        return self.collection.count()

    def _resolve_embedding_provider(self):
        if self.provider=="openai"
            if not settings.OPEAI_API_KEY:
                raise ValueError("EMBEDDING_PROVIDER is 'openai' but OPEAI_API_KEY is missing.")
        
        #openai embedding function
            ef=embedding_functions.OpenAIEmbeddingFunction(
                api_key=OPEAI_API_KEY,
                model_name="text-embedding-3-small"
            )
            collection_name="enterprise_rag_openai"

        elif self.provider=="local":
            ef=embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="all-MiniLM-L6-v2"
            )
            collection_name="enterprise_rag_local"

        else:
            raise ValueError(f"Unsupported EMBEDDINF_PROVIDER: '{self.provider}' Use 'openai' or 'local'")
        
        return ef, collection_name

    
    