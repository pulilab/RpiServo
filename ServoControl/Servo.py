import time
from Adafruit_PWM_Servo_Driver import PWM

def initPWM(freq=60):
    pwm = PWM(0x40)
    pwm.setPWMFreq(freq)
    return pwm

class Servo(object):

    def __init__(self, pwm, channel, degree_range):

        if not isinstance(pwm, PWM):
            raise TypeError('pwm is not instance of PWM')

        self.servoMin = 127.5  # Min pulse length out of 4096
        self.servoMax = 672.5  # Max pulse length out of 4096
        self.channel = channel
        self.pwm = pwm
        self.degree_range = degree_range
        self.current_degree = 0

        
    def setDegree(self, angle, ssec=0.5):

        if angle >= self.degree_range:
            angle = self.degree_range-1

        if angle < 0:
            angle = 0

        self.current_degree = angle

        pulse = self.translateDegreeToPulse(angle+10)

        self.pwm.setPWM(self.channel, 0, int(pulse))

        time.sleep(ssec)

        return self

    def translateDegreeToPulse(self, angle):
        onedegree = (self.servoMax - self.servoMin) / 200.0
        step2 = onedegree*angle
        print(onedegree)
        print(step2 + self.servoMin)
        return step2 + self.servoMin

    def setServoPulse(self, pulse):
        # pulseLength = 1000000                   # 1,000,000 us per second
        # pulseLength /= 60                       # 60 Hz
        # print "%d us per period" % pulseLength
        # pulseLength /= 4096                     # 12 bits of resolution
        # print "%d us per bit" % pulseLength
        # pulse *= 1000
        # pulse /= pulseLength
        self.pwm.setPWM(self.channel, 0, pulse)

    def turn(self, offset):
        self.setDegree(self.current_degree+offset)

    def sreset(self):
        PWM.softwareReset()


class Servo3d(object):
    """Meg lesz irva"""
    def __init__(self, s0, s1, s2):
        if not isinstance(s0, Servo) or not isinstance(s1, Servo) or not isinstance(s2, Servo):
            raise TypeError('servos are not Servo')
        self.s0 = s0
        self.s1 = s1
        self.s2 = s2
        self.s0.setDegree(90)
        self.s1.setDegree(90)
        self.s2.setDegree(90)
        
    def turn3d(self, x, y, z):
        self.s0.turn(x)
        self.s1.turn(y)
        self.s2.turn(z)