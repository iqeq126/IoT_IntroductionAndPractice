# 제어 프로그램
import paho.mqtt.client as mqtt
import random
import time
global distance # 거리 변수
distance = -1 # 초기값 -1로 지정
# LED 제어기 프로그램 : Lab04_LED로 보내기 위함
LED = [1,2,3] # 1 : Red, 2 : Yellow, 3 : Green을 의미
# mqtt 연결 함수
def on_connect(client, userdata, flags, rc):
    # 거리 데이터의 토픽(sensor/distance)을 구독한다.
	print("connected with result code " + str(rc))
	client.subscribe("sensor/distance")

# mqtt 메시지 함수
def on_message(client, userdata, msg):
	global distance # 거리 변수
    # 받은 토픽 내용
	print("Topic : " + msg.topic + " | Message : " + msg.payload.decode("utf-8"))
	# wait_for_publish를 통해 LED 제어 메시지를 보내기 위한 control 변수
    # control이 정의되었을 때만 publish하기 위해 None으로 지정
	control = None
    # Lab04_distancePub.py : 거리 데이터 제공 프로그램으로부터 수신된 데이터를
    # distance 변수에 저장한다.
	distance = int(msg.payload.decode("utf-8"))
    # 사람이 감지되지 않은 경우
	if distance == 10000:
		control = sensorClient.publish("control/led", str(distance))
	# Red Led High인 경우 : control/led 토픽에 1을 publish
	elif 0<= distance < 20:
		control = sensorClient.publish("control/led", "1")
    # Yellow Led High인 경우 : control/led 토픽에 2을 publish
	elif 20<= distance < 40:
		control = sensorClient.publish("control/led", "2")
	# Green Led High인 경우 : control/led 토픽에 3을 publish
	elif 40<= distance:
                control = sensorClient.publish("control/led", "3")
    # distance 데이터가 존재하여 control이 정의되었을 때
	if control is not None:
        # LED 제어 메시지를 LED 제어기 프로그램에 publish 한다.
		control.wait_for_publish()
		print("control_publish is success")

# LED 제어 메시지 publish를 위한 controlClient
controlClient = mqtt.Client()
controlClient.on_connect = on_connect
controlClient.on_message = on_message
controlClient.connect("localhost")

# 거리 데이터 메시지를 subscribe하기 위한 sensorClient
sensorClient = mqtt.Client()
sensorClient.connect("localhost")
sensorClient.loop_start()

try:
	# 루프 시작
	controlClient.loop_forever()

except KeyboardInterrupt:
	# 키보드 인터럽트 발생 시 구독 및 연결 종료
	print("Finished!")
	controlClient.unsubscribe("sensor/distance")
	controlClient.disconnect()
	sensorClient.disconnect()

