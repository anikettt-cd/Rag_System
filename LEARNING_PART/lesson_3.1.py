import math
def semantic_search(query, documents , top_k):
   
    result = []
    
    for text , vector in documents.items():
        dot_product = (vector[0] * query[0]) + (vector[1] * query[1])
    
        mag_vector = math.sqrt((vector[0]**2 + vector[1]**2))
        mag_query = math.sqrt((query[0]**2 + query[1]**2))
          
        if mag_vector == 0 or mag_query == 0:
            similarity = 0.0
        else:  
            similarity = dot_product / (mag_vector * mag_query)
        
        result.append((similarity , text))
    
    result.sort(key = lambda x : x[0] , reverse = True)  
    
    return result[:top_k]
        


documents = {
    "FastAPI is a Python framework for building web APIs.": [0.9, 0.1],
    "PostgreSQL is a relational database that supports SQL.": [0.1, 0.9],
    "Vector databases store embeddings for semantic search.": [0.7, 0.3]
}

query = [0.8, 0.2]

print(semantic_search(query , documents  , top_k = 2))