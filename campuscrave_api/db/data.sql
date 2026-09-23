-- Day-1 seed data. The menu from the approved app mockup, Anna Madam's
-- canteen settings, and three students you will meet in the course.

-- The canteen. One row, id 1. Times are IST.
insert into canteen_config (id, order_cutoff, rush_start, rush_end, max_active_orders, accepting_orders)
    values (1, '14:30:00', '12:15:00', '13:45:00', 3, true)
    on conflict (id) do nothing;

-- Students
insert into students (id, roll_number, name, email, hostel_block)
    values (1, 'CS21B042', 'Priya Sharma', 'priya.sharma@campus.edu', 'Block A'),
           (2, 'EC21B117', 'Rohan Mehta', 'rohan.mehta@campus.edu', 'Block D'),
           (3, 'CS23B001', 'New Dev', 'you@campus.edu', 'Block C')
    on conflict (id) do nothing;

insert into wallets (id, student_id, balance_rupees)
    values (1, 1, 340),
           (2, 2, 120),
           (3, 3, 500)
    on conflict (id) do nothing;

-- The menu. Wednesday special: Hyderabadi Biryani, Rs.90, stock 3 — canon.
insert into dishes (id, name, description, price_rupees, category, vegetarian, stock, emoji, prep_minutes, wednesday_special, active)
    values (1, 'Hyderabadi Biryani', 'Dum-cooked, served with raita. Wednesdays only, and it goes fast.', 90, 'Mains', false, 3, '🍚', 14, true, true),
           (2, 'Masala Dosa', 'Crisp, golden, potato-stuffed. The bestseller.', 50, 'South Indian', true, 40, '🥞', 8, false, true),
           (3, 'Veg Thali', 'Two sabzi, dal, rice, three rotis, pickle.', 70, 'Mains', true, 25, '🍛', 12, false, true),
           (4, 'Chai + Samosa', 'The thinking break. Cutting chai and one hot samosa.', 25, 'Snacks', true, 60, '☕', 4, false, true),
           (5, 'Idli (4 pc)', 'Steamed soft, sambar and two chutneys.', 40, 'South Indian', true, 30, '🍥', 6, false, true),
           (6, 'Chole Bhature', 'Friday-feeling food, available daily.', 60, 'Mains', true, 20, '🫓', 11, false, true),
           (7, 'Paneer Roll', 'Tandoori paneer, mint chutney, rumali wrap.', 45, 'Snacks', true, 18, '🌯', 7, false, true),
           (8, 'Vada Pav (2 pc)', 'Mumbai in your hand. Extra dry garlic chutney.', 30, 'Snacks', true, 35, '🍔', 5, false, true)
    on conflict (id) do nothing;
