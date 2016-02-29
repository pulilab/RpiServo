import time
import sys
import json
import ServoControl as SC
import SimpleWebSocketServer as sws

#init motors
pwm = SC.initPWM()
servo0 = SC.Servo(pwm, 0, 200)
servo1 = SC.Servo(pwm, 1, 90)
servo2 = SC.Servo(pwm, 2, 200)
servo2.setDegree(90)
servo0.setDegree(1)
servo1.setDegree(10)

class SimpleEcho(sws.WebSocket):
    enabled = True

    def handleMessage(self):
        if self.enabled:
            #self.enabled = False
            # echo message back to client
            self.sendMessage(self.data)
        
            print(self.data)

            data = json.loads(self.data)

            print(self.data)

            servo2.setDegree(int(data['x']))
            servo0.setDegree(int(data['z']))
            servo1.setDegree(int(data['y']))
            #last = time.time()
            
        #elif last+1 <= time.time():
        #    self.sendMessage(self.data)
        #    self.enabled = True


    def handleConnected(self):
        print self.address, 'connected'

    def handleClose(self):
        print self.address, 'closed'

server = sws.SimpleWebSocketServer('', 8000, SimpleEcho)
try:
    server.serveforever()
except KeyboardInterrupt:
    servo2.setDegree(90)
    servo0.setDegree(1)
    servo1.setDegree(10)
    sys.exit()

