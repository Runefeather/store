# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt
"""User models."""
import datetime as dt
from store.compat import basestring
from store.database import Column, Model, SurrogatePK, db, reference_col, relationship
from store.book.models import Book

"""
CREATE TABLE Consists_of (
    order_id VARCHAR(20),
    isbn VARCHAR(13),
    qty INTEGER(100),
    FOREIGN KEY order_id REFERENCES Order(order_id),
    FOREIGN KEY isbn REFERENCES Book(isbn),
    PRIMARY KEY(order_id, isbn)
);
"""
# how do you have a tuple for primary key????
class Order_Consists_Of(SurrogatePK, Model):
    """books one order consists of."""

    __tablename__ = 'consists_of'
    order_id = Column(db.String(80), unique=True, nullable=False)
    # isbn = reference_col('customers', nullable=False)
    # use ForeignKey here
    isbn = Column(db.String(80), unique=True, ForeignKey='book.isbn', nullable=False)

    qty = Column(db.Integer, default=1)

    # what is this for? user = relationship('User', backref='roles')

    def __init__(self, order_id, isbn, **kwargs):
        """Create instance."""
        db.Model.__init__(self, order_id=order_id, isbn=isbn, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Order_Consists_Of({order_id})>'.format(order_id=self.order_id)

    def toJson(self):
        """
        Json because Master Lee said so. 
        Also, because it makes sense and it can be used for views. 
        Yeah.
        """
        return dict(id=self.order_id, isbn=self.isbn, quantity=self.qty)


"""
CREATE TABLE Order_places_order (
    order_id VARCHAR(20),
    customer_id VARCHAR(20)  NOT NULL,
    date DATE,
    qty INTEGER,
    status VARCHAR(20),
    FOREIGN KEY customer_id REFERENCES Customer(customer_id),
    PRIMARY KEY(order_id)
);
"""
# qty is total number of books in 1 order by 1 customer
# Shopping cart part
class Order(Model):
    __tablename__ = 'orders'
    
    order_id = Column(db.String(80), unique=True, nullable=False, primary_key=True)
    # customer_id = Column(db.String(80), unique=True, ForeignKey='user.id', nullable=False)
    customer_id = Column(db.String(80), unique=True, nullable=False)
    date = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    qty = Column(db.Integer, default=1)
    status = Column(db.Boolean(), default=True)

    def __init__(self, order_id, customer_id, **kwargs):
        """Create instance."""
        db.Model.__init__(self, order_id=order_id, customer_id=customer_id, **kwargs)

    @property
    def details(self):
        """order and customer details."""
        return '{0} {1}'.format(self.order_id, self.customer_id)

    @classmethod
    def get_by_id(cls, order_id):
        """Get order by ID."""
        if any(
                (isinstance(order_id, basestring),
                 isinstance(order_id, str)),
        ):
            return cls.query.get(str(order_id))
        return None

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Order({order_id!r})>'.format(order_id=self.order_id)

    def toJson(self):
        """
        More json
        Yeah.
        """
        return dict(id=self.order_id, customer=self.customer_id, status=self.status)

# -------------------------------------------------------------------------------------


"""
CREATE TABLE Consists_of (
    order_id VARCHAR(20),
    isbn VARCHAR(13),
    qty INTEGER(100),
    FOREIGN KEY order_id REFERENCES Order(order_id),
    FOREIGN KEY isbn REFERENCES Book(isbn),
    PRIMARY KEY(order_id, isbn)
);
"""
# qty is number of copies of 1 book for that order id
# order_qty = sum(order_consists_of_qty for every isbn13 in 1 order_id)
class Order_Consists_Of(Model):
    """books one order consists of."""

    __tablename__ = 'consists_of'
    
    # use ForeignKey here
    consists_order_id = Column(db.String(80), db.ForeignKey('orders.order_id'), primary_key=True)
    consists_isbn13 = Column(db.String(80), db.ForeignKey('book.isbn13'), primary_key=True)
    # Non foreign key
    consists_qty = Column(db.Integer, default=1)

    book = db.relationship(Book, backref="consists_of")
    order = db.relationship(Order, backref="consists_of")


    def __init__(self, consists_order_id, consists_isbn13, consists_qty, **kwargs):
        """Create instance."""
        db.Model.__init__(self, consists_order_id=consists_order_id, consists_isbn13=consists_isbn13, consists_qty=consists_qty, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Order_Consists_Of({order_id})>'.format(order_id=self.consists_order_id)

    @classmethod
    def get_by_id(cls, tuplething):
        """Get order by ID."""
        if any(
                (isinstance(tuplething[0], basestring) and isinstance(tuplething[1], basestring),
                 isinstance(tuplething[0], str) and isinstance(tuplething[1], str)),
        ):
            return cls.query.get(tuplething)
        return None

    def toJson(self):
        """
        Json because Master Lee said so. 
        Also, because it makes sense and it can be used for views. 
        Yeah.
        """
        return dict(id=self.consists_order_id, isbn13=self.consists_isbn13, quantity=self.consists_qty)
