from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import backref
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    reviews = db.relationship('Review', back_populates='customer', lazy='dynamic')

    # Association proxy to directly access items through reviews
    items = association_proxy('reviews', 'item')

    serialize_rules = ('-reviews.customer', '-reviews.item.customers',)

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'

class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    reviews = db.relationship('Review', back_populates='item', lazy='dynamic')

    serialize_rules = ('-reviews.item', '-reviews.customer.items',)

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)

    customer = db.relationship('Customer', back_populates='reviews', lazy='select')
    item = db.relationship('Item', back_populates='reviews', lazy='select')

    serialize_rules = ('-customer.reviews', '-item.reviews',)

    def __repr__(self):
        return f'<Review {self.id}, {self.comment}>'
