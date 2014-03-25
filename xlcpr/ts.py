import os
import glob
import csv
import xlwt
import xlrd
from xlwt import *
from xlrd import *
import HTML

with open("config") as configfile :
	for i, row in enumerate(configfile):
		if (i == 0) :
			file1 = row.strip()
		elif (i == 1) :
			file2 = row.strip()
		table_names = []
		table_datas = []
		out = open("out/out.html", "w")

def chkCol(val, cols) :
	for col in cols :
		if (col.value == val or val == "" or val is None) :
			return True
	return False

def compareCols(sheet_name, worksheet1, worksheet2) :
	sheet1_cols = []
	sheet2_cols = []
	shared_cols = []
	table_data = []
	try :
		sheet1_cols = list(worksheet1.row(0))
	except IndexError:
		print (file1 + "::" + sheet_name + " does not have first row data");

	try :
		sheet2_cols = list(worksheet2.row(0))
	except IndexError:
		print (file2 + "::" + sheet_name + " does not have first row data");

	for sheet1_col in sheet1_cols :
		if not chkCol(sheet1_col.value, sheet2_cols) :
			print "Deleted column: " + sheet_name + "::" + sheet1_col.value
		else :
			shared_cols.append(sheet1_col.value)

	for sheet2_col in sheet2_cols :
		if not chkCol(sheet2_col.value, sheet1_cols) :
			print "Added column: " + sheet_name + "::" + sheet2_col.value

	table_data.append(shared_cols)

	num_rows = worksheet1.nrows - 1
	num_cols = worksheet2.ncols - 1
	curr_row = 0;
	while curr_row < num_rows :
		row_data = []
		curr_row += 1
		row = worksheet1.row(curr_row)
		curr_col = -1
		isSkipped = True
		while curr_col < num_cols :
			curr_col += 1
			# Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
			try :
				cell1_type = worksheet1.cell_type(curr_row, curr_col)
				cell1_value = worksheet1.cell_value(curr_row, curr_col)
				if isinstance(cell1_value, float) and int(cell1_value) == cell1_value :
					cell1_value = int(cell1_value)
			except IndexError :
				cell1_type = 0
				cell1_value = ""

			try :
				cell2_type = worksheet2.cell_type(curr_row, curr_col)
				cell2_value = worksheet2.cell_value(curr_row, curr_col)
				if isinstance(cell2_value, float) and int(cell2_value) == cell2_value :
					cell2_value = int(cell2_value)
			except IndexError :
				cell2_type = 0
				cell2_value = ""

			if cell1_value != cell2_value :
				cell1_str = cell1_value
				cell2_str = cell2_value
				if isinstance(cell1_value, float) or isinstance(cell1_value, int) :
					cell1_str = str(cell1_value)
				if isinstance(cell2_value, float) or isinstance(cell2_value, int) :
					cell2_str = str(cell2_value)
				row_data.append(cell1_str + "=>" + cell2_str)
				# print "[", curr_row, ", ", curr_col, "]: ", cell1_value, "=>", cell2_value
				isSkipped = False
			else :
				cell1_str = cell1_value
				if isinstance(cell1_value, float) or isinstance(cell1_value, int) :
					cell1_str = str(cell1_value)
				row_data.append(cell1_str)
				if (not cell1_str is None) and (cell1_str.strip() != "") :
					isSkipped = False

		if not isSkipped :
			table_data.append(row_data)

	table_names.append(sheet_name)
	table_datas.append(table_data)

def compareSheets(workbook1, workbook2) :
	sheet1_names = list(workbook1.sheet_names())
	sheet2_names = list(workbook2.sheet_names())
	shared_sheet_names = []

	# Compare sheet names
	for sheet1_name in sheet1_names :
		if not sheet1_name in sheet2_names :
			print "Deleted sheet: " + sheet1_name
		else :
			shared_sheet_names.append(sheet1_name)

	for sheet2_name in sheet2_names :
		if not sheet2_name in sheet1_names :
			print "Added sheet: " + sheet2_name

	# Compare shared sheets
	for sheet_name in shared_sheet_names :
		worksheet1 = workbook1.sheet_by_name(sheet_name)
		worksheet2 = workbook2.sheet_by_name(sheet_name)
		compareCols(sheet_name, worksheet1, worksheet2)

def main():
	workbook1 = xlrd.open_workbook(file1)
	workbook2 = xlrd.open_workbook(file2)
	compareSheets(workbook1, workbook2)

	for i, table_name in enumerate(table_names) :
		table_data = table_datas[i]
		out.write("<b>" + table_name + "</b><br/>\n")
		htmlcode = HTML.table(table_data)
		out.write(htmlcode)
		out.write("<br />\n")

	out.close()

main()