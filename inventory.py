"""
 AUTHOR:  Adam Stevens
   DEPT:  SISTA APS
   DATE:  09/30/2014
VERSION:  1.0.0
"""

#------------------------------------------------------------------IMPORTS-------------------------------------------------------------------------------------

from sys import exit

#------------------------------------------------------------------GLOBALS-------------------------------------------------------------------------------------

#booleans for list combinations/output
HAS_BROKEN = True
COMBINE_BROKEN = False
MAKE_OUTPUT = True

#expected number of columns
NUM_COLS = 32

#file IO names
#INPUT_FILE = 'wikitablescript.txt'
INPUT_FILE = 'server_inven.txt'
OUTPUT_FILE = 'wikitableout.txt'
CSV_FILE_ONE = 'inventory.csv'
CSV_FILE_TWO = 'broken.csv'

#------------------------------------------------------------------CLASSES-------------------------------------------------------------------------------------

class Item:
    """
    description -- class to hold each item of inventory.  has an instance variable to hold passed list    
    """

    def __init__(self, list):
        """
        description -- constructor, takes list of size columns
        """
        
        #holds passed list
        self.__instance_list = list
        
    #END FUNCTION CONSTRUCTOR
    
    def verify(self):
        """
        description -- creates string to match wiki format
        
        returns str
        """
        
        #joins instance list with pipes
        joined = "|".join(self.__instance_list)
        
        #format start and end pipes
        return_string = ("|" + joined + "|\n")
        
        return return_string
        
    #END FUNCTION VERIFY
        
    def csv_format(self):
        """
        description -- creates string for csv format
        
        returns str
        """
        
        #list to hold modified strings
        csv_list = []
        
        #replace \\ and commas then appends to new list
        for item in self.__instance_list:
            temp = item.replace("\\", "")
            temp = temp.replace(",", "")
            csv_list.append(temp.strip())
            
        #join csv list with commas
        joined = ",".join(csv_list)
        
        return joined
        
    #END FUNCTION CSV_FORMAT
        
#END CLASS ITEM
 
#------------------------------------------------------------------DEFINITIONS---------------------------------------------------------------------------------
 
def output(header_list, item_list, broken_list, file_name):
    """
    description -- this functions creates an output file that matches the input file from
                   a PROPERLY formatted sista inventory wiki
                   
    header_list -- a list containing non-line items
    item_list   -- a list of all the line items
    broken_list -- a list of all the items in the broken table (if present)
    file_name   -- the output file name
    
    returns None
    
    """

    #open file
    o = open(file_name, 'w')
    
    #write first three lines of the header
    o.write(header_list[0])
    o.write(header_list[1])
    o.write(header_list[2])
    
    #writes line items
    for item in item_list:
       o.write(item.verify())
       
    #if writing uncombined broken list
    if (HAS_BROKEN and (not COMBINE_BROKEN)): 
        
        #write broken headers
        for i in range(3, len(header_list)-1):
            o.write(header_list[i])
         
        #write broken items
        for item in broken_list:
           o.write(item.verify())
    
    #write footer
    o.write(header_list[-1])
    
    o.close()
    
#END FUNCTION OUTPUT
    
def csv(header, item_list, file_name):
    """
    description -- creates a csv file from input wiki file
    
    header      -- header for csv
    item_list   -- list of items to populate csv
    file_name   -- name to name the new csv file
    
    returns None
    """
    
    #count to determine newline placement
    count = 0
    
    #empty list to hold header for joining
    header_stripped = []
    
    o = open(file_name, 'w')
    
    #format header
    header = header.split("^")
    header.pop(0)
    header.pop(-1)
    
    for item in header:
        header_stripped.append(item.strip())
        
    header = ','.join(header_stripped)
    
    o.write(header + "\n")
    
    #write line items to csv
    for item in item_list:
        count += 1
        if (count != len(item_list)):
            o.write(item.csv_format() + "\n")
        else:
            o.write(item.csv_format())
            
    o.close()
    
#END FUNCTION CSV
 
#------------------------------------------------------------------MAIN----------------------------------------------------------------------------------------
def main():
    """
    description -- reads from inventory file and populates lists.  can create output file.
                   exits on error.
    """
    
    #lists to populate
    headers = []
    items = []
    broken = []
    
    #string to hold csv headers
    col_headers = ""
    
    #count for </sortable> occurrences
    count = 0
    
    #holds line count
    line_count = 0

    #begin file in
    with open(INPUT_FILE) as f:
    
        #for line in file
        for line in f:
        
            #increment line count
            line_count += 1
            
            #grabs header for csv
            if (line_count == 3):
                col_headers = line
        
            #if headers/footers
            if (("===" in line) or ("<sortable>" in line) or (line.count("^") > 2) or ("</sortable>" in line) or (line == '\n')):
                
                #counts number of footers
                if ("</sortable>" in line):
                    count += 1
                
                #appends headers/footers to headers list
                headers.append(line)
            
            #else line item
            else:  
   
                #put line into list and modify first/last columns
                split_list = line.split("|")  
                split_list.pop(0)
                split_list.pop(-1)

                #report column error and exit
                if (len(split_list) > NUM_COLS):
                    print("line: " + str(line_count) + " EXTRA columns FOUND " + str(len(split_list)) + " NEED " + str(NUM_COLS))
                    exit()
                elif (len(split_list) < NUM_COLS):
                    print("line: " + str(line_count) + " MISSING columns FOUND " + str(len(split_list)) + " NEED " + str(NUM_COLS))
                    exit()
                
                #create Item object
                item = Item(split_list)
                
                #puts all non broken items into list
                if (count == 0 or (not HAS_BROKEN)):
                    items.append(item)
                    
                #elif broken items but want master list
                elif (COMBINE_BROKEN and HAS_BROKEN):
                    items.append(item)
                    
                #elif broken items and want seperate
                elif (((not (COMBINE_BROKEN)) and HAS_BROKEN) and count != 0):
                    broken.append(item)
    
    #if output file is needed              
    if MAKE_OUTPUT:
        output(headers, items, broken, OUTPUT_FILE)
    
    #create csv file either working or combined (based on global booleans)
    csv(col_headers, items, CSV_FILE_ONE)
    
    #creates separate csv files for working and broken (based on global booleans)
    if (HAS_BROKEN and (not COMBINE_BROKEN)):
        csv(col_headers, broken, CSV_FILE_TWO)
            
if __name__ == '__main__':
    main()       