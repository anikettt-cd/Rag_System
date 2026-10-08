RAG Learning & Practice

A hands-on repository for learning and implementing the core engineering concepts behind Retrieval-Augmented Generation (RAG) systems using Python.

This repository is focused on understanding how RAG systems are actually built, how the individual components work together, and why different retrieval techniques are used.

It is intentionally a learning and experimentation repository, not a production-ready RAG application.

⸻

🎯 Purpose

The main goal of this repository is to build a strong practical understanding of RAG systems through implementation.

Instead of learning RAG only through theory, the concepts are explored by:

* Implementing each component
* Running it against real document data
* Inspecting the results
* Comparing different retrieval approaches
* Understanding the data flow between components
* Gradually combining individual components into a retrieval pipeline

The focus is on being an engineer who can build and understand RAG systems, rather than going deeply into research-level mathematics or model architecture.

⸻

🧠 What I’m Learning

The repository currently covers the following concepts:

Document Processing

* PDF text extraction
* Page-level extraction
* Text cleaning
* Unicode and whitespace normalization
* Preserving document structure
* Section detection
* Document chunking
* Chunk metadata and provenance

Embeddings

* Text embeddings
* Sentence Transformers
* Embedding dimensions
* Vector representations
* Query embeddings
* Similarity-based retrieval

Vector Database

* PostgreSQL
* pgvector
* Vector storage
* Vector similarity search
* Storing document metadata alongside embeddings

Information Retrieval

* Semantic search
* Keyword search
* BM25
* Comparing semantic and lexical retrieval

Hybrid Retrieval

* Combining semantic search and BM25
* Reciprocal Rank Fusion (RRF)
* Candidate generation

Reranking

* Cross-Encoder models
* Query-document relevance scoring
* Candidate reranking
* Final ranked retrieval results

⸻

🏗️ Practice Project

The main structured learning implementation is located inside:

Rag_practice_project/

The current pipeline is:

                 Sample PDF
                     │
                     ▼
              PDF Extraction
                     │
                     ▼
                Text Cleaning
                     │
                     ▼
                  Chunking
                     │
                     ▼
               PostgreSQL
                     │
                     ▼
                 Embeddings
                     │
                     ▼
             Semantic Search
                     │
                     ├──────────────┐
                     │              │
                     ▼              ▼
                 BM25 Search   Vector Search
                     │              │
                     └──────┬───────┘
                            ▼
                       RRF Fusion
                            │
                            ▼
                   Candidate Chunks
                            │
                            ▼
                  Cross-Encoder
                     Reranking
                            │
                            ▼
                 Final Ranked Chunks

This allows each retrieval technique to be understood independently before combining them.

⸻

📂 Repository Structure

Rag/
│
├── Rag_practice_project/
│   │
│   ├── bm25.py
│   ├── db.py
│   ├── embedding.py
│   ├── ingestion.py
│   ├── reranker.py
│   ├── rrf.py
│   ├── semantic_search.py
│   ├── sample.pdf
│   │
│   └── docs/
│       ├── LEARNING_PROGRESS.md
│       ├── NEXT_STEPS.md
│       └── PROJECT_CONTEXT.md
│
├── bm25_practice.py
├── cross_encoder_test.py
├── input.txt
├── lesson2_retriver.py
├── lesson3.py
├── lesson_3.1.py
├── lesson_3.2_any_size_of_vector.py
├── mini_project.py
├── solution.py
└── ...

⸻

🔎 Retrieval Pipeline

1. Document Extraction

The first stage extracts text from PDF documents using PyMuPDF.

The extraction process preserves useful metadata such as:

* Page number
* Document identity
* Text content

This provides the raw material for the rest of the RAG pipeline.

⸻

2. Text Cleaning

Extracted PDF text often contains unwanted artifacts.

The cleaning stage handles issues such as:

* Zero-width Unicode characters
* Non-breaking spaces
* Bullet artifacts
* Excessive whitespace
* Formatting inconsistencies

The goal is to produce cleaner text while preserving useful document structure.

⸻

3. Chunking

Large documents cannot simply be passed directly into retrieval or an LLM.

The document is therefore divided into smaller chunks.

Each chunk maintains metadata such as:

chunk_id
document_id
chunk_index
page_number
section_title
content

Keeping this metadata is important because retrieval results should eventually be traceable back to the original document.

⸻

🧮 Embeddings

The repository uses Sentence Transformers for generating embeddings.

Example model:

all-MiniLM-L6-v2

Text is converted into a numerical vector representation:

Text
 ↓
Embedding Model
 ↓
Vector

These vectors allow semantically similar pieces of text to be retrieved even when they don’t contain exactly the same words.

