# import pygame

# pygame.mixer.init()
# pygame.mixer.music.load("Library/Graze The Roof.mp3")
# pygame.mixer.music.play(0)
# while pygame.mixer.music.get_busy():
#     pass


import librosa

# y, sr = librosa.load("Library\The Tiger Warrior.mp3")
y, sr = librosa.load("Library\The Tiger Warrior.mp3", sr=44100)
