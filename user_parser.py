from flask_restful import reqparse
parser = reqparse.RequestParser()
parser.add_argument('id', required=True, type=int)
parser.add_argument('nickname')
parser.add_argument('password')
parser.add_argument('submit')
parser.add_argument('watched')
