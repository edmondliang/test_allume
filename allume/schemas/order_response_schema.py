from marshmallow import Schema, fields, validates_schema, ValidationError

class OrderResponseSchema(Schema):
	order_id = fields.Str(required=True)
	succeed = fields.Integer(required=True)
