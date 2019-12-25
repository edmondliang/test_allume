import os
import json
from flask import current_app
from tests.factories.order_factory import OrderFactory
from allume.repositories.order_repository import OrderRepository
from allume.schemas.order_request_schema import OrderRequestSchema
from allume.common.model import Model
from datetime import timedelta

def test_add_slot(client):
	order = OrderFactory(slot_length_min=90)
	data = [ OrderRequestSchema().dump(order)]
	r = client.post('order/', json = data)
	assert r.status_code == 200
	assert len(r.json)==1
	assert r.json[0]['succeed'] == 1

	slots = [ Model(stylist_id=order.stylist_id, slot_begin=order.slot_begin+timedelta(minutes=i*30)) for i in range(order.slot_length_min//30)]
	for slot in slots:
		assert OrderRepository().get_slot_by_stylist_and_time(slot.stylist_id,slot.slot_begin)

def test_add_overlap_slots(client):
	order1 = OrderFactory(slot_length_min=90)
	order2 = OrderFactory(slot_length_min=90, stylist_id=order1.stylist_id, slot_begin = order1.slot_begin+timedelta(minutes=30))
	data = OrderRequestSchema(many=True).dump([order1, order2])
	r = client.post('order/', json = data)
	assert r.status_code == 200
	assert len(r.json)==2
	assert r.json[0]['succeed'] == 1
	assert r.json[1]['succeed'] == 1

	time_length = (order2.slot_begin+timedelta(minutes = order2.slot_length_min)-order1.slot_begin).seconds//60
	slots = [ Model(stylist_id=order1.stylist_id, slot_begin=order1.slot_begin+timedelta(minutes=i*30)) for i in range(time_length//30)]
	for slot in slots:
		assert OrderRepository().get_slot_by_stylist_and_time(slot.stylist_id,slot.slot_begin)


def test_remove_slot(client):
	add_order = OrderFactory(slot_length_min=90)
	remove_order = OrderFactory(
		stylist_id=add_order.stylist_id,
		order_type='remove_slot',
		slot_begin=add_order.slot_begin+timedelta(minutes=30),
		slot_length_min=30
		)

	data = OrderRequestSchema(many=True).dump([add_order, remove_order])
	r = client.post('order/', json = data)
	assert r.status_code == 200
	assert len(r.json)==2
	assert not OrderRepository().get_slot_by_stylist_and_time(add_order.stylist_id, add_order.slot_begin+timedelta(minutes=30))


def test_book_appointment(client):
	add_order = OrderFactory(slot_length_min=90)
	book_appointment_order = OrderFactory(
		stylist_id=add_order.stylist_id,
		client_id=2222,
		order_type='book_appointment',
		slot_begin=add_order.slot_begin+timedelta(minutes=30),
		slot_length_min=60
		)

	data = OrderRequestSchema(many=True).dump([add_order, book_appointment_order])
	r = client.post('order/', json = data)
	assert r.status_code == 200
	assert len(r.json)==2
	slot1 = OrderRepository().get_slot_by_stylist_and_time(add_order.stylist_id, add_order.slot_begin+timedelta(minutes=30))
	assert slot1 and slot1.booking_id
	slot2 = OrderRepository().get_slot_by_stylist_and_time(add_order.stylist_id, add_order.slot_begin+timedelta(minutes=60))
	assert slot2 and slot2.booking_id


def test_book_appointment_with_empty_slot(client):
	book_appointment_order = OrderFactory(
		client_id=2222,
		order_type='book_appointment',
		slot_length_min=30
		)

	data = OrderRequestSchema(many=True).dump([book_appointment_order])
	r = client.post('order/', json = data)
	assert r.status_code == 200
	assert len(r.json)==1
	assert r.json[0]['succeed'] ==0
	assert not OrderRepository().get_slot_by_stylist_and_time(book_appointment_order.stylist_id, book_appointment_order.slot_begin)


def test_remove_slot_with_appointment(client):
	add_order = OrderFactory(slot_length_min=90)
	book_appointment_order = OrderFactory(
		stylist_id=add_order.stylist_id,
		client_id=2222,
		order_type='book_appointment',
		slot_begin=add_order.slot_begin,
		slot_length_min=30
		)

	remove_order = OrderFactory(
		stylist_id=add_order.stylist_id,
		order_type='remove_slot',
		slot_begin=add_order.slot_begin,
		slot_length_min=30
		)

	data = OrderRequestSchema(many=True).dump([add_order, book_appointment_order, remove_order])
	r = client.post('order/', json = data)
	assert r.status_code == 200
	assert len(r.json)==3
	assert r.json[0]['succeed'] ==1
	assert r.json[1]['succeed'] ==1
	assert r.json[2]['succeed'] ==0
	assert OrderRepository().get_slot_by_stylist_and_time(add_order.stylist_id, add_order.slot_begin)

def test_book_an_appointment_with_multiple_clients(client):
	add_order = OrderFactory(slot_length_min=90)
	book_appointment_order1 = OrderFactory(
		stylist_id=add_order.stylist_id,
		client_id=1111,
		order_type='book_appointment',
		slot_begin=add_order.slot_begin,
		slot_length_min=30
		)

	book_appointment_order2 = OrderFactory(
		stylist_id=add_order.stylist_id,
		client_id=2222,
		order_type='book_appointment',
		slot_begin=add_order.slot_begin,
		slot_length_min=30
		)

	data = OrderRequestSchema(many=True).dump([add_order, book_appointment_order1, book_appointment_order2])
	r = client.post('order/', json = data)
	assert r.status_code == 200
	assert len(r.json)==3
	assert r.json[0]['succeed'] ==1
	assert r.json[1]['succeed'] ==1
	assert r.json[2]['succeed'] ==0
	slot = OrderRepository().get_slot_by_stylist_and_time(add_order.stylist_id, add_order.slot_begin)
	assert slot.client_id==book_appointment_order1.client_id


def test_cancel_appointment(client):
	add_order = OrderFactory(slot_length_min=90)
	book_appointment_order = OrderFactory(
		stylist_id=add_order.stylist_id,
		client_id=2222,
		order_type='book_appointment',
		slot_begin=add_order.slot_begin,
		slot_length_min=30
		)
	cancel_appointment_order = OrderFactory(
		stylist_id=add_order.stylist_id,
		client_id=2222,
		order_type='cancel_appointment',
		slot_begin=add_order.slot_begin,
		slot_length_min=30
		)

	data = OrderRequestSchema(many=True).dump([add_order, book_appointment_order, cancel_appointment_order])
	r = client.post('order/', json = data)
	assert r.status_code == 200
	assert len(r.json)==3

	slot = OrderRepository().get_slot_by_stylist_and_time(add_order.stylist_id, add_order.slot_begin+timedelta(minutes=30))
	assert slot and not slot.booking_id




