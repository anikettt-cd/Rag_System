import math
def retriver(documents , query):
    
    result = []
    
    query_split = query.lower().split()
    
    for word in query_split:
        df = 0
        for text in documents.values():
            if word in text.lower().split():
                df += 1
        
        if df == 0:
            idf = 0.0 
        else:
            idf = math.log(len(documents) / df) 
            
            result.append((word , df , idf))   
    
    return  len(documents) , result  
         

documents = {
    "A": "Python is a programming language",
    "B": "Python is used to build APIs with FastAPI",
    "C": "FastAPI is a Python framework for APIs"
}

query = "Python FastAPI"

print(retriver(documents , query))