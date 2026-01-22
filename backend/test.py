from models import *
import random, datetime

init_db()

for i in range(1, 25):
    record_attendance(1, datetime.date(2026, 1, i), check_in=f"{random.randint(8, 10)}:{random.randint(0, 10)}:00")
    record_attendance(1, datetime.date(2026, 1, i), check_out=f"{random.randint(17, 18)}:{random.randint(0, 10)}:00")

for i in range(1, 5):
    add_overtime_adjustment(1, datetime.date(2026, 1, random.randint(1, 24)))

for i in range(1, 5):
    add_adjustment(1, datetime.date(2026, 1, random.randint(1, 24)), adj_type="late", reason="Flu")
print(get_employee_attendance(1, datetime.date(2026, 1, 1), datetime.date(2026, 1, 31)))
