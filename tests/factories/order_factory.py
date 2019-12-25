import factory
from factory import fuzzy
from allume.common.model import Model
import datetime
from datetime import timezone


class OrderFactory(factory.Factory):
	class Meta:
		model = Model

	order_id = fuzzy.FuzzyText(length=100)
	order_type = 'add_slot'
	stylist_id = fuzzy.FuzzyInteger(100,100000)
	slot_begin = factory.fuzzy.FuzzyDateTime(
    	datetime.datetime(2000, 1, 1, tzinfo=timezone.utc),
		datetime.datetime.now( tz=timezone.utc),
		force_minute=0,
		force_second=0,
		force_microsecond=0
	)
	slot_length_min = fuzzy.FuzzyInteger(30,300,30)