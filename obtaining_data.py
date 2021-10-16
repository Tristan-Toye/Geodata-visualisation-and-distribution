import serial
import sys
import json
from pykafka import KafkaClient
from datetime import datetime
from geopy import distance


ruweData=[]
data['auto']= 'Tiny_car'

client = KafkaClient(hosts="localhost:9092")
topic = client.topics['geo_spatial_data']
producer = topic.get_sync_producer()


def opkuis(L):
    data_opkuis=[]
    print("tweede stap")
    for i in range(len(L)):
        data_opkuis.append(float(int(L[i][2:-5])/pow(10, 7)))
    return data_opkuis

def schrijf(L):
    data['tijd'] = str(datetime.utcnow())
    data['key'] = data['auto'] + '_' + str(data['tijd'])
    data['breedtegraad'] = L[0]
    data['lengtegraad'] = L[1]
    opslag_coordinaten.append((L[0],L[1]))
    if len(opslag_coordinaten)>1:
        if len(opslag_coordinaten)>2:
            opslag_coordinaten.pop(0)
        afstand_tussen_twee_punten = (distance.geodesic(opslag_coordinaten[0],opslag_coordinaten[1], ellipsoid='WGS-84').km)*1000     # de ellips wordt wereldwijd gebruikt voor GPS, code: WGS-84
        totale_afstand += afstand_tussen_twee_punten
        data['afgelegde_weg']= totale_afstand
        data['snelheid']= afstand_tussen_twee_punten # steeds 1 s tussen twee punten.
    else:
        data['afgelegde_weg']=0
        data['snelheid']=0

    message = json.dumps(data)
    print(message)
    producer.produce(message.encode('ascii'))
# hier begint de code
try:
    arduino = serial.Serial("COM4",timeout=None, baudrate=9600)
except:
    print('check de USB-poort')
    sys.exit()


while True:
    ruweData.clear()
    for i in range (2):
        ruweData.append(str(arduino.readline()))
    cleanData = opkuis(ruweData)
    schrijf(cleanData)
