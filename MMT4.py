# -*- coding: utf-8 -*-
import Tkinter
import serial
import tkFileDialog
from BlocWrite import *
import threading
from findport import portscan
snifflag = 1
flaglock = threading.Lock()
excel = easyExcel(r"C:\Users\y.zhang\Documents\python\test.xls")
class SnifferThread(threading.Thread):
	
	def __init__(self, threadID, name, filename = "data",portname = "COM3"):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.filename = filename
		self.portname = portname
		self.snifflag = 1

        
	def run(self):
		global flaglock
		global snifflag
		global excel
		database = open(self.filename,'w')
		ser = serial.Serial(self.portname, baudrate = 9600, timeout = 0.2)
		n = 0
		print "Sniffing on: "+self.portname
		
		try:
			
			while snifflag:
				data = []
				flag = 1
				while flag:
					if snifflag is 0:
						break
					ch = ser.read(1)
					if len(ch) == 0:
						
						if len(data) > 0:
							
							s = ''
    
							for x in data:
								s += x
							
							print "%s  [len = %d]" % (s,len(data))
							#self.PrintString(s)
							string = s + " [len = " + str(len(data)) + "]"
							
							database.write(string)
							database.write("\n")
							bloque,line = preleveMesure(string)
							WriteExcel(bloque,self.excel,n)
							n += 1
							flag = 0
						data = []
						
					else:
						data.append(ch)
				if snifflag is 0:
					break
				#sleep(3)  #Attendre le changement de snifflag, j'avoue que c'est une façon bêtise... vous pourriez arriver aux autres solutions
		finally:
			database.close()
			
			print "thread end"	
		
	def stop(self):
		self.thread_stop = True
		
		
class MMTinterface(Tkinter.Tk):
	PortNameList = portscan()#######
	
	def __init__(self,parent):
		Tkinter.Tk.__init__(self,parent)
		self.parent = parent
		self.initialize()
		self.buttonflag = 0
		#self.Portname = "COM3"## variable instante, il sera remplacé par le portscan
	def initialize(self):
		self.grid()
        
		self.entryVariable = Tkinter.StringVar()
		self.entry = Tkinter.Entry(self,textvariable = self.entryVariable)
		self.entry.grid(column = 0, row = 0, columnspan = 2,sticky = 'EW')
		self.entry.bind("<Return>", self.OnPressEnter)
		self.entryVariable.set(u"Enter the file name you want to save")
        
		self.portList = Tkinter.Listbox(self,width = 10,height = 3)
		
		# le port name est le premiere element de tout les ports occupé par défaut
		self.Portname = self.PortNameList[0]
		
		listlen = len(self.PortNameList)
		for k in range(listlen):
			self.portList.insert(Tkinter.END, self.PortNameList[k])
		if listlen == 0:
			self.portList.insert(Tkinter.END,"No port avaible")
		self.portList.bind('<<ListboxSelect>>',self.ListSelect)
		self.portList.grid(column = 1, row = 0, sticky = 'EW')
		
		self.buttonChoose = Tkinter.Button(self, text = u"Choose dir",command = self.ChooseClick)
		self.buttonChoose.grid(column = 0,row = 2,sticky = 'EW' )
        
		self.buttonStart  = Tkinter.Button(self,text = u"Start sniffing",command = self.StartClick, state = Tkinter.DISABLED)
		self.buttonStart.grid(column = 0,row = 1, sticky = 'EW' )
        
		self.buttonStop = Tkinter.Button(self, text = u"Stop  sniffing", command = self.StopClick, state = Tkinter.DISABLED)
		self.buttonStop.grid(column = 1,row = 1, sticky = 'EW')
        
		self.buttonExcel = Tkinter.Button(self, text = u"Generate", command = self.GenererClick,state = Tkinter.DISABLED)
		self.buttonExcel.grid(column = 0, row = 3, sticky = 'EW')
        
		self.buttonHelp = Tkinter.Button(self, text = u"Help", command = self.HelpClick)
		self.buttonHelp.grid(column = 0,row = 4,columnspan = 2, sticky = "EW")
        
		self.labelVariable = Tkinter.StringVar()
		self.label = Tkinter.Label(self,textvariable = self.labelVariable,anchor = "w", fg = "black", bg ="grey",height = 4)
		self.label.grid(column = 0,row = 5,columnspan = 2,rowspan = 6,sticky = 'EW')
		self.labelVariable.set(u"Press the help button and \nread the using directions first!\n v:alpha1.0 \nCopywrite: Yiru ZHANG")
        
		self.grid_columnconfigure(0,weight = 1)
		self.resizable(True,True)
		self.update()
		self.geometry(self.geometry())
		self.entry.focus_set()
		self.entry.selection_range(0,Tkinter.END)
    
	def ListSelect(self,evt):
		w = evt.widget
		self.Portname = w.get(int(w.curselection()[0])) 
		#print self.Portname
	
	def ChooseClick(self):
		self.entry.delete(0,Tkinter.END)
		self.filepath = tkFileDialog.askdirectory(title='Please select a directory')+"/data" 
		if self.filepath:
			self.entry.insert(0,self.filepath) 
		
		self.buttonStart.config(state = Tkinter.NORMAL)
		self.buttonflag = 1

	def StartClick(self):
		global snifflag
		global flaglock
		flaglock.acquire()
		snifflag = 1
		flaglock.release()
		self.sniff = SnifferThread(1,"thread_sniffer",self.filepath,self.Portname) #set the sniff class
		self.sniff.isDaemon()
		self.sniff.setDaemon(True)
		self.sniff.start()
		self.labelVariable.set("Surveiller le port serie"+self.Portname)
		self.entry.focus_set()
		self.entry.selection_range(0, Tkinter.END)
		
		self.buttonStop.config(state=Tkinter.NORMAL)
		self.buttonStart.config(state=Tkinter.DISABLED)
		self.buttonflag = 2
		
        #in this fonctoin , we should start a new thread for port sniffing
        
	def StopClick(self):
		global snifflag
		global flaglock
		global excel
        #self.labelVariable.set(self.entryVariable.get() + "you clicked the stop!")
		flaglock.acquire()
		snifflag = 0
		flaglock.release()
		
		self.buttonStop.config(state=Tkinter.DISABLED)
		self.buttonStart.config(state=Tkinter.NORMAL)
		self.buttonExcel.config(state = Tkinter.NORMAL)
		self.entry.focus_set()
		self.entry.selection_range(0, Tkinter.END)
		self.sniff.stop()
		
		excel.save()
		excel.close()
		
	def GenererClick(self):
		self.ExcelName = self.entryVariable.get() + "result.xls"
		self.MesureData = MesureResult(self.filepath)
		self.MesureData.WriteExcel(self.ExcelName)
		self.labelVariable.set("Generating " + self.ExcelName)
		self.entry.focus_set()
		self.entry.selection_range(0, Tkinter.END)
		
		
        
	def HelpClick(self):
		self.labelVariable.set(self.entryVariable.get() + "you clicked the Help")
		self.entry.focus_set()
		self.entry.selection_range(0, Tkinter.END)
        
            
	def OnPressEnter(self,event):
		self.ExcelName = self.entryVariable.get() + ".xls"
		self.labelVariable.set("Excel file name is: " + self.ExcelName)
		self.entry.focus_set()
		self.entry.selection_range(0, Tkinter.END)
      
try:
	if __name__ == "__main__":
		app = MMTinterface(None)
		app.title('Gestion de MMT Donnée')
        
		app.mainloop()
except Exception,e:
    print "exception is "
    print  e
        
finally:
    pass