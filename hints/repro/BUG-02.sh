#!/usr/bin/env bash
# BUG-02 — the menu that queries the database once per dish.
# Turn on SQL logging first:
#   CAMPUSCRAVE_SQL_ECHO=1 uv run campuscrave
# Then load the menu once and count the SELECT statements that scroll past.

curl -s http://localhost:8080/api/menu > /dev/null
echo "Menu loaded once. Now count the SELECTs in the API log."
echo "One page. Eight dishes. How many queries should that take?"
