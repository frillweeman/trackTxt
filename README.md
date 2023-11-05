# trackTxt

Text notifications for approaching trains.

## Prerequisites
1. Python
2. [ATCS Monitor](https://groups.io/g/ATCSMonitor)

## Setup and Running

1. Clone this repository to your machine.
2. `cd` into `src/`
3. Run `pip install -r requirements.txt`
4. Open ATCS Monitor, and view the dispatch display for the subdivison you'd like to monitor.
5. Take a full-screen screenshot, and upload it to [https://pixspy.com/](https://pixspy.com/). Use the site to identify pixel coordinates of the signals/tracks you'd like to monitor.
6. Create your own version of `BNSF_BrushSub.py` that uses the pixel values you identified.
7. To set up texting, create a free [Twilio](https://www.twilio.com/en-us) account. Set up SMS on their site, which requires getting a phone number from them (free w/ trial credits).
8. Creat a copy of .env.example in the same directory, except name it `.env`. Replace the placeholder values with the actual values from your Twilio account.
9. Make sure nothing is blocking the dispatcher display on your computer, since it works based on automatic screenshots. Then, run `python3 YourFilename.py`, where the filename is what you copied from `BNSF_BrushSub.py`.

## How it Works

1. Takes screenshots of ATCS monitor at regular intervals
1. Analyzes pixels of interest (switches, track occupancy, etc)
1. Feeds that data into a state machine that determines where the train is and what it's doing.
1. Sends the appropriate messages with a link to a railfan camera.

## Plans to Improve

### Headlessness
ATCS Monitor is currently a closed-source Windows application. I don't have much experience with Windows, so I haven't tried to reverse engineer the application to obtain train location info headlessly. I might be able to analyze the network traffic via Wireshark and do it that way. Regardless, if someone wants to fork this and continue development, I'd appreciate it.

### Location Modules
I'd also like to add a more modular system for handling parameters on train movement. For example, the user could choose between NB and SB trains just by choosing the right data source and state machine to use. That would be encapsulated in a module, maybe in a database, so that the main application doesn't need to be modified every time there is a new route.

### Frontend
Eventually, a frontend will be necessary to manage when to receive and what types of notifications to receive per user.
