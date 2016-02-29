import time
import sys
import json
import ServoControl as SC
import SocketServer as sws

#init motors
pwm = SC.initPWM()
servo0 = SC.Servo(pwm, 0, 200)
servo1 = SC.Servo(pwm, 1, 90)
servo2 = SC.Servo(pwm, 2, 200)
servo2.setDegree(90)
servo0.setDegree(1)
servo1.setDegree(10)


class MyTCPHandler(sws.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    enabled = True
    
    def handle(self):
        if self.enabled:
        # self.request is the TCP socket connected to the client
            self.data = self.request.recv(1024).strip()
            print "{} wrote:".format(self.client_address[0])
            print self.data

            data = json.loads(self.data)
            
            self.request.sendall(self.data.upper())

            servo2.setDegree(int(data['x']))
            servo0.setDegree(int(data['z']))
            servo1.setDegree(int(data['y']))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8888

    # Create the server, binding to localhost on port 9999
    server = sws.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    try: 
        server.serve_forever()

    except KeyboardInterrupt:
        servo2.setDegree(90)
        servo0.setDegree(1)
        servo1.setDegree(10)
        sys.exit()
        
