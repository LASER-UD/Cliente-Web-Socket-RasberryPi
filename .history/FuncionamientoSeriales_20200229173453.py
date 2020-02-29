import time
import serial
ser_acm0 = serial.Serial('/dev/ttyACM0',115200)    # enable the serial port
ser_acm1 = serial.Serial('/dev/ttyACM1',115200)    # enable the serial port
data ="" 

while 1:    
	time.sleep(1)                                              
	ser_acm0.flush() #espera a que exista un dato
    data=ser_acm0.readline()
    print (int(data.decode('cp1250').replace('\r\n','')))
    ser_acm1.flush()
    data=ser_acm1.readline()
    print (int(data.decode('cp1250').replace('\r\n','')))
	