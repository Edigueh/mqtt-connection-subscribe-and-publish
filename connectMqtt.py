# python3.6

import json

from paho.mqtt import client as mqtt_client


broker = 'test.mosquitto.org'
port = 1883
topic_r = "Liberato/iotTro/44xx/data"
topic_w = "Liberato/iotTro/44xx/rply/19000286"

client_id = 'André Luckmann'
seq = 0
matricula = "19000286"
turma = "4411"
alarme = ""
difTemp = 0
tempExt = 0
tempInt = 0

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        recado = msg.payload.decode('utf-8')
        print(f"Received `{recado}` from `{msg.topic}` topic")

        jsonStr = json.loads(recado)
        seq = jsonStr["seq"] + 900000
        tempExt = jsonStr["tempExt"]
        tempInt = jsonStr["tempInt"]
        humidade = jsonStr["umidade"]

        if tempExt > tempInt:
            difTemp = round((tempExt - tempInt),1)
            alarme = "Está mais quente lá fora e há "
        else:
            difTemp = round((tempInt - tempExt),1)
            alarme = "Está mais frio lá fora e há "
        if humidade >= 60:
            alarme += "altas chances de chuva!"
        else:
            alarme += "baixas chances de chuva."

    client.subscribe(topic_r)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

run()