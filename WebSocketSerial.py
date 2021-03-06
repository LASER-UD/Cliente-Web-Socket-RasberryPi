from twisted.internet.protocol import ReconnectingClientFactory
from autobahn.twisted.websocket import WebSocketClientProtocol, WebSocketClientFactory
from twisted.internet import reactor, interfaces
from zope.interface import implementer
import json
import base64
import subprocess
from twisted.internet import task
from twisted.internet import reactor
import cv2
import threading
import sys
import time
import serial
import subprocess
from twisted.internet.task import LoopingCall
server = "ritaportal.udistrital.edu.co"  # Server IP Address or domain eg: tabvn.com
port = 10207  # Server Port

class SerialD():
     cuenta=0
     def __init__(self):
          self.datos=None;
          self.ser_acm0 = serial.Serial()
          self.ser_acm0.baudrate = 115200
          self.ser_acm0.port = '/dev/ttyACM0'
          self.sensores=[0,0]
          self.ser_acm1 = serial.Serial()
          self.ser_acm1.baudrate = 115200
          self.ser_acm1.port = '/dev/ttyUSB0'
          
     def start(self):
            try:
                self.ser_acm0.open()
            except:
                print("Error Abriendo acm0")
                exit()
            try:
                self.ser_acm1.open()
            except:
                print("Error Abriendo acm1")
                exit()
            self.hilo=threading.Thread(target=self.update, args=())
            self.hilo.start()
     def end(self):
          self.ser_acm0.close()
          self.ser_acm1.close()
     def update(self):
        while ((self.ser_acm0.isOpen())and(self.ser_acm1.isOpen())):
            self.ser_acm0.flush() #espera a  exista un dato
            datos=self.ser_acm0.readline()
            self.sensores[0]=datos.decode('cp1250').replace('\r\n','')
            self.ser_acm1.flush() #espera a  exista un dato
            datos=self.ser_acm1.readline()
            self.sensores[1]=datos.decode('cp1250').replace('\r\n','')
            time.sleep(0.1)
                          
     def press(self,key):
         #print(key.encode('cp1250'))
         self.ser_acm0.write(key.encode('cp1250'))#codifica y envia
       


class AppProtocol(WebSocketClientProtocol):    
    def onOpen(self):
        self.seri=SerialD()
        print("Abierto")

    def onConnect(self, response):
        print("server conectado")

    def onConnecting(self, transport_details):
        print("Conectando")
        return None  # ask for defaults

    def onMessage(self, payload, isBinary):
        text_data_json = json.loads(payload.decode('utf8'))
        if(text_data_json['type']=='MC'):
                print("MC")
                self.seri.start()
                self._loop = LoopingCall(self.envioSerial)
                self._loop.start(0.1)
               
        elif(text_data_json['type']=='MD'):
                subprocess.call('/usr/bin/pm2 restart 0',shell=True)
                print("MD")
        else:
            message = text_data_json['message']
            print(message)
            self.seri.press(str(message))

    def onClose(self, wasClean, code, reason): 
        print("WebSocket connection closed")
        
    def envioSerial(self):
        self.sendMessage(json.dumps({'userFrom':'2','userTo': '1','type':'sensores','message':self.seri.sensores}).encode('utf8'))
        
        
        
class AppFactory(WebSocketClientFactory, ReconnectingClientFactory):
    protocol = AppProtocol

    def clientConnectionFailed(self, connector, reason):
        print("Unable connect to the server")
        self.retry(connector)
        subprocess.call('/usr/bin/pm2 restart 0',shell=True)

    def clientConnectionLost(self, connector, reason):
        print("Lost connection and retrying...")
        self.retry(connector)
        subprocess.call('/usr/bin/pm2 restart 0',shell=True)


if __name__ == '__main__':
    
    from twisted.python import log
    from twisted.internet import reactor
    log.startLogging(sys.stdout)
    factory = AppFactory(u"ws://ritaportal.udistrital.edu.co:10207/jordan")
    reactor.connectTCP(server, port, factory)
    reactor.run()