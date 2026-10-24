import math

def cosine_similarity(a, b):

    
    dot_product = (a[0] * b[0]) + (a[1] * b[1])
    

    
    mag_b = math.sqrt((b[0]**2 + b[1]**2))
    mag_a = math.sqrt((a[0]**2 + a[1]**2))
    
    if mag_a == 0 or mag_b == 0:
        return 0.0
    
    return dot_product / (mag_b * mag_a)

    

print(cosine_similarity([1, 2], [3, 4]))
print(cosine_similarity([1, 0], [1, 0]))
print(cosine_similarity([1, 0], [0, 1]))
print(cosine_similarity([1, 0], [0.9, 0.1]))