from marshmallow import Schema, fields

class AcceptRideRequestDTO(Schema):
    ride_id = fields.String(required=True)

class DeclineRideRequestDTO(Schema):
    ride_id = fields.String(required=True)