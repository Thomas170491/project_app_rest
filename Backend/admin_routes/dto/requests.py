from marshmallow import Schema, fields

class SendLinkRequestDTO(Schema):
    email = fields.Email(required=True)
    role = fields.Str(required=True)
    
