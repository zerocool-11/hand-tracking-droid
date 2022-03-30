from utils.FaceDetector import mp_detector
import mediapipe as mp
import numpy as np
import cv2
import time
from websocket import create_connection

from pyfirmata import Arduino,SERVO,util
from time import sleep
import threading 
port="/dev/ttyACM0"
pin=10
pin2=9
ws = create_connection('ws://192.168.1.40')

old_angle1=0
old_angle=0
def rotateservo(pin,angle,ob="s1"):
    global old_angle
    print("angle: ",angle)
    print("old angle ",old_angle)
    print("\n")
    if angle>old_angle:
        for a in range(old_angle,angle):
            # print("......................................function called rotation servo  ")
            temp=[ob,str(a)]
            print("temp: ",temp)
            print("data: "," ".join(temp) )
            ws.send(" ".join(temp))
            sleep(0.015)
    elif angle< old_angle:
        for z in range(old_angle,angle,-1):
            # print("......................................function called rotation servo  ")
            temp=[ob,str(z)]
            print("temp: ",temp)
            print("data: "," ".join(temp) )
            ws.send(" ".join(temp))
            sleep(0.015)
    old_angle=angle
    # sleep(0.035)

def rotateservo_y(pin,angle1,ob="s2"):
    global old_angle1
    data=" "
    print("angle: ",angle1)
    print("old angle ",old_angle1)
    print("\n")
    if angle1>old_angle1:
        for a in range(old_angle1,angle1):
            # print("......................................function called rotation servo  ")
            temp=[ob,str(a)]
            print("temp: ",temp)
            print("data: "," ".join(temp) )
            ws.send(" ".join(temp))
            sleep(0.015)
    elif angle1< old_angle1:
        for z in range(old_angle1,angle1,-1):
            # print("......................................function called rotation servo  ")
            temp=[ob,str(z)]
            print("temp: ",temp)
            print("data: "," ".join(temp) )
            ws.send(" ".join(temp))
            sleep(0.015)
    old_angle1=angle1

cap = cv2.VideoCapture(0)
pTime = 0
run_once=True
run_once2=False
detector = mp_detector()
old_center_x=0
old_center_y=0
def NormalizeData_x(x):
    old_x=(640-0)
    new=(180-0)
    return (((x-0)*new)/old_x)+0
def NormalizeData_y(y):
    old_y=(480-0)
    new=(90-0)
    return (((y-0)*new)/old_y)+0
nx=0
old_nx=0
old_ny=0

ny=0
itr=0
itr2=0
threads1=[]
threads2=[]

old_thread=None
old_thread2=None

while True:
    success, img = cap.read()
    # print("shape: ",img.shape)
    img, label,landmarks,rect = detector.hand(img)
    # if not landmarks:
    #     board.digital[11].write(0)
    #     pass
    # else:
    #     pass
    #     board.digital[11].write(1)

    if rect:
        mid_x=rect[0]+rect[2]//2
        mid_y=rect[1]+rect[3]//2
        if run_once:
            old_center_x=mid_x
            old_center_y=mid_y
            # print("non normalized: ",old_center_x,old_center_y)
            old_nx,old_ny= int(NormalizeData_x(mid_x)),int(NormalizeData_y(mid_y))
            # print("normalized for once x,y : ",old_nx,old_ny)
            run_once=False
        # print("mid x ,y ",mid_x,mid_y)
        if old_center_x-10<= mid_x<=old_center_x+10:
            pass

        elif old_center_x-10> mid_x or mid_x >old_center_x+10 :
            # print("old x ",NormalizeData_x(old_center_x))
            old_center_x=mid_x
            # print("non normalized: ",mid_x)
            nx=int(NormalizeData_x(mid_x))
            # print("new x: ",nx)
            t=threading.Thread(target=rotateservo, args=(pin2,nx,))
            threads1.append(t)
            if threads1:
                if old_thread is None:
                    old_thread=threads1[itr]
                    old_thread.start()
                if not old_thread.is_alive():
                    itr+=1
                    threads1[itr].start()
                    old_thread=threads1[itr]
                # rotateservo(pin2,nx)
        if old_center_y-20<= mid_y<=old_center_y+20:
            pass
        elif old_center_y-20> mid_y or mid_y>old_center_y+20:
            # print("old y ",NormalizeData_y(old_center_y))
            old_center_y=mid_y
            # print("non normalized: ",mid_y)
            ny=int(NormalizeData_y(mid_y))
            # print("new y: ",ny)
            t2=threading.Thread(target=rotateservo_y, args=(pin,ny,))
            threads2.append(t2)
            if threads1:
                if old_thread2 is None:
                    old_thread2=threads2[itr2]
                    old_thread2.start()
                if not old_thread2.is_alive():
                    itr2+=1
                    threads2[itr2].start()
                    old_thread2=threads2[itr2]
      

        # if NormalizeData_x(old_center_x)>NormalizeData_x(mid_x):
        #     for i in range(old_nx,nx):
        #         rotateservo(pin2,nx)
        # else:
        #     for i in range(nx,old_nx):
        #         rotateservo(pin2,nx)
        # if NormalizeData_y(old_center_y)>NormalizeData_y(mid_y):
        #     for j in range(old_ny,ny):   
        #         rotateservo(pin,ny)
        # else:
        #     for j in range(ny,old_ny):   
        #         rotateservo(pin,ny)
        cv2.circle(img,(mid_x,mid_y),5,(255,255,0),-2)
    #print(bboxs)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2)
    cv2.imshow("Image", img)
    
    if cv2.waitKey(1) & 0xFF == 27:
        break
    
cap.release()
#cv2.destroyAllwindows()
