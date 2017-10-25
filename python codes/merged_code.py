
from time import sleep
import numpy as np
import socket
import pickle
import struct
import threading
import smtplib
import time
import os
import sys
from email.mime.image import MIMEImage;
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas

import cv2

face_cascade = cv2.CascadeClassifier(r"frontalface_default.xml");
walker_data = cv2.CascadeClassifier(r"pedestrian.xml")
car_data = cv2.CascadeClassifier(r"cars.xml")
# bike_data = cv2.CascadeClassifier(r"C:\users\Natesh\Documents\motorbike.xml")
# cycle_data =  cv2.CascadeClassifier(r"C:\users\Natesh\Documents\bicycle.xml")


cap = cv2.VideoCapture(r"cars1.avi")
#cap = cv2.VideoCapture(0) ;

print("\nConnected to server.\n") ;




flag_stop_usual_signal_loop = False;
total_number_red_bypasses = 0;
vehicles_count = [];
global_frame = None;


def take_commands_from_app(sapp):
    app, addr = sapp.accept();

    global total_number_red_bypasses
    global vehicles_count

    print("Data received from Traffic Control system ");

    while (1):
        msg = app.recv(4096).decode();

        print("CLIENT SENT : {}".format(msg));

        if "sendmail" in msg:
            print("Sending mail ...")
            mailsending();




def mailsending(message=None):
    global total_number_red_bypasses ;
    if message is None:
        msg = MIMEMultipart();
        if os.path.isfile("bypass.jpg"):
            img_data = open("bypass.jpg", 'rb').read();
        msg['Subject'] = "Traffic Data updates"
        msg['From'] = "Intel Control Board"
        msg['To'] = "Traffic management"

        text = MIMEText("""
Traffic Report :\n
Date and Time : {}
Average number of vehicles : {}

Number of vehicles which bypasses the signal : {}""".format(time.asctime(), int(
            sum(vehicles_count) / (len(vehicles_count) if len(vehicles_count) else 1)), total_number_red_bypasses))

        msg.attach(text);
        if (os.path.isfile("bypass.jpg")):
            image = MIMEImage(img_data, name="{}".format(time.asctime()));
            msg.attach(image)

        try:
            obj = smtplib.SMTP("smtp.gmail.com", 587);
            obj.starttls();
            obj.login("nateshmbhatofficial@gmail.com", "inteledison123");
            obj.sendmail("nateshmbhat1@gmail.com", ["nateshmbhatofficial@gmail.com", "gangadharashetty.gs@gmail.com"],
                         msg.as_string());
            print("Mail sent successfully ! ");
        except(KeyboardInterrupt):
            print("Program terminated by user ! ");


        except:
            print("Connection Error ! Password is wrong or internet is not connected");


    else:
        try:
            message = """Subject: Traffic Data updates

Traffic Report :\n
Date and Time : {}
Average number of vehicles : {}

Number of vehicles which bypasses the signal : {}""".format(time.asctime(), int(
                sum(vehicles_count) / (len(vehicles_count) if len(vehicles_count) else 1)), total_number_red_bypasses);

            obj = smtplib.SMTP("smtp.gmail.com", 587);
            obj.starttls();
            obj.login("nateshmbhatofficial@gmail.com", "inteledison123");
            obj.sendmail("nateshmbhat1@gmail.com", ["nateshmbhatofficial@gmail.com"], message);
            print("Mail sent successfully ! ");
        except(KeyboardInterrupt):
            print("Program terminated by user ! ");
            exit();

        except:
            print("Connection Error ! Password is wrong or internet is not connected");





def smssending(message):
    from twilio.rest import Client;
    try:
        client = Client("ACbd6f505b95082979dc6c0a74d5a81393", "df56a2ea3929758b6fcda6b75d8b7343");
        client.messages.create(to="+919481575049", from_="+19137474599", body=message);
        print("Message sent successfully");
    except(KeyboardInterrupt):
        print("Program terminated by user ! ");
        exit();
    except:
        print("Coudn't send SMS. Check your internet connection ! ");




def node_mcu_signals_manage():
    global flag_stop_usual_signal_loop
    while (1):
        if (not flag_stop_usual_signal_loop):
            for i in ["A", "B", "C", "D"]:
                node.send(i.encode());
                sleep(5);
                if flag_stop_usual_signal_loop:
                    break;
            continue;
        sleep(10);
        flag_stop_usual_signal_loop = False;




def wait_for_node_mcu(snode):
    global node;
    print("waiting to connect");
    node, addr = snode.accept();
    print("NODE MCU CONNECTED  :\nAddress = {}\n\n".format(addr));
    node.sendall("HEllo NOde MCU".encode());
    print("Node MCU CONNECTED ");

    threading.Thread(target=recvdata, args=[node]).start();
    node_mcu_signals_manage();




