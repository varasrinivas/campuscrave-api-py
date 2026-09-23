#!/usr/bin/env bash
# Lab mode — keeps the canteen taking orders while you work.
#
# If the API refuses your order with a message about closing times, that is the
# entry already sitting in your known-broken ledger from Episode 5. It is a real
# planted bug, it is not the bug your current lab is about, and you will hunt it
# properly in Episode 32.
#
# Until then, boot the API with this instead of the plain run command:
#     ./hints/lab-mode.sh
#
# Peeking inside is allowed — it's a small spoiler, not a big one. Your call.

CAMPUSCRAVE_EXTRA_SEED=hints/lab-mode.sql uv run campuscrave
