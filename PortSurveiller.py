import serial


#filename = raw_input("Creer un fichier pour stock les donnees:\n")
#Database = open("data.txt", 'w')
#port = raw_input("Le nom du port est:\n")
#port = "/dev/tty.usbmodem1421"
#Ser = serial.Serial(port, baudrate = 9600, timeout = 0.2)
#print "Surveiller le port serie" + Ser.name

def portscan():
	available = []
	for i in range(256):
		try:
			s = serial.Serial(i)
			available.append(s.portstr)
			s.close()
		except serial.SerialException:
			pass
	return available
	
	
class PortSurveiller():
    
    def __init__(self,filename,portname):
        self.__Database = open(filename, 'w')
        self.__Ser = serial.Serial(portname, baudrate = 9600, timeout = 0.2)
        self.__SniFlag = 1
    def Surveiller(self,database,ser):
        data = []
        flag = 1
        while flag:
            ch = ser.read(1)
            
            if len(ch) == 0:
                if len(data) > 0:
                    s = ''
    
                    for x in data:
    
                        s += x
    
                    print "%s [len = %d]" % (s,len(data))
                    self.PrintString(s)
                    string = s + " [len = " + str(len(data)) + "]"
                    database.write(string)
                    database.write("\n")
                    flag = 0
                data = []
            else:
                data.append(ch)
                #ser.write('\\xff')
    
    
    def PrintString(self,string):
        return string
    
    
    
    def ChangeFlag(self,flag):
        self.__SniFlag = flag
    
    def PortSniffer(self):
        
        #print "Surveiller le port serie" + self.__Ser.name
        print "Surveiller le port serie" + self.__Ser.name
        #self.PrintString(PortAff)
        try:
            while self.__SniFlag:
                self.Surveiller(self.__Database,self.__Ser)
            self.__Database.close()
        finally:       
            self.__Database.close()
			

			
#a = PortSurveiller("data","COM3")
#a.PortSniffer()