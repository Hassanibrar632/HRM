import streamlit as st
import pandas as pd
import requests
import datetime as dt

def highlight_late_row(row):
    if row['overtime_adjustment'] == 1 and row['adjustment']:
        return ['background-color: #007bff; color:white'] * len(row)
    if row['adjustment'] is not None:
        return ['background-color: #ffc107; color:black'] * len(row)
    if row['overtime_adjustment'] == 1:
        return ['background-color: #007bff; color:white'] * len(row)
    if row['late_hours'] != "00:00:00":
        return ['background-color: #dc3545; color:white'] * len(row)
    if row['early_out'] != "00:00:00":
        return ['background-color: #17a2b8; color:white'] * len(row)
    else:
        return ['background-color: #28a745; color:white'] * len(row)

def plot_legend(row):
    if row['Meaning'] == "Overtime Adjustment":
        return ['background-color: #007bff; color:white'] * len(row)
    if row['Meaning'] == "Adjusted Record":
        return ['background-color: #ffc107; color:black'] * len(row)
    if row['Meaning'] == "Late Check-in":
        return ['background-color: #dc3545; color:white'] * len(row)
    if row['Meaning'] == "Early Check-out":
        return ['background-color: #17a2b8; color:white'] * len(row)
    if row['Meaning'] == "On Time":
        return ['background-color: #28a745; color:white'] * len(row)

def profile_page():
    if 'user' in st.session_state and st.session_state['user'] is not None:
        user = st.session_state['user']
        st.header(f"**Name ({user['id']}):** {user['name']}")
        st.write(f"**Email:** {user['email']}")
        if st.button("Logout", type='primary', use_container_width=True):
            st.session_state['user'] = None
            st.success("Logged out successfully!")
            st.rerun()
        col1, col2 = st.columns([2, 2])
        with col1:
            if st.button("Check-IN", type='secondary', use_container_width=True):
                data = {'employee_id': user['id'], 'date': str(pd.Timestamp.now().date()), 'check_in': dt.datetime.fromisoformat(str(pd.Timestamp.now())).strftime("%H:%M:%S")}
                response = requests.post("http://127.0.0.1:5000/record_attendance", json=data)
                if response.status_code == 200:
                    st.success(f"{response.json().get('message', 'Check-in successful!')}")
                else:
                    st.error(f"{response.json().get('message', 'Check-in failed.')}")
            if st.button("Check-OUT", type='secondary', use_container_width=True):
                data = {"employee_id": user['id'], 'date': str(pd.Timestamp.now().date()), 'check_out': dt.datetime.fromisoformat(str(pd.Timestamp.now())).strftime("%H:%M:%S")}
                response = requests.post("http://127.0.0.1:5000/record_attendance", json=data)
                if response.status_code == 200:
                    st.success(f"{response.json().get('message', 'Check-out successful!')}")
                else:
                    st.error(f"{response.json().get('message', 'Check-out failed.')}")
        with col2:
            adj_date = st.date_input("Adjustment Date", value=dt.date.today())
            option = st.selectbox("Adjustment Type", ["late", "early_exit", "Both", "Overtime"])
            if st.button("Apply Adjustment", type='secondary'):
                data = {'employee_id': user['id'], 'date': str(adj_date), 'adjustment_type': option}
                response = requests.post("http://127.0.0.1:5000/adjust_attendance", json=data).json()
                st.info(response.get('message', 'No message from server.'))
        st.header("Attendance Records")
        start_date, end_date = st.date_input(
            "Attendance Period",
            value=(dt.date.today().replace(day=1), dt.date.today())
        )
        if start_date > end_date:
            st.error("End date must be after start date.")
        else:
            data = {"start_date": str(start_date), "end_date": str(end_date)}
            response = requests.get(f"http://127.0.0.1:5000/get_attendance/{user['id']}", json=data).json()
            df_data = response['attendance']
            df = pd.DataFrame(df_data)
            column_order = [
                'date',
                'check_in',
                'check_out',
                'late_hours',
                'early_out',
                'overtime_hours',
                'adjustment',
                'overtime_adjustment'
            ]
            df = df[column_order]
            col1, col2 = st.columns([1, 1])
            with col1:
                st.header("Overall Summary")
                st.bar_chart({
                    'Late Hours': df['late_hours'].apply(lambda x: pd.to_timedelta(x).total_seconds() / 3600).sum(),
                    'Early Out': df['early_out'].apply(lambda x: pd.to_timedelta(x).total_seconds() / 3600).sum(),
                    'Overtime Hours': df['overtime_hours'].apply(lambda x: pd.to_timedelta(x).total_seconds() / 3600).sum()
                })
            with col2:
                st.header("Time Overview")
                # let late hours and early out based on adjjusted reocrds and overtime adjustments
                total_late = df[df['adjustment'].isnull()]['late_hours'].apply(lambda x: pd.to_timedelta(x).total_seconds() / 3600).sum()
                total_early = df[df['adjustment'].isnull()]['early_out'].apply(lambda x: pd.to_timedelta(x).total_seconds() / 3600).sum()
                total_time_left = total_early + total_late
                total_overtime = df[df['overtime_adjustment'] == 1]['overtime_hours'].apply(lambda x: pd.to_timedelta(x).total_seconds() / 3600).sum()
                st.bar_chart({
                    'Total Late Hours': total_late,
                    'Overtime Hours': total_overtime
                })
            st.header("Attendance Details")
            st.dataframe(df.style.apply(highlight_late_row, axis=1))
            st.write("**Legend:**")
            st.dataframe(pd.DataFrame({
                "Color": ["#dc3545", "#17a2b8", "#ffc107", "#007bff", "#28a745"],
                "Meaning": ["Late Check-in", "Early Check-out", "Adjusted Record", "Overtime Adjustment", "On Time"]
            }).style.apply(plot_legend, axis=1))

if __name__ == "__main__":
    profile_page()