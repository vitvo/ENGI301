# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
Joystick Module : Controlling Cross-Hair on Asteroids
--------------------------------------------------------------------------
License:   
Copyright 2020 Vi Vo

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, 
this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF 
THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------

Use an Analog Thumb Joystick Module with built-in switch to control the 
cross-hair movement on the LED board to play Among Us - Clear Asteroids game

Requirements:
 * 
 *

--------------------------------------------------------------------------
Background Information:
  * Using an analog 2-Axis Thumb Joystick
    * http://msevm.com/2020/lafvin/33/pb.pdf
    
Use the following hardware components to make a mock-up of the Among Us 
Clear Asteroids Game (full hardware and build instructions @ link):
  - HT16K33 Display
  - Analog 2-Axis Thumb Joystick
  - Piezzo Buzzer
  - Adafruit 32x32 RGB Matrix

Requirements:
  - Hardware:
      
    - Joystick Switch/Button
      - Waiting for the joystick press allows the game display to be updated (i.e. asteroids spawn)
      - Any movement when the button is not pressed moves the crosshair on the game display. The RGB Matrix
        should display the game and updated any movements.
      - Time button pressed and released is taken to avoid players spamming the joystick button

Uses:
  - HT16K33 display library developed in class
  - Adapted library for RGB Matrix from Raspberry Pi ()
"""
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.PWM as PWM
import ht16k33 as HT16K33

import asteroids_audio as PiezzoBuzzer
import matrix_display as RGBMatrixDisplay

import random
import time

# ------------------------------------------------------------------------
# Constants / Global Variables 
# ------------------------------------------------------------------------
X_ANALOG_PIN        = "P1_19"
Y_ANALOG_PIN        = "P1_21"
SWITCH_PIN          = "P2_17"
PIEZZO_BUZZER_PWM   = "P2_1"

# ------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------

class CrossHairMove():
    """ Moving the cross hair on LED Panel """
    reset_time  = None
    button      = None
    x_analog    = None
    y_analog    = None
    piezzo      = None
    
    def __init__(self, reset_time=1.5, button=SWITCH_PIN, x_analog=X_ANALOG_PIN, y_analog=Y_ANALOG_PIN, 
                i2c_bus=1, i2c_address=0x70, piezzo=PIEZZO_BUZZER_PWM):
        """ Initialize variables"""
        self.reset_time     = reset_time
        self.button         = button
        self.xmove          = x_analog
        self.ymove          = y_analog
        self.piezzo         = piezzo
        self.display        = HT16K33.HT16K33(i2c_bus, i2c_address)
        self.game_sound     = PiezzoBuzzer.AsteroidsSound()
        self.game_display   = RGBMatrixDisplay.MatrixDisplay(32, 32)
        
        self._setup()
        
    # End def
    
    def _setup(self):
        """ Setup the hardware components."""
        
        # Initialize Button
        GPIO.setup(self.button, GPIO.IN)
        
        # Initialize Display
        self.display.update(0)
        
        # Initialize Joystick Inputs 
        ADC.setup()
        
    # End def
    
    def calibrate(self):
        """Calibrating the joystick module to correct sensitivity and movement"""
        print("Calibrating Joystick Module, DO NOT MOVE JOYSTICK!")
        time.sleep(2.0) # Time for user to read instructions..
        self.x_origin   = ADC.read_raw(self.xmove)
        self.y_origin   = ADC.read_raw(self.ymove)
        
        print("Calibration Finished")
    # End def
        
    def joystick_right(self):
        """ Move the crosshair right """
        if (self.game_display.crosshair_xpos + 1 >= 32):
            self.game_display.crosshair_xpos = 31
        else:
            self.game_display.crosshair_xpos += 1
    # End def
        
    def joystick_left(self):
        """ Move the crosshair left """
        if (self.game_display.crosshair_xpos - 1 < 0):
            self.game_display.crosshair_xpos = 0
        else:
            self.game_display.crosshair_xpos -= 1
    # End def
        
    def joystick_up(self):
        """ Move the crosshair up """
        if (self.game_display.crosshair_ypos + 1 >= 32):
            self.game_display.crosshair_ypos = 31
        else:
            self.game_display.crosshair_ypos += 1
    # End def
        
    def joystick_down(self):
        """ Move the crosshair down """
        if (self.game_display.crosshair_ypos - 1 < 0):
            self.game_display.crosshair_ypos = 0
        else:
            self.game_display.crosshair_ypos -= 1
    # End def
    
    def run(self):
        """Execute the main program."""
        x_position          = 0.0   # X-Position of the cross hair at origin
        y_position          = 0.0   # Y-Position of the cross hair at origin
        asteroids_count     = 0     # Number of asteroids hit to be displayed
        button_press_time   = 0.0   # Time button was pressed (in seconds)
        
        # Start calibration
        self.calibrate()
        
        while(1):
            
            # Wait for button press
            while(GPIO.input(self.button) == 1):
                # Start the game and spawn the asteroids..
                self.game_display.init_game()
                
                x_position  = ADC.read_raw(self.xmove) - self.x_origin
                y_position  = ADC.read_raw(self.ymove) - self.y_origin
                
                # Move the cross hair right
                if x_position > 500:
                    self.joystick_right()
                    
                # Move the cross hair left
                if x_position < -500:
                    self.joystick_left()
                    
                # Move the cross hair down
                if y_position > 50:
                    self.joystick_down()
                    
                # Move the cross hair up
                if y_position < -150:
                    self.joystick_up()
                
                self.game_display.translate_cross_hair(self.game_display.crosshair_xpos, self.game_display.crosshair_ypos, 
                self.game_display.crosshair_color)
                
                # Uncomment to debug the crosshair inputs if necessary
                #print(self.game_display.crosshair_xpos, self.game_display.crosshair_ypos)
                #time.sleep(0.15)
                
                # Un comment to display the game display on RGB Matrix
                self.game_display.display_matrix()

            # Record time
            button_press_time = time.time()

            # Wait for button release
            while(GPIO.input(self.button) == 0):
                pass

            # Compare time to increment or reset asteroids_count
            if time.time() - button_press_time > self.reset_time:
                asteroids_count = 0 
            else:
                # Check if the crosshair is on the asteroid's matrix
                asteroid_click = self.game_display.check_asteroid(self.game_display.crosshair_xpos, self.game_display.crosshair_ypos)
                
                # Sound the weapon fire
                self.game_sound.sound_weaponfire()
                
                # Increment the score if the crosshair selects on the asteroid
                if asteroid_click:
                    asteroids_count += 1
                    self.display.update(asteroids_count)
                    
                    # Sound a randomized noise to notify player asteroid has been destroyed
                    sound_choice = random.randint(1, 3)
                    if sound_choice == 1:
                        self.game_sound.sound_hitasteroids1()
                    elif sound_choice == 2:
                        self.game_sound.sound_hitasteroids2()
                    else:
                        self.game_sound.sound_hitasteroids3()
                
    # End def
    
    def cleanup(self):
        """Cleanup the hardware components."""
        
        # Set Display to something fun to show program is complete
        self.display.set_digit(0, 13)        # "D"
        self.display.set_digit(1, 14)        # "E"
        self.display.set_digit(2, 10)        # "A"
        self.display.set_digit(3, 13)        # "D"
        
    # End def
# End class

# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':
    
    print("Initializing joystick.py")
    crosshair_move = CrossHairMove()
    
    try:
        crosshair_move.run()
    except KeyboardInterrupt:
        # Clean up hardware when exiting
        crosshair_move.cleanup()
    
    print("Program Complete")
