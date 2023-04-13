# alerts users to trains going NB/EB on BNSF's Brush Sub out of Denver

from PIL import Image, ImageGrab
from texter import sendTextAlert
import time # temp


WAITING = "WAITING"
LEAVING_YARD = "LEAVING_YARD"
CROSSING_JCT = "CROSSING_JCT"

def signalIndication(pixelValue):
  if (pixelValue[0] != 0):
    return "RED"
  elif (pixelValue[1] != 0):
    return "GREEN"

state = WAITING
newState = WAITING
reason = ""

def analyze(imagePath):
  with Image.open(imagePath) as im:
    px = im.load()

  signal_eb_yard_main =  px[934,404]
  signal_eb_coal_1 = px[934,380]
  signal_eb_coal_2 = px[934,356]

  signal_eb_jct = px[1079,380]

  green_eb_coal_1 = signalIndication(signal_eb_coal_1) == "GREEN"
  green_eb_coal_2 = signalIndication(signal_eb_coal_2) == "GREEN"
  green_eb_yard_main = signalIndication(signal_eb_yard_main) == "GREEN"
  green_eb_jct = signalIndication(signal_eb_jct) == "GREEN"
  ebTrainApproachingFromBNSFYard = green_eb_coal_1 or green_eb_coal_2 or green_eb_yard_main

  global state
  global newState
  if (state == LEAVING_YARD):
    if (green_eb_jct):
      newState = CROSSING_JCT
  elif (state == CROSSING_JCT):
    if (not green_eb_jct):
      newState = WAITING
      sendTextAlert("EB BNSF has passed the catch out")
  else: # state == WAITING
    if (ebTrainApproachingFromBNSFYard):
      if (green_eb_jct):
        newState = CROSSING_JCT
      else:
        newState = LEAVING_YARD
      track_name =  green_eb_yard_main and "Main" or green_eb_coal_1 and "Coal 1" or green_eb_coal_2 and "Coal 2"
      sendTextAlert("EB BNSF is leaving the Yard from track: " + track_name)

  print(newState)

  if (newState == WAITING and state != WAITING):
    print("reason: " + reason)

  state = newState

while True:
  # take screenshot of the ATCS screen and analyze it using PIL
  ImageGrab.grab().save("testImages/screenshot.PNG", "PNG")
  analyze("testImages/screenshot.PNG")
  time.sleep(1)
