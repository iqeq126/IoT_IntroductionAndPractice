import paho.mqtt.client as mqtt # MQTT를 사용하기 위해 paho 라이프러리 사용

# 연결 문구 출력
# 만약 mosqitto가 활성화 되어있지 않은 경우 오류 문구를 출력한다.
# 오류가 없는 경우에는 rc에서 0을 출력
def on_connect(client, userdata, flags, rc):
	print("connected with result code " + str(rc))
	client.subscribe("building/light")


# 메시지를 받는 경우
# client에서 subscribe한 채널에서 publish된 msg를 받을 수 있다.
def on_message(client, userdata, msg):
	light = msg.payload.decode("utf-8") # payload는 binary형태로 전달되기에 utf-8로 변환되어야 한다.
	print("Topic : " + msg.topic + " | Message : " + msg.payload.decode("utf-8"))
	print(light)

# lightClient에서 building/light를 subscribe
# lightClient에서 subscribe한 채널에 대한 정보를 받는다.
lightClient = mqtt.Client()
lightClient.on_connect = on_connect
lightClient.on_message = on_message
lightClient.connect("localhost")


try:
	# subscribe한 채널에서 정보를 수신받는다.
	lightClient.loop_forever()
# 키보드 인터럽트 발생시 취소
except KeyboardInterrupt:
	print("Finished!")
	# 구독 해제 및 연결 해제
	lightClient.unsubscribe("building/light")
	lightClient.disconnect()
