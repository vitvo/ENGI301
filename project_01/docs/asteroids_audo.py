# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
Play Clear Asteroids Sound on Piezzo Buzzer
--------------------------------------------------------------------------
License:   
Copyright 2020 Vi Vo

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------
Use a Piezzo Buzzer/Passive Buzzer to play Clear Asteroids Sound from the 
Among Us Game when triggered by joystick press/a hit is detected in-game.

Software API:
  PiezzoBuzzer(buzzer = P1_36)
    - Connect the buzzer to a PWM source to control frequency input
    
    create_sound(audio_name):
      - Play a sound on the buzzer given the filename of .txt file containing
        the audio file frequencies separated by a line
        
    clear()
      - Disable and clear the PWM channel to stop the sound

--------------------------------------------------------------------------
Background Information:
  * Using a 5V Piezzo Buzzer/Active Buzzer 
    * http://msevm.com/2020/lafvin/33/pb.pdf
    
Uses:
  * Piezzo Buzzer library developed in class, base code:
    * https://learn.adafruit.com/setting-up-io-python-library-on-beaglebone-black/pwm
  * Frequencies extracted from in-game audio files using MATLAB Audio Toolbox
    * game_audio_hitasteroids1.txt
    * game_audio_hitasteroids2.txt
    * game_audio_hitasteroids3.txt
    * game_audio_weaponfire.txt

"""
import os
import Adafruit_BBIO.PWM as PWM
import time
import math

# ------------------------------------------------------------------------
# Sound Library
# ------------------------------------------------------------------------
WEAPON_FIRE_FILENAME    = "game_audio_weaponfire"
HIT_ASTEROIDS1_FILENAME = "game_audio_hitasteroids1"
HIT_ASTEROIDS2_FILENAME = "game_audio_hitasteroids2"
HIT_ASTEROIDS3_FILENAME = "game_audio_weaponfire"

# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------

class AsteroidsSound():
    """ Class to manage a Piezzo Buzzer """
    piezzo      = None
    init_duty   = None
    sound_delay = None
    
    def __init__(self, piezzo = "P1_36", init_duty = 66, sound_delay = 0.015):
        """ Initialize variables and set up display """
        self.piezzo      = piezzo
        self.init_duty   = init_duty
        self.sound_delay = sound_delay
        
    # End def
    
    def get_audio(self, audio_name):
        """ Extract the list of frequencies from text file """
        audio_file = open(audio_name + ".txt", "r")
        audio_frequency = [math.floor(float((line.strip()))) for line in audio_file]
        audio_file.close()
        return audio_frequency
        
    # End def
    
    def sound_game(self, audio_frequency): 
        """ Control the I/O of the sound """
        PWM.start(self.piezzo, self.init_duty)   #Starts with 66% of 5V, 3.3V supply to piezzo buzzer
        
        # Play the sound
        for frequency in audio_frequency:
            PWM.set_frequency(self.piezzo, frequency)
            time.sleep(self.sound_delay)
            
        # Stop the sound
        PWM.stop(self.piezzo)

    # End def
    
    def create_sound(self, audio_name):
        """ Retrieve the audio file and play on Piezzo """
        # Retrieve the audio file with the listed frequencies
        audio_frequency = self.get_audio(audio_name)
        
        # Play the sound using the frequencies
        self.sound_game(audio_frequency)
        
    # End def
    
    def sound_weaponfire(self):
        """ Play the audio of the weapon firing """
        self.create_sound(WEAPON_FIRE_FILENAME)
        
    # End def
        
    def sound_hitasteroids1(self):
        """ Play the audio of the asteroids being cleared (1st variation) """
        self.create_sound(HIT_ASTEROIDS1_FILENAME)
        
    # End def
        
    def sound_hitasteroids2(self):
        """ Play the audio of the asteroids being cleared (2nd variation) """
        self.create_sound(HIT_ASTEROIDS2_FILENAME)
        
    # End def
        
    def sound_hitasteroids3(self):
        """ Play the audio of the asteroids being cleared (3rd variation) """
        self.create_sound(HIT_ASTEROIDS3_FILENAME)

    # End def
    
    def clear(self):
        """Cleans and disables the PMW channel"""
        PWM.stop(self.piezzo)
        PWM.cleanup()
        
    # End def

# End class
