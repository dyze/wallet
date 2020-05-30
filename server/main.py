from flask import Flask
from flask_restful import reqparse,  Api, Resource
from server import Server
import logging
import tools

log = logging.getLogger('wallet')
logging.basicConfig(level=logging.DEBUG)
log.info("server starting...")

server = Server();

app = Flask(__name__)
api = Api(app)


@app.route('/')
def index():
    return "server running"
    
    


class Clean(Resource):
    def get(self):
        log.debug('/clean_history (get): ')
        return tools.HttpHelper.BuildGoodRequest('The database was erased.')
        
api.add_resource(Clean, '/clean')





class CreatePortfolio(Resource):
    def get(self):
        return {'instruction': 'To create a portfolio, you should post json to the /create_portfolio URI '
                               'containing the following fields: name, '}, 400
    def post(self):
        create_portfolio_parser = reqparse.RequestParser()
        create_portfolio_parser.add_argument('name', required=True, location='json', type=str, help='The name of the portfolio')
        args = create_portfolio_parser.parse_args()
        log.debug('/create_portfolio (post): ' + str(args))
        return server.CreatePortfolio(args['name'])

api.add_resource(CreatePortfolio, '/create_portfolio')


if __name__ == "__main__":
    app.run()
    
    
