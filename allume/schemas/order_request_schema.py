
from marshmallow import Schema, fields, validates_schema, ValidationError, validates, post_load
from marshmallow.validate import OneOf
from allume.common.model import Model

class OrderRequestSchema(Schema):
	order_id = fields.Str(required=True)
	order_type = fields.Str(required=True, validate=[OneOf(['add_slot','remove_slot','book_appointment','cancel_appointment'])])
	stylist_id = fields.Integer(required=True)
	client_id = fields.Integer()
	slot_begin = fields.DateTime(required=True)
	slot_length_min = fields.Integer(required=True)

	@validates_schema
	def validate_schema(self, data, **kwargs):
		if data['order_type'] in ('book_appointment','cancel_appointment') and not( data.get('client_id')):
			raise ValidationError('client_id cannot be empty.', 'client_id')

	@validates('slot_begin')
	def validate_slot_begin(self, data, **kwargs):
		if not(data.minute % 30 == 0):
			raise ValidationError('Minutes of slot_begin must be either 0 or 30.', 'slot_begin')

	@validates('slot_length_min')
	def validate_slot_length_min(self, data, **kwargs):
		if not(data % 30 == 0):
			raise ValidationError('slot_length_min must be the product of 30.', 'slot_begin')

	@post_load
	def make_object(self, data, many, **kwargs):
		if not data:
			return None
		return Model(**data)