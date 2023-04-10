# trackTxt

Text notifications for approaching trains.

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
