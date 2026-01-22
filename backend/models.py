# database manager
import sqlite3, datetime

def get_db_connection():
    """Establish a connection to the SQLite database."""
    conn = sqlite3.connect('./backend/database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Create necessary tables if they do not exist."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Employees / Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'employee',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        # Attendance table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER NOT NULL,
                date DATE NOT NULL,
                check_in DATETIME,
                check_out DATETIME,
                overtime_hours TEXT DEFAULT '00:00:00',
                early_out TEXT DEFAULT '00:00:00',
                late_hours TEXT DEFAULT '00:00:00',
                adjustment TEXT, -- late, early_exit, leave
                overtime_adjustment BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(employee_id, date),
                FOREIGN KEY (employee_id) REFERENCES employees(id)
            );
        """)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

def add_employee(name, email, password_hash, role='employee'):
    """Add a new employee to the database."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO employees (name, email, password_hash, role)
            VALUES (?, ?, ?, ?);
        """, (name, email, password_hash, role))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

def login_user(email, password_hash):
    """Login a user by verifying email and password hash."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM employees WHERE email = ? AND password_hash = ?;
        """, (email, password_hash))
        user = cursor.fetchone()
        conn.close()
        if user:
            return dict(user)
        else:
            return None
    except Exception as e:
        return None

def record_attendance(employee_id: int, date: datetime.date, check_in:str=None, check_out:str=None):
    """Manage attendance records for an employee."""
    if type(date) == str:
        # Date Format: 'YYYY-MM-DD'
        date = datetime.date.fromisoformat(date)
    try:
        if check_out is None:
            # add date with check-in time to get late hours
            check_in_dt = datetime.datetime.combine(date, datetime.time(*map(int, check_in.split(":"))))
            # calculate late hours
            late_time = check_in_dt - datetime.datetime.combine(date, datetime.time(9, 0))
            # if late_time is negative, set to 00:00:00 otherwise use the calculated late time
            if late_time.total_seconds() > 0:
                late_str = str(datetime.timedelta(seconds=late_time.total_seconds()))
            else:
                late_str = "00:00:00"
            # get db_connection and insert or replace attendance record
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO attendance (employee_id, date, check_in, late_hours)
                VALUES (?, ?, ?, ?);
            """, (employee_id, date, check_in, late_str))
            conn.commit()
            conn.close()
            return True
        if check_in is None:
            # add date with check-out time to get overtime hours or early out
            check_out_dt = datetime.datetime.combine(date, datetime.time(*map(int, check_out.split(":"))))
            overtime = check_out_dt - datetime.datetime.combine(date, datetime.time(18, 0))
            # if overtime is positive, it's overtime hours, else it's early out
            if overtime.total_seconds() > 0:
                overtime_str = str(datetime.timedelta(seconds=overtime.total_seconds()))
                early_out_str = "00:00:00"
            else:
                early_out_str = str(datetime.timedelta(seconds=overtime.total_seconds()*-1))
                overtime_str = "00:00:00"
            # get db_connection and update attendance record
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE attendance
                SET check_out = ?, overtime_hours = ?, early_out = ?
                WHERE employee_id = ? AND date = ?;
            """, (check_out, overtime_str, early_out_str, employee_id, date))
            conn.commit()
            conn.close()
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False
    
def add_overtime_adjustment(employee_id: int, date: datetime.date):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE attendance
            SET overtime_adjustment = 1
            WHERE employee_id = ? AND date = ?;
        """, (employee_id, date))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

def add_adjustment(employee_id: int, date: datetime.date, adj_type: str):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE attendance
            SET adjustment = ?
            WHERE employee_id = ? AND date = ?;
        """, (adj_type, employee_id, date))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

def get_employee_attendance(employee_id: int, start_date:datetime.date=None, end_date:datetime.date=None):
    """Get attendance records for an employee within a date range."""
    try:
        # if no dates provided, default to current month
        if start_date is None:
            start_date = datetime.date.today().replace(day=1)
        if end_date is None:
            end_date = datetime.date.today()
        # get records from the database
        conn = get_db_connection()
        cursor = conn.cursor()
        # run query to fetch attendance records from attendance table within date range
        cursor.execute("""
            SELECT * FROM attendance
            WHERE employee_id = ? AND date BETWEEN ? AND ?
            ORDER BY date ASC;
        """, (employee_id, start_date, end_date))
        records = cursor.fetchall()
        conn.close()
        # convert records to list of dicts
        df_data = {'date': [], 'check_in': [], 'check_out': [], 'early_out': [], 'overtime_hours': [], 'late_hours': [], 'adjustment': [], 'overtime_adjustment': []}
        for record in records:
            df_data['date'].append(record['date'])
            df_data['check_in'].append(record['check_in'])
            df_data['check_out'].append(record['check_out'])
            df_data['early_out'].append(record['early_out'])
            df_data['overtime_hours'].append(record['overtime_hours'])
            df_data['late_hours'].append(record['late_hours'])
            df_data['adjustment'].append(record['adjustment'])
            df_data['overtime_adjustment'].append(record['overtime_adjustment'])
        return df_data
    except Exception as e:
        print("Unable to fetch attendance:", e)
        return []
    
def get_employee_adjustments(employee_id, start_date, end_date):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM adjustments
            WHERE employee_id = ? AND date BETWEEN ? AND ?
            ORDER BY date ASC;
        """, (employee_id, start_date, end_date))
        records = cursor.fetchall()
        conn.close()
        adjustments_list = [dict(record) for record in records]
        return adjustments_list
    except Exception as e:
        return []
