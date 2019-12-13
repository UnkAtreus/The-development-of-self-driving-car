import serial
import pygame
from pygame.locals import *
import time

class Controller:
    def __init__(self):
        pygame.init()
        pygame.display.set_mode((250, 250))
        self.ser = serial.Serial("COM3", 115200, timeout=1)
        self.send_inst = True
        self.pressed = {}
        self.prevPressed = {}
        self.time = []
        self.press_release = []
        self.steer()

    def steer(self):
    
        while self.send_inst:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    key_input = pygame.key.get_pressed()

                    # complex orders
                    if key_input[pygame.K_e]:
                        print("Forward Right")
                        self.ser.write(chr(8).encode())
                        self.press_release.append('e_press')
                        self.time.append(time.time())

                    elif key_input[pygame.K_q]:
                        print("Forward Left")
                        self.ser.write(chr(9).encode())
                        self.press_release.append('q_press')
                        self.time.append(time.time())

                    # simple orders
                    elif key_input[pygame.K_s]:
                        print("Reverse")
                        self.ser.write(chr(1).encode())
                        self.press_release.append('s_press')
                        self.time.append(time.time())

                    elif key_input[pygame.K_w]:
                        print("Forward")
                        self.ser.write(chr(2).encode())
                        self.press_release.append('w_press')
                        self.time.append(time.time())

                    elif key_input[pygame.K_d]:
                        print("Right")
                        self.ser.write(chr(3).encode())
                        self.press_release.append('d_press')
                        self.time.append(time.time())

                    elif key_input[pygame.K_a]:
                        print("Left")
                        self.ser.write(chr(4).encode())
                        self.press_release.append('a_press')
                        self.time.append(time.time())

                    # exit
                    elif key_input[pygame.K_x]:
                        print("Exit")
                        self.send_inst = False
                        self.ser.write(chr(0).encode())
                        self.closing()
                        break

                elif event.type == pygame.KEYUP:
                    self.ser.write(chr(0).encode())

                    if key_input[pygame.K_e]:
                        self.press_release.append('e_release')
                        self.time.append(time.time())
                        print("Forward Right released")

                    elif key_input[pygame.K_q]:
                        self.press_release.append('q_release')
                        self.time.append(time.time())
                        print("Forward Left released")

                    elif key_input[pygame.K_s]:
                        self.press_release.append('s_release')
                        self.time.append(time.time())
                        print("Reverse released")

                    elif key_input[pygame.K_w]:
                        self.press_release.append('w_release')
                        self.time.append(time.time())
                        print("Forward released")

                    elif key_input[pygame.K_d]:
                        self.press_release.append('d_release')
                        self.time.append(time.time())
                        print("Right released")

                    elif key_input[pygame.K_a]:
                        self.press_release.append('a_release')
                        self.time.append(time.time())
                        print("Left released")
    
        
    def closing(self):
            with open('time_press_release/time_p_r.txt', 'w') as time_file:  
                for time_stamp in self.time:
                    time_file.write('%s\n' % time_stamp)           
            with open('time_press_release/press_release.txt', 'w') as press_release_file:  
                for key in self.press_release:
                    press_release_file.write('%s\n' % key)
            self.ser.close()


if __name__ == "__main__":
    Controller()