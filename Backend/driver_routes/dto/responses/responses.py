from marshmallow import Schema, fields

class DashboardResponseDTO(Schema):
    message = fields.String(required=True)

class DisplayRidesResponseDTO(Schema):
    ride_id = fields.String(required=True)
    status = fields.String(required=True)
    departure = fields.String(required=True)
    destination = fields.String(required=True)

class AcceptRideResponseDTO(Schema):
    message = fields.String(required=True)
    ride_id = fields.String(required=True)
    status = fields.String(required=True)
    driver_id = fields.String(required=True)
    accepted_time = fields.DateTime(required=True)

class DeclineRideResponseDTO(Schema):
    message = fields.String(required=True)
    ride_id = fields.String(required=True)
    status = fields.String(required=True)
    driver_id = fields.String(required=True)