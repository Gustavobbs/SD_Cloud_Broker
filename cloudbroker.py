from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson import json_util
from pprint import pprint
import json
import bson

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://admin:sd1234@ds159184.mlab.com:59184/sd"
mongo = PyMongo(app)

PROV_URL = 'http://127.0.0.1:5001/'
@app.route('/')
def main():
    return 'Welcome to SD'

@app.route('/provedor/cadastrar/<pid>',methods=['POST'])
def init_provedor(pid):
    data = request.get_json()
    mongo.db['vm'].insert_one(
        {
            'pid': pid,
            'vcpu': data['vcpu'],
            'ram': data['ram'],
            'hd': data['hd'],
            'preco':data['preco'],  
            'usando': 'False',
            'reserva': '0'
        })

    return jsonify({'Ok': True})

@app.route('/provedor/search/<pid>', methods=['POST'])
def search_provedor(pid):
    data = request.get_json()
    busca = mongo.db['vm'].find(
        {
            'pid': pid
        }
    )
    return bson.json_util.dumps(busca) 

@app.route('/search',methods=['POST'])
def search_vm():
    data = request.get_json()
    busca = mongo.db['vm'].find(
        {
            'vcpu':{'$gte': data['vcpu']},
            'ram': {'$gte': data['ram']},
            'hd': {'$gte': data['hd']},
            'usando': 'False'
        }
    )
    
    return bson.json_util.dumps(busca)

@app.route('/cliente/reservar/<pid>', methods=['POST'])
def reserve_vm(pid):
    data = request.get_json()
    mongo.db['vm'].update_one(
        {
            'vcpu':data['vcpu'],
            'ram': data['ram'],
            'hd': data['hd'],
        }, {'$set': {'usando':'True', 'reserva':pid}}
    )
    
    return jsonify({'Ok': True})

@app.route('/cliente/consultar/<pid>', methods=['POST'])
def consultar_vm(pid):
    data = request.get_json()
    busca = mongo.db['vm'].find(
        {
            'reserva':pid,
            'usando':'True'
        }
    )
    return bson.json_util.dumps(busca)

@app.route('/cliente/liberar', methods=['POST'])
def liberar_vm():
    data = request.get_json()
    mongo.db['vm'].update_one(
        {
            'vcpu':data['vcpu'],
            'ram':data['ram'],
            'hd':data['hd'],
        }, {'$set': {'usando':'False', 'reserva':'0'}}
    )

    return jsonify({'Ok': True})

if __name__ == '__main__':
    app.run()
