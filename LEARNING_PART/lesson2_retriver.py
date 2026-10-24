import string
def retrieve(query , documents , top_k):
    query_no_punct = query.translate(str.maketrans(" " , " " , string.punctuation))
    
    query_word = query_no_punct.lower().split()
    
    scored_documents = []
    
    for doc in documents:
        doc_no_punct = doc.translate(str.maketrans(" " , " " , string.punctuation))
        word_doc = doc_no_punct.lower().split()
        
        
        score = 0
        for word in query_word:
            if word in word_doc:
                score += 1
    
        scored_documents.append((score , doc))
    
    scored_documents.sort(key=lambda x: x[0], reverse=True)   
    
    return  scored_documents[:top_k]
    


documents = [
    "Python is a programming language used for web development and data science.",
    "FastAPI is a Python framework for building web APIs.",
    "PostgreSQL is a relational database that supports SQL queries.",
    "MongoDB is a NoSQL database that stores data as documents.",
    "Vector databases store embeddings for semantic search.",
    "Docker is used to package applications into containers.",
    "Git is a version control system used by software developers.",
    "Machine learning allows computers to learn patterns from data.",
    "RAG systems retrieve relevant documents before generating an answer.",
    "Redis is an in-memory data store commonly used for caching."
]
queries = [
   "How can I find information based on meaning?"
]

for query in queries:
    print(f"\nQUERY: {query}")
    results = retrieve(query, documents, top_k=3)

    for score, doc in results:
        print(f"Score: {score} | {doc}")