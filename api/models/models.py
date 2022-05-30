
from enum import Enum

from api import db

class User(db.Model):
    __tablename__= 'users'

    id=db.Column(db.Integer(),primary_key=True)
    email=db.Column(db.String(80),nullable=False,unique=True)
    username = db.Column(db.String(25),nullable=False)
    password_hash=db.Column(db.Text(),nullable=False)
    is_active=db.Column(db.Boolean(),default=True)
    is_staff=db.Column(db.Boolean(),default=False)
    orders=db.relationship('Order',backref='user',lazy=True)

    def __repr__(self):
        f"<User {self.id} {self.username}>"



class Size(Enum):
    SMALL='small'
    MEDIUM='medium'
    LARGE='large'
    EXTRA_LARGE='extra-large'


class OrderStatus(Enum):
    PENDING='pending'
    IN_TRANSIT='in-transit'
    DELIVERED='delivered'


class Order(db.Model):
    __tablename__='orders'

    id=db.Column(db.Integer(),primary_key=True)
    size=db.Column(db.Enum(Size),default=Size.SMALL)
    order_status=db.Column(db.Enum(OrderStatus) ,default=OrderStatus.PENDING)
    flavour=db.Column(db.String(),nullable=False)
    quantity=db.Column(db.Integer())
    customer=db.Column(db.Integer(),db.ForeignKey('users.id'))

    def __str__(self):
        return f"<Order {self.id}>"