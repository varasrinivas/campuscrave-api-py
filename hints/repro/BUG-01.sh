#!/usr/bin/env bash
# BUG-01 — the Biryani Bug.
# Several orders hit the same dish in the same instant. Wednesday special,
# Rs.90. Watch the API logs while this runs.
#
# Usage: ./BUG-01.sh   (API must be running on localhost:8080)
#
# Every request gets its own worker thread, so all of them are in flight
# at once. It reproduces warm or cold: no need to restart the API between runs.
#
# Safe to run as many times as you like: it puts the biryani back on the
# shelf, tops the wallets up and clears the order slots first.

BASE=http://localhost:8080
API=$BASE/api/orders
RACERS=8

# Put three portions back and make sure everyone can pay, so this is
# repeatable. Without this, run two fails for reasons that have nothing
# to do with the bug you came here to see.
curl -s -o /dev/null -X PUT "$BASE/api/admin/dishes/1/stock" \
  -H 'Content-Type: application/json' -d '{"stock":3}'
for s in 1 2 3; do
  curl -s -o /dev/null -X POST "$BASE/api/wallet/$s/topup" \
    -H 'Content-Type: application/json' -d '{"amountRupees":1000}'
  # Free up their order slots too — three in flight is the limit.
  for id in $(curl -s "$BASE/api/orders?studentId=$s" \
                | grep -oE '"orderId":[0-9]+' | grep -oE '[0-9]+'); do
    curl -s -o /dev/null -X POST "$BASE/api/orders/$id/cancel"
  done
done

order() {
  curl -s -o /dev/null -w "student $1 -> HTTP %{http_code}\n" "$API" \
    -H 'Content-Type: application/json' \
    -d '{
      "studentId": '"$1"',
      "pickupBlock": "Block C",
      "totalRupees": 90,
      "items": [ { "dishId": 1, "quantity": 1 } ]
    }'
}

echo "12:31 PM. Three biryanis on the shelf."
echo "$RACERS students tap ADD in the same second..."
echo

# The & is the whole experiment: every request is in flight at once.
# More racers than portions is the point — that is what a lunch rush is.
for i in $(seq 1 $RACERS); do
  order $(( (i % 3) + 1 )) &
done
wait

echo
echo "Now check the shelf:"
curl -s "$BASE/api/menu/1" | grep -o '"stock":[^,]*'
echo
echo "Three portions existed. Count the 201s above, and read that number again."
echo "Then look at the API log for what happened to the students who lost."
