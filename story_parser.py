from flask_restful import reqparse
parser = reqparse.RequestParser()
parser.add_argument('id', required=True, type=int)
parser.add_argument('text')
parser.add_argument('answer')
parser.add_argument('api')
parser.add_argument('proof')
parser.add_argument('answer_choice')
