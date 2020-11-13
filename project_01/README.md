Repository for ENGI 301 Project 1 - Clear Asteroids Game with PocketBeagle
- 
Visit the project page on Hackster.io for the build instructions and all of the necessary parts list:
(Link)

Background: 
- 
In recent months, a social deduction game named “Among Us” has begun to rise in popularity. The game involves crew members completing tasks on a spacecraft and finding out the impostor who wants to sabotage their mission by cold, blooded murder. One of the tasks the crew members are required to complete is a game called Clear Asteroids inspired by its arcade counterpart Asteroids! Amidst the development of this project is the COVID-19 Pandemic; With so much uncertainty during these times, setting aside some time to trust-issues with your friends...rephrase setting aside some time to build your logical prowess is a great activity! To pay homage to the game, I want to create a physical manifestation of the Clear Asteroids game with the same recognizable 8-bit PEW-PEW sounds and general game mechanics.

Research and Development:
- 
Taking into account the mechanics of the game, I devise a list of functions I want in the game and how to implement them using the PocketBeagle and good ol’ breadboard. These include:
  1. Added joystick than a push button to offer tilt control.
  2. Create a new algorithm/code for the asteroids where they will be projected in a randomized line rather than dropping directly down like the classic Asteroids game. 
  3. Scoring will be based on the number of asteroids cleared than based on time.
  4. Sounds! Using a passive buzzer to include the music from the game. 

I drew some inspirations from similar projects (although these were made using Arduino IE with C++ language, they still offer some general guidance on the necessary components and wiring):

  - https://create.arduino.cc/projecthub/kreck2003/max72xx-led-matrix-display-asteroids-game-070872
  - https://beagleboard.org/p/JasonLS/pocketinvaders-506e28
*The provided Hackerster.io link has extra links for useful information!

General comments on each components:
  - Joystick Module: 
  - Passive Buzzer:
  - Hex Code Display:
  - RGB Matrix Display:

Software Installations:
-

Necessary installations to the Pocketbeagle:
  ```
  sudo apt-get update
  sudo apt-get install build-essential python-dev python-setuptoolspython-pip python-smbus–y
  sudo apt-get install python3-pip
  sudo sudopip install Adafruit_BBIO
  sudo sudopip install Adafruit_BBIO --upgrade
  sudo apt-get install python3-dev python3-pillow -y
  sudo pip3 install Adafruit-Blinka
  sudo python3 -m pip install --upgrade Pillow
  sudo apt-get install -y libopenjp2-7
  ```

Helpful links and documentation resources:
  - How to set up your Pocketbeagle and get the necessary packages (Adafruit/Python): https://www.fernandomc.com/posts/pocket-beagle-board-getting-started/
  - How to connect the Pocketbeagle to the Internet to install the necessary libraries: https://ofitselfso.com/BeagleNotes/HowToConnectPocketBeagleToTheInternetViaUSB.php
  - Additional link on how to connect the Pocketbeagle to Internet (Windows): https://beagleboard.org/blog/2016-10-19-%E2%80%8Bhow-to-connect-a-beaglebone-black-to-the-internet-using-usb
  - How to autorun Python Script on startup (Linux): https://www.instructables.com/Raspberry-Pi-Launch-Python-script-on-startup/

Device Operation Instructions:
- 
Once you have set up all of the hardware and software for the game following the provided instructions in the Hackter.io page, follow these instructions:

  1. Power the PocketBeagle by plugging in the micro-USB adapter to your laptop or computer and run the script using Python3. Ensure that you DO NOT move the joystick module
  before calibration is finished or it will not move properly. 
  2. To play the game, simply move the joystick to the desired direction. The joystick does not have any sensitivity built-in, so make sure to move the joystick completely left,
  right, up, or down. 
  3. To clear the asteroids, activate the switch of the joystick module by pressing it. The hex display will update with your score once you have successfully cleared the
  asteroid. Every fire will initiate a noise and every clearance will result in a bonus noise!
  4. To stop the game, type CTRL + C to the command line. This will clear the display and you should see the display show “DEAD”. 

Note: The following game still has major bugs with the display. Instead of playing on the Adafruit RGB 32x32 matrix, it is recommended to play with the print lines on the Pocketbeagle command lines. Alternatively, you can hook this up on a smaller display such as a 16x16 LED display or 8x8 LED display and change the dimensions of the display in matrix_display.py file in init_game. 

Current Issues and Improvements:
- 
  1. The game still has major bugs in terms of accounting for the scores and based on how the code is set up, the display updates both the crosshair movement and the movement of 
  the asteroid synchronously which makes it incredibly difficult to detect if someone has cleared the asteroids.
  2. The game is very simplified with the shapes of the asteroids stored as rectangles and the trajectory is a randomized linear line with no built-in velocity adjustment such
  as the ones in the actual Among Us game.
  3. The joystick module only has 4 built-in directions with no sensitivity. Changing the code for the joystick module to account for all movements is a possibility.
  4. The current code works with the Adafruit 32x32 RGB Matrix Display which using the PyLedscape and Image Pillow Module has major issues in updating the display.
