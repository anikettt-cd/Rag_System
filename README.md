# 🧠 RAG Learning & Practice

> A hands-on, engineering-first repository for learning and implementing the core components of **Retrieval-Augmented Generation (RAG)** systems using Python.

This repository focuses on the "how" and "why" of RAG. It's built to demystify the black box of modern retrieval by implementing individual components from scratch, running them against real document data, and analyzing the data flow.

*Note: This is an active learning and experimentation sandbox, not a production-ready framework.*

---

## 🎯 Purpose & Philosophy

The goal is to build a strong, practical understanding of RAG architectures. Instead of relying entirely on high-level abstractions, this repo takes an implementation-first approach:

**LEARN** ➔ **UNDERSTAND WHY** ➔ **IMPLEMENT** ➔ **RUN** ➔ **VERIFY** ➔ **UNDERSTAND THE CODE** ➔ **NEXT CONCEPT**

The focus is on being an engineer who can architect, trace, and debug RAG systems, rather than getting lost in deep research-level model architecture.

---

## 🏗️ The Retrieval Pipeline

The core practice implementation lives inside `Rag_practice_project/`. It demonstrates a modern, multi-stage retrieval pipeline combining semantic search with lexical search, followed by reranking.

```text
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
        ┌─────────────────────────┐
        │                         │
        ▼                         ▼
 Semantic Search             BM25 Search
 (Vector Similarity)       (Lexical Keyword)
        │                         │
        └────────────┬────────────┘
                     ▼
            RRF (Reciprocal Rank Fusion)
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

```

---

## 🔎 Pipeline Deep Dive

### 1. Document Extraction & Cleaning

Extracting text from PDFs using **PyMuPDF**. Preserves crucial metadata like page numbers and document identity. Text is then sanitized (removing zero-width characters, fixing whitespace, standardizing bullets) to ensure clean inputs.

### 2. Chunking Strategy

Documents are divided into manageable chunks, each retaining dense metadata:
`chunk_id` | `document_id` | `page_number` | `section_title` | `content`
*Traceability is key: retrieval results must always map back to the source.*

### 3. Embeddings & Storage

Using **Sentence Transformers** (`all-MiniLM-L6-v2`) to generate vector representations of text. These embeddings, alongside their metadata, are stored in **PostgreSQL** using the **pgvector** extension for efficient vector similarity searches.

### 4. Hybrid Retrieval (Semantic + BM25)

* **Semantic Search:** Finds meaning and context using query embeddings against stored vectors.
* **BM25:** Handles exact keyword matches, technical identifiers, and terminology.
* **Reciprocal Rank Fusion (RRF):** Intelligently merges the ranked outputs of both search methods without needing raw score normalization.

### 5. Reranking

Passes the RRF candidate set through a **Cross-Encoder**. By evaluating the `(query, chunk)` pair simultaneously, the Cross-Encoder assigns a highly accurate relevance score, reordering the candidates into the final, high-precision retrieval list.

---

## 🧠 Core Concepts Covered

| Category | Topics Explored |
| --- | --- |
| **Document Processing** | PDF extraction, text cleaning, metadata preservation, section detection, intelligent chunking. |
| **Embeddings** | Sentence Transformers, vector dimensionality, query vs. document embeddings. |
| **Vector DB** | PostgreSQL, pgvector integration, storing embeddings alongside relational metadata. |
| **Information Retrieval** | Vector similarity search, BM25 lexical search, semantic vs. keyword tradeoffs. |
| **Advanced Retrieval** | Hybrid Search, Reciprocal Rank Fusion (RRF) candidate generation. |
| **Reranking** | Cross-Encoder models, precise query-document relevance scoring. |

---

## 🛠️ Tech Stack

| Technology | Purpose |
| --- | --- |
| **Python** | Core application logic |
| **PyMuPDF** | High-fidelity PDF parsing and extraction |
| **Sentence Transformers** | Embedding generation and Cross-Encoder reranking |
| **PostgreSQL + pgvector** | Document, metadata, and vector storage |
| **rank-bm25** | Lexical keyword retrieval |

---

## 📂 Repository Structure

```bash
Rag/
├── Rag_practice_project/         # 🟢 Main structured learning project
│   ├── bm25.py                   # Lexical search implementation
│   ├── db.py                     # PostgreSQL / pgvector connection
│   ├── embedding.py              # Sentence Transformer logic
│   ├── ingestion.py              # Document processing & chunking
│   ├── reranker.py               # Cross-Encoder logic
│   ├── rrf.py                    # Reciprocal Rank Fusion
│   ├── semantic_search.py        # Vector similarity search
│   ├── sample.pdf                # Test data
│   └── docs/                     
│       ├── LEARNING_PROGRESS.md  # Tracked milestones
│       ├── NEXT_STEPS.md         # Upcoming topics
│       └── PROJECT_CONTEXT.md    # Architecture notes
│
├── bm25_practice.py              # Sandbox files
├── cross_encoder_test.py
├── lesson2_retriver.py
└── ...                           # Early experiment scripts

```

---

## 🚀 Future Roadmap

This repository acts as the fundamental building block. Once these core concepts are mastered and battle-tested here, they will be migrated to a dedicated, production-ready system: **The Enterprise Document Intelligence System**.

For now, this repo remains a playground for breaking things, inspecting vectors, and truly understanding modern RAG pipelines from the ground up.
