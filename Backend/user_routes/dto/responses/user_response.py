from marshmallow import Schema, fields

class LoginResponseDTO(Schema):
    message = fields.String(required=True)
    next_page = fields.String(required=True)
   

class OrderRideResponseDTO(Schema):
    message = fields.String(required=True)
    ride_id = fields.String(required=True)
    price = fields.Float(required=True)

class OrderConfirmationResponseDTO(Schema):
    ride_id = fields.String(required=True)
    name = fields.String(required=True)
    departure = fields.String(required=True)
    destination = fields.String(required=True)
    time = fields.String(required=True)

class OrderStatusResponseDTO(Schema):
    ride_id = fields.String(required=True)
    status = fields.String(required=True)

class CalculatePriceResponseDTO(Schema):
    price = fields.Float(required=True)

class PayResponseDTO(Schema):
    ride_id = fields.String(required=True)
    name = fields.String(required=True)
    departure = fields.String(required=True)
    destination = fields.String(required=True)
    time = fields.String(required=True)
    client_id = fields.String(required=True)

class CreatePaymentResponseDTO(Schema):
    approval_url = fields.String(required=True)

class ExecutePaymentResponseDTO(Schema):
    message = fields.String(required=True)
