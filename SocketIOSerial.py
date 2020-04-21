import sys
import time
import serial
import subprocess
import socketio
import threading

sio = socketio.Client()

class SerialD():
     def __init__(self):
        self.dataSerial=None
        self.sensors=["","","",""]
        self._serial_acm0 = serial.Serial()
        self._serial_acm0.baudrate = 115200
        self._serial_acm0.port = '/dev/ttyACM0'
        self._loop = threading.Thread(target=self.update, args=())
        self._stopUpdate = False

     def start(self):
        # try:
        #     self._serial_acm0.open()
        # except:
        #     print("[Error] could not open port acm0")
        #     sio.disconnect()
        #     exit()
        self._stopUpdate = True
        self._loop.start()

     def stop(self):
        self._stopUpdate = False
        #self._serial_acm0.close()

     def update(self):
        while (self._stopUpdate):
            #self._serial_acm0.flush() #espera a  exista un dato
            #dataSerial=self._serial_acm0.readline()
            #self.sensors=dataSerial.decode('cp1250').replace('\r\n','').split(',', 4)
            print('sensores')
            self.sensors = ["4","3","2","1"]
        print('End Thread')

     def sendSerial(self,key):
         self._serial_acm0.write(key.encode('cp1250'))#codifica y envia

serial=SerialD()

def sendSocket():
    print('sendSocket')
    sio.emit('message',{'to': 'controller','type':'sensors','message':serial.sensors})

@sio.event
def connect():
    print('connected to server')

@sio.on('connected')
def on_message(data):
    print('Server says: {}'.format(data))

@sio.on('message')
def message(data):
    if(data['type']=='keys'):
        serial.sendSerial(str(message))  
    elif(data['type']=='arm'):
        serial.sendSerial(str(message))  
    elif(data['type']=='connect'):
        print('User controller Connect')
        serial.start()
        #loop.stop
    else:
        serial.stop()
        #loop.stop()
        print('User controller Disconnect')

@sio.event()
def disconnect():
    print('Disconned Websocket')
    serial.stop()
    #loop.stop()

if __name__ == '__main__':
    sio.connect('http://192.168.0.4:8000?user=botControl')
    sio.wait()
