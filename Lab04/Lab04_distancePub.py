# 거리 데이터 제공 프로그램
import paho.mqtt.client as mqtt
import RPi.GPIO as gpio
import time


# PIR센서와 초음파센서의 pin 번호 정의
# trig : GPIO13, echo : GPIO19, PIR : GPIO26
trig_pin = 13
echo_pin = 19
pir_pin = 26

# gpio 초기 상태정의
gpio.setwarnings(False) # gpio 오류를 막기 위해 정의
gpio.setmode(gpio.BCM)
gpio.setup(trig_pin, gpio.OUT)
gpio.setup(echo_pin, gpio.IN)
gpio.setup(pir_pin, gpio.IN)
gpio.output(trig_pin, False)
time.sleep(1)
print("start")

# 연결 함수
def on_connect(client, userdata, flags, rc):
	print("Connected with result code " + str(rc))

# 거리 데이터 publish를 위한 mqttc
mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.connect("localhost")
mqttc.loop_start()


try:
	# 거리 측정을 위한 pulse 변수들
	pulse_end = pulse_start = 0
	# 거리 측정 결과 publish를 위한 루프문
	while True:
		# 사람이 감지되지 않았을 때 실행되는 부분
		# 10,000을 publish하고 사람이 아니라는 뜻인 "Not human" 출력
		while gpio.input(pir_pin) == 0:
			sensor = mqttc.publish("sensor/distance", "10000")
			sensor.wait_for_publish()
			# LED와 distance 상태 출력
			print("Not human")
			print("Distance : ", 10000, "cm")
			time.sleep(5)
		# 사람이 감지되었을 때 실행되는 부분
		# 거리 데이터를 제어 프로그램에 publish.
		gpio.output(trig_pin, False)
		time.sleep(1)
		gpio.output(trig_pin, True)
		time.sleep(1)
		gpio.output(trig_pin, False)
		while gpio.input(echo_pin) == 0:
			pulse_start = time.time()
		while gpio.input(echo_pin) == 1:
			pulse_end = time.time()
		pulse_duration = pulse_end - pulse_start
		distance = pulse_duration * 34000 / 2
		distance = round(distance, 2)
		# int형으로 측정된 거리 데이터를 sensor/distance토픽에 publish
		sensor = mqttc.publish("sensor/distance", int(distance))
		sensor.wait_for_publish()
		# LED와 distance 상태 출력
		if distance > 40:
			print("Green High")
		elif distance > 20:
			print("Yellow High")
		else:
			print("Red High")
		print("Distance : ", distance, "cm")
		time.sleep(3)

# 키보드 인터럽트 발생시 탈출
except KeyboardInterrupt:
	print("FInished!")
	gpio.cleanup()

