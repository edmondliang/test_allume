insert into slots (stylist_id,slot_begin) 
values (%(stylist_id)s,%(slot_begin)s)
ON CONFLICT(stylist_id,slot_begin) DO NOTHING
returning *
