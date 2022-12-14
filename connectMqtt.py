# André Schaidhauer Luckmann - 4411 - 02


from paho.mqtt import client as mqtt_client

import json
import time
#libs

broker = "test.mosquitto.org"
port = 1883
#broker adress

topic_read = "Liberato/iotTro/44xx/data"
topic_send = "Liberato/iotTro/44xx/rply/19000286"
topic_check = "Liberato/iotTro/44xx/ack/19000286"
topic_error = "Liberato/iotTro/44xx/ack"
#topic addresses

client_id = "André Schaidhauer Luckmann"
seq = 0
matricula = "19000286"
turma = "4411"
alarme = ""
difTemp = 0
tempExt = 0
tempInt = 0
jsonDict = {}
strMsg = ""
connected = False
receivedMsg = False
#variables

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            connected = True
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)

    return client
#connect function

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        if msg.topic == topic_read:
            recado = msg.payload.decode("utf-8")
            print(f"Received `{recado}` from `{msg.topic}` topic")

            jsonDict = json.loads(recado)

            seq = jsonDict["seq"] + 900000
            tempExt = jsonDict["tempExt"]
            tempInt = jsonDict["tempInt"]
            humidade = jsonDict["umidade"]

            if tempExt > tempInt:
                difTemp = round((tempExt - tempInt),1)
                alarme = "Esta mais quente lá fora e ha "
            else:
                difTemp = round((tempInt - tempExt),1)
                alarme = "Esta mais frio lá fora e ha "

            if humidade >= 60:
                alarme += "altas chances de chuva!"
            elif humidade>=45:
                alarme += "chances de chuva."
            else:
                alarme += "baixas chances de chuva."
 
            jsonDict["seq"] = seq
            jsonDict["id"] = client_id
            jsonDict["matricula"] = matricula
            jsonDict["turma"] = turma
            jsonDict["alarme"] = alarme
            jsonDict["difTemp"] = difTemp
            del jsonDict["tempExt"]
            del jsonDict["tempInt"]
            del jsonDict["umidade"]

            jsonMsg = json.dumps(jsonDict)
            #Dict to JSON

            strMsg = str(jsonMsg)
            #json to string

            client.publish(topic_send,strMsg)

            print("\nString Msg:\n",strMsg,"\n")

        if msg.topic == topic_check:
                recado = msg.payload.decode("utf-8")
                print(f"\n{recado}`\n")

        if msg.topic == topic_error:
                recado = msg.payload.decode("utf-8")
                print(f"\n{recado}`\n")

    client.subscribe([(topic_read, 0), (topic_check, 0), (topic_error, 0)]) # Subscribe to Both topics

    client.on_message = on_message #Callback to function on_message

def on_publish(client,userdata,result):
    print(f"Sent Msg!\n")
    pass


def run():
    client = connect_mqtt()
    client.loop_start()
    subscribe(client)
    client.on_publish = on_publish

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print ("exiting")
        client.disconnect()
        client.loop_stop()

run()     