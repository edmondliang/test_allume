from marshmallow import Schema, fields


class OrderResponseSchema(Schema):
    order_id = fields.Str(required=True)
    succeed = fields.Integer(required=True)
