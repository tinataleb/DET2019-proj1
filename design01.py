# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

import picamera     #camera library
import pygame as pg #audio library
import os           #communicate with os/command line

from google.cloud import vision  #gcp vision library
from time import sleep
from adafruit_crickit import crickit
#import time
import signal
import sys
import re           #regular expression lib for string searches!

#set up your GCP credentials - replace the " " in the following line with your .json file and path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="../../cred.json"

# this line connects to Google Cloud Vision! 
client = vision.ImageAnnotatorClient()

# global variable for our image file - to be captured soon!
image = 'image.jpg'

our_ings = ["banana", "straw", "milk"]
scanned_ings = []


def stream(camera):
    
    rawCapture = PiRGBArray(camera, size=(640, 480))
    # capture frames from the camera
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image = frame.array

        # show the frame
        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF

        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)
        
        output_capture(camera)
        
        

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
def takephoto(camera):
    
    # this triggers an on-screen preview, so you know what you're photographing!
    camera.start_preview() 
#    sleep(.5)                   #give it a pause so you can adjust if needed
    camera.capture('image.jpg') #save the image
    camera.stop_preview()       #stop the preview
    
def web_search(image):
    #this function sends your image to google cloud using the
    #web_detection method, collects a response, and parses that
    #response for the 'best web association' found for the image.
    #there's no actuation here - just printing - but you can easily
    #engage with speaker_out() or motor_turn() if you like!
    
    response = client.web_detection(image=image)
    web_guess = response.web_detection
    
#    print(web_guess)
#    print("LABELS:")
#    print(web_guess.best_guess_labels)
    
#    for label in web_guess.best_guess_labels:
#        print('Best Web Guess Label: {}'.format(label.label))
    return [label for label in web_guess.best_guess_labels]
    
        

def output_capture(camera):
    takephoto(camera) # First take a picture
    """Run a label request on a single image"""

    with open('image.jpg', 'rb') as image_file:
        #read the image file
        content = image_file.read()
        #convert the image file to a GCP Vision-friendly type
        image = vision.types.Image(content=content)

        labels = web_search(image)
        print("labels")
        ing_checker(labels)
        
#        time.sleep(0.1)

def ing_checker(labels):
    for l in labels:
        if l in our_ings:
            scanned_ings.append(l)
            #output with speaker
            speaker_output(l)
            
def speaker_output(word):
    pg.init()
    pg.mixer.init()
    
    pg.mixer.music.load("/home/pi/DET2019_Class5/hello2.wav")
    pg.mixer.music.play()


def testTouch():
    time.sleep(0.1)
    if crickit.touch_1.value:
        print("touch is working")
    else:
        print("nope")
    
def main():
    
    #generate a camera object for the takephoto function to
    #work with
#    camera = picamera.PiCamera()

    # initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    

    # allow the camera to warmup
    time.sleep(0.1)
    
    #setup our pygame mixer to play audio in subsequent stages
    
    stream(camera)
        
          
        
if __name__ == '__main__':
        main() 
