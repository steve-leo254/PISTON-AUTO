from flask import Flask
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, StringField, FloatField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange
from enum import Enum
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///piston_autos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  # Initialize SQLAlchemy with the Flask app
migrate = Migrate(app, db)




def create_app():
    app = Flask(__name__, static_folder='.', static_url_path='')
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///piston_autos.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    return app


class UserRole(Enum):
    USER = 'USER'
    ADMIN = 'ADMIN'



bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(UserRole), default=UserRole.USER)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[
                       (role.value, role.name) for role in UserRole], validators=[DataRequired()])
    submit = SubmitField('Register')
        



class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    buying_price = db.Column(db.Float, nullable=False)
    selling_price = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)

class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description')
    buying_price = FloatField('Buying Price', validators=[
                              DataRequired(), NumberRange(min=0)])
    selling_price = FloatField('Selling Price', validators=[
                               DataRequired(), NumberRange(min=0)])
    stock_quantity = IntegerField('Stock Quantity', validators=[
                                  DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Add Product')




class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)

    product = db.relationship(
        'Product', backref=db.backref('sales', lazy=True))
    payments = db.relationship('Payments', back_populates='sale')  


class SaleForm(FlaskForm):
    product_id = SelectField('Product', coerce=int,
                             validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[
                            DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Record Sale')

class SaleDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sale.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    purchase_amount = db.Column(db.Float)  

    product = db.relationship('Product', backref=db.backref('sale_details'))
    sale = db.relationship('Sale', backref=db.backref('sale_details'))



class Customers(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sale.id'), nullable=True)
    full_name = db.Column(db.String(255))
    phone_no = db.Column(db.String(13), nullable=False)
    email = db.Column(db.String(255))
    sales = db.relationship('Sale', backref=db.backref('customers'))
    payments = db.relationship('Payments', back_populates='customer')  # Use back_populates


class CustomersForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired()])
    phone_number = IntegerField('phone_number',validators=[
        DataRequired(),NumberRange(min=0)])
    
    submit = SubmitField('Add Customers')




class Employees(db.Model):
    employee_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=True)
    phone_number = db.Column(db.String(13), nullable=False)
    position = db.Column(db.String(255), nullable=True)

class EmployeesForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired()])
    phone_number = StringField('phone_number',validators=[
        DataRequired(),NumberRange(min=0)])
    position = StringField('position',validators=[
        DataRequired()])
    email = StringField('email',validators=[
        DataRequired()])
    submit = SubmitField('Add Employee')



class Payments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sale.id'), nullable=False)
    customer_id = db.Column(
        db.Integer, db.ForeignKey('customers.customer_id'), nullable=False
    )
    sale = db.relationship('Sale', back_populates='payments')
    customer = db.relationship('Customers', back_populates='payments')


class BookingStatus(Enum):
    PENDING = 'PENDING'
    CONFIRMED = 'CONFIRMED'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    customer_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    vehicle_type = db.Column(db.String(100), nullable=True)
    service_type = db.Column(db.String(100), nullable=False)
    service_date = db.Column(db.DateTime, nullable=False)
    special_request = db.Column(db.Text, nullable=True)
    status = db.Column(
        db.Enum(BookingStatus), default=BookingStatus.PENDING, nullable=False
    )
    estimated_total = db.Column(db.Float, nullable=True)


class InvoiceStatus(Enum):
    DRAFT = 'DRAFT'
    SENT = 'SENT'
    PAID = 'PAID'
    OVERDUE = 'OVERDUE'
    CANCELLED = 'CANCELLED'


class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(50), unique=True, nullable=False)
    customer_name = db.Column(db.String(255), nullable=False)
    customer_email = db.Column(db.String(255), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    issue_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum(InvoiceStatus), default=InvoiceStatus.DRAFT, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    tax_rate = db.Column(db.Float, default=16.0, nullable=False)
    tax_amount = db.Column(db.Float, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class InvoiceItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    line_total = db.Column(db.Float, nullable=False)
    
    invoice = db.relationship('Invoice', backref='items')
    product = db.relationship('Product', backref='invoice_items')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    

class BookingForm(FlaskForm):
    customer_name = StringField('Your Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    vehicle_type = StringField('Vehicle Type')
    service_type = SelectField(
        'Service',
        choices=[
            ('general servicing', 'General Servicing'),
            ('diagnostics', 'Diagnostics'),
            ('repair', 'Repair'),
        ],
        validators=[DataRequired()],
    )
    service_date = StringField('Service Date', validators=[DataRequired()])
    special_request = StringField('Special Request')
    submit = SubmitField('Book Now')


class JobPartUsage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(
        db.Integer, db.ForeignKey('booking.id'), nullable=False
    )
    product_id = db.Column(
        db.Integer, db.ForeignKey('product.id'), nullable=False
    )
    quantity_used = db.Column(db.Integer, nullable=False)
    unit_cost = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    booking = db.relationship(
        'Booking', backref=db.backref('parts_used', lazy=True)
    )
    product = db.relationship(
        'Product', backref=db.backref('job_usages', lazy=True)
    )