from flask_restful import Resource
from app import db
from flask import jsonify

class DocsResource(Resource):
    def get(self,docs):
        return jsonify({
            "test":"111"
        })