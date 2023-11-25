import paho.mqtt.client as mqtt # MQTT를 사용하기 위해 paho 라이프러리 사용

# 연결 문구 출력
# 만약 mosqitto가 활성화 되어있지 않은 경우 오류 문구를 출력한다.
# 오류가 없는 경우에는 rc에서 0을 출력
def on_connect(client, userdata, flags, rc):
	print("connected with result code " + str(rc))
	client.subscribe("building/airpurifier")


# 메시지를 받는 경우
# client에서 subscribe한 채널에서 publish된 msg를 받을 수 있다.
def on_message(client, userdata, msg):
	airpurifier = msg.payload.decode("utf-8") # payload는 binary형태로 전달되기에 utf-8로 변환되어야 한다.
	print("Topic : " + msg.topic + " | Message : " + msg.payload.decode("utf-8"))
	print(airpurifier)

# airpurifierClient에서 building/airpurifier를 subscribe
# airpurifierClient에서 subscribe한 채널에 대한 정보를 받는다.
airpurifierClient = mqtt.Client()
airpurifierClient.on_connect = on_connect
airpurifierClient.on_message = on_message
airpurifierClient.connect("localhost")


try:
	# subscribe한 채널에서 정보를 수신받는다.
	airpurifierClient.loop_forever()
# 키보드 인터럽트 발생시 취소
except KeyboardInterrupt:
	print("Finished!")
	airpurifierClient.unsubscribe("building/airpurifier")
	airpurifierClient.disconnect()
