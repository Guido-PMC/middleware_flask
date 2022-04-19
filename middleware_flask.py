from flask import Flask
from flask import request
from flask import jsonify
import json
import os

app = Flask(__name__)


diccionario={}
salida={}
@app.route('/wallet/<wallet_id>', methods = ['GET', 'POST'])
def wallet(wallet_id):
    if request.method == 'GET':
        for x in diccionario:
            stream = os.popen("zabbix_sender -z 54.221.75.201    -s '"+str(x)+"' -k application.hash -o '"+str(diccionario[x])+"'")
            output = stream.read()
            print("Wallet: "+str(x)+" Hash: "+str(diccionario[x]))
            salida[x] = diccionario[x]
            diccionario[x] = int(0)
        return salida
    if request.method == 'POST':
        data = request.json # a multidict containing POST data
        try:
            diccionario[wallet_id] = int(diccionario[wallet_id]) + int(data["value"])
        except Exception as e:
            diccionario[wallet_id] = int(data["value"])
        return str(diccionario[wallet_id])
if __name__ == '__main__':
   app.run(host= '0.0.0.0')
