from PIL import Image
from texter import sendTextAlert
import time # temp


WAITING = "WAITING"
APPROACHING = "APPROACHING"

CLEAR = "CLEAR"
OCCUPIED = "OCCUPIED"

def trackOccupancy(pixelValue):
  if (pixelValue[2] != 0):
    return "UNKNOWN"
  elif (pixelValue[0] != 0):
    return OCCUPIED
  else:
    return CLEAR

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

  signal_nb_csxYardA = px[519, 703]
  signal_nb_csxYardB = px[519, 686]
  signal_nb_riverCrossing = px[615, 670]
  signal_nb_postRiver = px[712, 670]

  # track_csxYardA = px[426, 605]
  # track_csxPostYardA = px[470, 589]
  # track_csxYardB = px[431, 589]
  # track_csxPostYardB = px[463, 580]
  # track_csxPreRiver = px[518, 573]
  # track_csxRiverJct = px[562, 573]
  # track_csxRiverCrossing = px[600, 573]
  # track_csxJctToNash = px[638, 573]
  track_csxLocal = px[646, 678]

  nbTrainApproachingFromCSXYard = signalIndication(signal_nb_csxYardA) == "GREEN" or signalIndication(signal_nb_csxYardB) == "GREEN"

  global state
  global newState
  if (state == APPROACHING):
    if (signalIndication(signal_nb_riverCrossing) == "GREEN"):
      if (trackOccupancy(track_csxLocal) == CLEAR):
        newState = WAITING
        reason = "local"
        sendTextAlert("NB CSX has passed (local)")
    elif (signalIndication(signal_nb_csxYardA) == "RED" and signalIndication(signal_nb_csxYardB) == "RED" and signalIndication(signal_nb_riverCrossing) == "RED" and signalIndication(signal_nb_postRiver) == "RED"):
      newState = WAITING
      reason = "passed"
      sendTextAlert("NB CSX has passed")
  else:
    if (nbTrainApproachingFromCSXYard):
      newState = APPROACHING
      sendTextAlert("""NB CSX is Approaching
        https://youtu.be/zvtZVDBPupI""")

  print(newState)

  if (newState == WAITING and state == APPROACHING):
    print("reason: " + reason)

  state = newState

# test data
analyze("testImages/1.PNG")
time.sleep(1)
analyze("testImages/2.PNG")
time.sleep(1)
analyze("testImages/3.PNG")
time.sleep(1)
analyze("testImages/4.PNG")
time.sleep(1)
analyze("testImages/5.PNG")
time.sleep(1)
analyze("testImages/6.PNG")

# TODO: take screenshots of the ATCS screen and analyze them
