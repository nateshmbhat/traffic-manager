from time import sleep
import numpy as np
import pickle
import struct
import socket
import cv2

face_cascade = cv2.CascadeClassifier(os.path.join(os.path.dirname(__file__) , 'testdata' , "frontalface_default.xml")) ; 
walker_data = cv2.CascadeClassifier(os.path.join(os.path.dirname(__file__) , 'testdata' , "pedestrian.xml")) ; 
car_data = cv2.CascadeClassifier(os.path.join(os.path.dirname(__file__) , 'testdata' ,  "cars.xml")) ; 



cap = cv2.VideoCapture(os.path.join(os.path.dirname(__file__) , 'testvideos' , "cars2.avi")) ; 
# cap = cv2.VideoCapture(0) ;


s = socket.socket() ;
s.connect((input("Enter ip : "), 9876))
print("\nConnected to server.\n") ;


while(1):
	sleep(0.3) ;
	try:
		ret , frame = cap.read() ;
		if not ret:
			break;
		data = pickle.dumps(frame , protocol=2)
		print(len(data)) ;
		s.sendall(struct.pack("L" , len(data))+data) ;
		s.recv(2) ;


	except(KeyboardInterrupt):
		print("INTERRUPTED BY USER ! ") ;
		s.close()
		break;
		
	# if( input("\n\nPress exit to quit : ")=='exit' ):
