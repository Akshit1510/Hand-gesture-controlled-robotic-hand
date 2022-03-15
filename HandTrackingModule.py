import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self,static_image_mode=False, max_num_hands=1, model_complexity=1, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.static_image_mode=static_image_mode
        self.max_num_hands=max_num_hands
        self.model_complexity=model_complexity
        self.min_detection_confidence=min_detection_confidence
        self.min_tracking_confidence=min_tracking_confidence

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.static_image_mode,
                self.max_num_hands,
                self.model_complexity,
                self.min_detection_confidence,
                self.min_tracking_confidence)

        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(imgRGB)
        lmLst = []
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = img.shape
                    cx ,cy = int(lm.x*w), int(lm.y*h)
                    lmLst.append([cx, cy, lm.z*w])
                if draw:
                    self.mpDraw.draw_landmarks(img ,handLms, self.mpHands.HAND_CONNECTIONS)
        cv2.imshow("Image",img)
        return lmLst

def main():
     cap = cv2.VideoCapture(0)
     detector = handDetector()
     lmLst=[]
     while True:
         success, img = cap.read()
         lmLst=detector.findHands(img)
         print(lmLst)
         cv2.waitKey(1)

if __name__=="__main__":
    main()
