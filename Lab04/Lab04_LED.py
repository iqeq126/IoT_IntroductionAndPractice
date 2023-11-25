# LED 제어기 프로그램
import paho.mqtt.client as mqtt
import RPi.GPIO as gpio
import time
gpio.setwarnings(False)
# LED 핀 정의_ GPIO5 : Red, GPIO6 : Yellow, GPIO12 : Green
pin = [5, 6, 12]
# Iterative control을 위해 LED와 rgb를 배열로 받음
LED = [1,2,3]
rgb = ['Red', 'Yellow', 'Green'] 

global led # led 상태
led = 0 # 초기값 0
# gpio 초기화
gpio.setmode(gpio.BCM)
gpio.setup(pin, gpio.OUT)

# 연결 함수
# control/led subscribe
def on_connect(client, userdata, flags, rc):
	print("connected with result code " + str(rc))
	client.subscribe("control/led")

# mqtt 메시지 함수
def on_message(client, userdata, msg):
	global led # led 상태
	# subscribe 성공시 publish된 LED 제어 메시지 전달
	if msg.topic == "control/led":
		led = int(msg.payload.decode("utf-8"))
	# 사람이 존재할 때
	# 1일 때 Red, 2일 때 Yellow, 3일 때 Green HIGH
	if led != 10000:
		for i in LED:
			if led == i:
				gpio.output(pin[i-1], True)
			else:
				gpio.output(pin[i-1], False)
		print(rgb[led-1] + " LED is High")
	# 사람이 존재하지 않을 때
	# All LOW
	else:
		gpio.output(pin, False)
	# LED 제어 메시지 결과값 출력
	print("Topic : " + msg.topic + " | Message : " + msg.payload.decode("utf-8"))

# LED 제어 메시지를 subscribe하기 위한 mqtt
ledClient = mqtt.Client()
ledClient.on_connect = on_connect
ledClient.on_message = on_message
ledClient.connect("localhost")


try:
	# 루프 시작
	ledClient.loop_forever()

# 키보드 인터럽트 발생시 control/led 토픽 subscribe 취소
except KeyboardInterrupt:
	print("Finished!!")
	gpio.cleanup()
	ledClient.unsubscribe("control/led")
	ledClient.disconnect()