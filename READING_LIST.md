# Enterprise RAG Middleware — Core Concepts & Reading List
# Enterprise RAG Middleware — Core Concepts & Reading List

This file consolidates the daily architectural deep dives, core concepts, and official reading resources across the 14-day build.

---

## 📌 Day 1: Production FastAPI Setup & Pydantic V2 Schemas

* **FastAPI Request Lifecycle & Pydantic V2 Validation:**
  Learn how FastAPI leverages Pydantic for high-performance data parsing, strict typing, and automated OpenAPI (Swagger) documentation generation.
  * 🔗 [FastAPI First Steps & Tutorial](https://fastapi.tiangolo.com/tutorial/first-steps/)
  * 🔗 [Pydantic V2 Migration Guide & Improvements](https://docs.pydantic.dev/latest/migration/)

* **Docker Multi-Stage Builds for Python:**
  Understand container optimization, image layer caching, non-root user security, and managing virtual environments in production containers.
  * 🔗 [Dockerizing FastAPI Applications Guide](https://fastapi.tiangolo.com/deployment/docker/)

---

## 📌 Day 2: Document Chunking Strategies & ChromaDB Vector Persistence

* **Token-Bounded Chunking & Overlaps:**
  Explore strategies for splitting text without breaking context boundaries. Understand why sliding-window token chunking outperforms arbitrary character limits.
  * 🔗 [OpenAI Cookbook: How to Count Tokens with Tiktoken](https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb)

* **HNSW (Hierarchical Navigable Small World) Indexing:**
  Deep dive into probability skip lists and proximity graphs that power high-speed Approximate Nearest Neighbor (ANN) search inside ChromaDB.
  * 🔗 [Pinecone Deep-Dive: Hierarchical Navigable Small Worlds (HNSW)](https://www.pinecone.io/learn/series/faiss/hnsw/)

---

## 📌 Day 3: Embedding Provider Factory & Metadata Pre-Filtering

* **Dense Embeddings & Dimensionality Alignment:**
  Compare high-dimensional cloud APIs (	ext-embedding-3-small / 1536-D) against lightweight local CPU models (ll-MiniLM-L6-v2 / 384-D).
  * 🔗 [OpenAI Embeddings Official Documentation](https://platform.openai.com/docs/guides/embeddings)
  * 🔗 [Hugging Face: sentence-transformers/all-MiniLM-L6-v2 Model Card](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)

* **Pre-Filtering vs. Post-Filtering in Vector Stores:**
  Learn why applying structured metadata filters (where clauses) *before* similarity calculations maintains search speed and prevents precision degradation.
  * 🔗 [ChromaDB Docs: Querying Collections with Metadata Filtering](https://docs.trychroma.com/docs/querying-collections/metadata-filtering)

---

## 📌 Day 4: Hybrid Search Engine Architecture & Reciprocal Rank Fusion (RRF)

* **Sparse vs. Dense Retrieval (BM25 + Vector Search):**
  Understand why dense semantic vectors fail at exact keyword lookups (error codes, product SKUs) and how sparse BM25 indices fill the gap.
  * 🔗 [Pinecone Guide: Hybrid Search Overview & Concepts](https://docs.pinecone.io/guides/search/hybrid-search)
  * 🔗 [GitHub: Rank-BM25 Python Package Repository](https://github.com/dorianbrown/rank_bm25)

* **Reciprocal Rank Fusion (RRF) Mathematics:**
  Examine the math behind position-based rank fusion (\_Score(d) = \sum \frac{1}{k + r(d)}$) and how it merges incompatible score distributions.
  * 🔗 [MongoDB Engineering: Better RAG Results With Reciprocal Rank Fusion](https://www.mongodb.com/resources/basics/reciprocal-rank-fusion)
  * 🔗 [SIGIR 2009 Research Paper: Reciprocal Rank Fusion Outperforms Condorcet](https://dl.acm.org/doi/10.1145/1571941.1572114)

---

## 📌 Day 5: Language-Agnostic gRPC Contracts with Protocol Buffers

* **Protocol Buffers v3 (proto3) Syntax & Encoding:**
  Master language-agnostic interface definitions, field numbering rules, and binary serialization advantages over JSON.
  * 🔗 [Protobuf Language Guide (proto3)](https://protobuf.dev/programming-guides/proto3/)

* **gRPC Concepts & Code Generation:**
  Understand HTTP/2 multiplexing, streaming capabilities, and stub generation workflow in Python using grpcio-tools.
  * 🔗 [gRPC Core Concepts & Architecture](https://grpc.io/docs/what-is-grpc/core-concepts/)
  * 🔗 [gRPC Python Basics Guide](https://grpc.io/docs/languages/python/basics/)
