import madmom
import librosa

song = 'chilling.wav'

print('loading...')
x, sr = librosa.load(song)

print('processing...')
proc = madmom.features.beats.DBNBeatTrackingProcessor(fps=100)
act = madmom.features.beats.RNNBeatProcessor()(song)

beat_times = proc(act) #время битов
print(beat_times)

clicks = librosa.clicks(beat_times, sr=sr, length=len(x))
print('writing...')
librosa.output.write_wav('audio.wav', x + clicks, sr)
