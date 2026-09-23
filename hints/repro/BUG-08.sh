#!/usr/bin/env bash
# BUG-08 — three files, two vocabularies.
# Place an order, then read the raw status the API sends to the browser.
#
# Safe to run repeatedly: it frees the student's order slots and tops the
# wallet up first, so a previous run can't confuse this one.

API=http://localhost:8080
STUDENT=3

# --- reset ---------------------------------------------------------------
curl -s -o /dev/null -X PUT "$API/api/admin/dishes/2/stock" \
  -H 'Content-Type: application/json' -d '{"stock":40}'
curl -s -o /dev/null -X POST "$API/api/wallet/$STUDENT/topup" \
  -H 'Content-Type: application/json' -d '{"amountRupees":1000}'
for id in $(curl -s "$API/api/orders?studentId=$STUDENT" \
              | grep -oE '"orderId":[0-9]+' | grep -oE '[0-9]+'); do
  curl -s -o /dev/null -X POST "$API/api/orders/$id/cancel"
done
# -------------------------------------------------------------------------

RESPONSE=$(curl -s "$API/api/orders" \
  -H 'Content-Type: application/json' \
  -d '{"studentId": '"$STUDENT"', "pickupBlock": "Block C", "totalRupees": 50,
       "items": [ { "dishId": 2, "quantity": 1 } ]}')
ORDER_ID=$(echo "$RESPONSE" | grep -o '"orderId":[0-9]*' | cut -d: -f2)

if [ -z "$ORDER_ID" ]; then
  echo "The order did not go through, so there is no status to read."
  echo "The API said:"
  echo "  $RESPONSE"
  echo
  echo "If it mentions closing times, boot with ./hints/lab-mode.sh and try again."
  exit 1
fi

curl -s "$API/api/orders/$ORDER_ID/status"
echo
echo "Note the exact spelling of every status this API can produce"
echo "(campuscrave_api/models/order_status.py). Then read both of the browser's lists:"
echo "  campuscrave-web/src/components/StatusTimeline.jsx"
echo "  campuscrave-web/src/mocks/handlers.js"
echo "Three files, two dialects. Compare them slowly."
