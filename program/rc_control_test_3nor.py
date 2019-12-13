__author__ = 'zhengwang'
import RPi.GPIO as GPIO
from time import *
import pygame
from pygame.locals import *
 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
 
right_pin = 23
left_pin = 24
forward_pin = 18
reverse_pin = 25
time = 50
 
class RCTest(object):
 
    def __init__(self):
        pygame.init()
        pygame.display.set_mode((250, 250))
        GPIO.setup(right_pin,GPIO.OUT)
        GPIO.setup(left_pin,GPIO.OUT)
        GPIO.setup(forward_pin,GPIO.OUT)
        GPIO.setup(reverse_pin,GPIO.OUT)
        # self.ser = serial.Serial("/dev/tty.usbmodem1421", 115200, timeout=1)    # mac
        # self.ser = serial.Serial("/dev/ttyACM0", 115200, timeout=1)           # linux
        self.send_inst = True
        self.steer()
 
    def steer(self):
 
        while self.send_inst:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    key_input = pygame.key.get_pressed()
 
                    # complex orders
                    if key_input[pygame.K_UP] and key_input[pygame.K_RIGHT]:
                        print("Forward Right")
                        GPIO.output(forward_pin,False)
                        GPIO.output(right_pin,False)
                        sleep(0.05)
                        #self.ser.write(chr(6).encode())
 
                    elif key_input[pygame.K_UP] and key_input[pygame.K_LEFT]:
                        print("Forward Left")
                        GPIO.output(forward_pin,False)
                        GPIO.output(left_pin,False)
                        sleep(0.05)
                        #self.ser.write(chr(7).encode())
 
                    elif key_input[pygame.K_DOWN] and key_input[pygame.K_RIGHT]:
                        print("Reverse Right")
                        GPIO.output(reverse_pin,False)
                        GPIO.output(right_pin,False)
                        sleep(0.05)
                        #self.ser.write(chr(8).encode())
 
                    elif key_input[pygame.K_DOWN] and key_input[pygame.K_LEFT]:
                        print("Reverse Left")
                        GPIO.output(reverse_pin,False)
                        GPIO.output(left_pin,False)
                        sleep(0.05)
                        #self.ser.write(chr(9).encode())
 
                    # simple orders
                    elif key_input[pygame.K_UP]:
                        print("Forward")
                        GPIO.output(forward_pin,False)
                        sleep(0.05)
                        #self.ser.write(chr(1).encode())
 
                    elif key_input[pygame.K_DOWN]:
                        print("Reverse")
                        GPIO.output(reverse_pin,False)
                        sleep(0.05)
                        #self.ser.write(chr(2).encode())
 
                    elif key_input[pygame.K_RIGHT]:
                        print("Right")
                        GPIO.output(right_pin,False)
                        sleep(0.05)
                        #self.ser.write(chr(3).encode())
 
                    elif key_input[pygame.K_LEFT]:
                        print("Left")
                        GPIO.output(left_pin,False)
                        sleep(0.05)
                        #self.ser.write(chr(4).encode())
 
                    # exit
                    elif key_input[pygame.K_x] or key_input[pygame.K_q]:
                        print("Exit")
                        self.send_inst = False
                        GPIO.output(forward_pin,True)
                        GPIO.output(reverse_pin,True)
                        GPIO.output(right_pin,True)
                        GPIO.output(left_pin,True)
                        GPIO.cleanup()
                        #self.ser.write(chr(0).encode())
                        #self.ser.close()
                        break
 
                elif event.type == pygame.KEYUP:
                    GPIO.output(forward_pin,True)
                    GPIO.output(reverse_pin,True)
                    GPIO.output(right_pin,True)
                    GPIO.output(left_pin,True)
                    #self.ser.write(chr(0).encode())
 
 
if __name__ == '__main__':
    RCTest()