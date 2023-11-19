import paho.mqtt.client as mqtt
import random
import time
global total
total = 0
def on_connect(client, userdata, flags, rc):
	print("connected with result code " + str(rc))
	client.subscribe("building/person")

def on_message(client, userdata, msg):
	global total
	print("Topic : " + msg.topic + "Message : " + msg.payload.decode("utf-8"))
	total = int(msg.payload.decode("utf-8"))
	#inout_sign = int(msg.payload.decode("utf-8"))
	#if inout_sign == 1:
	#	total += 1
	#elif inout_sign == 0:
	#	total -= 1
	#print("person : ", total)
	if total >= 1:
		infot = pubClient.publish("building/light", "on")
		infot.wait_for_publish()
		print("person hear | now person : ", total, " ***Buiding Light  ON***")
	elif total == 0:
		infot = pubClient.publish("building/light", "off")
		infot.wait_for_publish()
		print( "person void | new person :", total, "***Building Light  OFF***")

subClient = mqtt.Client()
subClient.on_connect = on_connect
subClient.on_message = on_message
subClient.connect("localhost")

pubClient = mqtt.Client()
pubClient.connect("localhost")
pubClient.loop_start()

try:
	subClient.loop_forever()

except KeyboardInterrupt:
	print("Finished!")
	subClient.unsubscribe("building/person")
	subClient.disconnect()
	pubClient.disconnect()

