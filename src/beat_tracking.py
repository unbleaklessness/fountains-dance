import madmom
import librosa

song = '../music/kill-the-universe.wav'

print('loading...')
x, sr = librosa.load(song)

print('processing...')
proc = madmom.features.beats.DBNBeatTrackingProcessor(fps=100)
act = madmom.features.beats.RNNBeatProcessor()(song)

beat_times = proc(act)
print(beat_times)

clicks = librosa.clicks(beat_times, sr=sr, length=len(x))
print('writing...')
librosa.output.write_wav('../music/audio.wav', x + clicks, sr)
