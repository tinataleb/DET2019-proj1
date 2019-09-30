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

our_ings = ["banana", "strawberries", "milk", "strawberry", "carton", "lactis", "liquid"]
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

        if len(scanned_ings) == 3:
            walkthrough()



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
    response = client.web_detection(image=image)
    web_guess = response.web_detection

    return [label for label in web_guess.best_guess_labels]



def output_capture(camera):
    takephoto(camera) # First take a picture
    """Run a label request on a single image"""

    with open('image.jpg', 'rb') as image_file:
        content = image_file.read()
        image = vision.types.Image(content=content)
        labels = web_search(image)
        for label in labels:
            l = label.label
            print(l)
            ing_checker(l)

def ing_checker(ing):
    print('checking {}'.format(ing))
    ing_strings = ing.split(" ")
    for i in ing_strings:
        if i in our_ings:
            scanned_ings.append(i)
            print('scanned {}'.format(i))

            speak(i)


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
OFF = (0,0,0)


########## END LED SECTION ###########

<<<<<<< HEAD
def timer_on(t):
=======
def timer_on(time):
>>>>>>> 9465950034e75005d21cb3d554b24549bab6155c
    #5 degree tick marks
    #31 marks
    # 16 is center
    #total is 120 degrees
    crickit.servo_1.angle = 0
    time.sleep(1)
<<<<<<< HEAD
    for i in range(0,120, 120//t):
        crickit.servo_1.angle = i
        time.sleep(1)
    crickit.servo_1.angle = 60
=======
    for i in range(0,120, 120/time):
        crickit.servo_1.angle = i
        time.sleep(.1)
>>>>>>> 9465950034e75005d21cb3d554b24549bab6155c


########## START SPEAKING SECTION ###########

def speak(ing):
    pg.init()
    pg.mixer.init()
    led_found()
    if ing=="strawberry":
        pg.mixer.music.load("/home/pi/Desktop/audio/strawberries.wav")
        pg.mixer.music.play()
    if ing=="banana":
        pg.mixer.music.load("/home/pi/Desktop/audio/banana.wav")
        pg.mixer.music.play()
<<<<<<< HEAD
    if ing=="milk" or ing=="carton" or ing=="lactis" or ing=="liquid":
=======
    if ing=="milk":
>>>>>>> 9465950034e75005d21cb3d554b24549bab6155c
        pg.mixer.music.load("/home/pi/Desktop/audio/milk.wav")
        pg.mixer.music.play()
    leds_discovery()

def walkthrough():
    scanned_ings.append("done")
    pg.init()
    pg.mixer.init()

<<<<<<< HEAD
    pg.mixer.music.load("/home/pi/Desktop/audio/i-found.wav")
    pg.mixer.music.play()
    time.sleep(5)

    pg.mixer.music.load("/home/pi/Desktop/audio/instructions-1.wav")
=======
    pg.mixer.music.load("/home/pi/Desktop/audio/instructions-1.wav")
    pg.mixer.music.play()
    time.sleep(5)

    pg.mixer.music.load("/home/pi/Desktop/audio/instructions-2.wav")
>>>>>>> 9465950034e75005d21cb3d554b24549bab6155c
    pg.mixer.music.play()
    time.sleep(15)

<<<<<<< HEAD
    pg.mixer.music.load("/home/pi/Desktop/audio/instructions-2.wav")
=======
    pg.mixer.music.load("/home/pi/Desktop/audio/instructions-3.wav")
>>>>>>> 9465950034e75005d21cb3d554b24549bab6155c
    pg.mixer.music.play()
    time.sleep(15)

<<<<<<< HEAD
    pg.mixer.music.load("/home/pi/Desktop/audio/instructions-3.wav")
=======
    pg.mixer.music.load("/home/pi/Desktop/audio/instructions-4.wav")
>>>>>>> 9465950034e75005d21cb3d554b24549bab6155c
    pg.mixer.music.play()
    time.sleep(10)

<<<<<<< HEAD
    pg.mixer.music.load("/home/pi/Desktop/audio/instructions-4.wav")
    pg.mixer.music.play()
    time.sleep(10)

    pg.mixer.music.load("/home/pi/Desktop/audio/instructions-5.wav")
    pg.mixer.music.play()
    timer_on(15)
    time.sleep(15)

    pg.mixer.music.load("/home/pi/Desktop/audio/recipe-complete.wav")
    pg.mixer.music.play()
=======
    pg.mixer.music.load("/home/pi/Desktop/audio/instructions-5.wav")
    pg.mixer.music.play()
    timer_on(60)
    time.sleep(5)
>>>>>>> 9465950034e75005d21cb3d554b24549bab6155c


########## END SPEAKING SECTION ###########


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
    sound_file = "/home/pi/Desktop/audio/on-sound.wav"
    pg.mixer.music.load(sound_file)
    pg.mixer.music.play()
    time.sleep(5)
    pixels.fill(OFF)
    pixels.show()

def led_found():
    print("GREEN LED")
    pixels.fill(GREEN)
    pixels.show()
#    time.sleep(2)

def leds_on():
    print("PURPLE LED")
    pixels.fill(PURPLE)
    pixels.show()
    leds_discovery()


def leds_discovery():
    for i in range(4):
        print("BLUE LED")
        time.sleep(1)
        pixels.fill(BLUE)
        pixels.show()
        color_chase(BLUE, 0.1)


def main():

    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    # allow the camera to warmup
    time.sleep(0.1)

    while True:
        if testTouch():
            sound_on()
            leds_on()
            crickit.servo_1.angle = 60
            stream(camera)
        else:
            print("searching...")


if __name__ == '__main__':
        main()
