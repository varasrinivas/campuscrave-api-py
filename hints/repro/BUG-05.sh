#!/usr/bin/env bash
# BUG-05 — the fourth order.
# MAX_ACTIVE_ORDERS is 3. Place four dosa orders in a row for the same
# student, then look at the order history and the wallet.
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

WALLET_BEFORE=$(curl -s "$API/api/wallet/$STUDENT" | grep -o '"balanceRupees":[0-9]*' | cut -d: -f2)
echo "Wallet before: Rs.$WALLET_BEFORE"
echo

for i in 1 2 3 4; do
  echo "--- order $i ---"
  curl -s "$API/api/orders" \
    -H 'Content-Type: application/json' \
    -d '{"studentId": '"$STUDENT"', "pickupBlock": "Block C", "totalRupees": 50,
         "items": [ { "dishId": 2, "quantity": 1 } ]}'
  echo
done

WALLET_AFTER=$(curl -s "$API/api/wallet/$STUDENT" | grep -o '"balanceRupees":[0-9]*' | cut -d: -f2)
ACTIVE=$(curl -s "$API/api/orders?studentId=$STUDENT" | grep -c '"status":"PLACED"')

echo
echo "The 4th order was rejected. Was it also... created?"
echo "  wallet:  Rs.$WALLET_BEFORE  ->  Rs.$WALLET_AFTER"
echo "  three orders at Rs.50 should cost Rs.150. Count what actually left."
echo
echo "Look for yourself:"
echo "  curl -s '$API/api/orders?studentId=$STUDENT'   # how many are in there?"
echo "  curl -s '$API/api/wallet/$STUDENT'"
