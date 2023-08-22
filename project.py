import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

path = 'D:\A-projects\project Reg_webcam\Image_folder'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList
encodeListKnown = findEncodings(images)
print(len(encodeListKnown))
print("Encoding completed succeessfuly")

def markAttendance(name):
    with open('Att sheet.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        #print(myDataList)
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            d1=now.strftime("%d/%m/%y")
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString},{d1},Present')

cap = cv2.VideoCapture(0)
i=0
while  True:
    
    success, img = cap.read()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25) #style of vedio capture screen
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
   
    
 
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)
 
    for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
        #print(faceDis)
        matchIndex = np.argmin(faceDis) 
        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            #print(name)
            y1,x2,y2,x1 = faceLoc 
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            markAttendance(name)
            if((name=="DR.FAROOQ SHAH" or name=="DR.RAMESH K" or name=="DR.VILAS SAPKAL") and i<1):
                from tkinter import *
                from PIL import ImageTk, Image
                win = Tk()
            # Define the geometry of the window
                win.geometry("700x500")
                frame = Frame(win, width=600, height=400)
                frame.pack()
                frame.place(anchor='center', relx=0.5, rely=0.5)
                win.title("welcome")
                win.geometry('500x300')
                l1=Label(win,text=" ' Welcome to Nandha Engineering College '\n Our Institution is very happy to invite you \n  We Believe that you can move our institution to its next level !!! ",fg='Red',font=('Times new roman',14),)
            # Create an object of tkinter ImageTk
                im = ImageTk.PhotoImage(Image.open("C:\\Users\\raghu\\OneDrive\\Pictures\\Saved Pictures\\download.png"))
            # Create a Label Widget to display the text or Image
                l1.grid()
                label = Label(frame, image = im)
                label.pack()
                win.after(10000,lambda:win.destroy())
                win.mainloop()
                i+=1    



        else:
            y1,x2,y2,x1 = faceLoc 
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,0,255),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,0,255),cv2.FILLED)
            cv2.putText(img,"UnKnown person",(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),2)
        
    cv2.imshow('MY_Webcam', img)


    key=cv2.waitKey(5)
    if key==ord('x'):
        break
cv2.destroyAllWindows()
cv2.imread

    
