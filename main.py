import pygame
import time
import os

sound_directory = (f"{os.getcwd()}/audio")


for filename in os.listdir(sound_directory):
    pygame.mixer.init()
    pygame.mixer.music.load(f"{sound_directory}/{filename}")
    pygame.mixer.music.play()
    try:
        while pygame.mixer.music.get_busy():
            time.sleep(1)
    except KeyboardInterrupt():
        print("stop")