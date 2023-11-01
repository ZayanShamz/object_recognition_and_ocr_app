# Object Recognition and OCR App

The Object Recognition and Optical Character Recognition (OCR) app is designed to assist individuals, especially the visually impaired, in their daily routines. This app enables users to identify objects in front of them and have printed text read aloud. It features a tkinter graphical user interface with buttons for object detection and text reading.

## Features

### Object Detection and Recognition
- Users can perform object recognition, allowing them to identify objects in their environment.
- The app uses the YOLOv3 configuration and weight files for object detection.
- Recognized objects are read aloud to the user, enhancing their understanding of the surroundings.

### Optical Character Recognition (OCR)
- Users can utilize the OCR feature to extract and read printed text.
- Text detection is achieved using pytesseract, making it possible to convert printed text into spoken words.
- The app uses the GTTS library to generate voice for reading aloud, and playsound to play the audio.

## Technology Stack

- **Python:** Version 3.10.8
- **pytesseract:** Version 0.3.10
- **opencv-python:** Version 4.5.5.64
- **Flask**
- **tkinter**
- **pymysql**
- **gtts**

## Getting Started

To set up and run the Object Recognition and OCR App, follow these steps:

1. Clone this repository to your local machine.
2. Install the required Python packages and dependencies listed in the "Technology Stack" section.
3. Configure any additional hardware, such as a camera.
4. Run the app to start object recognition and OCR functionality.

## Usage

1. Launch the app and use the provided buttons to perform object recognition and OCR.
2. For object recognition, the app will describe recognized objects audibly.
3. For OCR, the app will read aloud the text it identifies.

## Extending the App

When implementing this app, consider extending its capabilities by integrating it with physical buttons and wearable devices, such as a Raspberry Pi with a camera. This will make it more accessible and user-friendly for the visually impaired.

## Note

- The accuracy of object recognition and OCR may vary based on the quality of the camera, lighting conditions, and the objects or text to be recognized.
