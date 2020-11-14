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

Software Installations:
-

General comments on each components:
  - Joystick Module
    - Ensure that you use Analog Ref +/- to power the joystick module. The current software of the module only includes 4 basic directions: up, down, left, and right. The 
      controls for the module can be viewed in play_asteroids_game.py. Due to the fluctuations of the analog readings and sensitivity of the joystick module, please do not
      touch it until calibration is finished (this message will be displayed in cloud9 command line). Additional information can be viewed in play_asteroids_game.py header.
  - Piezzo Buzzer
    - The frequencies used for this project were obtained using MATLAB Audio Toolbox which takes in a .ogg file and detects the frequencies of the track. See the provided
      Matlab code for additional information. You can generate your own list of frequencies to extract with correct audio format! The .m file will generate a matrix to your
      workspace. To convert this to a .txt file, simply open an empty text editor, copy and paste the contents of the matrix by double clicking the variable in the workspace,
      and save! Make sure each line of .txt file represents one frequency. 
  - Hex Code Display
    - Once you press the joystick module, the code will detect if the center of the crosshair is on an asteroid. If it is, your score will update on the hex code display.
  - RGB Matrix Display:
    - Please follow the hardware installations instructions carefully: https://learn.adafruit.com/32x16-32x32-rgb-led-matrix/
    - The current code uses the Image Pillow Module and PyLedscape (received from Professor Erik Welsh which has been adapted from Keith Henrickson     
      https://github.com/KeithHenrickson/LEDscape with limited supported for the RGB 32x32 Matrix. Ensure that the pins are correctly configured using configure_pins.sh 
      in the zip file and UIO have been successfully set up. Alternatively, the display can be displayed using pin configurations. Please see this link for additional 
      information: https://learn.adafruit.com/connecting-a-16x32-rgb-led-matrix-panel-to-a-raspberry-pi/experimental-python-code/.

**Required Packages and Libraries**
Enter the following command in the command:
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

**Python Code**
Download all of the files in ENGI301/project_01/docs (excluding extractaudiofrequency.m) and unzip the folder for pyledscape.zip. Move all of the code files into
pyledscape folder in the unzip folder (this provides the most direct way to run the code). You can change the permissions of the run script to auto-run the game
on boot, please see the 4th link below on more detail instructions. Before setting the code on auto-run, ensure that you have tested out the code after configuring the pins
by `sudo bash configure_pins.sh` (file provided in the zip folder) and successfully enabling the UIO by changing /boot/uEnt.txt file in the Pocketbeagle.

In your Pocketbeagle command line on Cloud9, create a folder to store of all the files using the following commands:

  ```
  mkdir ENGI301
  cd ENGI301
  mkdir clear_asteroids_game
  cd clear_asteroids_game
  ```

Helpful links and documentation resources:
  1. How to set up your Pocketbeagle and get the necessary packages (Adafruit/Python): https://www.fernandomc.com/posts/pocket-beagle-board-getting-started/
  2. How to connect the Pocketbeagle to the Internet to install the necessary libraries: https://ofitselfso.com/BeagleNotes/HowToConnectPocketBeagleToTheInternetViaUSB.php
  3. Additional link on how to connect the Pocketbeagle to Internet (Windows): https://beagleboard.org/blog/2016-10-19-%E2%80%8Bhow-to-connect-a-beaglebone-black-to-the-internet-using-usb
  4. How to autorun Python Script on startup (Linux): https://www.instructables.com/Raspberry-Pi-Launch-Python-script-on-startup/
  5. How to modify Pocketbeagle to use UIO: https://beagleboard.org/static/prucookbook/#io_uio

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

Current Software Issues and Improvements:
- 
  1. The game has major bugs in terms of accounting for the scores and based on how the code is set up, the display updates both the crosshair movement and the movement of 
  the asteroid synchronously which makes it incredibly difficult to detect if someone has cleared the asteroids.
  2. The game is very simplified with the shapes of the asteroids stored as rectangles and the trajectory is a randomized linear line with no built-in velocity adjustment such
  as the ones in the actual Among Us game.
  3. The joystick module only has 4 built-in directions with no sensitivity. Changing the code for the joystick module to account for all movements is a possibility.
