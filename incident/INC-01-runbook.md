# INC-01 — Fest Night (sealed until Episode 42)

**Do not open this folder during normal labs.** It is the script for the
scripted production incident on Fest Night. If you've arrived here from
Episode 42, welcome to the worst evening of the semester.

## The setup
- Campus fest. The canteen stays open late; Anna Madam bumps stock at 19:40
  while orders are landing.
- Two things interact: a stock update during the rush, and a cancellation
  behaviour nobody has thought about since Week 1.

## Timeline (inject these in order)
| T | Event |
|---|---|
| 19:32 | Rush meter pegged. Orders every few seconds. |
| 19:40 | Anna Madam sets Paneer Roll stock to 40 from the tablet. |
| 19:41 | Students report "sold out" on dishes the kitchen can see on the shelf. |
| 19:44 | Cancellations spike (long queue). Stock numbers drift further from reality. |
| 19:51 | First wallet complaint: "money gone, no token". |

## Your job (as written on the EP42 lab card)
1. Triage from `logs/fest-night.log` — what do you *know* vs *suspect*?
2. Reproduce the drift locally with `hints/repro/BUG-06.sh` + a stock update.
3. Decide the mitigation order: stop the bleeding, then fix, then reconcile.
4. Write the postmortem using the blameless template below.

## Postmortem template
- What happened (timeline, no adjectives)
- Impact (orders, rupees, students)
- Root causes (plural — there are at least two)
- What we're changing (code, process, monitoring)
- What we are explicitly not changing, and why
