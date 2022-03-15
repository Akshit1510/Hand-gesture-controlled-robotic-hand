import serial
import cv2
import Calculate
import time


cap = cv2.VideoCapture(0)
mySerial = serial.Serial('COM3' ,9600 ,timeout = 1)
Cal = Calculate.controller()
sendLst = []

def releative(angle):
    return 2*(angle - 90)

while True:
    sucess, img = cap.read()
    cv2.waitKey(1)
    sendLst = Cal.generator(img)
    arduinoSend = "$"
    for i in range(0,10):
        tlst = []
        temp = sendLst[i]
        sendLst[i] = releative(sendLst[i])
        if sendLst[i]>180:
            sendLst[i] = 180
        if sendLst[i]<0:
            sendLst[i] = 0
        for j in range(0,3):
            tlst.append(sendLst[i]%10)
            sendLst[i] = sendLst[i]/10
        for j in range(0,3):
            c = str(int(tlst[2-j]))
            c = c[0]
            arduinoSend = arduinoSend + c
        sendLst[i] = temp
    mySerial.write(arduinoSend.encode())
    time.sleep(0.1)
    #print(mySerial.readline().decode('ascii'))
    print(arduinoSend)
    

