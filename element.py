# -*- coding: utf-8 -*-
import formatter
import xlwt

        
class BLOQUE:
    """C'est bloque général"""
    def __init__(self,nom,bloque):
        """initialiser un bloque"""
        self._nom = nom
        self._bloque = bloque
        self._piece,self._echantillon = formatter.PieceEchan(bloque)
		
#    def WriteExcel(self,book):
        
        

class POINT(BLOQUE):
    """Point classe, hérité du BLOQUE"""
    def __init__(self,nom,bloque):
        """initialiser un point"""
        BLOQUE.__init__(self,nom,bloque)
        self.__type = 'POINT'
        self.__coordonnee = formatter.ConvertBloque(bloque)
    def SetCoor(self, X, Y, Z):
        """Mettre les coordonnées d'un point"""
        self.__coordonnee[0] = X
        self.__coordonnee[1] = Y
        self.__coordonnee[2] = Z
        
    def Afficher(self):
        """Afficher les informatinos d'un point"""
        print "Type:%s\nName:%s"%(self.__type,self._nom)
        print "Coordonnées: (%s,%s,%s)"%(self.__coordonnee[0],self.__coordonnee[1],self.__coordonnee[2])
    
    def getCoordonnee(self):
        return self.__coordonnee    
#    def WriteExcel(self,sheet,position):
        
    
    
class CYLINDRE(BLOQUE):
    """Cylindre classe ,hérité du BLOQUE"""
    def __init__(self,nom,bloque):
        """initialiser un cylindre"""
        BLOQUE.__init__(self,nom,bloque)
        self.__coordonnee, self.__Diametre, self.__EcartType = formatter.ConvertBloque(bloque)
        self.__type = "CYLINDRE"
        
    def Afficher(self):
        """Afficher les informations d'un cylindre"""
        print "Type:%s\nName:%s"%(self.__type,self._nom)
        print "Coordonnées: (%s,%s,%s)"%(self.__coordonnee[0],self.__coordonnee[1],self.__coordonnee[2])
        print "Diametre : %s\nÉcart Type : %s" % (self.__Diametre,self.__EcartType)
        
    #def WriteExcel(self,excel_file): 
    def getDiametre(self):
        return self.__Diametre
    def getEcartType(self):
        return self.__EcartType
    def getCoordonnee(self):
        return self.__coordonnee
class PLANEITE(BLOQUE):
    """Planeité classe ,hérité du BLOQUE"""
    def __init__(self,nom,bloque):
        """initialiser un planète"""
        BLOQUE.__init__(self,nom,bloque)
        self.__Distance = formatter.ConvertParaD(self._bloque)
        self.__EcartType = formatter.ConvertEcartType(bloque)
        self.__type = "PLANEITE"
        
        
    def Afficher(self):
        """Afficher les informations d'un planète"""
        print "Type:%s\nName:%s"%(self.__type,self._nom)
        print "Distance : %s\nÉcart Type : %s" % (self.__Distance,self.__EcartType)
        
    def getDistance(self):
        return self.__Distance
    def getEcartType(self):
        return self.__EcartType    
    #def WriteExcel(self,excel_file): 
    
class CYLINDRICITE(BLOQUE):
    """Cylindricité classe ,hérité du BLOQUE"""
    def __init__(self,nom,bloque):
        """initialiser une cylindricité"""
        BLOQUE.__init__(self,nom,bloque)
        self._nom = nom
        self.__Distance,self.__EcartType = formatter.ConvertParaD(bloque),formatter.ConvertEcartType(bloque)
        self.__type = "CYLINDRICITÉ"
        
    def Afficher(self):
        """Afficher les informations d'une cylindricité"""
        print "Type:%s\nName:%s"%(self.__type, self._nom)
        print "Distance : %s\nÉcart Type : %s" % (self.__Diametre, self.__EcartType)
    
    def getDistance(self):
        return self.__Distance
    def getEcartType(self):
        return self.__EcartType    
    #def WriteExcel(self,excel_file):  
    
class CERCLE(BLOQUE):
    """Cercle classe ,hérité du BLOQUE"""
    def __init__(self,nom,bloque):
        """initialiser un cercle"""
        BLOQUE.__init__(self,nom,bloque)
        self.__coordonnee, self.__Diametre,self.__EcartType = formatter.ConvertBloque(bloque)
        self.__type = "CERCLE"
        
    def Afficher(self):
        """Afficher les informations d'une cylindricité"""
        print "Type:%s\nName:%s"%(self.__type, self._nom)
        print "Coordonnées: (%s,%s,%s)"%(self.__coordonnee[0],self.__coordonnee[1],self.__coordonnee[2])
        print "Distance : %s\nÉcart Type : %s" % (self.__Diametre, self.__EcartType)
    
    def getDiametre(self):
        return self.__Diametre
    def getEcartType(self):
        return self.__EcartType
    def getCoordonnee(self):
        return self.__coordonnee
        
    #def WriteExcel(self,excel_file):  