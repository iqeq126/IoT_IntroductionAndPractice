import paho.mqtt.client as mqtt
import random
import time
global total
total = 0
def getMsg():
	global total
	d = random.randint(0, 1)
	if total == 0 or d == 1:
		total += 1
		d = 1
	elif d == 0:
		total -= 1
	return d
def on_connect(client, userdata, flags, rc):
	print("Connected with result code " + str(rc))

mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.connect("localhost")
mqttc.loop_start()
try:
	while True:
		t = getMsg()
		if t == 0:
			print("person out | now person : ", total)
		elif t == 1:
			print("person in | now person : ", total)
		infot = mqttc.publish("building/person", total)
		infot.wait_for_publish()

		time.sleep(5)

except KeyboardInterrupt:
	print("Finished!")
