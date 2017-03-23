import swalign
#match = 2
#mismatch = -1
#scoring = swalign.NucleotideScoringMatrix(match, mismatch)

#sw = swalign.LocalAlignment(scoring)  # you can also choose gap penalties, etc...
#alignment = sw.align('Trademark ','Trademark Anderson \"Detroit\" Art, Black Matte W/Black Frame, 11\" x 14\"')
#alignment.dump()


from scipy import spatial
dataSetI = [2.34343]
dataSetII = [233333]
result = 1 - spatial.distance.cosine(dataSetI, dataSetII)
print result