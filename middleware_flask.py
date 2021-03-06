from flask import Flask
from flask import request
from flask import jsonify
import json
import os

app = Flask(__name__)
zabbix_address = os.environ['ZABBIX']
print("Zabbix Adress: "+zabbix_address)
cantidad_envios={}
diccionario={}
salida={}
@app.route('/wallet/<wallet_id>', methods = ['GET', 'POST'])
def wallet(wallet_id):
    if request.method == 'GET':
        for x in diccionario:
            stream = os.popen("zabbix_sender -z "+zabbix_address+"    -s '"+str(x)+"' -k application.hash -o '"+str(diccionario[x])+"'")
            output = stream.read()
            print("Wallet: "+str(x)+" Hash: "+str(diccionario[x])+" Cantidad envios: "+str(cantidad_envios[x]))
            salida[x] = diccionario[x]
            diccionario[x] = int(0)
            cantidad_envios[x] = int(0)
        return salida
    if request.method == 'POST':
        data = request.json # a multidict containing POST data
        try:
            hostname_minero = next(iter(data))
            diccionario[wallet_id] = int(diccionario[wallet_id]) + int(data[hostname_minero])
            print("Wallet: "+wallet_id+" Hash: "+data[hostname_minero]+" Hostname: "+hostname_minero[:5])
            #1#diccionario[wallet_id] = int(diccionario[wallet_id]) + int(data["value"])
            #1#print("Wallet: "+wallet_id+" Hash: "+data["value"])
        except Exception as e:
            diccionario[wallet_id] = int(data[hostname_minero])
            print("Wallet: "+wallet_id+" Hash: "+data[hostname_minero]+" Hostname: "+hostname_minero[:5])
            #1#diccionario[wallet_id] = int(data["value"])
            #1#print("Wallet: "+wallet_id+" Hash: "+data["value"])
        try:
            cantidad_envios[wallet_id] = cantidad_envios[wallet_id] + " " + hostname_minero[:5]
        except Exception as e:
            cantidad_envios[wallet_id] = hostname_minero[:5]

        return str(diccionario[wallet_id])
if __name__ == '__main__':
   app.run(host= '0.0.0.0')
