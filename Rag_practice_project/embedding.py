from sentence_transformers import SentenceTransformer

from db import get_chunks, save_embeddings


model = SentenceTransformer("all-MiniLM-L6-v2")


chunks = get_chunks()

texts = [chunk["content"] for chunk in chunks]

embeddings = model.encode(texts)

print("Number of chunks:", len(chunks))
print("Embedding shape:", embeddings.shape)

save_embeddings(chunks, embeddings)