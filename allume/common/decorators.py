from functools import wraps
from flask import jsonify, request
from marshmallow import ValidationError
from allume.common.model import Model



def json_validate(schema_cls, many=False):
    def outer_wrapper(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            json_data = request.get_json(silent=True)
            if json_data is None:
                return jsonify({'error': 'Invalid data provided'}), 400

            try:
                data = schema_cls(many=True).load(json_data) if many else schema_cls().load(json_data)
                return function(data, **kwargs)
            except ValidationError as err:
                return jsonify({'error': err.messages}), 400

        return wrapper
    return outer_wrapper


def json_output(schema_cls=None, many=False):
    def outer_wrapper(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            result = function(*args, **kwargs)
            if schema_cls and result:
                result = schema_cls(many=many).dump(result)
            return jsonify(result)
        return wrapper
    return outer_wrapper