⸻

🗄️ PostgreSQL + pgvector

The practice project uses PostgreSQL with the pgvector extension.

Document chunks and their embeddings are stored together.

Conceptually:

Document Chunk
│
├── content
├── page_number
├── section_title
└── embedding

This allows PostgreSQL to perform vector similarity searches directly against stored embeddings.

⸻

🔍 Semantic Search

Semantic search converts the user’s query into an embedding and searches for chunks with similar vector representations.

User Query
    ↓
Query Embedding
    ↓
Vector Similarity Search
    ↓
Relevant Chunks

The practice implementation uses the stored pgvector embeddings to retrieve candidate chunks.

⸻

🔤 BM25 Search

Semantic search is not always enough.

Exact keywords, technical terms, names, identifiers, and terminology can sometimes be better handled by traditional lexical retrieval.

The repository therefore also implements BM25.

Query
 ↓
Tokenization
 ↓
BM25
 ↓
Keyword-based ranking

This gives us a second retrieval signal.

⸻

🔀 Hybrid Retrieval with RRF

Instead of choosing between semantic search and BM25, both can be combined.

The repository implements Reciprocal Rank Fusion (RRF).

Semantic Search
       │
       ├───────┐
       │       │
       ▼       ▼
    Ranking  Ranking
       │       │
       └───┬───┘
           ▼
          RRF
           │
           ▼
 Combined Candidate Ranking

RRF combines rankings without requiring the raw scores from the different retrieval systems to be directly comparable.

This produces a stronger candidate set for the next retrieval stage.

⸻

🤖 Cross-Encoder Reranking

After RRF, the retrieved candidates are passed through a Cross-Encoder.

The Cross-Encoder evaluates:

(query, chunk)

together and produces a relevance score.

For example:

Query + Chunk A → 8.7
Query + Chunk B → 5.2
Query + Chunk C → -1.4

The candidates are then sorted according to their reranking scores.

The overall retrieval process becomes:

Semantic Search ──┐
                  │
                  ▼
                 RRF
                  │
                  ▼
             Candidates
                  │
                  ▼
           Cross-Encoder
                  │
                  ▼
          Final Ranking

This demonstrates the difference between candidate retrieval and precise relevance ranking.

⸻

🛠️ Technologies Used

Technology	Purpose
Python	Main programming language
PyMuPDF	PDF text extraction
Sentence Transformers	Embeddings and Cross-Encoder
PostgreSQL	Document and metadata storage
pgvector	Vector storage and similarity search
rank-bm25	BM25 keyword retrieval
Git	Version control

⸻

📚 Learning Progress

The structured learning progress is maintained inside:

Rag_practice_project/docs/LEARNING_PROGRESS.md

Additional project notes and upcoming topics are maintained in:

Rag_practice_project/docs/PROJECT_CONTEXT.md
Rag_practice_project/docs/NEXT_STEPS.md

These files document the learning process and help keep track of what has already been implemented.

⸻

🧪 Learning Philosophy

The repository follows an implementation-first approach:

LEARN
  ↓
UNDERSTAND WHY
  ↓
IMPLEMENT
  ↓
RUN
  ↓
VERIFY RESULTS
  ↓
UNDERSTAND THE CODE
  ↓
MOVE TO NEXT CONCEPT

The objective is not to simply copy implementations, but to understand:

* What each component does
* Why it is required
* What problem it solves
* What libraries are being used
* How the APIs work
* What data flows between components
* How the individual components combine into a RAG system

⸻

🚧 Project Status

This repository is actively being developed as part of a structured RAG learning journey.

Completed

* PDF extraction
* Text cleaning
* Chunking
* PostgreSQL storage
* pgvector setup
* Embedding generation
* Semantic search
* BM25 retrieval
* RRF hybrid retrieval
* Cross-Encoder testing
* Cross-Encoder reranking

Current Focus

Improving and understanding the retrieval and reranking pipeline:

Semantic Search
      +
BM25
      ↓
     RRF
      ↓
Cross-Encoder
      ↓
Final Ranked Chunks

Additional RAG concepts will be added as the learning journey progresses.

⸻

🎯 Future Application

This repository is intentionally separate from the larger project that will be built later.

The knowledge gained here will eventually be applied to a dedicated:

Enterprise Document Intelligence System

That future project will use the concepts learned here as building blocks for a more complete production-oriented system.

This repository remains focused on learning, experimentation, implementation, and understanding RAG fundamentals and modern retrieval techniques.

⸻

📌 Note

This is a learning/practice repository, not a production-ready RAG framework.

The code may contain experiments, temporary scripts, and simplified implementations created while learning individual concepts.
