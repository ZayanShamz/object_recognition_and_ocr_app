import os
from flask import *
import time
import tkinter as tk
from tkinter import Button, Label
import cv2
import numpy as np
from PIL import Image, ImageTk
import threading
import sys
from gtts import gTTS
from playsound import playsound
import pytesseract
from pytesseract import Output


classesFile = 'static/coco.names'
with open(classesFile,'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')
    print(classNames)


# Load Yolo weights and config
modelConfig = 'static/yolov3.cfg'
modelWeight = 'static/yolov3.weights'

net = cv2.dnn.readNetFromDarknet(modelConfig, modelWeight)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

app = Flask(__name__)

cap = cv2.VideoCapture(0)
frame = None


# Create the main tkinter window
root = tk.Tk()
root.title("Webcam Feed")


# Signals the app to send current location
@app.route('/Help_fn', methods=['GET', 'POST'])
def Help_fn():
    print("hello")


def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)


def obj_fn(obj):
    classIds = []
    timeout = 5  # Set the timeout in seconds
    start_time = time.time()  # Record the start time

    # process the frame until an object is detected or the timeout is reached
    while True:
        # Preprocess the frame for object detection
        blob = cv2.dnn.blobFromImage(obj, 1 / 255, (320, 320), [0, 0, 0], 1, crop=False)
        net.setInput(blob)

        outputNames = net.getUnconnectedOutLayersNames()

        # Forward pass through the network
        outputs = net.forward(outputNames)

        objects = []

        for output in outputs:
            for detection in output:
                scores = detection[5:]
                classId = np.argmax(scores)
                confidence = scores[classId]

                if confidence > 0.7:
                    if classId not in classIds:
                        classIds.append(classId)

                        object_name = classNames[classId]
                        objects.append((object_name, confidence))

        # Print detected objects
        # print(objects)
        voice = "detected "
        for obj_name, conf in objects:
            voice = voice + obj_name + " "
            # print(f"Object: {obj_name}, Confidence: {conf:.2f}%")

        if objects:
            lang = 'en'
            speak = gTTS(text=voice, lang=lang, slow=False)
            if os.path.exists("static/object.mp3"):
                os.remove("static/object.mp3")
            speak.save("static/object.mp3")
            playsound('static/object.mp3')
            break

        # Check if the timeout has been reached
        if time.time() - start_time >= timeout:
            playsound('static/NoObject.mp3')
            break

    print("Object Detection Completed")


def read_fn(obj):
    print("EXTRACTING TEXT")
    tess_config = r"--oem 3 --psm 3"

    data = pytesseract.image_to_data(obj, config=tess_config, output_type=Output.DICT)

    boxes = len(data['text'])
    text = ''
    for i in range(boxes):
        if data['conf'][i] > 80:
            text = pytesseract.image_to_string(frame, config=tess_config)

    if text:
        speak = gTTS(text=text, lang='en', slow=False)
        if os.path.exists("static/text.mp3"):
            os.remove("static/text.mp3")
        speak.save("static/text.mp3")

        print(text)
        playsound('static/text.mp3')
    else:
        playsound('static/NoText.mp3')


def on_close():  # Define a function to be called when the close button is pressed
    cap.release()
    root.destroy()
    sys.exit()


def update_frame():
    global frame
    while True:
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=img)
            label.img = img
            label.config(image=img)
            root.update()
        else:
            break


label = Label(root, compound="center", anchor="center", relief="raised")
label.pack()

# --------- BUTTONS ------------------------------
ocr_btn = Button(root, text="Read Text", bg="#F4FDD9", font="Helvetica, 16", command=lambda: read_fn(frame))
obj_btn = Button(root, text="Detect Object", bg="#F4FDD9", font="Helvetica, 16", command=lambda: obj_fn(frame))
help_btn = Button(root, text="Help", bg="#DE3C4B", fg="#DDFDFE", font="Helvetica, 16", command=Help_fn)
close_btn = Button(root, text="Close", bg="#DE3C4B", fg="#DDFDFE", font="Helvetica, 16", command=on_close)

ocr_btn.place(bordermode="inside", relx=0.2, rely=0.9, anchor="center", width=150, height=40)
obj_btn.place(bordermode="inside", relx=0.45, rely=0.9, anchor="center", width=150, height=40)
help_btn.place(bordermode="inside", relx=0.7, rely=0.9, anchor="center", width=100, height=40)
close_btn.place(bordermode="inside", relx=0.9, rely=0.9, anchor="center", width=100, height=40)

# Start the Flask server in a separate thread
flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

# Start updating the frame
update_frame()

root.protocol("WM_DELETE_WINDOW", on_close)  # Call on_close when the window is closed using the 'X' button
root.mainloop()
