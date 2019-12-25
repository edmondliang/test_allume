from allume.repositories.order_repository import OrderRepository
from allume.common.model import Model
from datetime import timedelta
from allume.common.model import Model

class BookAppointmentInteractor:

	def __init__(self, repo = OrderRepository() ):
		self.repo = repo

	def execute(self, order):
		bookings = []
		slots = [ Model(stylist_id=order.stylist_id, slot_begin=order.slot_begin+timedelta(minutes=i*30)) for i in range(order.slot_length_min//30)]		
		for slot in slots:
			slot_record = self.repo.get_slot_by_stylist_and_time(slot.stylist_id, slot.slot_begin)
			if not slot_record:
				raise Exception(f'Could not find slot at {slot.slot_begin.isoformat()}')
			bookings += [ Model(slot_id=slot_record.slot_id,client_id=order.client_id)]	
		return self.repo.book_appointment(order, bookings)