from flask import Blueprint
from allume.interactors.add_slot_interactor import AddSlotInteractor
from allume.interactors.remove_slot_interactor import RemoveSlotInteractor
from allume.interactors.book_appointment_interactor import BookAppointmentInteractor
from allume.interactors.cancel_appointment_interactor import CancelAppointmentInteractor
from allume.schemas.order_request_schema import OrderRequestSchema
from allume.schemas.order_response_schema import OrderResponseSchema
from allume.common.decorators import json_validate, json_output
from allume.common.model import Model
order_api_bp = Blueprint(__name__, __name__, url_prefix='/order')


@order_api_bp.route('/', methods=['POST'])
@json_validate(OrderRequestSchema, many=True)
@json_output(OrderResponseSchema, many=True)
def process_orders(orders, interactor_mapping={
    'add_slot': AddSlotInteractor(),
    'remove_slot': RemoveSlotInteractor(),
    'book_appointment': BookAppointmentInteractor(),
    'cancel_appointment': CancelAppointmentInteractor()
}):

    result = []
    for order in orders:
        try:
            interactor_mapping.get(order.order_type).execute(order)
            result += [Model(order_id=order.order_id, succeed=1)]
        except Exception as e:
            print(e)
            result += [Model(order_id=order.order_id, succeed=0)]
    return result
