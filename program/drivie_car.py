import io
import socket
import serial
import struct
import time
import cv2
import numpy as np
from keras.models import load_model

import picamera
from picamera import PiCamera


def predict_driving(img, model):
    """
    Predict key presses for driving (Left/Forward/Right)
    :param img: The image from the Pi camera, model: The pre trained driving model
    :return: Driving command
    """
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Grayscale 
    img = cv2.resize(img, (320,160))  # Resize to fit model input size
    img = np.expand_dims(img, axis=0)  # Expand axis to fit model input size
    img = np.expand_dims(img, axis=3)  # Expand axis to fit model input size
    pred = model.predict(img)
    pred = np.where(pred==np.max(pred))[1][0]  # Extract prediction with highest probability
    
    if pred == 0:
        command = "2"
        print('Prediction: W')
    elif pred == 1:
        command = "9"
        print('Prediction: Q')
    elif pred == 2:
        command = "8"
        print('Prediction: E')

    return command


def stream_normal(model, connection):
    """
    Stream images (640x320) to PC for stop sign detection
    Predict key presses for driving (Left/Forward/Right) and send signal to arduino
    :param model: The pre trained driving model
    connection: Image stream to PC
    """
    # initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera()
    camera.resolution = (640, 320)
    camera.framerate = 25
    # Set some camera parameters to avoid different image qualities
    camera.iso = 800  # Set ISO to the desired value
    time.sleep(2)  # Wait for the automatic gain control to settle
    camera.shutter_speed = camera.exposure_speed
    camera.exposure_mode = 'off'
    g = camera.awb_gains
    camera.awb_mode = 'off'
    camera.awb_gains = g
            
    time.sleep(0.1)  # allow the camera to warmup

    print('Driving...')
    print('Press Ctrl-C to end')

    try:    
        stream = io.BytesIO()  # Image stream to PC
        
        # Send jpeg format video stream
        for frame in camera.capture_continuous(stream, format='jpeg', use_video_port = True):
            print('Stream 1')
            # PC stream
            connection.write(struct.pack('<L', stream.tell()))
            connection.flush()
            stream.seek(0)
            connection.write(stream.read())  
        
            # Grab image from camera for driving prediction on Pi
            data = np.frombuffer(stream.getvalue(), dtype=np.uint8)
            # "Decode" the image from the array, preserving colour
            img = cv2.imdecode(data, 1)
            cv2.imwrite('driving_frames_pi/'+str(time.time())+'.jpg', img)  # Save timnestamped images 

            command = predict_driving(img, model)
            connection.send(int(command))
    
            stream.seek(0)
            stream.truncate()
    
    except (KeyboardInterrupt, picamera.exc.PiCameraValueError): 
        print('Stopped')
        camera.close()
        connection.close()
        client_socket.close()
        client_socket_2.close()
        pass

if __name__ == "__main__":
    # Load trained self-driving model from disc (within Pi)
    model = load_model('driving_model_grey.h5')
    
    # Image stream to PC
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('Jannis', 8000))
    connection = client_socket.makefile('wb')
    
    # Start streaming/driving
    stream_normal(model, connection)