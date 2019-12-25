from allume.repositories.order_repository import OrderRepository
from allume.common.model import Model
from datetime import timedelta
from allume.common.model import Model

class RemoveSlotInteractor:

	def __init__(self, repo = OrderRepository() ):
		self.repo = repo

	def execute(self, order):
		slots = [ Model(stylist_id=order.stylist_id, slot_begin=order.slot_begin+timedelta(minutes=i*30)) for i in range(order.slot_length_min//30)]
		return self.repo.remove_slot(order, slots)