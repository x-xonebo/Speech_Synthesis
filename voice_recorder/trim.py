from pydub import AudioSegment
num = 0
wavString = ".wav"

def cut_audio() :
	audio = AudioSegment.from_wav(str(num)+wavString)
	start_trim = detect_leading_silence(audio)
	end_trim = detect_leading_silence(audio.reverse())

	duration = len(audio)
	trimmed_sound = audio[start_trim:duration-end_trim]
	trimmed_sound.export(str(num)+"_mod"+wavString, format="wav")

	#cut = audio[0:2000]
	#cut.export(str(num)+"_mod"+wavString, format="wav")
#sound = AudioSegment.from_wav(str(i)+s)
#sound = sound.set_channels(1)
#sound.export("sample.wav", format="wav")i


def detect_leading_silence(sound, silence_threshold=-50.0, chunk_size=10):
	trim_ms = 0
	assert chunk_size>0
	while sound[trim_ms+chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
		trim_ms += chunk_size
	return trim_ms

cut_audio()
