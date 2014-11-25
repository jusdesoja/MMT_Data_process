from easyExcel import *
from formatter import *

def preleveMesure(contenu):
	"""Prelever un bloque a partir d'un string, 
	return bloque et end. end est le nombre de lignes du bloque"""
	Commutateur = 0
    bloque = []
    for lineN in range(len(contenu)):
        if "> No DU BLOQUE" in contenu[lineN]:
            Commutateur = 1
        if "[len" in contenu[lineN]:
            Commutateur = 0
            end = lineN  + 1
            break
        if Commutateur == 1:
            bloque.append(contenu[start+lineN]) 
    return bloque, end 

def WriteExcel(bloque,excel,n):
	i = n // 5
	j = n % 5
	excel.setCell('Cartes de controle', 12 + j, i + 1, ConvertParaD(bloque))
	
	