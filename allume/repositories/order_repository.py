import os
from allume.core.db import DBAPI
from allume.common import sql as SQL
from allume.common.model import Model

queries_dir = os.path.join(os.path.dirname(__file__), 'queries')


class OrderRepository:

    def __init__(self, dbapi=DBAPI()):
        self.dbapi = dbapi
        self.table_name = 'orders'

    def get_slot_by_stylist_and_time(self, stylist_id, slot_begin):
        get_sql = SQL.load_from_file(queries_dir, 'get_slot_by_stylist_and_time_with_booking.sql')
        params = {'stylist_id': stylist_id, 'slot_begin': slot_begin}
        with self.dbapi as db:
            result = db.query(get_sql, params).as_dict()
            return Model(**result) if result else None

    def add_slot(self, order, slots):
        insert_order_sql = SQL.insert(order, self.table_name, ['client_id'])
        insert_slot_sql = SQL.load_from_file(queries_dir, 'add_slot.sql')
        with self.dbapi as db:
            db.query(insert_order_sql, order)
            for slot in slots:
                db.query(insert_slot_sql, slot)

    def remove_slot(self, order, slots):
        insert_order_sql = SQL.insert(order, self.table_name, ['client_id'])
        remove_slot_sql = SQL.delete_by_fields('slots', ['stylist_id', 'slot_begin'])
        with self.dbapi as db:
            db.query(insert_order_sql, order)
            for slot in slots:
                db.query(remove_slot_sql, slot)

    def book_appointment(self, order, bookings):
        insert_order_sql = SQL.insert(order, self.table_name, ['client_id'])
        insert_booking_sql = SQL.insert(bookings[0], 'bookings')

        with self.dbapi as db:
            db.query(insert_order_sql, order)
            for booking in bookings:
                db.query(insert_booking_sql, booking)

    def cancel_appointment(self, order, bookings):
        insert_order_sql = SQL.insert(order, self.table_name, ['client_id'])
        remove_booking_sql = SQL.delete_by_fields('bookings', ['booking_id'])

        with self.dbapi as db:
            db.query(insert_order_sql, order)
            for booking in bookings:
                db.query(remove_booking_sql, booking)
