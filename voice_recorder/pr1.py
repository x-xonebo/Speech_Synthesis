from pydub import AudioSegment

def detect_leading_silence( sound, silence_threshold = -50.0, chunk_size=10):
	trim_ms = 0
	assert chunk_size >0
	while sound[trim_ms:trim_ms+chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
		trim_ms += chunk_size
	return trim_ms

sound = AudioSegment.from_file("0.wav",format="wav")

start_trim = detect_leading_silence(sound)
end_trim = detect_leading_silence(sound.reverse())

duration= len(sound)
trimmed_sound = sound[start_trim:duration-end_trim]
