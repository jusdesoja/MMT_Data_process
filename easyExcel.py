# -*- coding: utf-8 -*-
from win32com.client import Dispatch
from shutil import copyfile
import win32com.client
class easyExcel:
	"""A utility to make it easier to get at Excel.  Remembering 
	to save the data is your problem, as is  error handling. 
	Operates on one workbook at a time.""" 
	def __init__(self, filename=None): 
		self.xlApp = win32com.client.Dispatch('Excel.Application') 
		self.xlApp.Visible = True
		if filename: 
			copyfile("carte_de_controle_brute.xlsx", filename)
			self.filename = filename 
			self.xlBook = self.xlApp.Workbooks.Open(filename) 
		else: 
			self.xlBook = self.xlApp.Workbooks.Add()
			self.filename = r'CDCresult.xlsx'    
	def save(self, newfilename=None): 
		if newfilename: 
			self.filename = newfilename 
			self.xlBook.SaveAs(newfilename) 
		else: 
			self.xlBook.Save()    
	def close(self): 
		self.xlBook.Close(SaveChanges=0) 
		del self.xlApp 
		
	def SearchCell(self,sheet,text):
		"find the position of the text"
		sht = self.xlBook.Worksheets(sheet)
		sht.Activate()
		find = sht.UsedRange.Find(text)
		print find.Address
		return find.Address
		
	def getCell(self, sheet, row, col): 
		"Get value of one cell" 
		sht = self.xlBook.Worksheets(sheet) 
		return sht.Cells(row, col).Value 
	def setCell(self, sheet, row, col, value): 
		"set value of one cell" 
		sht = self.xlBook.Worksheets(sheet) 
		sht.Cells(row, col).Value = value 
	def getRange(self, sheet, row1, col1, row2, col2): 
		"return a 2d array (i.e. tuple of tuples)" 
		sht = self.xlBook.Worksheets(sheet) 
		return sht.Range(sht.Cells(row1, col1), sht.Cells(row2, col2)).Value 
	def addPicture(self, sheet, pictureName, Left, Top, Width, Height): 
		"Insert a picture in sheet" 
		sht = self.xlBook.Worksheets(sheet) 
		sht.Shapes.AddPicture(pictureName, 1, 1, Left, Top, Width, Height) 
	def cpSheet(self, before): 
		"copy sheet" 
		shts = self.xlBook.Worksheets 
		shts(1).Copy(None,shts(1)) 
#try:		
#	excel = easyExcel(r"C:\Users\y.zhang\Documents\python\test.xls")  #obligatoir d'être en cette forme
#	excel.setCell('Cartes de controle',1,1,"test")
#	excel.save()
#finally:
#	excel.close()