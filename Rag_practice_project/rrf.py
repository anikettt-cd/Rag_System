from semantic_search import semantic_search
from bm25 import bm25_search


def rrf_fusion(result_lists, k=60):

    scores = {}
    results = {}

    for results_list in result_lists:

        for rank, result in enumerate(results_list, start=1):

            chunk_id = result["chunk_id"]

            scores[chunk_id] = (
                scores.get(chunk_id, 0)
                + 1 / (k + rank)
            )

            if chunk_id not in results:
                results[chunk_id] = result

    fused_results = []

    for chunk_id, score in scores.items():

        result = results[chunk_id].copy()

        result["rrf_score"] = score

        fused_results.append(result)

    fused_results.sort(
        key=lambda x: x["rrf_score"],
        reverse=True
    )

    return fused_results


# -------------------------
# Single query point
# -------------------------

query = "What does the application layer do?"


semantic_results = semantic_search(
    query,
    limit=20
)

bm25_results = bm25_search(
    query,
    limit=20
)


# -------------------------
# Show Semantic Ranking
# -------------------------

print("\n========== SEMANTIC RESULTS ==========")

for rank, result in enumerate(semantic_results, start=1):

    print(
        f"{rank}. "
        f"Chunk {result['chunk_id']} | "
        f"Distance: {result['score']}"
    )


# -------------------------
# Show BM25 Ranking
# -------------------------

print("\n========== BM25 RESULTS ==========")

for rank, result in enumerate(bm25_results, start=1):

    print(
        f"{rank}. "
        f"Chunk {result['chunk_id']} | "
        f"Score: {result['score']}"
    )


# -------------------------
# RRF
# -------------------------

final_results = rrf_fusion(
    [semantic_results, bm25_results]
)


# -------------------------
# Show Final RRF Ranking
# -------------------------

print("\n========== RRF RESULTS ==========")

for rank, result in enumerate(final_results[:5], start=1):

    print("\n------------------------")
    print("Rank:", rank)
    print("Chunk:", result["chunk_id"])
    print("Section:", result["section_title"])
    print("Page:", result["page_number"])
    print("RRF Score:", result["rrf_score"])
    print("Content:", result["content"])
    print("content" , result["content"])
    