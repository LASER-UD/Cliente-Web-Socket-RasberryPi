import time
import serial
flag_acm0=True
flag_acm1=False
try:
	ser_acm0 = serial.Serial('/dev/ttyACM0',baudrate=115200,timeout=1.0)    # enable the serial port
	print("Si pudo ACM0")
	flag_acm0=True
except:
	print("No pudo ACM0")
	flag_acm0=False
try:
	ser_acm1 = serial.Serial('/dev/ttyUSB0',baudrate=115200,timeout=1.0)    # enable the serial port
	print("Si pudo USB0")
	flag_acm1=True
except:
	print("No pudo USB0")
	flag_acm1=False
data ="" 

if((flag_acm1==True) and (flag_acm1)==True):
	while True:
		ser_acm0.flush() #espera a que exista un dato
		data=ser_acm0.readline()
		print ("ACM0 ",data.decode('cp1250').replace('\r\n',''))
		ser_acm1.flush()
		data=ser_acm1.readline()
		print ("ACM1 ",data.decode('cp1250').replace('\r\n',''))
