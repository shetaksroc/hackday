import re
import webcolors

colors= ['alice blue', 'antique white', 'aqua', 'aquamarine', 'azure', 'beige', 'bisque', 'black', 'blanched almond', 'blue', 'blue violet', 'brown', 'burly wood', 'cadet blue', 'chartreuse', 'chocolate', 'coral', 'cornflower blue', 'cornsilk', 'crimson', 'cyan', 'dark blue', 'dark cyan', 'dark golden rod', 'dark gray', 'dark grey', 'dark green', 'dark khaki', 'dark magenta', 'dark olive green', 'dark orange', 'dark orchid', 'dark red', 'dark salmon', 'dark sea green', 'dark slate blue', 'dark slate gray', 'dark slate grey', 'dark turquoise', 'dark violet', 'deep pink', 'deep sky blue', 'dim gray', 'dim grey', 'dodger blue', 'fire brick', 'floral white', 'forest green', 'fuchsia', 'gainsboro', 'ghost white', 'gold', 'golden rod', 'gray', 'grey', 'green', 'green yellow', 'honey dew', 'hot pink', 'indian red', 'indigo', 'ivory', 'khaki', 'lavender', 'lavender blush', 'lawn green', 'lemon chiffon', 'light blue', 'light coral', 'light cyan', 'light golden rod yellow', 'light gray', 'light grey', 'light green', 'light pink', 'light salmon', 'light sea green', 'light sky blue', 'light slate gray', 'light slate grey', 'light steel blue', 'light yellow', 'lime', 'lime green', 'linen', 'magenta', 'maroon', 'medium aqua marine', 'medium blue', 'medium orchid', 'medium purple', 'medium sea green', 'medium slate blue', 'medium spring green', 'medium turquoise', 'medium violet red', 'midnight blue', 'mint cream', 'misty rose', 'moccasin', 'navajo white', 'navy', 'old lace', 'olive', 'olive drab', 'orange', 'orange red', 'orchid', 'pale golden rod', 'pale green', 'pale turquoise', 'pale violet red', 'papaya whip', 'peach puff', 'peru', 'pink', 'plum', 'powder blue', 'purple', 'rebecca purple', 'red', 'rosy brown', 'royal blue', 'saddle brown', 'salmon', 'sandy brown', 'sea green', 'sea shell', 'sienna', 'silver', 'sky blue', 'slate blue', 'slate gray', 'slate grey', 'snow', 'spring green', 'steel blue', 'tan', 'teal', 'thistle', 'tomato', 'turquoise', 'violet', 'wheat', 'white', 'white smoke', 'yellow', 'yellow green']

def print_nos(text):
	numbers = re.findall(r' \d+"', text)
	print 'Numbers : ',numbers

def getDimensionSizes(text):
	pattern = '\d+\s\d+\/\d+\&quotH\s*(x|X)\s*\d+\s\d+\/\d+\&quotW\s*(x|X)\s*(\s|^)\d+\s\d+\/\d+\&quotD'
	compiled = re.compile(pattern)
	result = compiled.search(text)
	size=""
	if result:
	    size = result.group(0)
	
	return size

def getSizes(text):
	dimension=getDimensionSizes(text)
	if("" != dimension):
		return dimension
	pattern = '(\s|^)\d+(\.\d*)?(\"|\')?(\d+)?(\"|\')?(\s)*[x|X](\s)*\d+(\.\d*)?(\"|\')?(\d+)?(\"|\')?'
	compiled = re.compile(pattern)
	result = compiled.search(text)
	size=""
	if result:
	    size = result.group(0)
	
	return size

def split_line(text):
    # split the text
    words = text.split()
    
    # for each word in the line:
    for word in words:
        # print the word
        print(word)

def getColor(text):
	colorSet=list()
	for color in colors:
		redefinedColor=str(' '+color+' ')
		if redefinedColor in text.lower():
			colorSet.append(color)
	return colorSet

def getProductType(original_title,original_size,brand):
	#print original_title,brand
	#brand=row_list[2].lower()
	#title=title.replace(brand,"")
	#print "Params are size: ",original_size,"\tbrand : ",brand,"\tTitle : ",original_title,""
	pack=getPackQuantity(original_title).lower()
	colors=getColor(original_title)
	original_title=original_title.lower()
	original_title=original_title.replace(original_size,"")
	original_title=original_title.replace(pack,"")
	original_title=original_title.replace(brand,"")
	for color in colors:
		original_title=original_title.replace(color.lower(),"")
	#original_title=original_title.replace("\(.*\)", "")
	original_title=re.sub('\(.*\)', '', original_title)

	#print original_title
	return original_title
	
def getPackQuantity(text):
	slashPackPattern = '(\d+\/Pack)'
	packOfPattern = '(Pack Of\s?\d+)'
	compiled = re.compile(slashPackPattern)
	result = compiled.search(text)
	quantity=""
	if result:
	   quantity = result.group(0)
	else:
		compiled = re.compile(packOfPattern)
		result = compiled.search(text)
		quantity=""
		if result:
		   quantity = result.group(0)
	
	return quantity