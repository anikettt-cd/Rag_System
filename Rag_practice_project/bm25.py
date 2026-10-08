from rank_bm25 import BM25Okapi

from db import get_chunks


chunks = get_chunks()

documents = [chunk["content"] for chunk in chunks]

tokenized_documents = [
    document.lower().split()
    for document in documents
]

bm25 = BM25Okapi(tokenized_documents)


def bm25_search(query, limit=5):

    tokenized_query = query.lower().split()

    scores = bm25.get_scores(tokenized_query)

    ranked_indices = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True
    )

    bm25_results = []

    for i in ranked_indices[:limit]:

        bm25_results.append({
            "chunk_id": chunks[i]["chunk_index"],
            "content": chunks[i]["content"],
            "section_title": chunks[i]["section_title"],
            "page_number": chunks[i]["page_number"],
            "score": scores[i]
        })

    return bm25_results