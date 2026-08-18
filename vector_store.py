import os
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
from typing import List, Dict, Any
from schemas import SearchResultItem

load_dotenv()

class VectorStoreService:
    def __init__(self, collection_name: str="enterprise_rag_docs"):
        api_key = os.getenv("OPEAI_API_KEY")

        #persistant storage locally inside chromadb folder
        self.chroma_client = chromadb.PersistentClient(path="./chromadb")

        #openai embedding function
        self.openai_ef = embedding_functions.OpenAIEmbeddingFunction(
            api_key=api_key,
            model_name="text-embedding-3-small"
        )

        #initialize or get chroma collection
        self.collection=self.chroma_client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.openai_ef,
            metadata={"hnsw:space":"cosine"},
        )

    def add_chunks(self,chunks: List[Dict[str,Any]])-> int :
        """
        Adds text chunks and metadata to ChromaDB collection
        """

        ids=[c["chunk_id"] for c in chunks]
        documents=[c["text"] for c in chunks]
        metadatas=[c["metadata"] for c in chunks]

        self.collection.add(
            ids= ids,
            documents=documents,
            metadatas=metadatas
        )

    def search(Self, query:str, top_k: int =3)-> List[SearchResultItem]:
        """
        Queries the vector index using cosine similarity
        """
        results=self.collection.query(
            query_texts=[query],
            n_results=top_k,
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
