select 
	s.slot_id,
	s.stylist_id,
	s.slot_begin,
	b.booking_id,
	b.client_id
from slots s left join bookings b on s.slot_id=b.slot_id 
where s.stylist_id =%(stylist_id)s and s.slot_begin =%(slot_begin)s
