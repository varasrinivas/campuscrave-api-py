#!/usr/bin/env bash
# BUG-04 — the canteen that closes at breakfast.
# Cutoff is 14:30 IST. Try ordering between 09:00 and 14:30 on a machine
# whose clock is IST (or any zone east of UTC) and read the error carefully.

curl -s http://localhost:8080/api/orders \
  -H 'Content-Type: application/json' \
  -d '{
    "studentId": 3,
    "pickupBlock": "Block C",
    "totalRupees": 50,
    "items": [ { "dishId": 2, "quantity": 1 } ]
  }'
echo
echo "If it's before 14:30 and the canteen claims to be closed:"
echo "what time does the server think it is, and in which timezone?"
