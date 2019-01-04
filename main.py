# -*- coding: utf-8 -*-
from flask import Flask, json, jsonify, abort
from flask_restful import Resource, Api
from eventos import Eventos

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

class get_eventos(Resource):
    def get(self):
        eventos = Eventos()
        res = eventos.get_all()
        if not res.lista:
            return "Oh não! Um erro inesperado ao obter os eventos!", 500
        else:
            res_dict = [x.__dict__ for x in res.lista]
            print (res_dict)
            #("{'eventos: {} }".format(res_dict))
            a = "{ 'eventos' :" + str(res_dict) + "}"
            return jsonify(res_dict)

api.add_resource(HelloWorld, '/')
api.add_resource(get_eventos, '/eventos')

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')