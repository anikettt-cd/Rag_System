from sentence_transformers import CrossEncoder


MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"


model = CrossEncoder(MODEL_NAME)


def rerank(query, candidates):

    pairs = [
        (query, candidate["content"])
        for candidate in candidates
    ]

    scores = model.predict(pairs)

    reranked_results = []

    for candidate, score in zip(candidates, scores):

        result = candidate.copy()

        result["rerank_score"] = float(score)

        reranked_results.append(result)

    reranked_results.sort(
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    return reranked_results

from rrf import rrf_fusion
from semantic_search import semantic_search
from bm25 import bm25_search


query = "What does the application layer do?"


semantic_results = semantic_search(
    query,
    limit=20
)

bm25_results = bm25_search(
    query,
    limit=20
)


rrf_results = rrf_fusion(
    [semantic_results, bm25_results]
)


final_results = rerank(
    query,
    rrf_results
)


print("\n========== FINAL RERANKED RESULTS ==========")

for rank, result in enumerate(final_results[:5], start=1):

    print("\n------------------------")
    print("Rank:", rank)
    print("Chunk:", result["chunk_id"])
    print("Section:", result["section_title"])
    print("Page:", result["page_number"])
    print("RRF Score:", result["rrf_score"])
    print("Rerank Score:", result["rerank_score"])
    print("Content:", result["content"])