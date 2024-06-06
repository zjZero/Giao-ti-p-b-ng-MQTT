import paho.mqtt.client as mqtt
import time
import json

##########Defining all call back functions###################
global A, B, x, y
def on_connect(client,userdata,flags,rc,pro):# called when the broker responds to our connection request
    print("Connected - rc:",rc)
def on_message(client,userdata,message):#Called when a message has been received on a topic that the client has subscirbed to.
    global FLAG
    global chat
    if str(message.topic) == subtop:
        # msg = str(message.payload.decode("utf-8"))
        msg = json.loads(message.payload)
        print(str(message.topic),msg)
        A = msg['Alpha']
        B = msg['Beta']
        x = msg['x']
        y = msg['y']
        print('Góc Alpha:', A)
        print('Góc Beta :', B)
        print('Tọa độ x :', x)
        print('Tọa độ y :', y)
        if msg == "Stop" or msg == "stop":
            FLAG = False

def on_subscribe(client, userdata,mid,granted_qos,pro):##Called when the broker responds to a subscribe request.
    print("Subscribed:", str(mid),str(granted_qos))
def on_unsubscirbe(client,userdata,mid):# Called when broker responds to an unsubscribe request.
    print("Unsubscribed:",str(mid))
def on_disconnect(client,userdata,rc):#called when the client disconnects from the broker
    if rc !=0:
        print("Unexpected Disconnection")


broker_address = "mqtt.eclipseprojects.io" #"mqtt.eclipse.org"
port = 1883

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_subscribe = on_subscribe
client.on_unsubscribe = on_unsubscirbe
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address,port)

time.sleep(1)

pubtop = "/chat/client2"
subtop = "/chat/client1"
FLAG = True
chat = None

def run():
    client.loop_start()
    client.subscribe(subtop)
    while True:
        if FLAG == False or chat == "Stop" or chat == "stop":
            break
    client.disconnect()
    client.loop_stop()

if __name__ == '__main__':
    run()
    