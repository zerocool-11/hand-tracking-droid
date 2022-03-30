from turtle import position
from utils.FaceDetector import mp_detector
import mediapipe as mp
import numpy as np
import cv2
import time
from websocket import create_connection
import PIL.Image as Image
from time import sleep
import threading 
import io
import urllib

# ws = create_connection('ws://192.168.1.59/Camera')
ws1=create_connection('ws://192.168.1.67/ServoInput')
class w:
    def __init__(self) -> None:
        pass
    def send(self,data):
        pass

# ws1=w()
url="http://192.168.1.67/picture"
detector=mp_detector()
cap=cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)
pTime=0
mid_x=None
position=90
position_y=90
pid=[0.1,0.1]
pErrorW=0
pErrorH=0

pan=65
def blink():
    global ws1 ,hand_id
    if hand_id=="fist":
        temp=["Light",str(55)]
        data=","
        ws1.send(data.join(temp))
        
        print("data: ",data.join(temp))
        sleep(2)
        temp=["Light",str(0)]
        ws1.send(data.join(temp))
        

def track(bbox,w,h,pid,pErrorW,pErrorH):
    cx,cy=bbox[0],bbox[1]
    errorW=cx-w//2
    errorH=cy-h//2
    speedW=pid[0]*errorW + pid[1]*(errorW-pErrorW)
    speedW=int(np.clip(speedW,-90,90))
    speedH=pid[0]*errorH + pid[1]*(errorH-pErrorH)
    speedH=int(np.clip(speedH,-73,73))
    if speedH >= 0:
        speedH=speedH+73
    else:
        speedH=speedH+73
    if speedW >= 0:
        speedW=speedW+90
    else:
        speedW=(speedW)+90
    print("sending speed y ",speedH)

    return errorW,errorH,speedW,speedH

old_speed_x=90
old_speed_y=90




while True:
    imgResp=urllib.request.urlopen(url)
    imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
    img=cv2.imdecode(imgNp,-1)
    # --------------uncomment till here----------
    # x= ws.recv()
    # image = Image.open(io.BytesIO(x))
    # # print("done ",type(image))
    # # image.save("x.jpg")
    # img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    # success, img = cap.read()
    # img=cv2.flip(img, 1)
    img=cv2.resize(img,(640,480))
    
    img, label,landmarks,rect,hand_id = detector.hand(img)
    buffer=30
    speed=5
    # print("shape: ",img.shape)
    rows, cols, _ = img.shape
    center_x=cols//2
    center_y=rows//2
    # If no hand is there then no movement at all
    mid_x=center_x
    mid_y=center_y
    # print("row and cols : ",rows,cols)
    if rect:
        mid_x=((rect[0]+rect[2]+rect[0])//2)
        mid_y=((rect[1]+rect[3]+rect[1])//2)
        cv2.circle(img, (mid_x,mid_y), 3, (0,0,255),-2)
        # print("cirlce: ",rows//2,cols//2)
        cv2.circle(img, (cols//2,rows//2), 3, (0,255,255),-2)
    cv2.circle(img, (center_x+buffer,center_y), 3, (255,255,255),-2)
    cv2.circle(img, (center_x,center_y+buffer), 3, (255,255,255),-2)
    
    if mid_x:
        if mid_x<center_x-buffer:
            if position<180:
                position+=speed
        elif mid_x>center_x+buffer:
            if position>2:
                position-=speed
        if mid_y<center_y-buffer:
            if position_y<180:
                position_y-=speed
        elif mid_y>center_y+buffer:
            if position_y>70:
                position_y+=speed
        cv2.putText(img, f'sending for x {position}', (20, 200), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        cv2.putText(img, f'sending for y {position_y}', (20, 230), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        
        temp=["Tilt",str(position)]
        data=","
        print("data : ",data.join(temp))
        ws1.send(data.join(temp))
        temp=["Pan",str(position_y)]
        data=","
        print("data: ",data.join(temp))
        ws1.send(data.join(temp))
        cv2.putText(img, f'Gesture: {hand_id}', (20, 130), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        t=threading.Thread(target=blink,args=())
        t.start()
        #         
        # pErrorW,pErrorH,position,position_y= track([mid_x,mid_y],cols,rows,pid,pErrorW,pErrorH)
        # if old_speed_x>position:
        #     if old_speed_x-position>5:  ##check if angle change more than 5 degree then only move
        #         temp=["Tilt",str(position)]
        #         data=","
        #         ws1.send(data.join(temp))
        #         print("data: ",data.join(temp))
        #         cv2.putText(img, f'sending for x {position}', (20, 200), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        #         old_speed_x=position
        # elif old_speed_x<position:
        #     if position-old_speed_x>5:  ##check if angle change more than 5 degree then only move
        #         temp=["Tilt",str(position)]
        #         data=","
        #         print("data: ",data.join(temp))
        #         ws1.send(data.join(temp))
        #         cv2.putText(img, f'sending for x {position}', (20, 200), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        #         old_speed_x=position
        # if old_speed_y>position_y:
        #     if old_speed_y-position_y > 5:  ##check if angle change more than 5 degree then only move            
        #         if position_y<73:
        #             temp_y=["Pan",str(73)]
        #         else:
        #             temp_y=["Pan",str(position_y)]
        #         data_y=","
        #         ws1.send(data_y.join(temp_y))
        #         cv2.putText(img, f'sending for y {position}', (20, 230), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        #         print("data: ",data_y.join(temp_y))
        #         old_speed_y=position_y
        # elif old_speed_y<position_y:
        #     if position_y-old_speed_y >5:  
        #         if position_y<73:
        #             temp_y=["Pan",str(73)]
        #         else:
        #             temp_y=["Pan",str(position_y)]
                
        #         data_y=","
        #         ws1.send(data_y.join(temp_y))
        #         cv2.putText(img, f'sending for y {position}', (20, 230), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        #         print("data: ",data_y.join(temp_y))
        #         old_speed_y=position_y
                
    
    
    
    
    
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    # cv2.putText(img, f'Position x: {position}', (20, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
    # cv2.putText(img, f'Position y: {position_y}', (20, 150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
    
    cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
    cv2.imshow("Image", img)
    
    if cv2.waitKey(1) & 0xFF == 27:
        break
    
# cap.release()
cv2.destroyAllWindows()
# ws.close()
ws1.close()
