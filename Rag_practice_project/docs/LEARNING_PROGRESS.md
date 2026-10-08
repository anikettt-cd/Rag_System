RAG Learning Progress

Completed

1. PDF Extraction

Learned and implemented:

* PDF text extraction using PyMuPDF
* Page-level extraction
* Retaining page information
* Converting PDF content into usable text

Status: DONE

⸻

2. Text Cleaning

Learned why raw PDF extraction needs cleaning.

Handled concepts such as:

* Excessive whitespace
* Repeated blank lines
* Unusual Unicode characters
* Zero-width characters
* Preserving useful paragraph structure

Status: DONE

⸻

3. Section Detection

Learned how document structure can be detected and retained.

Chunks can contain section information so retrieval can later understand document context.

Status: DONE

⸻

4. Chunking

Learned:

* Why documents need to be divided into chunks
* Chunk boundaries
* Structured chunks
* Chunk metadata
* Page and section provenance

Approximately 60 chunks have been created.

Status: DONE

⸻

5. Structured Chunk Objects

The extracted document content was converted into structured chunk objects containing metadata and text.

Chunks currently contain information such as:

* Document ID
* Chunk index
* Page number
* Section title
* Content/text
* Provenance information

Status: DONE

⸻

6. PostgreSQL + pgvector

Set up PostgreSQL and pgAdmin 4 for storing document and chunk information.

Current database:

rag_tut

Implemented:

* Document storage
* Chunk storage
* Chunk retrieval
* Embedding storage using pgvector
* Vector similarity search

SQLAlchemy is used to communicate with PostgreSQL.

Status: DONE

⸻

7. Embeddings

Learned the engineering-level embedding concepts.

We understand that an embedding model converts text into a numerical vector so that semantic relationships between chunks and queries can be compared.

Implemented:

* Selected all-MiniLM-L6-v2
* Loaded the model using Sentence Transformers
* Generated embeddings for document chunks
* Stored embeddings in PostgreSQL using pgvector
* Generated embeddings for user queries
* Used the same embedding model for documents and queries

Important implementation concepts understood:

* Why the embedding model is needed
* What model.encode() does
* Embedding vectors and their dimensions
* Why document and query embeddings must use the same model
* How embeddings are stored in pgvector
* How the query vector is passed to PostgreSQL
* How vector distance is used for retrieval

Status: DONE

⸻

8. Semantic Retrieval

Implemented semantic/vector search using:

* Sentence Transformers
* all-MiniLM-L6-v2
* PostgreSQL
* pgvector
* SQLAlchemy

Pipeline:

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
* Other semantically related chunks

Status: DONE

⸻

9. BM25 / Lexical Retrieval

Implemented lexical retrieval using:

* rank_bm25
* Tokenized document content
* BM25 scoring

Pipeline:

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

Learned why lexical retrieval remains useful even when semantic embeddings are available:

* Exact terminology
* Keywords
* Names
* Technical terms
* Cases where semantic similarity may miss an exact match

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

Learned why raw scores should not simply be added:

Semantic distance → one scale
BM25 score        → another scale

Therefore:

Do not directly combine raw scores.

Instead, RRF combines rank positions.

Formula:

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
                  Ranked Candidates

Successfully verified RRF on the practice IoT document.

Example RRF ranking:

1. Chunk 48 — Application
2. Chunk 19 — Application Layer Protocols
3. Chunk 18 — General
4. Chunk 15 — General
5. Chunk 24 — Transport Layer

We also verified that chunks appearing highly in both retrieval systems receive stronger RRF scores.

Status: DONE

⸻

12. Cross-Encoder Reranking

Learned and implemented cross-encoder reranking on top of the RRF candidate set.

The practical model used was:

cross-encoder/ms-marco-MiniLM-L-6-v2

using the Sentence Transformers CrossEncoder API.

Learned:

* Why retrieval and reranking are separate stages
* Bi-encoder vs cross-encoder
* Why cross-encoders can provide more precise query-to-chunk relevance scoring
* Why cross-encoders are more computationally expensive
* How a query and candidate chunk are paired
* How model.predict() produces relevance scores
* Why reranker scores are not probabilities
* How candidates are sorted using reranker scores
* Why reranking should operate on a smaller candidate set rather than the entire document collection

Cross-encoder input:

(query, candidate_chunk)

Example:

Query + Chunk
     ↓
Cross-Encoder
     ↓
Relevance Score

Implemented reranker.py to:

1. Receive the user query and RRF candidates
2. Create query/chunk pairs
3. Generate cross-encoder scores
4. Preserve existing chunk metadata
5. Add rerank_score
6. Sort candidates by reranker score

Verified using the real practice IoT document.

For the query:

What does the application layer do?

RRF initially ranked:

1. Chunk 48 — Application
2. Chunk 19 — Application Layer Protocols
3. Chunk 18 — General
4. Chunk 15 — General
5. Chunk 24 — Transport Layer

After reranking:

1. Chunk 19 — Application Layer Protocols
2. Chunk 48 — Application
3. Chunk 20 — HTTP
4. Chunk 45 — Services
5. Chunk 27 — Network Layer

Example reranker scores:

Chunk 19 → 8.4276
Chunk 48 → 8.2948
Chunk 20 → 3.5832
Chunk 45 → 3.3779
Chunk 27 → 1.9551

This demonstrated that the cross-encoder can change the ordering produced by RRF based on its direct query-to-chunk relevance judgment.

Status: DONE

⸻

Currently Learning

There is currently no unfinished component in the basic retrieval + reranking pipeline.

The next stage is to move beyond retrieval and learn how retrieved chunks are prepared and used for RAG generation.

⸻

Not Yet Covered

* Query rewriting
* Multi-query retrieval
* Multi-hop retrieval
* Context assembly
* RAG answer generation
* Prompt construction for RAG
* Citations and grounding
* Retrieval evaluation
* Answer evaluation
* Advanced reranking strategies
* Production RAG architecture
* Agentic RAG
* Agentic AI workflows

⸻

Current Retrieval Architecture

The practice project now has:

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
                  Candidate Set
                        │
                        ▼
                 Cross-Encoder
                   Reranker
                        │
                        ▼
                  Final Ranking
                        │
                        ▼
                     Top-K

The important distinction is:

Semantic Search / BM25
        ↓
Candidate Retrieval
        ↓
RRF
        ↓
Candidate Fusion
        ↓
Cross-Encoder
        ↓
Precise Reranking

⸻

Learning Depth Rule

For RAG and Agentic AI, maintain an engineering-level depth.

Focus on:

What is it?
      ↓
Why do we need it?
      ↓
How does it work in our system?
      ↓
How do we implement it correctly?
      ↓
How do we verify the result?

Avoid unnecessary research-level theory.

The goal is to become capable of building practical RAG and Agentic AI systems, not to design or train embedding, retrieval, or reranking models from scratch.

Only introduce deeper theory when it is necessary to understand or correctly implement the system.

⸻

Core Learning Principle

Understand enough
      ↓
Implement
      ↓
Inspect the result
      ↓
Understand the implementation
      ↓
Move forward

The goal is to develop practical engineering knowledge that can later be transferred to larger RAG and AI systems.