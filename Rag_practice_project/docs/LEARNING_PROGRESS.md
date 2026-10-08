RAG Learning Progress

Completed

1. PDF Extraction

Learned and implemented:

* PDF text extraction using PyMuPDF
* page-level extraction
* retaining page information
* converting PDF content into usable text

Status: DONE

⸻

2. Text Cleaning

Learned why raw PDF extraction needs cleaning.

Handled concepts such as:

* excessive whitespace
* repeated blank lines
* unusual Unicode characters
* zero-width characters
* preserving useful paragraph structure

Status: DONE

⸻

3. Section Detection

Learned how document structure can be detected and retained.

Chunks can contain section information so retrieval can later understand document context.

Status: DONE

⸻

4. Chunking

Learned:

* why documents need to be divided into chunks
* chunk boundaries
* structured chunks
* chunk metadata
* page and section provenance

Approximately 60 chunks have been created.

Status: DONE

⸻

5. Structured Chunk Objects

The extracted document content was converted into structured chunk objects containing metadata and text.

Chunks currently contain information such as:

* document ID
* chunk index
* page number
* section title
* content/text
* provenance information

Status: DONE

⸻

6. PostgreSQL + pgvector

Set up PostgreSQL and pgAdmin 4 for storing document and chunk information.

Current database:

rag_tut

Implemented:

* document storage
* chunk storage
* chunk retrieval
* embedding storage using pgvector
* vector similarity search

SQLAlchemy is used to communicate with PostgreSQL.

Status: DONE

⸻

7. Embeddings

Learned the engineering-level embedding concepts.

We understand that an embedding model converts text into a numerical vector so that semantic relationships between chunks and queries can be compared.

Implemented:

* selected all-MiniLM-L6-v2
* loaded the model using Sentence Transformers
* generated embeddings for document chunks
* stored embeddings in PostgreSQL using pgvector
* generated embeddings for user queries
* used the same embedding model for documents and queries

Important implementation concepts understood:

* why the embedding model is needed
* what model.encode() does
* embedding vectors and their dimensions
* why document and query embeddings must use the same model
* how embeddings are stored in pgvector
* how the query vector is passed to PostgreSQL
* how vector distance is used for retrieval

Status: DONE

⸻

8. Semantic Retrieval

Implemented semantic/vector search using:

* Sentence Transformers
* all-MiniLM-L6-v2
* PostgreSQL
* pgvector
* SQLAlchemy

The pipeline is:

User Query
    ↓
Embedding Model
    ↓
Query Vector
    ↓
PostgreSQL + pgvector
    ↓
Vector Distance
    ↓
Ranked Chunks

The SQL query uses pgvector’s vector distance operator:

embedding <=> query_embedding

The returned distance is used to rank semantically relevant chunks.

Example retrieval successfully returned:

* Chunk 48 — Application
* Chunk 19 — Application Layer Protocols
* other semantically related chunks

Status: DONE

⸻

9. BM25 / Lexical Retrieval

Implemented lexical retrieval using:

* rank_bm25
* tokenized document content
* BM25 scoring

The pipeline is:

User Query
    ↓
Tokenization
    ↓
BM25
    ↓
Keyword-based scoring
    ↓
Ranked Chunks

BM25 provides a complementary retrieval signal to semantic search.

We learned why lexical retrieval is useful even when semantic embeddings are available:

* exact terminology
* keywords
* names
* technical terms
* cases where semantic similarity may miss an exact match

Status: DONE

⸻

10. Hybrid Retrieval

Combined two different retrieval strategies:

Semantic Search
        +
BM25 Search
        ↓
Hybrid Retrieval

Semantic search captures meaning and conceptual similarity.

BM25 captures lexical/keyword relevance.

The two systems use the same user query but retrieve candidates independently.

Status: DONE

⸻

11. Reciprocal Rank Fusion (RRF)

Implemented Reciprocal Rank Fusion to combine semantic and BM25 rankings.

We learned why raw scores should not simply be added:

Semantic distance → one scale
BM25 score        → another scale

Therefore:

Do not directly combine raw scores.

Instead, RRF combines rank positions.

The implemented formula is:

RRF(d) = Σ 1 / (k + rank)

with:

k = 60

Implemented architecture:

                    User Query
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
       Semantic Search          BM25
          Top 20                Top 20
              │                   │
              └─────────┬─────────┘
                        ▼
                       RRF
                        │
                        ▼
                  Final Ranking
                        │
                        ▼
                     Top 5

Successfully verified RRF on the practice IoT document.

Example final ranking:

1. Chunk 48 — Application
2. Chunk 19 — Application Layer Protocols
3. Chunk 18 — General
4. Chunk 15 — General
5. Chunk 24 — Transport Layer

We also verified that chunks appearing highly in both retrieval systems receive stronger RRF scores.

Status: DONE

⸻

Currently Learning

12. Reranking

The next stage is reranking the candidate chunks produced by hybrid retrieval.

Current retrieval pipeline:

Query
  ↓
Semantic Search → Top 20
  ↓
BM25 → Top 20
  ↓
RRF
  ↓
Candidate Ranking

Next:

RRF Candidates
      ↓
Reranker
      ↓
Final Top-K

We will learn and implement cross-encoder reranking at an engineering level.

Important concepts to understand:

* why retrieval and reranking are separate stages
* bi-encoder vs cross-encoder
* why a cross-encoder can provide more precise relevance scoring
* how query + candidate chunk are passed to the reranker
* how reranker scores differ from embedding similarity
* how reranking improves the final context selection

Status: NEXT

⸻

Not Yet Covered

* cross-encoder reranking implementation
* advanced reranking strategies
* query rewriting
* multi-query retrieval
* multi-hop retrieval
* RAG answer generation
* context assembly
* citations and grounding
* retrieval evaluation
* answer evaluation
* production RAG architecture
* agentic RAG
* Agentic AI workflows

⸻

Current Retrieval Architecture

The project currently has:

                    User Query
                        │
             ┌──────────┴──────────┐
             ▼                     ▼
      Semantic Search           BM25
        Top 20 candidates      Top 20 candidates
             │                     │
             └──────────┬──────────┘
                        ▼
                       RRF
                        │
                        ▼
                  Final Top 5

The next improvement is:

                    User Query
                        │
             ┌──────────┴──────────┐
             ▼                     ▼
      Semantic Search           BM25
        Top 20 candidates      Top 20 candidates
             │                     │
             └──────────┬──────────┘
                        ▼
                       RRF
                        │
                        ▼
                   Candidates
                        │
                        ▼
                  Cross-Encoder
                    Reranker
                        │
                        ▼
                    Final Top-K

⸻

Learning Depth Rule

For RAG and Agentic AI, maintain an engineering-level depth.

Focus on:

What is it? → Why do we need it? → How does it work in our system? → How do we implement it correctly?

Avoid unnecessary research-level theory.

The user is learning to build RAG systems, not to design or train embedding or retrieval models from scratch.

Only introduce deeper theory when it is necessary to understand or correctly implement the system.

⸻

Core Learning Principle

Understand enough → implement → inspect the result → understand the implementation → move forward.

The goal is to become capable of building practical, modern RAG and Agentic AI systems.