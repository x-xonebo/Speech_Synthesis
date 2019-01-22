from pydub import AudioSegment

song = AudioSegment.from_mp3('0.wav')

ten_seconds = 10 * 1000
one_min = ten_seconds * 6

first_10_seconds = song[:ten_seconds]
last_5_seconds = song[0:]

beginning = first_10_seconds +6


beginning.export('result.wav',format='wav', parameters=["-q:a", "10", "-ac", "1"])
