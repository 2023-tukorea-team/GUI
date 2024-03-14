import paho.mqtt.client as mqtt

def message(client,data,message):
    print("received message: "+str(message.payload))

broker_add="15.164.151.155"
broker_port=1883

client=mqtt.Client("rpi_client")
client.on_message=message
client.connect(broker_add,broker_port)

client.subscribe("request")
client.subscribe("code")


client.loop_forever()