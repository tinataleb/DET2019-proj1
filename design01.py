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

from adafruit_seesaw.neopixel import NeoPixel

# The number of NeoPixels
num_pixels = 8

pixels = NeoPixel(crickit.seesaw, 20, num_pixels)

#set up your GCP credentials - replace the " " in the following line with your .json file and path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/pi/Desktop/DET-2019-Pancham.json"

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


########## START LED SECTION ###########

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)

def color_chase(color, wait):
    for i in range(num_pixels):
        pixels[i] = color
        time.sleep(wait)
        pixels.show()
    time.sleep(0.5)

def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            rc_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(rc_index & 255)
        pixels.show()
        time.sleep(wait)

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)


########## END LED SECTION ###########

def speak(ing):
    pg.init()
    pg.mixer.init()

    if ing=="strawberry":
        pg.mixer.music.load("/home/pi/DET2019_Proj1/audio/strawberry.wav")
        pg.mixer.music.play()
    if ing=="banana":
        pg.mixer.music.load("/home/pi/DET2019_Proj1/audio/banana.wav")
        pg.mixer.music.play()
    if ing=="milk":
        pg.mixer.music.load("/home/pi/DET2019_Proj1/audio/milk.wav")
        pg.mixer.music.play()

def walkthrough():
    pg.init()
    pg.mixer.init()

    pg.mixer.music.load("/home/pi/DET2019_Proj1/audio/instructions-1.wav")
    pg.mixer.music.play()
    time.sleep(5)

    pg.mixer.music.load("/home/pi/DET2019_Proj1/audio/instructions-2.wav")
    pg.mixer.music.play()
    time.sleep(5)



def testTouch():
    time.sleep(0.1)
    if crickit.touch_1.value:
        print("DEVICE TURNS ON")
        return True
    else:
        print("OFFLINE.")
        return False

def sound_on():
    print("playing sound")
    pg.init()
    pg.mixer.init()
    pg.mixer.music.load("/home/pi/DET2019_Proj1/audio/on-sound.wav")
    pg.mixer.music.play()
    time.sleep(5)


def leds_on():
    for i in range(10):
        print("BLUE LED")
        time.sleep(1)
        pixels.fill(BLUE)
        pixels.show()
        time.sleep(1)
        color_chase(BLUE, 0.1)

def leds_discovery():
    for i in range(4):
        print("GREEN LED")
        time.sleep(1)
        pixels.fill(GREEN)
        pixels.show()
        color_chase(GREEN, 0.1)


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

    # Tests for touch being on. ONLY if it is activated, the stream begins.
    while True:
        if testTouch():
            sound_on()
            leds_on()
            stream(camera)
        else:
            print("offline")


if __name__ == '__main__':
        main()
