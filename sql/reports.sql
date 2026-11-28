-- SeatDesk operations reports. Each query is separated by a "-- R<n>:" label line.

-- R1: bookings, seats and amount per route (non-cancelled bookings only)
SELECT r.origin, r.destination,
       COUNT(b.id) AS bookings,
       SUM(b.seats) AS seats,
       SUM(b.amount_inr) AS amount_inr
FROM bookings b
JOIN trips t ON t.id = b.trip_id
JOIN routes r ON r.id = t.route_id
WHERE b.status <> 'cancelled'
GROUP BY r.id, r.origin, r.destination
ORDER BY r.origin, r.destination;

-- R2: bus types whose non-cancelled booking amount is above 60000
SELECT t.bus_type, SUM(b.amount_inr) AS amount_inr
FROM bookings b
JOIN trips t ON t.id = b.trip_id
WHERE b.status <> 'cancelled'
GROUP BY t.bus_type
HAVING SUM(b.amount_inr) > 60000
ORDER BY t.bus_type;

-- R3: trips that have no booking of any status
SELECT t.id, r.origin, r.destination, COUNT(b.id) AS bookings
FROM trips t
JOIN routes r ON r.id = t.route_id
LEFT JOIN bookings b ON b.trip_id = t.id
GROUP BY t.id, r.origin, r.destination
HAVING COUNT(b.id) = 0
ORDER BY t.id;

-- R4: held bookings created more than 15 minutes before the desk clock
SELECT id, created_at
FROM bookings
WHERE status = 'held' AND created_at < '2026-12-01 08:45:00'
ORDER BY id;

-- R5: ledger entries and amount per entry type
SELECT entry_type, COUNT(*) AS entries, SUM(amount_inr) AS amount_inr
FROM ledger
GROUP BY entry_type
ORDER BY entry_type;
