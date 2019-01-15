# -*- coding: utf-8 -*-

import sys
import psycopg2
import os
import pyaudio
import wave
from array import array

def recordingOne(script, path):
	FORMAT = pyaudio.paInt16
	CHANNELS = 1
	RATE = 16000
	CHUNK = 1024
	RECORD_SECONDS = 30
	THRESHOLD = 50
	THRESHOLD2 = 1000
	FILE_NAME = path

	userInput = "R"
	while userInput[0] == 'R':
		audio = pyaudio.PyAudio()

		stream = audio.open(format = FORMAT, channels = CHANNELS, rate = RATE, input = True, frames_per_buffer = CHUNK)


		print("다음 문장을 읽어 주세요.\n[%s]" % script)
		#os.system("touch %s" % path)

		frames = []
		cnt = 0
		voice_check = False

		for i in range(0, int(RATE/CHUNK * RECORD_SECONDS)):
			if cnt > 10 and i > 50 and voice_check:
				break
			data = stream.read(CHUNK)
			data_chunk = array('h', data)
			len(data_chunk)

			vol = max(data_chunk)
			
			if (voice_check == False and vol >= THRESHOLD2) or voice_check == True:
#`			if (voice_check == False and vol >= THRESHOLD2) or (voice_check == True and vol >= THRESHOLD) :
				print("+", end="")
				frames.append(data)
			else:
				print("-", end="")

			if vol < 1200:
				cnt += 1
			else:
				voice_check = True
				cnt = 0
		print("")
	# end of recording
		stream.stop_stream()
		stream.close()
		audio.terminate()

	# writing to file
		wavfile = wave.open(FILE_NAME, 'wb')
		wavfile.setnchannels(CHANNELS)
		wavfile.setsampwidth(audio.get_sample_size(FORMAT))
		wavfile.setframerate(RATE)
		wavfile.writeframes(b''.join(frames)) # append frames recorded to file
		wavfile.close()

		os.system("afplay %s" % FILE_NAME)
		#print("touch %s" % path)
		userInput = input("다시 녹음 [R->Enter], 종료 [Q->Enter], 계속 [Enter] 입력 :")
		if len(userInput) == 0:
			userInput = 'GO'
		userInput = userInput.upper()
	
	return userInput


# DB 접속
conn = psycopg2.connect(host="10.100.0.2", database="edberg", user="postgres", password="postgres")
cur = conn.cursor()

# user_info Table에서 사용자 목록 가지고 옴
# 1행에 5명씩 보여주고 번호 입력 받아서 사용자 선택
sql = "select * from user_info"
cur.execute(sql)
# fetch everything
result = cur.fetchall()
# number of result
resultnum = len(result)

print ("User List :")

for x in range(resultnum):
	print("%2d. %s" % (x + 1, result[x][1]), end="\t")
	if (x + 1) % 5 == 0:
		print()

userInput = input("Who Are You? (in number) :")	
userNumber = int(userInput) - 1

# userID - DB 상의 uid
# userName - DB 상의 사용자 이름
# userPosition - 녹음 시작할 문장 번호
userID = int(result[userNumber][0])
userName = result[userNumber][1]
userPosition = int(result[userNumber][2])
userDirectory = './%d' % userID
print("You Are %d - %s - %d" % (userID, userName, userPosition))

# ./[userID] 디렉토리 있는지 체크. 없으면 만들기
# TODO

try:
	if not(os.path.isdir(userDirectory)):
		os.makedirs(os.path.join(userDirectory))
except OSError as e:
	if e.error != errno.EEXIST:
		print("Failed to create directory.")
		raise


# sebtence Table에서 문장 목록 가지고 옴
sql = "select * from sentence"
cur.execute(sql)

# sentenced의 개수 : sentenceNum
# TODO
result = cur.fetchall()
sentenceNum = len(result)

# if sentenceNum < userPosition --> 녹음 완료
# TODO
if sentenceNum < userPosition:
	print("이미 녹음이 끝난 사용자 입니다.")
	sys.exit(0)

# 만약 userPosition이 0이다 --> update userPosition to 1
# TODO
if userPosition == 0:
	userPosition = 1
	cur2 = conn.cursor()
	updateSql = "update user_info set position = 1 where user_id = %d" % userID
	cur2.execute(updateSql)
	conn.commit()
	cur2.close()

# [0] - 1 [1] - 2.... n을 읽어야 하니까 [n-1] - n
# loop가 userPosition - 1에서 끝까지
# TODO
recordingResult = ''
for x in range(userPosition - 1, sentenceNum):
	recordingScript = result[x][1]

# fetch한 문장을 보여주고 안내문
# TODO
	wavpath = "./%s/%s.wav" % (userID, x)
	recordingResult = recordingOne(recordingScript, wavpath)
	#TODO x 를 00001 이렇게 변경
	userPosition = userPosition + 1
	cur2 = conn.cursor()
	updateSql = "update user_info set position = %d where user_id = %d" % (userPosition, userID)
	cur2.execute(updateSql)
	conn.commit()
	cur2.close()

	if recordingResult[0] == 'Q':
		break

if recordingResult[0] == 'Q':
	print("참여해 주셔서 감사합니다. 다음 녹음에는 다음 문장부터 이어서 녹음하실 수 있습니다.")
else:
	print("참여해 주셔서 감사합니다. 모든 녹음이 종료되었습니다.")

#close cursor
cur.close()

#close connection
conn.close()
