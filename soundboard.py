

import pygame, sys
import time
import RPi.GPIO as gpio

from pygame.locals import *

gpio.setmode(gpio.BCM)
gpio.setup(23, gpio.IN, pull_up_down = gpio.PUD_DOWN)
gpio.setup(24, gpio.IN, pull_up_down = gpio.PUD_UP)
gpio.setup(18, gpio.OUT)

def playSound1(channel):
        print('playing sound 1')
        sound_files[1].play()

def playSound2(channel):
        print('playing sound 2')
        sound_files[2].play()

FREQ = 44100
BITSIZE = -16
CHANNELS = 2
BUFFER = 1024
FRAMERATE = 30

BLACK = (0, 0, 0)

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

sounds = ['beep1.ogg', 'beep2.ogg', 'beep3.ogg']
sound_files = []

def main():
        pygame.mixer.pre_init(FREQ, BITSIZE, CHANNELS, BUFFER)
        pygame.init()
        pygame.mixer.init()

        gpio.add_event_detect(23, gpio.FALLING, callback=playSound1, bouncetime=200)
        gpio.add_event_detect(24, gpio.FALLING, callback=playSound2, bouncetime=200)
        
        # set up the game window and screen
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Music Game')

        background = pygame.Surface(screen.get_size())
        background = background.convert()
	
        print 'loading sound files'
        
        for file in sounds:
                temp_sound = pygame.mixer.Sound(file)
                sound_files.append(temp_sound)

        gpio.output(18, gpio.HIGH)
        while 1:
                for event in pygame.event.get():
                        if event.type == QUIT:
                                gpio.remove_event_detect(23)
                                gpio.remove_event_detect(24)
                                gpio.output(18, gpio.LOW)
                                gpio.cleanup()
                                pygame.quit()
                                sys.exit()                                
                                return
                        elif event.type == KEYDOWN:
                                keys = pygame.key.get_pressed()

                                print 'Keydown event detected'
                                
                                if keys[K_ESCAPE]:
                                        gpio.remove_event_detect(23)
                                        gpio.remove_event_detect(24)
                                        gpio.output(18, gpio.LOW)
                                        gpio.cleanup()
                                        pygame.quit()
                                        sys.exit()
                
                time.sleep(0.05)


if __name__ == '__main__': main()
