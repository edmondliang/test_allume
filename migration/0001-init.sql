CREATE table if not EXISTS orders
(
	order_id text NOT NULL PRIMARY KEY,
    order_type text NOT NULL,
    stylist_id INT NOT NULL,
    client_id INT,
    slot_begin timestamp without time zone NOT NULL,
    slot_length_min INT,
    created timestamp without time zone NOT NULL DEFAULT (now() at time zone 'utc')
);

CREATE table if not EXISTS slots
(
	slot_id SERIAL PRIMARY KEY,
    stylist_id INT NOT NULL,
    slot_begin timestamp without time zone NOT NULL,
    created timestamp without time zone NOT NULL DEFAULT (now() at time zone 'utc'),
    updated timestamp without time zone NOT NULL DEFAULT (now() at time zone 'utc'),
    UNIQUE(stylist_id, slot_begin)
);

CREATE TABLE if not EXISTS bookings
(
    booking_id SERIAL PRIMARY KEY,
    slot_id INT REFERENCES slots(slot_id)
    client_id INT NOT NULL,
    created timestamp without time zone NOT NULL DEFAULT (now() at time zone 'utc'),
    UNIQUE(slot_id)
);
