import cv2
from time import sleep
import numpy as np
import os ; 
from imutils.object_detection import non_max_suppression
from imutils import paths


ped_cascade = cv2.CascadeClassifier(os.path.join(os.path.dirname(__file__) , 'testdata' , "frontalped_default.xml")) ; 
walker_data = cv2.CascadeClassifier(os.path.join(os.path.dirname(__file__) , 'testdata' , "pedestrian.xml")) ; 
car_data = cv2.CascadeClassifier(os.path.join(os.path.dirname(__file__) , 'testdata' ,  "cars.xml")) ; 


cap = cv2.VideoCapture(os.path.join(os.path.dirname(__file__) ,'testvideos' , "cars1.avi")) ; 

array = []

while(1):
    frame = cap.read()[1] ;

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