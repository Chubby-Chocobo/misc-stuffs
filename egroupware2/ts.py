import os
import glob
import csv
import xlwt
from xlwt import *

with open("config") as configfile :
	for i, row in enumerate(configfile):
		if (i == 0) :
			yy = int(row)
		elif (i == 1) :
			mm = int(row)
		elif (i == 2) :
			dd_start = int(row)
		elif (i == 3) :
			duration = int(row)

	mm_str = ""
	if (mm == 1) :
		mm_str = "Jan"
	elif (mm == 2) :
		mm_str = "Feb"
	elif (mm == 3) :
		mm_str = "Mar"
	elif (mm == 4) :
		mm_str = "Apr"
	elif (mm == 5) :
		mm_str = "May"
	elif (mm == 6) :
		mm_str = "Jun"
	elif (mm == 7) :
		mm_str = "Jul"
	elif (mm == 8) :
		mm_str = "Aug"
	elif (mm == 9) :
		mm_str = "Sep"
	elif (mm == 10) :
		mm_str = "Oct"
	elif (mm == 11) :
		mm_str = "Nov"
	elif (mm == 12) :
		mm_str = "Dec"
	date_string = "From " + str(dd_start) + mm_str + " to " + str(dd_start + duration - 1) + mm_str
	file_name = "Art team timesheet " + str(dd_start) + mm_str + " to " + str(dd_start + duration - 1) + mm_str

def processRow(sheet, row_data) :
	header_rows = 3
	row_index = header_rows
	row = list(row_data)

	row_date = row[4]
	y = int(row_date[:4])
	m = int(row_date[5:7])
	d = int(row_date[8:10])

	if (y != yy or m != mm or d < dd_start or d >= dd_start + duration) :
		return
	else :
		row_index = row_index + d - dd_start

	isOffwork = False
	for i, col in enumerate(row) :
		if i == 1 and str(col).find("Off-Work") > -1 :
			print ("Off-Work")
			isOffwork = True

		if (i < 6) :
			if (i == 0) :
				sheet.write(row_index, i, int(col))
			elif (i == 5) :
				if isOffwork :
					sheet.write(row_index, 5, 0)
					sheet.write(row_index, 6, int(col))
				else :
					sheet.write(row_index, 5, int(col))
					sheet.write(row_index, 6, 0)
			else :
				sheet.write(row_index, i, col)
		elif (i == 6) :
			sheet.write(row_index, i+1, int(col))
		elif (i < 10) :
			sheet.write(row_index, i+1, col)

def processFile(workbook, name, filepath) :
	sheet = workbook.add_sheet(name, cell_overwrite_ok=True)
	style_header = xlwt.easyxf('font: bold 1, color white; pattern: pattern solid, fore_color dark_blue_ega;')
	sheet.write(0, 0, "Name", style_header)
	sheet.write_merge(0, 0, 1, 10, name, style_header)
	sheet.write_merge(1, 1, 1, 10, date_string, style_header)
	sheet.write(1, 0, "Date", style_header)
	with open(filepath, 'r') as f:
		reader = csv.reader(f, delimiter=";")
		for row_index, row in enumerate(reader) :
			if (row_index == 0) :
				style_header2 = xlwt.easyxf('font: bold 1; pattern: pattern solid, fore_color silver_ega;')
				cols = ['ts_id', 'ts_project', 'ts_title', 'ts_description', 'ts_start', 'ts_duration', 'off_work', 'ts_quantity', 'ts_unitprice', 'cat_id', 'ts_owner']
				for i, col in enumerate(cols) :
					sheet.write(2, i, col, style_header2)
			else :
				processRow(sheet, row)

		# ts_id
		sheet.col(0).width = 256 * 7
		# ts_project
		sheet.col(1).width = 256 * 30
		# ts_title
		sheet.col(2).width = 256 * 45
		# ts_description
		sheet.col(3).width = 256 * 10
		# ts_start
		sheet.col(4).width = 256 * 20
		# ts_duration
		sheet.col(5).width = 256 * 10
		# off_work
		sheet.col(6).width = 256 * 10
		# ts_quanity
		sheet.col(7).width = 256 * 10
		# ts_unitprice
		sheet.col(8).width = 256 * 5
		# cat_id
		sheet.col(9).width = 256 * 5
		# ts_owner
		sheet.col(10).width = 256 * 15

		sheet.write(8, 5, Formula("SUM(F4:F8)"))
		sheet.write(8, 6, Formula("SUM(G4:G8)"))

		style_sum1 = xlwt.easyxf('font: bold 1, color black; pattern: pattern solid, fore_color aqua;')
		sheet.write(10, 4, "Total working (hours)", style_sum1)
		sheet.write(10, 5, Formula("SUM(F9/60)"), style_sum1)
		style_sum2 = xlwt.easyxf('font: bold 1, color black; pattern: pattern solid, fore_color light_orange;')
		sheet.write(11, 4, "Over time (hours)", style_sum2)
		sheet.write(11, 5, Formula("F11+F13-40"), style_sum2)
		style_sum3 = xlwt.easyxf('font: bold 1, color black; pattern: pattern solid, fore_color silver_ega;')
		sheet.write(12, 4, "Off work (hours)", style_sum3)
		sheet.write(12, 5, Formula("G9/60"), style_sum3)

def main():
	members = []
	os.chdir("./")
	workbook = xlwt.Workbook()
	for filepath in glob.glob("in/*.csv"):
		name, ext = os.path.splitext(os.path.basename(filepath))
		processFile(workbook, name, filepath)

	workbook.save("out/" + file_name + ".xls")

main()