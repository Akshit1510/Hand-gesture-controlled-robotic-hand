import cv2
import time
import HandTrackingModule as htm
import math
pi = 3.1415926535
detector = htm.handDetector()


def angle(c1, c2, c3):
    a1 = c1[0] - c2[0]
    b1 = c1[1] - c2[1]
    c1 = c1[2] - c2[2]
    a2 = c3[0] - c2[0]
    b2 = c3[1] - c2[1]
    c2 = c3[2] - c2[2]
    ang = (a1*a2 + b1*b2 + c1*c2)/(math.sqrt(math.pow(a1,2) + math.pow(b1,2) + math.pow(c1,2)) * math.sqrt(math.pow(a2,2) + math.pow(b2,2) + math.pow(c2,2)))
    ang = math.degrees(math.acos(ang))
    ang = int(ang)
    return ang

def angLst(lmLst):
    lst = []
    lst.append(angle(lmLst[1],lmLst[2],lmLst[3]))
    lst.append(angle(lmLst[2],lmLst[3],lmLst[4]))
    lst.append(angle(lmLst[0],lmLst[5],lmLst[6]))
    lst.append(angle(lmLst[5],lmLst[6],lmLst[7]))
    lst.append(angle(lmLst[0],lmLst[9],lmLst[10]))
    lst.append(angle(lmLst[9],lmLst[10],lmLst[11]))
    lst.append(angle(lmLst[0],lmLst[13],lmLst[14]))
    lst.append(angle(lmLst[13],lmLst[14],lmLst[15]))
    lst.append(angle(lmLst[0],lmLst[17],lmLst[18]))
    lst.append(angle(lmLst[17],lmLst[18],lmLst[19]))
    return lst



class controller():

    def __init__(self):
        self.currLst=[180,180,180,180,180,180,180,180,180,180]
        self.prevLst = self.currLst

    def generator(self,img):
        lmLst = detector.findHands(img)
        if len(lmLst):
            self.prevLst = self.currLst
            self.currLst = angLst(lmLst)
        return self.currLst




def main():
    cap = cv2.VideoCapture(0)
    control = controller()
    pTime = time.time()
    cTime = pTime
    while True:
        success, img = cap.read()
        cv2.waitKey(1)
        print(control.generator(img))

if __name__ == "__main__":
    main()
