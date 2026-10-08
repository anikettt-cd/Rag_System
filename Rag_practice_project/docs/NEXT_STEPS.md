RAG Project — Next Steps

Current Position

Completed:

* PDF extraction
* Text cleaning
* Section detection
* Chunking
* Structured chunk objects
* PostgreSQL setup
* Chunk storage and retrieval
* Embedding model selection
* Embedding generation
* pgvector embedding storage
* Query embeddings
* Vector similarity search
* Semantic retrieval
* BM25 / lexical retrieval
* Hybrid retrieval
* Reciprocal Rank Fusion (RRF)
* Cross-Encoder reranking

⸻

Current Stage

→ Post-Retrieval / RAG Generation

The retrieval pipeline is now working through:

User Query
    ↓
Semantic Search
    ↓
BM25
    ↓
RRF
    ↓
Candidate Set
    ↓
Cross-Encoder Reranker
    ↓
Final Top-K

We have successfully implemented and verified the retrieval + reranking stage.

The next step is to understand what happens after the final relevant chunks have been retrieved.

⸻

Immediate Next Tasks

1. Context Assembly

Learn how the final reranked chunks are prepared as context for an LLM.

Understand:

* What context assembly means
* How final chunks are selected
* How chunk ordering affects the context
* How metadata can be preserved
* How to avoid unnecessary context
* Why sending every retrieved chunk to the LLM is undesirable
* How the final context should be structured

Target:

Reranked Chunks
      ↓
Top-K Selection
      ↓
Context Assembly
      ↓
LLM Context

⸻

2. RAG Answer Generation

Learn how the retrieved context is provided to an LLM to generate a grounded answer.

Understand:

* How retrieved chunks are inserted into a prompt
* How the LLM is instructed to answer from the provided context
* How context and user query are separated
* Why the LLM should not rely on unsupported information
* How retrieved evidence influences generation

Target:

User Query
     +
Retrieved Context
     ↓
    LLM
     ↓
Grounded Answer

⸻

3. Citations and Grounding

Learn how retrieved chunk metadata can be used to produce traceable answers.

Our chunks already contain information such as:

chunk_id
page_number
section_title
content

Use this metadata to support citations such as:

Document
Page
Section

Understand:

* Why citations matter
* How provenance is preserved through retrieval
* How the answer can reference supporting chunks
* Difference between retrieval evidence and generated text

⸻

4. Query Rewriting

After basic RAG generation is working, learn how the original user query can be transformed into a better retrieval query.

Understand:

* Why query rewriting is useful
* When the original query may be poorly suited for retrieval
* How an LLM can improve retrieval queries
* When query rewriting should and should not be used

Target:

User Query
    ↓
Query Rewriting
    ↓
Improved Retrieval Query
    ↓
Retrieval Pipeline

⸻

5. Multi-Query Retrieval

Learn how one user question can be transformed into multiple retrieval queries.

Understand:

* Why multiple query formulations can improve recall
* How multiple retrieval results are combined
* How this differs from simple query rewriting
* When multi-query retrieval is useful

Target:

User Query
     ↓
Query 1 ──→ Retrieval
Query 2 ──→ Retrieval
Query 3 ──→ Retrieval
     ↓
Combine Results
     ↓
Reranking

⸻

6. Multi-Hop Retrieval

Learn how some questions require retrieving information in multiple steps.

Understand:

* What multi-hop retrieval means
* Why one retrieval operation may not be sufficient
* How information from one retrieved result can lead to another retrieval step
* Where multi-hop retrieval fits into advanced RAG systems

⸻

7. Retrieval Evaluation

Learn how to evaluate whether our retrieval system is actually retrieving useful chunks.

Understand practical retrieval metrics such as:

* Recall
* Precision
* Hit Rate
* MRR
* Recall@K

Focus on how these metrics help diagnose retrieval quality rather than going deeply into evaluation theory.

⸻

8. Answer Evaluation

After answer generation is implemented, learn how to evaluate:

* Groundedness
* Relevance
* Faithfulness
* Answer correctness
* Citation quality

Understand the difference between:

Good Retrieval

and:

Good Final Answer

A RAG system can retrieve the correct chunk but still generate a poor answer.

⸻

After Basic RAG

Continue toward:

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
Production RAG Patterns
      ↓
Advanced RAG
      ↓
Agentic RAG
      ↓
Agentic AI Workflows

⸻

Target RAG Architecture

After the next stages are implemented, the learning project should conceptually look like:

                         User Query
                             │
                             ▼
                     Query Processing
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
                             │
                             ▼
                    Context Assembly
                             │
                             ▼
                            LLM
                             │
                             ▼
                   Grounded Answer
                             │
                             ▼
                         Citations

⸻

Learning Rule

For every stage:

Understand enough
        ↓
Implement
        ↓
Inspect
        ↓
Understand the implementation
        ↓
Move forward

Focus on:

How do I use this correctly in a production RAG system, and why does it work?

Do not spend unnecessary time on research-level theory.

The goal is to become an AI/RAG engineer, not an embedding, retrieval, reranking, or model-training researcher.

⸻

Last Known Milestone

Approximately 60 structured chunks are stored in PostgreSQL.

The project currently has:

* PDF extraction
* Text cleaning
* Section detection
* Chunking
* Structured chunk objects
* PostgreSQL storage
* Embedding generation
* pgvector storage
* Semantic retrieval
* BM25 retrieval
* Hybrid retrieval
* RRF fusion
* Top-20 candidate retrieval
* Cross-Encoder reranking
* Final ranked chunks

The verified retrieval pipeline is:

Semantic Top 20
       +
BM25 Top 20
       ↓
      RRF
       ↓
Candidate Set
       ↓
Cross-Encoder
       ↓
Final Top-K

The next practical learning task is:

Learn how to assemble the final reranked chunks into LLM context and implement basic RAG answer generation.