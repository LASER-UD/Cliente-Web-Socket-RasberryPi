import os
import subprocess
import time
import base64
import cv2
import subprocess
import socketio
import threading

sio = socketio.Client()

class VideoCamera(object):
    def __init__(self):
        self._encode_param = [int(cv2.IMWRITE_WEBP_QUALITY), 70]
        #self._encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 70]

        try:
            self.video = cv2.VideoCapture(0)
        except cv2.error:
            self.video = cv2.VideoCapture(1)
        (self.grabbed, self.frame) = self.video.read()
        self._loop = threading.Thread(target=self.update, args=())
        self._stopUpdate = False

    def start(self):
        self._stopUpdate=True
        self._loop.start()
        
    def stop(self):
        self.video.release()
        self._stopUpdate=False

    def get_frame(self):
        image=cv2.resize(self.frame,(320,180),4)
        ret, buffer = cv2.imencode('.webp', image, self._encode_param)
        #ret, buffer = cv2.imencode('.jpg', image, self._encode_param)
        out = base64.b64encode(buffer.tobytes()).decode('ascii')
        return out
            
    def update(self):
        while self._stopUpdate:
            (self.grabbed, self.frame) = self.video.read()
            time.sleep(0.03)
        print('Stopped Loop')

class SendWebsocket():
    def __init__(self):
        self._loop = threading.Thread(target=self.update, args=())
        self._stopUpdate = False
        self.camera = VideoCamera()
    def startSend(self):
        self.camera.start()
        self._stopUpdate = True
        self._loop.start()
    def stopSend(self):
        self.camera.stop()
        self._stopUpdate = False
        subprocess.call('sudo kill -9 {}'.format(os.getpid()),shell=True)

    def update(self):
        while (self._stopUpdate):
            sio.emit('message',{'to': 'controller','type':'image','message':self.camera.get_frame()})
            time.sleep(0.03)
        print('Thread Send Stopped')

sendWebsocket=SendWebsocket()


@sio.event
def connect():
    print('connected to server')

@sio.on('connected')
def on_message(data):
    print('User controller Connect')
    sendWebsocket.startSend()

@sio.on('message')
def message(data):
    sendWebsocket.stopSend()
    print('User controller Disconnect')

@sio.event()
def disconnect():
    print('Disconned Websocket')
    sendWebsocket.stopSend()

if __name__ == '__main__':
    sio.connect('ws://192.168.0.4:8000?user=botVideo')
    #sio.connect('ws://ritaportal.udistrital.edu.co:10207/?user=botVideo')
    sio.wait()
