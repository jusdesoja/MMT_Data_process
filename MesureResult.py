# -*- coding: utf-8 -*-
import element
from formatter import PreleverBloque
from formatter import DefType
from xlwt import Workbook
from easyExcel import easyExcel
class MesureResult:
	"""Cette classe sert à enregistrer les résultat mesuré en fichier excel
	"""
	_LineInd = 0
	_con = []
	_PointList = []
	_CylindreList = []
	_PlaneiteList = []
	_CercleList = []
	_CylindriciteList = []
	_PointN = 0
	_CylindreN = 0
	_PlaneiteN = 0
	_CercleN = 0
	_CylindriciteN = 0
	def __init__(self,SourceFile = "data.txt"):
		"""initialiser la classe. L'initialisation demande le nom de SourceFile qui contient les données brutes
		"""
		self._filename = SourceFile
		self._con = file(SourceFile,"r").readlines()
		self._LineTotal = len(self._con)
		while (self._LineInd < self._LineTotal):
			bloque, self._LineInd = PreleverBloque(self._con, self._LineInd)
			FormType = DefType(bloque)
			if FormType == "POINT":
				self._PointList.append(element.POINT("Point" + str(self._PointN), bloque))
				self._PointN += 1
                
			if FormType == "CYLINDRE":
				self._CylindreList.append(element.CYLINDRE("Cylindre" + str(self._CylindreN), bloque))
				self._CylindreN += 1
                
			if FormType == "CERCLE":
				self._CercleList.append(element.CERCLE("Cercle" + str(self._CercleN), bloque))
				self._CercleN += 1
                
			if FormType == "PLANEITE":
				self._PlaneiteList.append(element.PLANEITE("Planeite" + str(self._PlaneiteN), bloque))
				self._PlaneiteN += 1
                
			if FormType == "CYLINDRICITE": #en fait je sais pas son vrai nom, il faut encore fait des expérimentations
				self._CylindriciteList.append(element.CYLINDRICITE("Cylindricite" + str(self._CylindriciteN), bloque))
				self._CylindriciteN += 1
	
	def AlimenterExcel(self,ResultName = 'CDC.xlsx'):
		"""Alimenter la carte de contrôle sans donnée. Cette fonction est basé d'une carte de contrôle brute"""
		#excel = easyExcel(ResultName)
		book = Workbook()
		if self._PointN > 0:
			PointSheet = book.add_sheet("Point")
			PointSheet.write(0,0,"Pièce")
			for n in range(30):
				PointSheet.write(0,n,str(n))
			for n in range(self._PointN):
				print "Point more"
		if self._CylindreN > 0:
			CylindreSheet = book.add_sheet("Cylindre")
			PointSheet.write(0,0,"Pièce")
			for n in range(30):
				PointSheet.write(0,n,str(n))
			for n in range(self._CylindreN):
				CylindreSheet.write(self._CylindreList[n]._echantillon + 1,self._CylindreList[n]._piece,self._CylindreList[n].getDiametre())	
		
		if self._PlaneiteN > 0:
			PlaneiteSheet = book.add_sheet("Planeite")
			PlaneiteSheet.write(0,0,"Pièce")
			for n in range(30):
				PlaneiteSheet.write(0,n,str(n))
			for n in range(self._PlaneiteN):
				PlaneiteSheet.write(self._PlaneiteList[n]._echantillon + 1,self._PlaneiteList[n]._piece,self._PlaneiteList[n].getDistance())
		
		if self._CercleN > 0:
			CercleSheet = book.add_sheet("Cercle")
			CercleSheet.write(0,0,"Pièce")
			for n in range(30):
				CercleSheet.write(0,n,str(n))
			for n in range(self._CercleN):
				CercleSheet.write(self._CercleList[n]._echantillon + 1,self._CercleList[n]._piece,self._CercleList[n].getDiametre())

		if self._CylindriciteN > 0:
			CylindriciteSheet = book.add_sheet("Cylindricite")
			CylindriciteSheet.write(0,0,"Pièce")
			for n in range(30):
				CylindriciteSheet.write(0,n,str(n))
			for n in range(self._CylindriciteN):
				CylindriciteSheet.write(self._CylindriciteList[n]._echantillon + 1,self._CylindriciteList[n]._piece,self._CylindriciteList[n].getDistance())

		book.save(ExcelName)
	
	def WriteExcel(self,ExcelName = "Result1.xls"):
		"""Créer un fichier Excel et le remplir avec les données utiles
		"""
		book = Workbook()
		if self._PointN > 0:
			PointSheet = book.add_sheet("Point")
			PointSheet.write(0,0,"No.")
			PointSheet.write(0,1,"NAME")
			PointSheet.write(0,2,"X")
			PointSheet.write(0,3,"Y")
			PointSheet.write(0,4,"Z")
			for n in range(self._PointN):
				PointSheet.write(n + 1,0,str(n))
				PointSheet.write(n + 1,1,self._PointList[n]._nom)                
				for i in range(3):
					PointSheet.write(n + 1,i +2 ,self._PointList[n].getCoordonnee()[i])
				PointSheet.write(n + 1,5,self._PointList[n]._piece)
				PointSheet.write(n + 1,6,self._PointList[n]._echantillon)
		if self._CylindreN > 0:
			CylindreSheet = book.add_sheet("Cylindre")
			CylindreSheet.write(0,0,"No.")
			CylindreSheet.write(0,1,"NAME")
			CylindreSheet.write(0,2,"X")
			CylindreSheet.write(0,3,"Y")
			CylindreSheet.write(0,4,"Z")
			CylindreSheet.write(0,5,"Diametre")
			CylindreSheet.write(0,6,"Ecart Type")
			for n in range(self._CylindreN):
				CylindreSheet.write(n + 1,0,str(n))
				CylindreSheet.write(n + 1,1,self._CylindreList[n]._nom)
				for i in range(3):
					CylindreSheet.write(n + 1,i +2 ,self._CylindreList[n].getCoordonnee()[i])
				CylindreSheet.write(n + 1,5,self._CylindreList[n].getDiametre())
				CylindreSheet.write(n + 1,6,self._CylindreList[n].getEcartType())
		if self._PlaneiteN > 0:
			PlaneiteSheet = book.add_sheet("Planeite")
			PlaneiteSheet.write(0,0,"No.")
			PlaneiteSheet.write(0,1,"NAME")
			PlaneiteSheet.write(0,2,"Distance")
			PlaneiteSheet.write(0,3,"Ecart Type")
			for n in range(self._PlaneiteN):
				PlaneiteSheet.write(n + 1,0,str(n))
				PlaneiteSheet.write(n + 1,1,self._PlaneiteList[n]._nom)
				PlaneiteSheet.write(n + 1,2,self._PlaneiteList[n].getDistance())
				PlaneiteSheet.write(n + 1,3,self._PlaneiteList[n].getEcartType())
		if self._CercleN > 0:
			CercleSheet = book.add_sheet("Cercle")
			CercleSheet.write(0,0,"No.")
			CercleSheet.write(0,1,"NAME")
			CercleSheet.write(0,2,"X")
			CercleSheet.write(0,3,"Y")
            #CercleSheet.write(0,4,"Z")
			CercleSheet.write(0,4,"Diametre")
			CercleSheet.write(0,5,"Ecart Type")
			for n in range(self._CercleN):
				CercleSheet.write(n + 1,0,str(n))
				CercleSheet.write(n + 1,1,self._CercleList[n]._nom)
				for i in range(2):
					CercleSheet.write(n + 1,i +2 ,self._CercleList[n].getCoordonnee()[i])
				CercleSheet.write(n + 1,4,self._CercleList[n].getDiametre())
				CercleSheet.write(n + 1,5,self._CercleList[n].getEcartType())
		if self._CylindriciteN > 0:
			CylindriciteSheet = book.add_sheet("Cylindricite")
			CylindriciteSheet.write(0,0,"No.")
			CylindriciteSheet.write(0,1,"NAME")
			CylindriciteSheet.write(0,2,"Distance")
			CylindriciteSheet.write(0,3,"Ecart Type")
			for n in range(self._CylindriciteN):
				CylindriciteSheet.write(n + 1,0,str(n))
				CylindriciteSheet.write(n + 1,1,self._CylindriciteList[n]._nom)
				CylindriciteSheet.write(n + 1,2,self._CylindriciteList[n].getDistance())
				CylindriciteSheet.write(n + 1,3,self._CylindriciteList[n].getEcartType())
        
		book.save(ExcelName)

#a = MesureResult("data")
#a.WriteExcel("result.xls")