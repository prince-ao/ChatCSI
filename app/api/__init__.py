from flask_restx import Namespace, Resource
from flask import make_response

api_ns = Namespace('api', description="A namespace for apis")


@api_ns.route("/hello")
class Basic(Resource):
    def post(self):
        response = make_response('<div>hello</div>')
        response.headers['Content-Type'] = 'text/html'
        return response


@api_ns.route('/chat')
class Chat(Resource):
    def post(self):

        return {"message": "boi oh boi"}
