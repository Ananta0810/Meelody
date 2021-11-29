from eyed3 import id3, load, mp3

af = load("Library\Cool Kids.mp3")
duration = af.info.time_secs
freq = af.info.sample_freq
print(freq)