def recvdata(node, img=None):
    global global_frame;
    global total_number_red_bypasses
    while (1):
        data = "";
        char = "";

        while (char != "\n"):
            char = node.recv(1).decode();
            print(char);
            data += char;

        if ("bypass" in data):
            print("thing is running");
            if global_frame is None:
                print("NO PICTURE PRESENTLY BEING TAKEN ! ");
            else:
                total_number_red_bypasses+=1 ;
                cv2.imwrite("bypass.jpg", global_frame);
                print("\n\nIMAGE SAVED !\n\n");

        print("Data Received from ", data);
        if not len(data): break;




def temporary_Funtion_to_check_image_processing():
    global flag_stop_usual_signal_loop
    global vehicles_count
    global global_frame
    time.sleep(10);

    cap = cv2.VideoCapture(r"cars1.avi");

    while (1):
        sleep(10);

        ret, frame = cap.read();
        global_frame = frame;
        if not ret:
            print("\n\n\n\nVIDEO FULLY COMPLETED \n\n\n\n");
            break;

        walker_data = cv2.CascadeClassifier(r"pedestrian.xml")
        car_data = cv2.CascadeClassifier(r"cars.xml")

        # PEDESTRIAN DETECTION

        ped = walker_data.detectMultiScale(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 3, 5);

        print("pedestrians detected : ", len(ped));

        for (x, y, j, k) in ped:
            cv2.rectangle(frame, (x, y), (x + j, y + k), (0, 255, 0), 2);

        # CARS DETECTION

        cars = car_data.detectMultiScale(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 1.1, 1);

        print("Vehicles detected : ", len(cars))

        for (x, y, j, k) in cars:
            cv2.rectangle(frame, (x, y), (x + j, y + k), (0, 255, 0), 2);

        # cv2.imshow('image', frame);
        # if (cv2.waitKey(1) == ord('q')):
        #     break;

        if (len(cars) >= 6):
            if ('node' in globals()):
                node.send("G".encode());
            flag_stop_usual_signal_loop = True;

        vehicles_count.append(len(cars));




s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
s.connect(("10.255.255.255", 0));
ref = s.getsockname()[0]

snode = socket.socket();
snode.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
snode.bind((ref, 34569));  # DATA SENDING TO NODE MCU

sapp = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
sapp = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
sapp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sapp.bind((ref, 8888));

print("\nNODE MCU server ip : {}\nPort : {}\n".format(ref, 34569));
print("\nAPP server ip : {} \nPort : {}\n".format(ref, 8888));

sapp.listen(20);
snode.listen(100)

threading.Thread(target=take_commands_from_app, args=[sapp]).start();
threading.Thread(target=wait_for_node_mcu, args=[snode]).start();

# COMMENT THE BELOW TWO LINES WHEN PUTTING INTO INTEL EDISON
# temporary_Funtion_to_check_image_processing() ; #ONLY USE THIS IF YOU ARE CHECKING THE WORKING FROM YOUR PC AND NOT SENDING THE IMAGE DATA TO INTEL
# exit(0) ;




while (1):
    try:

        frame = cap.read()

        if not frame[0]:
            print("\n\n\n\n>>>>>\nVIDEO COMPLETED !!! \n>>>>>>") ;
            cap = cv2.VideoCapture("cars1.avi") ;
            continue ;
        else:
            frame = frame[1]

        global_frame = frame

        walker_data = cv2.CascadeClassifier(r"pedestrian.xml")
        car_data = cv2.CascadeClassifier(r"cars.xml")

        # PEDESTRIAN DETECTION

        ped = walker_data.detectMultiScale(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 3, 5);
        print("pedestrians detected : ", len(ped));

        for (x, y, j, k) in ped:
            cv2.rectangle(frame, (x, y), (x + j, y + k), (0, 255, 0), 2);



            # CARS DETECTION

        cars = car_data.detectMultiScale(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 1.1, 1);

        for (x, y, j, k) in cars:
            cv2.rectangle(frame, (x, y), (x + j, y + k), (0, 255, 0), 2);

        # cv2.imshow("Security Feed", frame)
        # if cv2.waitKey(1)==ord('q'):break;


        print("Vehicles detected : ", len(cars))

        if (len(cars) >= 6):
            if ('node' in globals()):
                node.send("G".encode());
            flag_stop_usual_signal_loop = True;

        vehicles_count.append(len(cars));


    # for(x,y,j,k) in cars:
    #     cv2.rectangle(frame , (x, y) , (x+j , y+k) , (0,255 , 0) , 2) ;


    # cv2.destroyAllWindows() ;


    except(KeyboardInterrupt):
        print("\nINTERRUPTED BY USER !!! EXITING");
        snode.close();
        sapp.close() ;
        sys.exit(100) ;
