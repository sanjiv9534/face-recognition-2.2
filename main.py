import tkinter as tk
from tkinter import *
import cv2
import csv
import time
import datetime
import os
import numpy as np
from PIL import Image
from tkinter import messagebox

root = tk.Tk()
root.title("Face Recognition Attendance System")
root.geometry('1280x720')
root.configure(background='light blue')
logo_image = tk.PhotoImage(file="images.png")
logo_label = tk.Label(root, image=logo_image)
logo_label.place(x=0, y=0)

# For title
title_lbl = tk.Label(root, text="Face Recognition Attendance System", font=("times new roman", 35, "bold"),
                     bg="light blue", fg="navy blue")
title_lbl.place(x=200, y=20, width=1280, height=45)

# labels
lbl = tk.Label(root, text="Enter Roll", width=20, fg="black", bg="light blue", font=('times', 15, 'bold'))
lbl.place(x=400, y=200)

def testVal(inStr, acttyp):
    if acttyp == '1':  # insert
        if not inStr.isdigit():
            return False
    return True

txt = tk.Entry(root, validate="key", width=20, bg="white", fg="black", font=('times', 25, 'bold'))
txt['validatecommand'] = (txt.register(testVal), '%P', '%d')
txt.place(x=750, y=210)

lbl2 = tk.Label(root, text="Enter Name", width=20, fg="black", bg="light blue", font=('times', 15, 'bold'))
lbl2.place(x=400, y=310)

txt2 = tk.Entry(root, width=20, bg="white", fg="black", font=('times', 25, 'bold'))
txt2.place(x=750, y=310)

def clear():
    txt.delete(0, 'end')

def clear1():
    txt2.delete(0, 'end')

clearButton = tk.Button(root, text="Clear", command=clear, fg="black", bg="light blue", width=10, height=1,
                        activebackground="light blue", font=('times', 15, 'bold'))
clearButton.place(x=1180, y=210)

clearButton1 = tk.Button(root, text="Clear", command=clear1, fg="black", bg="light blue", width=10, height=1,
                         activebackground="light blue", font=('times', 15, 'bold'))
clearButton1.place(x=1180, y=310)

AP = tk.Button(root, text="Check Registered Students", fg="black", bg="navy blue", width=19, height=1,
                activebackground="navy blue", font=('times', 15, 'bold'))
AP.place(x=990, y=410)

# Error screen1
def del_sc():
    sc.destroy()

def err_screen():
    global sc
    sc = tk.Tk()
    sc.geometry('300x100')
    sc.iconbitmap('images.png')
    sc.title('Please fill both fields')
    sc.configure(background='snow')
    Label(sc, text='Please enter both Roll and Name!', fg='red', bg='white',
          font=('times', 16, 'bold')).pack()
    Button(sc, text='OK', command=del_sc, fg="black", bg="lawn green", width=9, height=1,
           activebackground="Red", font=('times', 15, 'bold')).place(x=90, y=50)

# Error screen2
def del_sc2():
    sc2.destroy()

def err_screen1():
    global sc2
    sc2 = tk.Tk()
    sc2.geometry('300x100')
    sc2.iconbitmap('AMS.ico')
    sc2.title('Warning!!')
    sc2.configure(background='snow')
    Label(sc2, text='Please enter your subject name!!!', fg='red', bg='white',
          font=('times', 16, 'bold')).pack()
    Button(sc2, text='OK', command=del_sc2, fg="black", bg="lawn green", width=9, height=1,
           activebackground="Red", font=('times', 15, 'bold')).place(x=90, y=50)

# Taking photos
def taking():
    l1 = txt.get()
    l2 = txt2.get()
    if l1 == '':
        err_screen()
    elif l2 == '':
        err_screen1()
    else:
        try:
            cam = cv2.VideoCapture(0)
            detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            Enrollment = txt.get()
            Name = txt2.get()
            sampleNum = 0
            while True:
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    sampleNum += 1
                    cv2.imwrite(f"TrainingImage/{Name}.{Enrollment}.{sampleNum}.jpg", gray[y:y + h, x:x + w])
                    cv2.imshow('Frame', img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                elif sampleNum > 70:
                    break
            cam.release()
            cv2.destroyAllWindows()
            ts = time.time()
            Date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            row = [Enrollment, Name, Date, Time]
            with open('./StudentDetails/StudentDetails.csv', 'a+', newline='') as csvFile:
                writer = csv.writer(csvFile)
                if csvFile.tell() == 0:  # Check if the file is empty
                    writer.writerow(["Enrollment", "Name", "Date", "Time"])  # Write header row
                writer.writerow(row)
            csvFile.close()
            res = f"Images Saved for Enrollment: {Enrollment}, Name: {Name}"
            Label(root, text=res, bg="SpringGreen3", width=50, font=('times', 18, 'bold')).place(x=250, y=400)
        except FileExistsError as F:
            f = 'Student Data already exists'
            Label(root, text=f, bg="Red", width=21).place(x=450, y=400)

# Train the model
def trainimg():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    try:
        faces, Id = getImagesAndLabels("StudentDetails/StudentDetails.csv")
    except Exception as e:
        l = 'Please make "TrainingImage" folder & put Images'
        Notification.configure(text=l, bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
        Notification.place(x=350, y=400)
        return

    recognizer.train(faces, np.array(Id))
    try:
        recognizer.save("TrainingImageLabel/Trainner.yml")
    except Exception as e:
        q = 'Please make "TrainingImageLabel" folder'
        Notification.configure(text=q, bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
        Notification.place(x=350, y=400)
        return

    res = "Model Trained"
    Notification.configure(text=res, bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
    Notification.place(x=250, y=400)

def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faceSamples = []
    Ids = []
    for imagePath in imagePaths:
        pilImage = Image.open(imagePath).convert('L')
        imageNp = np.array(pilImage, 'uint8')
        Id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(imageNp)
        for (x, y, w, h) in faces:
            faceSamples.append(imageNp[y:y + h, x:x + w])
            Ids.append(Id)
    return faceSamples, Ids

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# message = tk.Label(root, text="Face-Recognition-Based-Attendance-Management-System", bg="cyan", fg="black",
#                    width=50, height=3, font=('times', 30, 'italic bold'))
# message.place(x=80, y=20)

Notification = tk.Label(root, text="All things good", bg="Green", fg="white", width=15, height=3,
                        font=('times', 17, 'bold'))

# Buttons
takeImg = tk.Button(root, text="Take Images", command=taking, fg="black", bg="navy blue", width=20, height=3,
                    activebackground="navy blue", font=('times', 15, 'bold'))
takeImg.place(x=90, y=500)

trainImg = tk.Button(root, text="Train Images", command=trainimg, fg="black", bg="navy blue", width=20, height=3,
                     activebackground="navy blue", font=('times', 15, 'bold'))
trainImg.place(x=390, y=500)

FA = tk.Button(root, text="Automatic Attendance", fg="black", bg="navy blue", width=20, height=3,
                activebackground="navy blue", font=('times', 15, 'bold'))
FA.place(x=690, y=500)

quitroot = tk.Button(root, text="Manually Fill Attendance", fg="black", bg="navy blue", width=20, height=3,
                     activebackground="navy blue", font=('times', 15, 'bold'))
quitroot.place(x=990, y=500)

dashboard = tk.Button(root, text="Graph", fg="black", bg="navy blue", width=20, height=3, activebackground="navy blue",
                      font=('times', 15, 'bold'))
dashboard.place(x=1290, y=500)

root.mainloop()
