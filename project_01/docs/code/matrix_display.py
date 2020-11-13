# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
RGB Matrix Display: Graphics of Clear Asteroids Game
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

Use a RGB 32x32 Matrix to display the Clear Asteroids game graphics from the
Among Us Game. Asteroids are generated and will move to a randomized location.
The crosshair on the matrix will move with each refreshed frame controlled by
the player.

--------------------------------------------------------------------------
Background Information:
  * Using a Adafruit 32x32 RGB Matrix
    * http://msevm.com/2020/lafvin/33/pb.pdf
    
Uses:
  * LEDscape
    * https://beagleboard.org/blog/tag/ledscape
  * Pillow Image Module
    * https://pillow.readthedocs.io/en/stable/reference/Image.html
  * Adapted library for RGB Matrix from Raspberry Pi 
    * Link
"""

import random 
from PIL import Image, ImageFont, ImageDraw
import io
import pyledscape
import time

# ------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------

class MatrixDisplay():
    """ Class to control the matrix display elements """
    width = None
    height = None
    
    def __init__(self, width, height):
        # Matrix dimensions
        self.width = width
        self.height = height
        
        # Screen matrix storage
        self.screen_asteroid = self.create_empty_matrix()
        self.screen_crosshair = self.create_empty_matrix()
        self.screen_display = self.create_empty_matrix()
        
        # Game information
        self.asteroids_start = [0]
        self.asteroids_end = [0]
        self.asteroids_step_size = [0]
        self.asteroids_shape = [0]
        self.asteroid_idx = 1
        self.asteroid_list = [0]
        self.time_delay = 1
        
        self.crosshair_xpos = int((self.width / 2) - 1)
        self.crosshair_ypos = int((self.height / 2) - 1)
        
        # Color settings
        self.crosshair_color = 3
        self.asteroid_color = 7

    # End def
    
    def create_empty_matrix(self, default_value = 0):
        """ Create an empty array to store information """
        empty_mat_display = [[default_value for x in range(self.width)] for x in range(self.height)]
        return empty_mat_display
        
    # End def
    
    def mat_to_rgbdisplay(self):
        """ Translate the array to inputs for im_draw, part of Image Pillow Module """
        # Obtain the new matrix
        self.refresh()
        
        # Obtain the tuples to feed into im_draw
        fill_asteroids  = []
        fill_crosshair  = []
        
        for row in range(self.width):
            for col in range(self.height):
                pixel = self.screen_display[col][row]
                if pixel!=0:
                    if pixel == self.asteroid_color:
                        RGB_matrix_x = row
                        RGB_matrix_y = col
                        fill_asteroids.append((RGB_matrix_x, RGB_matrix_y))
                    else:
                        RGB_matrix_x = row
                        RGB_matrix_y = col
                        fill_crosshair.append((RGB_matrix_x, RGB_matrix_y))
        return fill_asteroids, fill_crosshair
        
    # End def

    def print_display(self):
        """ Print the 'display' on the command screen """
        self.refresh()
        
        for col in range(self.height):
            print(self.screen_display[col])
    
    # End def    
            
    def create_rectangle(self, x1, y1, x2, y2, int_value, mat):
        """ Create a filled rectangle array """
        for col in range(y1, y2):
            for row in range(x1, x2):
                try:
                    mat[col][row] = int_value
                except:
                    pass
                
    # End def
                
    def create_pixel(self, x, y, int_value, mat):
        """ Create a pixel in an array """
        try:
            mat[y][x] = int_value
        except:
            pass
    # End def
        
    def create_cross_hair(self, x, y, integer_value):
        """ Create the shape of the cross-hair for the game """
        # Create the outer-perimeter of the cross-hair
        self.create_rectangle(x - 2, x - 2, y + 3, y + 3, integer_value, self.screen_crosshair)
        
        # Create the inner-perimeter of the cross-hair
        self.create_rectangle(x - 1, x - 1, y + 2, y + 2, 0, self.screen_crosshair)
        
        for add_pix in range(-2, 3):
            self.create_pixel(x, y + add_pix, integer_value, self.screen_crosshair)
            self.create_pixel(x + add_pix, y, integer_value, self.screen_crosshair)
            
    # End def
            
    def check_asteroid(self, x, y):
        """ Check if the pixel selected by the crosshair is a piece of asteroid """
        if self.screen_asteroid[y][x] != 0:
            return 1
            
    # End def
        
    def create_asteroids(self, x, y, shape, integer_value):
        """ Create an asteroid in the array """
        self.create_rectangle(x, y, x+shape[0], y+shape[1], integer_value, self.screen_asteroid)
        
    # End def
    
    def spawn_asteroids(self, integer_value, asteroid_idx):
        """ Create an asteroid in the array and store information on its movement to class """
        # Shape of asteroid
        self.find_shape()
        shape = self.asteroids_shape[asteroid_idx]
        
        # Find the values of the ending coordinate
        end_x_coord = -shape[0]
        end_y_coord = random.randint(0, self.height - shape[1])
        self.asteroids_end.append((end_x_coord, end_y_coord))
        
        # Create an asteroid starting from left size of matrix
        start_x_coord = self.width - shape[0]
        start_y_coord = random.randint(0, self.height - shape[1])
        
        self.create_asteroids(start_x_coord, start_y_coord, shape, integer_value)
        self.asteroids_step_size.append((self.width - shape[0]) * self.time_delay)
        
        # Store the value of the current x, y value 
        self.asteroids_start.append((start_x_coord, start_y_coord))
    
    # End def
        
    def find_shape(self):
        """ Generate a random shape for the spawned asteroids """
        asteroid_shapes = random.choice([(2,2), (3,3), (4,4), (3,2), (4,3), (4,5)])
        self.asteroids_shape.append(asteroid_shapes)
        
    # End def
        
    def translate_asteroids(self, integer_value, asteroid_idx):
        """ Move the asteroids in the array """
        # Shape of asteroid
        shape = self.asteroids_shape[asteroid_idx]
        
        # Find the values of the starting coordinate
        step_size = self.asteroids_step_size[asteroid_idx]
        
        if step_size == 0:
            self.delete_asteroid(asteroid_idx)
        
        if step_size !=0:
            end_point = self.asteroids_end[asteroid_idx]
            start_point = self.asteroids_start[asteroid_idx]

            target_point_x = int((start_point[0] - end_point[0]) / step_size)
            target_point_y = int((start_point[1] - end_point[1]) / step_size)
            target_point = (start_point[0] - target_point_x, start_point[1] - target_point_y)
            self.asteroids_step_size[asteroid_idx] -= 1

            # Remove the original asteroid location
            self.delete_asteroid(asteroid_idx)

            # Create the new asteroid at the new location
            self.create_rectangle(target_point[0], target_point[1], target_point[0] + shape[0], target_point[1] + shape[1],
                                  integer_value, self.screen_asteroid)
            self.asteroids_start[asteroid_idx] = target_point
            
    # End def
        
    def delete_asteroid(self, asteroid_idx):
        """ Remove an asteroid from the array """
        shape = self.asteroids_shape[asteroid_idx]
        start_point = self.asteroids_start[asteroid_idx]
        self.create_rectangle(start_point[0], start_point[1], start_point[0] + shape[0], start_point[1] + shape[1],
                              0, self.screen_asteroid)
                              
    # End def
        
    def translate_cross_hair(self, x, y, integer_value):
        """ Move the crosshair on the array """
        # Clear the previous location of the cross_hair
        self.screen_crosshair = self.create_empty_matrix()
        
        # Create the new center of the cross_hair
        self.create_cross_hair(x, y, integer_value)
        
    # End def
    
    def refresh(self):
        """ Generate the display matrix with the crosshair and asteroids """
        # Combine both matrices...
        for col in range(self.height):
            for row in range(self.width):
                asteroid_val = self.screen_asteroid[col][row]
                crosshair_val = self.screen_crosshair[col][row]
                
                #Make sure the crosshair is always on top
                if crosshair_val == self.crosshair_color:
                    self.screen_display[col][row] = crosshair_val
                elif (crosshair_val !=3) and (asteroid_val !=0):
                    self.screen_display[col][row] = self.asteroid_color
                    
    # End def
                    
    def display_matrix(self):
        """ Display the array on the RGB Matrix """
        im        = Image.new("RGBX", (self.width, self.height), "white")
        im_draw   = ImageDraw.Draw(im)
        disp      = Image.new("RGBX", (self.width, self.height), "black")
        disp_draw = ImageDraw.Draw(disp)
        
        matrix = pyledscape.pyLEDscape()
        
        try:
            # Draw image
            rgb_asteroid, rgb_crosshair = self.mat_to_rgbdisplay()
            
            # Implement the new display...
            im.paste("black", (0, 0, self.width, self.height))
            im_draw.point(rgb_crosshair, fill = (255, 0, 0, 128))
            im_draw.point(rgb_asteroid, fill = (255, 0, 20, 128))
            im_draw.line([(self.crosshair_xpos, self.crosshair_ypos), (self.width - 1, self.height - 1)], fill = (255, 0, 0, 128))
            im_draw.line([(self.crosshair_xpos, self.crosshair_ypos), (0, self.height - 1)], fill = (255, 0, 0, 128))
            
            # Paste the image on the empty display
            region = im.crop((0, 0, self.width, self.height))
            disp.paste(region, (0, 0, self.width, self.height))
            
            matrix.draw(disp)
            time.sleep(5.0)
        except:
            pass
    # End def
                    
    def init_game(self):
        """ Initialize the next frame of the game """
        self.create_cross_hair(self.crosshair_xpos, self.crosshair_ypos, self.crosshair_color)

        # Create the first asteroid to start off the game...
        if self.asteroid_idx == 1:
            self.asteroid_list.append(self.asteroid_idx)
            self.spawn_asteroids(self.asteroid_idx, self.asteroid_idx)
            self.asteroid_idx += 1
        if self.asteroid_idx > 1:
            asteroid_exist = 1
            
            # Check if there is a space for new asteroid (to avoid overcrowding)
            for col in range(self.height):
                for row in range(self.width - 7, self.width):
                    if self.screen_asteroid[col][row] != 0:
                        asteroid_exist = 0
                        break
            if asteroid_exist: 
                # Create a new asteroid if a spot allows it
                self.spawn_asteroids(self.asteroid_idx, self.asteroid_idx)
                self.asteroid_list.append(self.asteroid_idx)
                self.asteroid_idx += 1

        for aster in self.asteroid_list[1:]:
            self.translate_asteroids(aster, aster)
            
        time.sleep(0.15)
        #self.display_matrix()
        
    # End def
    
# End class
