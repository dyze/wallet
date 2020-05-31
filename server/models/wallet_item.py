from mongoengine import *


class WalletItem(Document):
    wallet = StringField(required=True)
    stock =  StringField(required=True)
    amount = IntField(required=True)
    last_unitary_value = DecimalField(min_value=0, precision=2)
    average_cost = DecimalField(min_value=0, precision=2)

    def toJSON(self):
        """Converts the object to JSON."""
                
        return {
            'wallet': str(self.wallet),
            'stock': str(self.stock), 
            'amount':self.amount, 
            'last_unitary_value':self.last_unitary_value, 
            'average_cost':self.average_cost
            }
