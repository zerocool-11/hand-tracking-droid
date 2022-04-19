from utils.FaceDetector import mp_detector
import numpy as np
import cv2
import time
from websocket import create_connection
from time import sleep
import threading 
import io
import urllib

ip='192.168.1.67'
# ws = create_connection('ws://192.168.1.59/Camera')
ws1=create_connection('ws://{}/ServoInput'.format(ip))
url="http://{}/picture".format(ip)

detector=mp_detector()


pTime=0
mid_x=None
position=90
position_y=90


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
        

old_speed_x=90
old_speed_y=90




while True:
    imgResp=urllib.request.urlopen(url)
    imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
    img=cv2.imdecode(imgNp,-1)
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
        
    
    
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    
    cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
    cv2.imshow("Image", img)
    
    if cv2.waitKey(1) & 0xFF == 27:
        break
    
# cap.release()
cv2.destroyAllWindows()
# ws.close()
ws1.close()
