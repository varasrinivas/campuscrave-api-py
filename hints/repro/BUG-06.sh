#!/usr/bin/env bash
# BUG-06 — the dish that sells out forever.
# Order the last portions, cancel, then look at the shelf.
#
# Safe to run repeatedly: it puts stock back, tops the wallet up and frees
# the student's order slots first, so a previous run can't confuse this one.

API=http://localhost:8080
STUDENT=3

# --- reset, so the only thing you see is the bug -------------------------
curl -s -o /dev/null -X PUT "$API/api/admin/dishes/1/stock" \
  -H 'Content-Type: application/json' -d '{"stock":3}'
curl -s -o /dev/null -X POST "$API/api/wallet/$STUDENT/topup" \
  -H 'Content-Type: application/json' -d '{"amountRupees":1000}'
for id in $(curl -s "$API/api/orders?studentId=$STUDENT" \
              | grep -oE '"orderId":[0-9]+' | grep -oE '[0-9]+'); do
  curl -s -o /dev/null -X POST "$API/api/orders/$id/cancel"
done
# ------------------------------------------------------------------------

echo "Biryani stock before:"
curl -s "$API/api/menu/1" | grep -o '"stock":[^,]*'

echo "Ordering 2 biryani..."
RESPONSE=$(curl -s "$API/api/orders" \
  -H 'Content-Type: application/json' \
  -d '{"studentId": '"$STUDENT"', "pickupBlock": "Block C", "totalRupees": 180,
       "items": [ { "dishId": 1, "quantity": 2 } ]}')
ORDER_ID=$(echo "$RESPONSE" | grep -o '"orderId":[0-9]*' | cut -d: -f2)

if [ -z "$ORDER_ID" ]; then
  echo
  echo "The order did not go through, so there is nothing to cancel yet."
  echo "The API said:"
  echo "  $RESPONSE"
  echo
  echo "That is a different problem from the one this script is about."
  echo "If it mentions closing times, boot with ./hints/lab-mode.sh and try again."
  exit 1
fi

echo "Cancelling order $ORDER_ID..."
curl -s -o /dev/null -X POST "$API/api/orders/$ORDER_ID/cancel"

echo "Biryani stock after the cancel:"
curl -s "$API/api/menu/1" | grep -o '"stock":[^,]*'
echo "The student got their money back. Did the kitchen get its biryani back?"
