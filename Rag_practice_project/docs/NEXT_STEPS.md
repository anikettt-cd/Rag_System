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

⸻

Current Stage

→ Reranking

We have now implemented a hybrid retrieval pipeline using semantic search + BM25 + RRF.

Current architecture:

User Query
    ↓
 ┌──┴──┐
 ↓     ↓
Semantic    BM25
Top 20     Top 20
 ↓           ↓
 └─────┬─────┘
       ↓
      RRF
       ↓
Candidates

The next step is to improve the ordering of these candidates using a reranker.

⸻

Immediate Next Tasks

1. Understand Reranking

Learn at an engineering level:

* what reranking means
* why retrieval and reranking are separate stages
* why initial retrieval prioritizes recall
* why reranking prioritizes relevance/precision
* where reranking fits into our RAG pipeline

Target architecture:

Query
  ↓
Candidate Retrieval
  ↓
RRF
  ↓
Candidate Set
  ↓
Reranker
  ↓
Final Top-K

⸻

2. Understand Bi-Encoder vs Cross-Encoder

Understand only the concepts needed for implementation.

Bi-encoder:

Query ──→ Embedding
             │
             ├── similarity ──→ Chunk
             │
Chunk ──→ Embedding

Cross-encoder:

Query + Chunk
      ↓
Cross-Encoder
      ↓
Relevance Score

Understand why cross-encoders are generally more precise for reranking but more computationally expensive.

⸻

3. Choose a Practical Cross-Encoder

Select a practical pretrained cross-encoder suitable for our local learning project.

Understand briefly:

* why we choose it
* what input it expects
* what it returns
* whether it is practical on our hardware
* how it fits into our current Python environment

Avoid researching or training our own reranker.

⸻

4. Implement Reranking

Take the candidates produced by RRF:

RRF candidates
      ↓
Query + candidate text
      ↓
Cross-Encoder
      ↓
Relevance scores
      ↓
Sort by score

Understand:

* how the query is paired with each chunk
* how the model scores relevance
* how candidates are sorted
* why only the final top-K chunks are passed forward

⸻

5. Inspect Reranking Results

Use the same real IoT document and queries we’ve already been using.

Compare:

Semantic ranking
BM25 ranking
RRF ranking
Reranked ranking

Understand which chunks moved and why.

⸻

After Reranking

Continue toward:

1. Query rewriting
2. Multi-query retrieval
3. Multi-hop retrieval
4. Context assembly
5. RAG answer generation
6. Citations and grounding
7. Retrieval evaluation
8. Answer evaluation
9. Production RAG architecture
10. Agentic RAG
11. Agentic AI workflows

⸻

Target Retrieval Architecture

After reranking, our retrieval pipeline should look approximately like:

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
                             │
                             ▼
                      Context Assembly

⸻

Learning Rule

For every stage:

Understand enough → implement → inspect → understand the implementation → move forward.

Focus on:

How do I use this correctly in a production RAG system, and why does it work?

Do not spend unnecessary time on research-level theory.

The goal is to become an AI/RAG engineer, not an embedding, retrieval, or model-training researcher.

⸻

Last Known Milestone

Approximately 60 structured chunks are stored in PostgreSQL.

The project currently has:

* embedding generation
* pgvector storage
* semantic retrieval
* BM25 retrieval
* hybrid retrieval
* RRF fusion
* top-20 candidate retrieval
* final top-5 selection

The immediate next practical task is:

Implement and understand cross-encoder reranking on top of the RRF candidate set.