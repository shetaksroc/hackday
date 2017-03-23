from difflib import SequenceMatcher
text1 = 'Trademark Fine Art Andrea \'Mia\'  16 x 16 (MA0606-B1616BMF)'
text2 = 'Trademark Fine Art Andrea \'Pale Blue Eyes\'  16 x 16 (MA0608-B1616BMF)'
s1='08.8"(L)X 5.5"(W)X12.2"(H) GPP Gift Shipping Box, Holiday Line, Teal Snowflakes, 24/Pack'
s2='08.8"(L)X 5.5"(W)X12.2"(H) GPP Gift Shipping Box, Holiday Line, Teal Snowflakes, 6/Pack'
m = SequenceMatcher(None, text1, text2)
print m.ratio()