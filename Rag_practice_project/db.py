from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql+psycopg://aniketsaini@localhost:5432/rag_tut"

engine = create_engine(DATABASE_URL)


def save_document(document_id, filename, file_path, mime_type, file_size):

    query = text("""
        INSERT INTO documents
        (id, filename, file_path, mime_type, file_size)
        VALUES
        (:id, :filename, :file_path, :mime_type, :file_size)
    """)

    with engine.begin() as connection:
        connection.execute(
            query,
            {
                "id": document_id,
                "filename": filename,
                "file_path": file_path,
                "mime_type": mime_type,
                "file_size": file_size
            }
        )

    print(f"Saved document: {filename}")


def save_chunks(chunks):

    query = text("""
        INSERT INTO document_chunks
        (document_id, chunk_index, content, page_number, section_title)
        VALUES
        (:document_id, :chunk_index, :content, :page_number, :section_title)
    """)

    with engine.begin() as connection:

        for chunk in chunks:
            connection.execute(
                query,
                {
                    "document_id": chunk["document_id"],
                    "chunk_index": chunk["chunk_index"],
                    "content": chunk["text"],
                    "page_number": chunk["page_number"],
                    "section_title": chunk["section"]
                }
            )

    print(f"Saved {len(chunks)} chunks to PostgreSQL.")

def get_chunks():

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT
                    chunk_index,
                    content,
                    page_number,
                    section_title
                FROM document_chunks
                ORDER BY chunk_index
            """)
        )

        chunks = []

        for row in result:
            chunks.append({
                "chunk_index": row.chunk_index,
                "content": row.content,
                "page_number": row.page_number,
                "section_title": row.section_title
            })

        return chunks
    
def save_embeddings(chunks, embeddings):

    query = text("""
        UPDATE document_chunks
        SET embedding = :embedding
        WHERE chunk_index = :chunk_index
    """)

    with engine.begin() as connection:

        for chunk, embedding in zip(chunks, embeddings):

            connection.execute(
                query,
                {
                    "embedding": embedding.tolist(),
                    "chunk_index": chunk["chunk_index"]
                }
            )

    print(f"Saved {len(embeddings)} embeddings to PostgreSQL.")

def semantic_search(query_embedding, limit=5):

    sql = text("""
        SELECT
            chunk_index,
            content,
            page_number,
            section_title,
            embedding <=> CAST(:query_embedding AS vector) AS distance
        FROM document_chunks
        WHERE embedding IS NOT NULL
        ORDER BY embedding <=> CAST(:query_embedding AS vector)
        LIMIT :limit
    """)

    with engine.connect() as connection:

        result = connection.execute(
            sql,
            {
                "query_embedding": str(query_embedding.tolist()),
                "limit": limit
            }
        )

        return result.fetchall()       