import re, math
from collections import Counter

WORD = re.compile(r'\w+')

def get_cosine(vec1, vec2):
     print vec1
     print vec2
     intersection = set(vec1.keys()) & set(vec2.keys())
     numerator = sum([vec1[x] * vec2[x] for x in intersection])
     print 'set1 : ',set(vec1.keys()) 
     print 'set2 : ',set(vec2.keys()) 
     print '\n\n',[vec1[x] * vec2[x] for x in intersection],'\n\n'
     print 'set1 & set2 :' ,set(vec1.keys()) & set(vec2.keys()) 
     print 'intersection : ',intersection
     print 'numerator : ', numerator

     sum1 = sum([vec1[x]**2 for x in vec1.keys()])
     print 'sum1 : ', sum1
     sum2 = sum([vec2[x]**2 for x in vec2.keys()])
     print 'sum2 : ', sum2
     denominator = math.sqrt(sum1) * math.sqrt(sum2)
     print 'denominator : ', denominator
     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator

def text_to_vector(text):
     words = WORD.findall(text)
     return Counter(words)

text1 = 'Trademark Fine Art Andrea \'Mia\'  16 x 16 (MA0606-B1616BMF)'
text2 = 'Trademark Fine Art Andrea \'Pale Blue Eyes\'  16 x 16 (MA0608-B1616BMF)'

vector1 = text_to_vector(text1)
vector2 = text_to_vector(text2)

cosine = get_cosine(vector1, vector2)

print 'Cosine:', cosine