from marshmallow import Schema, fields, validate, validates, ValidationError 

class LoginRequestDTO(Schema):
    username = fields.String(required=True, validate=validate.Length(min=1))
    password = fields.String(required=True, validate=validate.Length(min=1))
    remember_me = fields.Bool(missing=False)

class OrderRideRequestDTO(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1))
    departure = fields.String(required=True, validate=validate.Length(min=1))
    destination = fields.String(required=True, validate=validate.Length(min=1))
    time = fields.String(required=True)

class CalculatePriceRequestDTO(Schema):
    departure = fields.String(required=True, validate=validate.Length(min=1))
    destination = fields.String(required=True, validate=validate.Length(min=1))

class CreatePaymentRequestDTO(Schema):
    departure = fields.String(required=True, validate=validate.Length(min=1))
    destination = fields.String(required=True, validate=validate.Length(min=1))

class ExecutePaymentRequestDTO(Schema):
    paymentId = fields.String(required=True)
    PayerID = fields.String(required=True)

class AuthorizationRequestDTO(Schema):
    authorization = fields.String(required=True, load_only=True)

    @validates('authorization')
    def validate_authorization(self, value):
        if not value.startswith("Bearer "):
            raise ValidationError("Invalid authorization header. Must start with 'Bearer '")