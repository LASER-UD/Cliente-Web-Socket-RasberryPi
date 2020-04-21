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
        self._startUpdate = False

     def start(self):
        self._startUpdate = True
        self._loop.start()

     def stop(self):
        self._startUpdate = False

     def update(self):
        while (self._startUpdate):
            print('sensores')
            self.sensors = ["4","3","2","1"]
            time.sleep(0.9)
        print('Thread Serial Stopped')

     def sendSerial(self,key):
         self._serial_acm0.write(key.encode('cp1250'))#codifica y envia



class SendWebsocket():
    def __init__(self):
        self._loop = threading.Thread(target=self.update, args=())
        self._startUpdate = False
    def startSend(self):
        self._startUpdate = True
        self._loop.start()
    def stopSend(self):
        self._startUpdate = False
    def update(self):
        while (self._startUpdate):
            print('sendSocket')
            sio.emit('message',{'to': 'controller','type':'sensors','message':serial.sensors})
            time.sleep(0.9)
        print('Thread Send Stopped')

serial=SerialD()
sendWebsocket=SendWebsocket()

@sio.event
def connect():
    print('connected to server')

@sio.on('connected')
def on_message(data):
    print('User controller Connect')
    serial.start()
    sendWebsocket.startSend()

@sio.on('message')
def message(data):
    print(data)
    if(data['type']=='keys'):
        serial.sendSerial(str(message))  
    elif(data['type']=='arm'):
        serial.sendSerial(str(message))  
    else:
        serial.stop()
        sendWebsocket.stopSend()
        print('User controller Disconnect')

@sio.event()
def disconnect():
    print('Disconned Websocket')
    serial.stop()

if __name__ == '__main__':
    sio.connect('ws://192.168.0.4:8000?user=botControl')
    #sio.connect('ws://ritaportal.udistrital.edu.co:10207/')
    sio.wait()
