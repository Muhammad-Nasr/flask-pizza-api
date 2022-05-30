from flask import request
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.models.models import User, Order
from http import HTTPStatus
from api import db

order = Namespace('orders', description="Namespace for orders")

order_model=order.model(
    'Order',{
        'id':fields.Integer(description="An ID"),
        'size':fields.String(description="Size of order",required=True,
            enum=['SMALL','MEDIUM','LARGE','EXTRA_LARGE']
        ),
        'order_status':fields.String(description="The status of the Order",
            required=True, enum=['PENDING','IN_TRANSIT','DELIVERED']
        )
    }
)


@order.route('/orders')
class GetCreateOrders(Resource):

    @order.marshal_with(order_model)
    @order.doc(description='retreive all orders')
    @jwt_required()
    def get(self):
        """
        get all orders
        """
        orders = Order.query.all()
        print(orders)
        return orders, HTTPStatus.ACCEPTED


    @order.expect(order_model)
    @order.marshal_with(order_model)
    @jwt_required()
    def post(self):
        """
        create a new order
        """
        username=get_jwt_identity()

        current_user=User.query.filter_by(username=username).first()

        data= request.get_json()
        print(data)
        new_order=Order(
            size=data.get('size'),
            quantity=data.get('quantity'),
            flavour=data.get('flavour')
        )

        new_order.user=current_user
        db.session.add(new_order)
        db.session.commit()
        
        return new_order, HTTPStatus.CREATED


@order.route('/order/<int:order_id>')
class GetUpdateDeleteOrderById(Resource):

    @order.marshal_with(order_model)
    @order.doc(description='retreive an order with id',
    params={"order_id": 'an id for a given order'})
    @jwt_required()
    def get(self, order_id):
        """
        get a specific order by id
        """
        order = Order.query.get_or_404(order_id)
        return order, HTTPStatus.OK

    def put(self, order_id):
        """
        update a specific order by id
        """
        order = Order.query.get_or_404(order_id)
        return order, HTTPStatus.OK


    def delete(self, order_id):
        """
        delete a specific order by id
        """
        order = Order.query.get_or_404(order_id)
        db.session.delete(order)
        db.session.commit()


@order.route('/user/<int:user_id>/orders')
class GetUpdateUserOrders(Resource):
    @order.marshal_with(order_model)
    def get(self, user_id):
        """
        get all orders for a user by user id
        """
        user = User.query.get_or_404(user_id)
        orders  = user.orders
        return orders, HTTPStatus.OK

    def put(self, user_id):
        """
        update orders for a user by user_id
        """
        pass

@order.route('/user/<int:user_id>/order/<int:order_id>')
class GetUpdateDeleteUserOrder(Resource):

    def get(self, user_id, order_id):
        """
        get a specific order for a specific user
        """
        pass

    def put(self, user_id, order_id):
        """
        update a specific order by id
        """
        pass

    def delete(self, user_id, order_id):
        """
        delete a specific order 
        """
        pass
