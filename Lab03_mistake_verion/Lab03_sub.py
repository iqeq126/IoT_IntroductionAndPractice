import paho.mqtt.client as mqtt
import random
import time
global total
total = 0
lst = [0, "off", "off"]
num = 0
def on_connect(client, userdata, flags, rc):
	print("connected with result code " + str(rc))
	print("person		|Airpurifier	|Light	")
	client.subscribe("building/person")
	client.subscribe("building/light")
	client.subscribe("building/airpurifier")

def on_message(client, userdata, msg):
	global total
	#print("Topic : " + msg.topic + "Message : " + msg.payload.decode("utf-8"))
	#inout_sign = int(msg.payload.decode("utf-8"))
	num = lst[0]
	if msg.topic == "building/person":
		lst[0] = msg.payload.decode("utf-8")
	if msg.topic == "building/airpurifier":
		lst[1] = msg.payload.decode("utf-8")
	if msg.topic == "building/light":
		lst[2] = msg.payload.decode("utf-8")
		print(*lst, sep="		")
	# print("person : ", total)
	#if temp > 30:
	#	infot = pubClient.publish("room1/aircon", "on")
	#	infot.wait_for_publish()
	#	print("temp : ", temp, "***Air conditioning ON***")
	#elif temp < 22:
	#	infot = pubClient.publish("room1/aircon", "off")
	#	infot.wait_for_publish()
	#	print(*"temp : ", temp, "***Air conditioning OFF***")

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
	subClient.unsubscribe("building/light")
	subClient.unsubscribe("building/airpurifier")
	subClient.disconnect()
	pubClient.disconnect()

