
from twisted.internet.protocol import ReconnectingClientFactory
from autobahn.twisted.websocket import WebSocketClientProtocol, WebSocketClientFactory
import json
import base64
import subprocess
from twisted.internet.task import LoopingCall
from twisted.internet import reactor

server = "ritaportal.udistrital.edu.co"  # Server IP Address or domain eg: tabvn.com
port = 10207  # Server Port
 

class AppProtocol(WebSocketClientProtocol):
    INTERVAL=1        
    def onConnect(self, response):
        self._loop = LoopingCall(self.envioImage)
        print("server conectado")

    def onConnecting(self, transport_details):
        return None  # ask for defaults

    def onMessage(self, payload, isBinary):
        text_data_json = json.loads(payload.decode('utf8'))
        
        if(text_data_json['type']=='MC'):
                print("MC")
                self._loop.start(self.INTERVAL)
        elif(text_data_json['type']=='MD'):
                print("MD")
                if _loop.running:
                    _loop.stop()
        else:
            print("No entiendo")

    async def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))
        
    def Send(self):
            print("Sending")
            self.sendMessage(json.dumps({'userFrom':'2','userTo': '1','type':'data','message':'hello'}).encode('utf8'))

        
        
class AppFactory(WebSocketClientFactory, ReconnectingClientFactory):
    protocol = AppProtocol

    def clientConnectionFailed(self, connector, reason):
        print("Unable connect to the server {0}".format(reason))
        self.retry(connector)

    def clientConnectionLost(self, connector, reason):
        print("Lost connection and retrying... {0}".format(reason))
        self.retry(connector)




if __name__ == '__main__':
    import sys
    from twisted.python import log
    from twisted.internet import reactor
    log.startLogging(sys.stdout)
    factory = AppFactory(u"ws://ritaportal.udistrital.edu.co:10207/jordan")
    reactor.connectTCP(server, port, factory)
    reactor.run()
