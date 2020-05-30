import logging
import tools

log = logging.getLogger('wallet')


class Server():
    def __init__(self):
            log.info('Init Server class...')
                
                
    def CreatePortfolio(self,  name):
            log.info('CreatePortfolio(' + name + ')...')
        
            return tools.HttpHelper.BuildGoodRequest('Portfolio created') 
        
        
