import paho.mqtt.client as mqtt # MQTT를 사용하기 위해 paho 라이프러리 사용
import random # getMsg()에서 랜덤한 수를 전달하기 위함.
import time # 3초마다 한 번 씩 보내기 위함
global total # 전역으로 선언. 들어온 인원수를 처리하기 위함.
total = 0
# 들어가고 나간 사람들을 파악하기 위함.
def getMsg():
	# total의 수를 가짐
	global total
	# 0 : 나감, 1 : 들어옴
	d = random.randint(0, 1)
	# d가 1이거나 total이 0명일 때
	if total == 0 or d == 1:
		total += 1 # 총합을 더 해 준다.
		d = 1 # total이 0인데 d도 0인 경우를 반영해주기 위함.
	# 그 이외에 d가 0일 때
	elif d == 0:
		total -= 1 # 총합을 빼 준다.
	return d # 인원을 출력
# 연결 문구 출력
# 만약 mosqitto가 활성화 되어있지 않은 경우 오류 문구를 출력한다.
# 오류가 없는 경우에는 rc에서 0을 출력
def on_connect(client, userdata, flags, rc):
	print("Connected with result code " + str(rc))

# mqtt 클라이언트 시작
# publish 하는 형태
mqttc = mqtt.Client() # mqtt Client 설정
mqttc.on_connect = on_connect # mqtt의 on_connect함수 설정
mqttc.connect("localhost") # 로컬 호스트에 연결
mqttc.loop_start() # mqttc 시작


try:
	while True:
		t = getMsg() 		# 1 or 0, 들어오고 나가는 결과를 저장하는 변수
		# 나가는 경우 출력
		if t == 0:
			print("person out | now person : ", total)
		# 들어오는 경우 출력
		elif t == 1:
			print("person in | now person : ", total)
		# inout 결과를 building/person에 publish
		inout = mqttc.publish("building/person", total)
		inout.wait_for_publish()

		# 문제 조건. 3초에 1번씩 보낸다.
		time.sleep(3)
# 키보드 인터럽트 발행시 취소
except KeyboardInterrupt:
	print("Finished!")
	# 연결 해제
	mqttc.disconnect()











