from flask import Flask
from flask_restful import reqparse,  Api, Resource
from server import Server
import logging


log = logging.getLogger('wallet')
logging.basicConfig(level=logging.DEBUG)
log.info("server starting...")

server = Server();

app = Flask(__name__)
api = Api(app)


@app.route('/')
def index():
    return "server running"
    
    


class DropDatabase(Resource):
    def get(self):
        return {'instruction': 'Drop database '}, 400
        
    def delete(self):
        log.debug('/drop_database (delete): ')
        return server.DropDatabase()
        
api.add_resource(DropDatabase, '/drop_database')


class CreateWallet(Resource):
    def get(self):
        return {'instruction': 'To create a wallet, you should post json to the /create_wallet URI '
                               'containing the following fields: name, '}, 400
    def post(self):
        create_wallet_parser = reqparse.RequestParser()
        create_wallet_parser.add_argument('name', required=True, location='json', type=str, help='The name of the wallet')
        args = create_wallet_parser.parse_args()
        log.debug('/create_wallet (post): ' + str(args))
        return server.CreateWallet(args['name'])

api.add_resource(CreateWallet, '/create_wallet')


class GetWallet(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, location='json', type=str, help='The name of the wallet')
        args = parser.parse_args()
        log.debug('/get_wallet (get): ' + str(args))
        return server.GetWallet(args['name'])

api.add_resource(GetWallet, '/get_wallet')


class UpdateWallet(Resource):
    def get(self):
        return {'instruction': 'To update a wallet, you should post json to the /update_wallet URI '
                               'containing the following fields: balance, '}, 400
    def post(self):
        create_wallet_parser = reqparse.RequestParser()
        create_wallet_parser.add_argument('name', required=True, location='json', type=str, help='The name of the wallet')
        create_wallet_parser.add_argument('balance', required=True, location='json', type=str, help='The new balance')
        args = create_wallet_parser.parse_args()
        log.debug('/update_wallet (post): ' + str(args))
        return server.UpdateWallet(args['name'],  args['balance'])

api.add_resource(UpdateWallet, '/update_wallet')


class GetWallets(Resource):
    def get(self):
               return server.GetWallets()

api.add_resource(GetWallets, '/get_wallets')


class AddOrder(Resource):
    def get(self):
        return {'instruction': 'To add an order, you should post json to the /add_order URI '
                               'example: '
                               '{"wallet": "pouet", "stock":"company1","amount":100,"unitary_price":1.5,"type":"buy","fees":1.5}'}, 400
                               
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('wallet', required=True, location='json', type=str, help='The name of the wallet')
        parser.add_argument('stock', required=True, location='json', type=str, help='The name of the stock')
        parser.add_argument('amount', required=True, location='json', type=int, help='Amount')
        parser.add_argument('unitary_price', required=True, location='json', type=float, help='Price per stock')
        parser.add_argument('type', required=True, location='json', type=str, help='buy or sell')
        parser.add_argument('fees', required=True, location='json', type=float, help='Fees')
        args = parser.parse_args()
        log.debug('/add_order (post): ' + str(args))
        return server.AddOrder(args['wallet'], args['stock'], args['amount'],  args['unitary_price'],  args['type'],   args['fees'])

api.add_resource(AddOrder, '/add_order')



if __name__ == "__main__":
    app.run()
    
    
