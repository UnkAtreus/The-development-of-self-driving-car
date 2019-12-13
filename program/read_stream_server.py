import numpy as np
import cv2
import socket
import struct
import serial
import io
import time

class ReadStream(object):

    def __init__(self):
        self.ser = serial.Serial("COM3", 115200, timeout=1)
        self.send_inst = True
        # Image stream from Pi
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', 8000))
        server_socket.listen(0)
        # accept a single connection
        connection = server_socket.accept()[0].makefile('rb')
        run(connection)

    def run(conncetion):

        print('Start collecting images...')

        # stream video frames one by one
        try:
            while True:
                    
                # Read the length of the image as a 32-bit unsigned int. If the
                # length is zero, quit the loop
                image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
                if not image_len:
                    break
                # Construct a stream to hold the image data and read the image
                # data from the connection
                image_stream = io.BytesIO()
                image_stream.write(connection.read(image_len))
                image_stream.seek(0)
                data = np.frombuffer(image_stream.getvalue(), dtype=np.uint8)
                # "Decode" the image from the array, preserving colour
                img = cv2.imdecode(data, 1)   
                #cv2.imwrite('driving_frames_pc/'+str(time.time())+'.jpg', img)  # Save image
                        
                img = cv2.resize(img, (640,320))
                #conn.recv(1024)
                command_msg = conn.recv(1024)
                self.ser.write(chr(int(command_msg)).encode())
        
        finally:
            connection.close()
            server_socket.close()

if __name__ == "__main__":
    ReadStream()
