RAG Learning Project — Project Context

Purpose

This is a small practical RAG learning project.

The goal is to learn Retrieval-Augmented Generation from fundamentals through advanced, career-relevant RAG techniques by actually implementing each important stage.

This is currently a learning/sandbox project.

The larger Enterprise Document Intelligence System is a separate future project. This learning project should teach and validate the individual RAG components before those concepts are transferred into the larger system.

The practice project should remain focused on understanding and implementing RAG concepts rather than becoming the final enterprise application.

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
Cross-Encoder Reranking
 ↓
Final Ranked Chunks

The next stage is to move from retrieval/reranking toward:

Final Ranked Chunks
 ↓
Context Assembly
 ↓
RAG Generation
 ↓
Citations / Grounding

⸻

Current Technologies

* Python
* PyMuPDF
* Sentence Transformers
* all-MiniLM-L6-v2
* cross-encoder/ms-marco-MiniLM-L-6-v2
* PostgreSQL
* pgAdmin 4
* SQLAlchemy
* pgvector
* rank_bm25
* Virtual environment (.venv)

⸻

Current Project Structure

Important current files include:

Ragg/
│
├── ingestion.py
├── db.py
├── embedding.py
├── semantic_search.py
├── bm25.py
├── rrf.py
├── reranker.py
│
├── sample.pdf
├── documents/
├── .venv/
└── docs/

File Responsibilities

ingestion.py

Responsible for:

* Processing the source PDF
* Extracting text
* Cleaning extracted text
* Detecting useful structure
* Preparing structured chunks

⸻

db.py

Responsible for PostgreSQL operations such as:

* Saving documents
* Saving chunks
* Retrieving chunks
* Saving embeddings
* Performing semantic vector search

⸻

embedding.py

Responsible for embedding-related functionality.

The project uses:

all-MiniLM-L6-v2

for generating text embeddings.

⸻

semantic_search.py

Responsible for:

* Loading the embedding model
* Converting a query into an embedding
* Performing semantic retrieval through db.py
* Returning standardized semantic search results

⸻

bm25.py

Responsible for:

* Preparing the BM25 corpus
* Tokenization
* BM25 scoring
* Returning ranked lexical search results

⸻

rrf.py

Responsible for:

* Running semantic retrieval
* Running BM25 retrieval
* Combining their ranked results
* Applying Reciprocal Rank Fusion
* Producing the hybrid candidate ranking

RRF uses:

RRF(d) = Σ 1 / (k + rank)

with:

k = 60

⸻

reranker.py

Responsible for:

* Loading the Cross-Encoder
* Receiving RRF candidates
* Creating query/chunk pairs
* Generating relevance scores
* Preserving candidate metadata
* Adding rerank_score
* Sorting candidates by relevance

Current model:

cross-encoder/ms-marco-MiniLM-L-6-v2

⸻

Current Dataset

The current practice document has been processed into approximately 60 structured chunks.

Each chunk contains information such as:

* Document ID
* Chunk index
* Page number
* Section title
* Content/text
* Provenance information

The practice document is an IoT-related document containing sections such as:

* Application
* Application Layer Protocols
* Transport Layer
* General
* Other IoT-related sections

⸻

Current Database

Database:

rag_tut

PostgreSQL is accessed through SQLAlchemy.

The document chunks table currently stores:

* Document ID
* Chunk index
* Content
* Page number
* Section title
* Embedding

pgvector is used for vector storage and vector similarity search.

⸻

Current Retrieval Architecture

The current retrieval architecture is:

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
                       Candidate Set
                             │
                             ▼
                     Cross-Encoder
                       Reranker
                             │
                             ▼
                         Final Top-K

Semantic search and BM25 use the same query but retrieve independently.

RRF combines their rankings instead of directly combining their raw scores.

The Cross-Encoder then evaluates the relationship between the query and each candidate chunk.

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

RRF combines these results into a hybrid candidate ranking.

⸻

Cross-Encoder Reranking

The Cross-Encoder operates after RRF.

Its input is:

Query + Candidate Chunk

The model directly evaluates the relationship between the query and candidate chunk.

Conceptually:

Query ───────────┐
                 ├──→ Cross-Encoder → Relevance Score
Chunk ───────────┘

This differs from the embedding model used for semantic search.

Semantic Retrieval

Query
 ↓
Embedding
 ↓
Vector
 ↓
Similarity Search

Cross-Encoder Reranking

Query + Chunk
      ↓
Cross-Encoder
      ↓
Relevance Score

The Cross-Encoder is more computationally expensive, so it is applied to a relatively small candidate set produced by the initial retrieval stages.

⸻

Verified Reranking Example

For the query:

What does the application layer do?

RRF produced:

1. Chunk 48 — Application
2. Chunk 19 — Application Layer Protocols
3. Chunk 18 — General
4. Chunk 15 — General
5. Chunk 24 — Transport Layer

After Cross-Encoder reranking:

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

This verified that reranking can change the ordering produced by RRF.

It also demonstrated that reranking scores are a separate relevance signal and should not be treated as probabilities.

⸻

Learning Approach

The user is learning to become an AI/RAG engineer, not an embedding or RAG researcher.

The teaching approach should therefore be:

Understand enough
        ↓
Implement
        ↓
Inspect
        ↓
Understand the implementation
        ↓
Move forward

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

* Advanced neural-network mathematics
* Transformer internals
* Embedding training objectives
* Research-level retrieval theory
* Lengthy toy experiments
* Unnecessary benchmark experiments

Only introduce deeper theory when it becomes necessary to understand or correctly implement the system.

The primary question should be:

How do I use this correctly in a production RAG system, and why does it work?

Not:

How would I mathematically design and train this model?

This learning depth should remain consistent throughout RAG and Agentic AI.

⸻

Current RAG Learning Stage

The project has completed the retrieval and reranking foundation.

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
     ↓
Cross-Encoder Reranking

The current next stage is:

Context Assembly

The target is:

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
        ↓
Context Assembly
        ↓
LLM

⸻

Important Project Rule

We learn RAG practically.

The small project should remain a sandbox for learning the RAG pipeline.

Do not turn this project into the full Enterprise Document Intelligence System yet.

The larger Enterprise Document Intelligence System is a separate future project.

The goal of this learning project is to understand and implement each important RAG component properly before moving to:

* Advanced retrieval
* RAG generation
* Grounding
* Evaluation
* Production RAG patterns
* Agentic RAG
* Agentic AI

The project should remain simple enough to understand while still using engineering patterns that transfer to production systems.

⸻

Future Direction

After the current retrieval and reranking stage, the learning path is:

Cross-Encoder Reranking
        ↓
Context Assembly
        ↓
RAG Answer Generation
        ↓
Citations / Grounding
        ↓
Retrieval Evaluation
        ↓
Answer Evaluation
        ↓
Query Rewriting
        ↓
Multi-Query Retrieval
        ↓
Multi-Hop Retrieval
        ↓
Production RAG Patterns
        ↓
Agentic RAG
        ↓
Agentic AI

The final goal is not merely to build a basic “PDF chatbot”.

The goal is to understand how modern RAG systems:

* Retrieve information
* Combine retrieval signals
* Rank relevant evidence
* Assemble useful context
* Generate grounded answers
* Preserve provenance
* Evaluate retrieval and answers
* Scale toward more advanced AI workflows

The knowledge gained here will later be applied when building larger AI systems, including the separate Enterprise Document Intelligence System.