from bregman import Chromagram
audio_file = "music.wav"
F = Chromagram(audio_file, nfft=16384, wfft=8192, nhop=2205)
F.X # all chroma features
F.X[:,0] # one feature