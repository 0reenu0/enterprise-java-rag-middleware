import tiktoken
from typing import List, Dict, Any

class DocumentChunker:
    def __init__(self, chunk_size: int = 250, chunk_overlap: int = 50, model_name: str = "text-embedding-3-small"):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.tokenizer = tiktoken.encoding_for_model(model_name)

    def split_text(self, text: str, doc_id: str, title: str, extra_metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Splits raw text into token-bounded chunks with sliding window overlap.
        """
        tokens = self.tokenizer.encode(text)
        chunks = []
        
        if not tokens:
            return chunks

        start = 0
        chunk_idx = 0

        while start < len(tokens):
            end = start + self.chunk_size
            chunk_tokens = tokens[start:end]
            chunk_text = self.tokenizer.decode(chunk_tokens)
            
            chunk_metadata = {
                "document_id": doc_id,
                "title": title,
                "chunk_index": chunk_idx,
                "token_count": len(chunk_tokens),
            }
            if extra_metadata:
                chunk_metadata.update(extra_metadata)

            chunks.append({
                "chunk_id": f"{doc_id}_chunk_{chunk_idx}",
                "text": chunk_text,
                "metadata": chunk_metadata
            })

            chunk_idx += 1
            start += (self.chunk_size - self.chunk_overlap)

        return chunks