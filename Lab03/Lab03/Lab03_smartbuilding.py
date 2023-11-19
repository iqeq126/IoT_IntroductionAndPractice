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
	print("Topic : " + msg.topic + " | Message : " + msg.payload.decode("utf-8"))
	total = int(msg.payload.decode("utf-8"))
	light, airpurifier = None, None
	if total == 0:
		light = pubClient.publish("building/light", "light off")
		airpurifier = pubClient.publish("building/airpurifier", "airpurifier off")

	elif total == 1:
		light = pubClient.publish("building/light", "light on")
		airpurifier = pubClient.publish("building/airpurifier", "airpurifier off")

	elif total >= 2:
		light = pubClient.publish("building/light", "light on")
		airpurifier = pubClient.publish("building/airpurifier", "airpurifier on")

		airpurifier.wait_for_publish()
	if (airpurifier is not None) and (light is not None):
		light.wait_for_publish()
		airpurifier.wait_for_publish()
		print("Smart Building_publish is success")

buildingClient = mqtt.Client()
buildingClient.on_connect = on_connect
buildingClient.on_message = on_message
buildingClient.connect("localhost")

pubClient = mqtt.Client()
pubClient.connect("localhost")
pubClient.loop_start()

try:
	buildingClient.loop_forever()

except KeyboardInterrupt:
	print("Finished!")
	buildingClient.unsubscribe("building/person")
	buildingClient.disconnect()
	pubClient.disconnect()
