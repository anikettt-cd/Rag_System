import math
def semantic_search(query, documents , top_k):
   
    result = []
    
    for text , vector in documents.items():
        dot_product = 0
        sum_mag_vector = 0
        sum_mag_query = 0
        
        for i in range( 0 , len(query)):
          dot_product += (vector[i] * query[i])
          sum_mag_vector += vector[i]**2 
          sum_mag_query += query[i]**2
        
        mag_vector = math.sqrt(sum_mag_vector)
        mag_query = math.sqrt(sum_mag_query)
          
        if mag_vector == 0 or mag_query == 0:
            similarity = 0.0
        else:  
            similarity = dot_product / (mag_vector * mag_query)
        
        result.append((similarity , text))
    
    result.sort(key = lambda x : x[0] , reverse = True)  
    
    return result[:top_k]
        


query = [0.8, 0.2, 0.4]

documents = {
    "Document A": [0.9, 0.1, 0.3],
    "Document B": [0.1, 0.9, 0.2],
    "Document C": [0.7, 0.3, 0.5]
}

print(semantic_search(query , documents  , top_k = 2))