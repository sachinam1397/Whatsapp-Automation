import xlrd

class InvalidRange(Exception):
	pass

		

def excel_to_dict_with_range(sheet,start,end,message = None):      # covert sheet to dictionary object 
	no_col=sheet.ncols                                             # get no of column in the sheet
	number_column = 0                                              # initialize number column with none
	message_column = None                                          # initialize message column with none
	name_column = None
	if(message == None):
		message = "NO MESSAGE"
	for column in range(no_col):                                   # loop to get both message and number column
		if (sheet.col_values(colx=column)[0]=="Phone Number"):
			number_column = column
		if (sheet.col_values(colx=column)[0]=="Message"):
			message_column = column
		if(sheet.col_values(colx=column)[0] == "Name"):
			name_column = column
	if(number_column == None):                                     # if number column will be none then throw error
		print("[ KEY ERROR ] Column Phone Number Not Found\n")
		return None
	else:
		dictionary = dict()                                         # final data dictionary
		name_dictionary = dict()
		if(message_column == None):
			message_to_be_send = message
			for n in range(start - 1,end):
				l = str(sheet.cell_value(n,number_column)).split('.')
				l = l[0]
				dictionary[l] = message
		else:
			for n in range(start - 1,end):
				l = str(sheet.cell_value(n,number_column)).split('.')
				l = l[0]
				dictionary[l] = sheet.cell_value(n,message_column)
		if(name_column == None):
			pass
		else:
			for n in range(start - 1, end):
				l = str(sheet.cell_value(n,number_column)).split('.')
				l = l[0]
				name_dictionary[l] = sheet.cell_value(n,name_column)
		return dictionary,name_dictionary
			

# Function to get workbook object
def open_file(file_loc,sheet_index,starting_index = None,ending_index = None,message = None):
	try:
		workbook = xlrd.open_workbook(file_loc)       # open workbook and get object of the workbook
	except Exception as error:
		print("[ OPEN Error ] " + str(error))
	try: 
		sheet_index = sheet_index                     # sheet number (might be multiple sheets were there in book)
		sheet = workbook.sheet_by_index(sheet_index)  # get specified sheet object of the workbook 
		starting_index = starting_index               # starting row
		ending_index = ending_index                   # starting column
		if(ending_index == 0):
			ending_index = sheet.nrows


		if(starting_index < 1 or ending_index < 1 or starting_index > ending_index): # check for index range to be valid 
			raise InvalidRange("Invalid START and END Range")                        # raise invalid range exception 
		else:
			dictionary,name_dictionary = excel_to_dict_with_range(sheet,starting_index,ending_index,message)	
		return dictionary,name_dictionary
	except InvalidRange as e:
		print(str(e))
	except Exception as error: # Exception to handle error other than InvalidRange
		print(str(error))
	


