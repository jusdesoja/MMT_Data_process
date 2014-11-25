import serial

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

#print "Found ports:"
#for n,s in portscan(): 
#	print "(%d) %s"% (n,s)

print portscan()