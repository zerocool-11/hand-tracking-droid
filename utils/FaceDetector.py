import mediapipe as mp
import cv2
import time
import numpy as np
from utils.classifier import KeyPointClassifier
from utils.mediapipe_utils import draw_landmarks,calc_bounding_rect,calc_landmark_list,pre_process_landmark


 
class mp_detector:
    def __init__(self,model="hand"):
        if model=="face":
            self.minDet=0.75
            self.mp_face=mp.solutions.face_detection
            self.mp_draw=mp.solutions.drawing_utils
            self.face_detector=self.mp_face.FaceDetection(self.minDet)

        else:
            self.mp_hand=mp.solutions.hands
            self.model=self.mp_hand.Hands(max_num_hands=1,min_detection_confidence=0.4,
                                        min_tracking_confidence=0.5)
            self.keypoint_classifier=KeyPointClassifier()
            self.keypoint_classifier_labels=['fist','none']
        
    def faces(self,img,draw=True):
        self.results=self.model.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        bboxs=[]
        if self.results.detections:
            for id,detection in enumerate(self.results.detections):
                bboxC=detection.location_data.relative_bounding_box
                ih,iw,ic=img.shape
                bbox=int(bboxC.xmin*iw),int(bboxC.ymin*ih),int(bboxC.width*iw),int(bboxC.height*ih)
                bboxs.append([id,bbox,detection.score])
                cv2.rectangle(img, bbox, (255, 0, 255), 2)
                cv2.putText(img, f'{str(int(detection.score[0]*100))}%',
                        (bbox[0], bbox[1] - 20), cv2.FONT_HERSHEY_PLAIN,
                        2, (255, 0, 255), 2)

        return img,bboxs
    def hand(self,img):
        self.res_hand=self.model.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        Label=None
        hand_sign_id=""
        if self.res_hand.multi_hand_landmarks:
            for hand_landmarks, handedness in zip(self.res_hand.multi_hand_landmarks,self.res_hand.multi_handedness):
                landmark_list= calc_landmark_list(img,hand_landmarks)
                pre_processed_landmark_list = pre_process_landmark(
                    landmark_list)
                id = self.keypoint_classifier(pre_processed_landmark_list)
                hand_sign_id=self.keypoint_classifier_labels[id]
                
                rect=calc_bounding_rect(img,hand_landmarks)
                Label=handedness.classification[0].label[0:]
                img = draw_landmarks(img, landmark_list)
                img=cv2.rectangle(img, (rect[0], rect[1],rect[2], rect[1]),
                 (0, 0, 0), 2)

            

        else:
            landmark_list= None
            rect=None
        return img,Label,landmark_list,rect,hand_sign_id
    


def main():
    cap = cv2.VideoCapture(0)
    pTime = 0
    detector = faceDetector()
    while True:
        success, img = cap.read()
        img, bboxs = detector.faces(img)
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
 
if __name__ == "__main__":
    main()