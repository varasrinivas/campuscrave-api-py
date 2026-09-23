@echo off
REM Lab mode - keeps the canteen taking orders while you work.
REM
REM If the API refuses your order with a message about closing times, that is the
REM entry already sitting in your known-broken ledger from Episode 5. It is a real
REM planted bug, it is not the bug your current lab is about, and you will hunt it
REM properly in Episode 32.
REM
REM Peeking inside is allowed - it's a small spoiler, not a big one. Your call.

set CAMPUSCRAVE_EXTRA_SEED=hints/lab-mode.sql
uv run campuscrave
