import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
	print("connected with result code " + str(rc))
	#client.subscribe("building/light")
	client.subscribe("building/airpurifier")
def on_message(client, userdata, msg):
	airpurifier = msg.payload.decode("utf-8")
	print("Topic : " + msg.topic + " | Message : " + msg.payload.decode("utf-8"))
	print(airpurifier)

airpurifierClient = mqtt.Client()
airpurifierClient.on_connect = on_connect
airpurifierClient.on_message = on_message
airpurifierClient.connect("localhost")


try:
	airpurifierClient.loop_forever()

except KeyboardInterrupt:
	print("Finished!!")
	#lightClient.unsubscribe("building/light")
	airpurifierClient.unsubscribe("building/airpurifier")
	airpurifierClient.disconnect()
