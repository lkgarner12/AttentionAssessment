# Attention Assessment
## What is this for?
This repository sets up the environment for an experiment that assesses attention through responsiveness to changes in a video given a distraction task.

## How does it work?
AttentionAssessment.py streams the test video for the experiment in two phases:
### Phase 1
Keeps the brightness of the video at 75% for at least one and half to two minutes (as defined by `phase_one_length`) to hide any frame buffering and adjust the participant to the experiment environment.

### Phase 2
1. Once Phase 1 is complete, the brightness of the video is turned up to 100%.
2. Black frames start playing at the lowest threshold (50 fps). 
3. The program is open to user input to adjust the brightness of the test video and the frequency of the black frames as they are being viewed by the participant.
4. After thirty seconds, or `distraction_start seconds`, a distraction task will start playing in a second window. The participant will be directed to hit the space bar whenever the letter "A" appears on the screen.
Once the videos end, or the user manually closes out of the program, the following data values will be printed to an excel spreadsheet:
- `time`: the current local time as the process is being run
- `brightness`: the current brightness of the test video at the given time
- `fps`: the frequency of the black frames
- `participant input`: a boolean value representing whether or not the participant has hit the space button
- `correct input`: whether the participant hit the space button when the letter "A" appeared

## What should I do?
1.  Add an "input.mp4" file to the src folder to serve as the test video.
2.  Make sure at least Python 3.8 is installed on your device by running ```python -V``` in your command line. If you do not have Python installed, you can do so from the following link: https://www.python.org/downloads/.
3.  Import opencv using `pip install -m opencv`. 
4.  Run the program from its file path with
>  `python AttentionAssessment.py`, `py AttentionAssessment.py` or `python3 AttentionAssessment.py`.
5.  Adjust the parameters with the following keys:
- *b*: lowers brightness
- *B*: raises brightness
- *f*: lowers fps
- *F*: raises fps
6. Either wait for the video to close, or close out of the experiment using `Ctrl`+`C` so that the data will print to the spreadsheet in the **output** folder.

