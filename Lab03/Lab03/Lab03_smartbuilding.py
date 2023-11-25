import paho.mqtt.client as mqtt
global total
total = 0
# 연결 문구 출력
# 만약 mosqitto가 활성화 되어있지 않은 경우 오류 문구를 출력한다.
# 오류가 없는 경우에는 rc에서 0을 출력
def on_connect(client, userdata, flags, rc):
	print("connected with result code " + str(rc))
	client.subscribe("building/person")

# 메시지를 받는 경우
# client에서 subscribe한 채널에서 publish된 msg를 받을 수 있다.
def on_message(client, userdata, msg):
	global total# 전체 인원수 정보 받음
	print("Topic : " + msg.topic + " | Message : " + msg.payload.decode("utf-8"))	# Topic과 Message 정보를 출력
	total = int(msg.payload.decode("utf-8")) # 전체 인원수를 total에 저장, payload는 binary형태로 전달되기에 utf-8로 변환되어야 한다.
	light, airpurifier = None, None # light와 airpurifier의 정보를 받았을 때에만 정보를 출력하기 위해 다음과 같이 처리
	# total이 0일 때, 둘 다 Off
	if total == 0:
		light = pubClient.publish("building/light", "light off")
		airpurifier = pubClient.publish("building/airpurifier", "airpurifier off")
	# total이 1일 때, light On, airpurifier Off
	elif total == 1:
		light = pubClient.publish("building/light", "light on")
		airpurifier = pubClient.publish("building/airpurifier", "airpurifier off")
	# total이 2이상일 때, 둘 다 On
	elif total >= 2:
		light = pubClient.publish("building/light", "light on")
		airpurifier = pubClient.publish("building/airpurifier", "airpurifier on")

	# light와 airpurifier의 정보의 수신을 성공했을 때
	if (light is not None) and (airpurifier is not None):
		# 각자의 채널에 publish해준다.
		light.wait_for_publish()
		airpurifier.wait_for_publish()
		# 성공적인 전송을 확인하기 위해 다음 문구를 출력한다
		print("Smart Building_publish is success")

# buildingClient에서 building/person을 subscribe
# buildingClient에서 subscribe한 채널에 대한 정보를 받는다.
buildingClient = mqtt.Client()
buildingClient.on_connect = on_connect
buildingClient.on_message = on_message
buildingClient.connect("localhost")

# pubClient에서 building/light와 building/airpurifier Topic에 publish
# buildingClient의 on_message에서 발행이 진행된다.
pubClient = mqtt.Client()
pubClient.connect("localhost")
pubClient.loop_start()

try:
	# subscribe한 채널에서 정보를 수신받는다.
	buildingClient.loop_forever()

# 키보드 인터럽트 발생시 취소
except KeyboardInterrupt:
	print("Finished!")
	# 구독 해제 및 연결 해제
	buildingClient.unsubscribe("building/person")
	buildingClient.disconnect()
	pubClient.disconnect()


