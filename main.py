# -*- coding: utf-8 -*-
from flask import Flask, json, jsonify, abort
from flask_restful import Resource, Api
from eventos import Eventos

#https://medium.com/the-andela-way/deploying-a-python-flask-app-to-heroku-41250bda27d0

app = Flask(__name__)
api = Api(app)
eventos = Eventos()

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

class get_eventos(Resource):
    def get(self):
        res = eventos.get_all()
        if not res:
            return "Oh não! Um erro inesperado ao obter os eventos!", 500
        else:
            res_dict = [x.__dict__ for x in res]
            print (res_dict)
            #("{'eventos: {} }".format(res_dict))
            a = "{ 'eventos' :" + str(res_dict) + "}"
            return jsonify(res_dict)

class get_events_today(Resource):
    def get(self):
        res = eventos.get_events_today()
        res_dict = [x.__dict__ for x in res]
        return jsonify(res_dict)

api.add_resource(HelloWorld, '/')
api.add_resource(get_eventos, '/eventos')
api.add_resource(get_events_today, '/eventos-hoje')

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')