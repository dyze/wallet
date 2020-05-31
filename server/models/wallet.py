from mongoengine import *
from models.order import Order
from models.wallet_item import WalletItem
import logging
import tools
from decimal import Decimal


log = logging.getLogger('wallet')


class Wallet(Document):
    name = StringField(required=True)
    balance = DecimalField(min_value=0, precision=2, required=True)
    
        
    def toJSON(self):
        """Converts the object to JSON."""
        
        items = WalletItem.objects(wallet=self.name)
        
        arr = []
        
        for item in items:
            arr.append(item.toJSON())
        
        #data = items.to_json()
        
        return {
            'name': str(self.name),
            'balance': str(self.balance), 
            'items':str(arr)
            }


    def GetAverageCost(self,  stock):
        buy_sum = Decimal('0.00')
        orders = Order.objects(wallet=self.name,  stock=stock,  type='buy')
        
        for order in orders:
            buy_sum += order.amount * order.unitary_price
        log.debug('buy_sum=' + str(buy_sum))
        
        sell_sum = Decimal('0.00')
        orders = Order.objects(wallet=self.name,  stock=stock,  type='sell')
        
        for order in orders:
            sell_sum += order.amount * order.unitary_price
      
        log.debug('sell_sum=' + str(sell_sum))
        wallet_item = WalletItem.objects.get(wallet=self.name,  stock=stock)
        
        new_average_cost = (buy_sum - sell_sum) / wallet_item.amount
        log.debug('new_average_cost=' + str(new_average_cost))
      
        return new_average_cost


    def UpdateWalletItem(self,  stock,  amount,  unitary_price,  type):
        log.info('UpdateWalletItem(' + stock + ',' +  str(amount) + ')...')
        
        try:
            item = WalletItem.objects.get(wallet=self.name,  stock=stock)
            #item = WalletItem.objects.get(wallet = args['wallet'], stock = args['stock'])
                
            log.debug('WalletItem found, update it')
                
            last_amount = item.amount
            
            if type == 'sell':
                if amount > last_amount:
                    log.error("Unsufficient amount left")
                    return tools.HttpHelper.BuildBadRequest("Unsufficient amount left")
                
            if type == 'buy':
                new_amount=  last_amount + amount 
            else:
                new_amount = last_amount - amount
                
            item.amount = new_amount
            return item
                          
        except WalletItem.DoesNotExist:
            # Not found
            log.debug('WalletItem not found, create new one')
            
            last_amount = 0
            new_amount = amount
            
            if type == 'sell':
                log.error('No stock found, invalid buy order')
                return tools.HttpHelper.BuildBadRequest('No stock found, invalid buy order')
            
            item = WalletItem(wallet = self.name, 
                stock = stock, 
                amount = amount, 
                last_unitary_value = unitary_price
            )
            return item
            
        except Exception as e:
            log.error('Exception: ' + str(e))
            return tools.HttpHelper.BuildBadRequest('Exception: ' + str(e))
        
        #return tools.HttpHelper.BuildGoodRequest('Wallet Item updated: last_amount=' + str(last_amount) +  ', new_amount=' + str(new_amount) )

