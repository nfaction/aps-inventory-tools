#!/usr/bin/python

out = []
 
def parser():
 
	"""This function reads in our file that has our inventory data from Wiki Doku
	and it parses the data into individual rows and columns for ease of transferring 
	to sql"""
 
	inputFile = 'wikitablescript.txt'
	outputFile = 'database.txt'
 
	#Reads in the file that has our inventory data from Wiki Doku.
	fileIn = open(inputFile, "r")
	fileOut = open(outputFile, "w")
 
	for line in fileIn:
		#if statements that will skip the rows we do not need for our database.
		if """====""" in line:
			continue
		if """sortable>""" in line:
			continue
		if line.count("^") > 2:
			continue
		if """</sort""" in line:
			continue
			#end loop
		#Removes the first pipe out of each line in the file.    
		pipeRemoved = line.partition("|")	
		newList = list(pipeRemoved)
		#calling a specific string in our list to further parse.
		newLine = newList[2]
		#Removes the trailing pipe at the end of each line.
		pipeRemoved = newLine.rpartition("|")
		newLine = pipeRemoved[0]
		#creates a variable for each row that has the columns split and seperated.
		parsedLine = newLine.split("| ")
		cleanLine = [i.strip(' ') for i in parsedLine]
		# for i in cleanLine:
		# 	# print i
		# 	if "\\" in i:
		# 		print "Slashes were found on this item: ", i
		# 	else:
		# 		continue
		out.append(cleanLine)
		# print out
 
 
def checker():	
	fileOut = 'out.txt'
	ourFile = open(fileOut, "w")
	newList = []
	#inserting pipe at beginning and end of each line
 	for lists in out:
 		if len(lists) < 3:
 			lists = "\n\n"
 		else:
 			#insert _pipe_ between each column in list
 			for item in lists:
 					newList = [item + " | " for item in lists]
 			newList = ''.join(newList)
 		ourFile.write("| " + newList + "\n")	
 
 
 
def main():
	parser()
	checker()
 
 
 
 
if __name__ == "__main__":
	main()