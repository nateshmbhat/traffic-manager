import cv2
from time import sleep
import numpy as np
from imutils.object_detection import non_max_suppression
from imutils import paths


ped_cascade = cv2.CascadeClassifier(r"C:\Users\Natesh\Documents\frontalped_default.xml");
walker_data = cv2.CascadeClassifier(r"C:\users\Natesh\Documents\pedestrian.xml")
car_data = cv2.CascadeClassifier(r"C:\users\Natesh\Documents\cars.xml")
# bike_data = cv2.CascadeClassifier(r"C:\users\Natesh\Documents\motorbike.xml")
# cycle_data =  cv2.CascadeClassifier(r"C:\users\Natesh\Documents\bicycle.xml")


cap = cv2.VideoCapture(r"C:\Users\Natesh\Desktop\INTEL\cars1.avi")



array = []


while(1):
    frame = cap.read()[1] ;


    	# ped DETECTION
    # frame = cv2.imread(r"C:\Users\Natesh\Documents\pedestrians.jpg")
    # frame = cap.read()[1]
    # frame = cap.read()[1] ;
    # ped = ped_cascade.detectMultiScale(cv2.cvtColor( frame, cv2.COLOR_BGR2GRAY) , 1.3 , 5) ;
    #
    # array.append(len(ped)) ;
    #
    # if(len(array)==50):
    # 	freq  =[]
    # 	for i in array:
    # 		freq.append(array.count(i)) ;
    #
    # 	maxfreqindex = freq.index(max(freq))
    # 	print("peds detected : ",array[maxfreqindex]) ;
    # 	array.clear();
    #
    #
    #
    #
    # for(x,y,j,k) in ped:
    #     cv2.rectangle(frame , (x, y) , (x+j , y+k) , (0,255 , 0) , 2) ;
    #




#PEDESTRIAN DETECTION
   

    ped = walker_data.detectMultiScale(cv2.cvtColor( frame, cv2.COLOR_BGR2GRAY) , 3, 5) ;

    array.append(len(ped)) ;

    if(len(array)==50):
      freq  =[]
      for i in array:
          freq.append(array.count(i)) ;

      # print("array = {}\nFreq = {}\n\n\n" , array , freq) ;
      maxfreqindex = freq.index(max(freq))
      print("pedestrians detected : " , array[maxfreqindex]) ;
      array.clear();

    for(x,y,j,k) in ped:
        cv2.rectangle(frame , (x, y) , (x+j , y+k) , (0,255 , 0) , 2) ;


    # cv2.imshow("Security Feed", frame)
    # if cv2.waitKey(1)==ord('q'):break;






     #CARS DETECTION

    cars = car_data.detectMultiScale(cv2.cvtColor( frame, cv2.COLOR_BGR2GRAY) , 1.1, 1) ;


    print("Vehicles detected : " ,len(cars))

    for(x,y,j,k) in cars:
        cv2.rectangle(frame , (x, y) , (x+j , y+k) , (0,255, 0) , 1) ;



    cv2.imshow("Security Feed", frame)
    if cv2.waitKey(1)==ord('q'):break;

        
    sleep(0.1) ;



cv2.destroyAllWindows() ;
cap.release() ;