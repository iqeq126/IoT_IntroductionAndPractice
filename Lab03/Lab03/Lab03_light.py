import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
	print("connected with result code " + str(rc))
	client.subscribe("building/light")
	#client.subscribe("building/airpurifier")
def on_message(client, userdata, msg):
	light = msg.payload.decode("utf-8")
	print("Topic : " + msg.topic + " | Message : " + msg.payload.decode("utf-8"))
	print(light)

lightClient = mqtt.Client()
lightClient.on_connect = on_connect
lightClient.on_message = on_message
lightClient.connect("localhost")


try:
	lightClient.loop_forever()

except KeyboardInterrupt:
	print("Finished!!")
	lightClient.unsubscribe("building/light")
	#airpurifierClient.unsubscribe("building/airpurifier")
	lightClient.disconnect()
