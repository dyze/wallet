from mongoengine import *
from datetime import datetime


class Order(Document):
    wallet = StringField(required=True)
    stock =  StringField(required=True)
    amount = IntField(required=True)
    unitary_price = DecimalField(min_value=0, precision=2, required=True)
    type = StringField(choices=('buy', 'sell'), required=True)
    time = DateTimeField(default=datetime.now())
    fees = DecimalField(min_value=0, precision=2, required=True)

    def GetBalanceChange(self):
        if self.type == 'buy':
            return -(self.amount * self.unitary_price + self.fees)
        else:
             return self.amount * self.unitary_price - self.fees
