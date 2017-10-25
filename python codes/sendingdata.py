from time import sleep
import cv2
import numpy as np
import pickle
import struct
import socket


face_cascade = cv2.CascadeClassifier(r"C:\Users\Natesh\Documents\frontalface_default.xml");
walker_data = cv2.CascadeClassifier(r"C:\users\Natesh\Documents\pedestrian.xml")
car_data = cv2.CascadeClassifier(r"C:\users\Natesh\Documents\cars.xml")
# bike_data = cv2.CascadeClassifier(r"C:\users\Natesh\Documents\motorbike.xml")
# cycle_data =  cv2.CascadeClassifier(r"C:\users\Natesh\Documents\bicycle.xml")


cap = cv2.VideoCapture(r"C:\Users\Natesh\Desktop\INTEL\cars1.avi")

s = socket.socket() ;
s.connect(("192.168.0.100", 9876))
print("\nConnected to server.\n") ;


while(1):
	try:
		ret , frame = cap.read() ;
		if not ret:
			break;
		data = pickle.dumps(frame , protocol=2)
		print(len(data)) ;
		s.sendall(struct.pack("L" , len(data))+data) ;
		sleep(0.3) ;
	except(KeyboardInterrupt):
		print("INTERRUPTED BY USER ! ") ;
		s.close()
		break;
		
	# if( input("\n\nPress exit to quit : ")=='exit' ):
