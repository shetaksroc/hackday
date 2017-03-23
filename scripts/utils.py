import re

def print_nos(text):
	numbers = re.findall(r' \d+"', text)
	print 'Numbers : ',numbers

def getSizes(text):
	pattern = '\s\d+(\.\d*)?(\"|\')?(\s)*(\d+)?(\"|\')?(\s)*[x|X](\s)*\d+(\.\d*)?(\"|\')?(\s)*(\d+)?(\"|\')?(\s)'
	compiled = re.compile(pattern)
	result = compiled.search(text)
	size=""
	if result:
	    size = result.group(0)
	else:
		print "No size found"
	return size

def split_line(text):
    # split the text
    words = text.split()
    
    # for each word in the line:
    for word in words:
        # print the word
        print(word)
