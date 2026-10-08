from sentence_transformers import SentenceTransformer
from db import semantic_search as db_semantic_search


model = SentenceTransformer("all-MiniLM-L6-v2")


def semantic_search(query, limit=5):

    query_embedding = model.encode(query)

    results = db_semantic_search(
        query_embedding,
        limit=limit
    )

    semantic_results = []

    for row in results:

        semantic_results.append({
            "chunk_id": row.chunk_index,
            "content": row.content,
            "section_title": row.section_title,
            "page_number": row.page_number,
            "score": row.distance
        })

    return semantic_results