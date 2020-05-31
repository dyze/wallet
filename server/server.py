import logging
import tools
from mongoengine import *
from models.wallet import Wallet
from models.wallet_item import WalletItem
from models.order import Order


DB_NAME='wallet'


log = logging.getLogger('wallet')
db = connect(DB_NAME)






class Server():
    def __init__(self):
            log.info('Init Server class...')
            
    def DropDatabase(self):
        db.drop_database(DB_NAME)
        connect(DB_NAME)
        return tools.HttpHelper.BuildGoodRequest('Database dropped') 


    def CreateWallet(self,  name):
        log.info('CreateWallet(' + name + ')...')
            
        try:
            Wallet.objects.get(name=name)
            log.info('Name %s already exists. Aborting creation ', name)
            return tools.HttpHelper.BuildBadRequest('The wallet %s already exists.' % (name))

        except DoesNotExist:
            # Not found
            pass
            
        #except Exception as e:
         #   log.error('Exception: ' + str(e))
          #  return tools.HttpHelper.BuildBadRequest('Exception: ' + str(e))
            
            
        # create wallet
        wallet = Wallet(name=name,  balance=0)
        wallet.save()
                
        return tools.HttpHelper.BuildGoodRequest('CreateWallet created') 


    def GetWallets(self):
        return tools.HttpHelper.BuildGoodRequest({'wallets':[wallet.name for wallet in Wallet.objects]}) 


    def GetWallet(self,  name):
        log.debug('GetWallet(' + name + ')...')
        wallet = Wallet.objects.get(name=name)
        return tools.HttpHelper.BuildGoodRequest({'wallet':wallet.toJSON()}) 

    def UpdateWallet(self,  name,  balance):
        log.debug('GetWallet(' + name + ')...')
        wallet = Wallet.objects.get(name=name)
        wallet.balance = balance
        wallet.save()
        return tools.HttpHelper.BuildGoodRequest({'wallet':wallet.toJSON()}) 

    def AddOrder(self,  wallet,  stock,  amount,  unitary_price,  type,  fees):
        log.debug('AddOrder(' + wallet + ',' + stock + ')...')
        
        order = Order(wallet = wallet, 
            stock = stock, 
            amount = amount, 
            unitary_price = unitary_price, 
            type = type, 
            fees = fees
        )
        
        # Check order feasability
        balance_change = order.GetBalanceChange()
        log.debug('balance_change=' + str(balance_change))
        

        
        try:
            wallet = Wallet.objects.get(name=wallet)
            
            new_balance = wallet.balance + balance_change           
            
            if new_balance < 0:
                return tools.HttpHelper.BuildBadRequest('Wallet balance is too low ' + str(wallet.balance))
        except DoesNotExist:
            return tools.HttpHelper.BuildBadRequest('Wallet doesn t exist')
        except Exception as e:
            log.error('Exception: ' + str(e))
            return tools.HttpHelper.BuildBadRequest('Exception: ' + str(e))

        wallet.balance = new_balance

        result = wallet.UpdateWalletItem(stock,  amount,  unitary_price,  type)

        if isinstance(result, WalletItem):
            wallet_item = result
            
            # save all at once
            log.debug('save all at once')
            wallet_item.save();
            order.save()
            wallet.save()
            
            wallet_item.average_cost = wallet.GetAverageCost(stock)
            wallet_item.save()
        else:
            return result            

        log.debug('order applied')
        
        return  tools.HttpHelper.BuildGoodRequest('Order applied') 
        
        

    def DeleteOrder(self,  args):     
        return {'message':'Not implemented'},  501


