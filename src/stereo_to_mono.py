from pydub import AudioSegment
sound = AudioSegment.from_wav("music.wav")
sound = sound.set_channels(1)
sound.export("music-mono.wav", format="wav")