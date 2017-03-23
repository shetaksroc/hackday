from nltk import metrics, stem, tokenize
 
stemmer = stem.PorterStemmer()
 
def normalize(s):
    words = tokenize.wordpunct_tokenize(s.lower().strip())
    return ' '.join([stemmer.stem(w) for w in words])
 
def fuzzy_match(s1, s2, max_dist=3):
    return metrics.edit_distance(normalize(s1), normalize(s2)) <= max_dist

text1 = 'Trademark Fine Art Andrea \'Mia\'  16 x 16 (MA0606-B1616BMF)'
text2 = 'Trademark Fine Art Andrea \'Pale Blue Eyes\'  16 x 16 (MA0608-B1616BMF)'
fuzzy_match(text1,text2)
