RAG Learning Project — Project Context

Purpose

This is a small practical RAG learning project.

The goal is to learn Retrieval-Augmented Generation from fundamentals to advanced, career-relevant RAG techniques by actually implementing each important stage.

This is currently a learning/sandbox project.

The larger Enterprise Document Intelligence System is a separate future project. The learning project should teach and validate the individual RAG components before those concepts are transferred into the larger system.

⸻

Current Pipeline

The project currently implements:

PDF
 ↓
PyMuPDF extraction
 ↓
Text cleaning
 ↓
Section detection
 ↓
Chunking
 ↓
Structured chunk objects
 ↓
PostgreSQL
 ↓
Embeddings
 ↓
pgvector
 ↓
Semantic retrieval
 ↓
BM25 retrieval
 ↓
Hybrid retrieval
 ↓
RRF
 ↓
Reranking        ← CURRENT NEXT STAGE
 ↓
RAG generation
 ↓
Citations / grounded answers

⸻

Current Technologies

* Python
* PyMuPDF
* Sentence Transformers
* all-MiniLM-L6-v2
* PostgreSQL
* pgAdmin 4
* SQLAlchemy
* pgvector
* rank_bm25
* Virtual environment (.venv)

⸻

Current Project Structure

The important current files include:

Ragg/
│
├── ingestion.py
├── db.py
├── semantic_search.py
├── bm25.py
├── rrf.py
│
├── documents/
├── .venv/
└── ...

File responsibilities

ingestion.py

Responsible for processing the source PDF and preparing structured chunks.

db.py

Responsible for PostgreSQL operations such as:

* saving documents
* saving chunks
* retrieving chunks
* saving embeddings
* semantic vector search

semantic_search.py

Responsible for:

* loading the embedding model
* converting a query into an embedding
* performing semantic retrieval through db.py
* returning standardized semantic search results

bm25.py

Responsible for:

* preparing the BM25 corpus
* tokenization
* BM25 scoring
* returning ranked lexical search results

rrf.py

Responsible for:

* receiving one user query
* running semantic retrieval
* running BM25 retrieval
* combining their ranked results using Reciprocal Rank Fusion
* producing the final hybrid ranking

⸻

Current Dataset

The current practice document has been processed into approximately 60 structured chunks.

Each chunk contains information such as:

* document ID
* chunk index
* page number
* section title
* content/text
* provenance information

The practice document is an IoT-related document containing sections such as:

* Application
* Application Layer Protocols
* Transport Layer
* General
* other IoT-related sections

⸻

Current Database

Database:

rag_tut

PostgreSQL is accessed through SQLAlchemy.

The document_chunks table currently stores:

* document ID
* chunk index
* content
* page number
* section title
* embedding

pgvector is used for vector storage and vector similarity search.

⸻

Current Retrieval Architecture

The current hybrid retrieval architecture is:

                         User Query
                             │
                ┌────────────┴────────────┐
                ▼                         ▼
         Semantic Search               BM25
            Top 20                    Top 20
                │                         │
                └────────────┬────────────┘
                             ▼
                            RRF
                             │
                             ▼
                         Final Top 5

Semantic search and BM25 use the same query but retrieve independently.

RRF combines their ranks instead of directly combining their raw scores.

⸻

RRF Implementation

RRF uses:

RRF(d) = Σ 1 / (k + rank)

with:

k = 60

The reason for using RRF is that semantic distance and BM25 scores are not directly comparable.

Instead of:

semantic_score + bm25_score

we combine rank positions.

Current candidate generation:

Semantic → Top 20
BM25     → Top 20

RRF then produces the final ranking.

The current final output selects the top 5 results.

⸻

Current Verified Example

For the query:

What does the application layer do?

the hybrid retrieval system produced:

Rank 1 → Chunk 48 — Application
Rank 2 → Chunk 19 — Application Layer Protocols
Rank 3 → Chunk 18 — General
Rank 4 → Chunk 15 — General
Rank 5 → Chunk 24 — Transport Layer

This verified that semantic retrieval and BM25 can be combined successfully using RRF.

⸻

Learning Approach

The user is learning to become an AI/RAG engineer, not an embedding or RAG researcher.

The teaching approach should therefore be:

Understand enough → implement → inspect → understand the implementation → move forward.

For every RAG concept:

1. Explain the engineering-level concept.
2. Explain why it is needed.
3. Explain how it fits into the current pipeline.
4. Implement it in the project.
5. Explain the important code, libraries, APIs, data flow, and results.
6. Verify it using the real project data.
7. Move to the next stage.

Avoid unnecessary research-level theory.

Do not spend time on:

* advanced neural-network mathematics
* transformer internals
* embedding training objectives
* research-level retrieval theory
* lengthy toy experiments
* unnecessary benchmark experiments

Only introduce deeper theory when it becomes necessary to understand or correctly implement the system.

The primary question should be:

“How do I use this correctly in a production RAG system, and why does it work?”

Not:

“How would I mathematically design and train this model?”

This learning depth should remain consistent throughout RAG and Agentic AI.

⸻

Current RAG Learning Stage

The project has completed the basic and intermediate retrieval foundation.

Completed:

PDF processing
     ↓
Cleaning
     ↓
Structure detection
     ↓
Chunking
     ↓
PostgreSQL
     ↓
Embeddings
     ↓
Vector search
     ↓
Semantic retrieval
     ↓
BM25
     ↓
Hybrid retrieval
     ↓
RRF

The current stage is:

Reranking

The immediate next component is a cross-encoder reranker.

Target:

Semantic Top 20
        +
BM25 Top 20
        ↓
       RRF
        ↓
Candidate Set
        ↓
Cross-Encoder Reranker
        ↓
Final Top-K

⸻

Important Project Rule

We learn RAG practically.

The small project should remain a sandbox for learning the RAG pipeline.

Do not turn this project into the full Enterprise Document Intelligence System yet.

The goal is to understand and implement each important RAG component properly before moving to more advanced retrieval, RAG generation, evaluation, and Agentic AI.

The project should remain simple enough to understand while still using engineering patterns that transfer to production systems.

⸻

Future Direction

After reranking, the learning path is:

Reranking
   ↓
Query Rewriting
   ↓
Multi-Query / Advanced Retrieval
   ↓
Multi-Hop Retrieval
   ↓
Context Assembly
   ↓
RAG Answer Generation
   ↓
Citations / Grounding
   ↓
Evaluation
   ↓
Production RAG Patterns
   ↓
Agentic RAG
   ↓
Agentic AI

The final goal is not merely to build a basic “PDF chatbot”.

The goal is to understand how modern RAG systems retrieve, rank, ground, and generate answers reliably, and then use those principles when building larger AI systems.