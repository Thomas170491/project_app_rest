from marshmallow import Schema, fields

class SendLinkResponseDTO(Schema):
    message = fields.Str(required=True)
