# -*- coding: utf-8 -*-
"""Module pour formatter les résultat de musure"""
import re
#filename = "data.txt"



CHIFFRE = ('0','1','2','3','4','5','6','7','8','9','.','-')
LETTRE = ('a','b','c','d','e','f','g','h','i','j','k','l',
            'm','n','o','p','q','r','s','t','u','v','w','x','y','z',
            'A','B','C','D','E','F','G','H','I','J','K','L','M','N',
            'O','P','Q','R','S','T','U','V','W','X','Y','Z')
def File_Findline(filename, string):
    """trouver numéro de ligne d'un string à partir de début d'un fichier
    Retourne le numéro de ligne
    """
    datafile = file(filename,"r")
    LineNb = []
    n = 0
    for s in datafile.readlines():
        li = re.findall(string, s)
        n += 1
        if len(li) != 0:
            LineNb.append(n)
    datafile.close()
    return LineNb

def Findline(contenu,string):
    """trouver numéro de ligne d'un string à partir d'une liste de string.
    Retourner le numéro de ligne
    """
    LineNb = []
    n = 0
    for s in contenu:
        li = re.findall(string, s)
        n += 1
        if len(li) != 0:
            LineNb.append(n)
    return LineNb

	
def PieceEchan(bloque):
	"""Trouver le numéro de piece d'un bloque"""
	for line in bloque:
		if "Piece" in line:
			PieceNum = str(AutoConvertFloat(line))
		if "Echantillon" in line:
			EchanNum = str(AutoConvertFloat(line))
	return PieceNum,EchanNum
def AutoConvertFloat(string):
    """Trouver le figure en caracter et le convertir en float automatiquement.
    Cette méthode saisi tous les chiffre et '.' '-' dans le string.
    Retourne le donnée en float
    S'il a plusieurs de '.' ou '-' ou le '-' n'est pas au début, il y aura errors
    """
    figure = ''
    for char in string:
        if char in CHIFFRE:
            figure += char
    floatfigure = float(figure)
    return floatfigure
 
def ConvertCoordonnee(bloque):
    """Trouver les coordonnées dans un bloque et renvoyer ses valeurs
    """
    Coordonnee = [0.0,0.0,0.0]
    #Flag = 0
    for line in bloque:
        if '  X   ' in line:
            Coordonnee[0] = AutoConvertFloat(line)
        if '  Y   ' in line:
            Coordonnee[1] = AutoConvertFloat(line)
        if '  Z   ' in line:
            Coordonnee[2] = AutoConvertFloat(line)
        return Coordonnee
    

def ConvertBloque(bloque):
    """Convertir une liste de str s'agissant d'un résultat en format propre
    (qui peut être utilisé dans excel)
    retourne les coordonnées , le diametre et l'écart type (s'ils existent)
    """
    Coordonnee = [0.0,0.0,0.0]
    Flag = 0
    for line in bloque:
        if '  X   ' in line:
            Coordonnee[0] = AutoConvertFloat(line)
        if '  Y   ' in line:
            Coordonnee[1] = AutoConvertFloat(line)
        if '  Z   ' in line:
            Coordonnee[2] = AutoConvertFloat(line)
        if '  D   ' in line:
            Flag = 1
            ParaD = AutoConvertFloat(line)
        if 'ECART TYPE :' in line:
            EcartType = AutoConvertFloat(line)
            if Flag == 1:
                Flag = 2
            else:
                Flag = 3
    if Flag == 0:
        return Coordonnee
    if Flag == 1:
        return Coordonnee, ParaD, 0
    elif Flag == 2:
        return Coordonnee, ParaD, EcartType
    elif Flag == 3:
        return Coordonnee, EcartType

def ConvertParaD(bloque):
    """Trouver le Parametre D dans un bloque et renvoyer son valeur """
    flag = 0
    for line in bloque:
        if '  D   ' in line:
            ParaD = AutoConvertFloat(line)
            flag = 1
    if flag == 1: 
        return ParaD
    else:
        return "Pas de Parametre D"
def ConvertEcartType(bloque):
    """Trouver l'écart type dans un bloque et renvoyer son valeur"""
    flag = 0
    for line in bloque:
        if 'ECART TYPE :' in line:
            EcartType = AutoConvertFloat(line)
            flag = 1
        
    if flag == 1:
        return EcartType
    else:
        return -1
##cette méthode a encore des fautes à corriger    
def PreleverBloque(contenu,start):
    """Prélever un bloque de la contenu
    un bloque se commence par "> No DU BLOQUE" et se termine par "[len"
    retourne un bloque de mesure, et le numéro de derniere ligne lié au bloque de la contenu
    """
    Commutateur = 0
    bloque = []
    for lineN in range(len(contenu[start:])):
        if "> No DU BLOQUE" in contenu[start+lineN]:
            Commutateur = 1
        if "[len" in contenu[start+lineN]:
            Commutateur = 0
            end = start + lineN  + 1
            break
        if Commutateur == 1:
            bloque.append(contenu[start+lineN]) 
    return bloque, end    
    
def DefType(bloque):
    """Trouver le type de mesure du bloque"""
    BloqueType = ''
    theList = list(bloque[1])
    lenth = len(theList)
    for n in range(lenth):
        if (theList[n] == ' ') :
            if ((n+1) >= lenth) or (theList[n + 1] == ' '): 
                break
        if theList[n] in LETTRE:
            BloqueType += theList[n]
    return BloqueType