from sentence_transformers import SentenceTransformer
import math

def semantic_search(query, documents , model ,top_k):
    vector_que = model.encode(query)
    
    vector_docs = model.encode(documents)
   
    result = []
    
    for doc, vector  in zip(documents, vector_docs):
        dot_product = 0
        sum_mag_vector = 0
        sum_mag_query = 0
        
        for i in range( 0 , len(vector_que)):
          dot_product += (vector[i] * vector_que[i])
          sum_mag_vector += vector[i]**2 
          sum_mag_query += vector_que[i]**2
        
        mag_vector = math.sqrt(sum_mag_vector)
        mag_query = math.sqrt(sum_mag_query)
          
        if mag_vector == 0 or mag_query == 0:
            similarity = 0.0
        else:  
            similarity = dot_product / (mag_vector * mag_query)
        
        result.append((similarity , doc ))
    
    result.sort(key = lambda x : x[0] , reverse = True)  
    
    return result[:top_k]
        

documents = [
    "FastAPI is a Python framework for building web APIs.",
    "PostgreSQL is a relational database that supports SQL.",
    "Vector databases store embeddings for semantic search.",
    "Python is a programming language used for software development."
]
query = "database"

print(semantic_search(query , documents  , top_k = 2 , model = SentenceTransformer("all-MiniLM-L6-v2")))