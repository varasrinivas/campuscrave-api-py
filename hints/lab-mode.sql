-- Lab mode seed: Anna Madam keeps the counter open late during exam week.
-- Loaded on top of data.sql by hints/lab-mode.sh and lab-mode.cmd — see either for why.
--
-- Why 05:29:59 and not 23:59: the cutoff check shifts the configured time before
-- comparing it, and lab mode does not disable that shift — 23:59 landed on 18:29 and
-- the counter closed every evening. The shift wraps past midnight, so 05:29:59 lands
-- on 23:59:59 instead and lab mode stays open all day. The shift itself is the planted
-- bug and stays exactly where it is; Episode 32 is where you deal with it.
insert into canteen_config (id, order_cutoff, rush_start, rush_end, max_active_orders, accepting_orders)
    values (1, '05:29:59', '12:15:00', '13:45:00', 3, true)
    on conflict (id) do update set order_cutoff = excluded.order_cutoff;
