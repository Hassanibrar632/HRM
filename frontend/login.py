import streamlit as st, requests

def Login_registration_page():
    st.title("Login / Registration Page")
    col1, col2 = st.columns(2)
    with col1:
        st.header("Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            # Call backend login function
            repsonse = requests.post("http://127.0.0.1:5000/login", json={
                "email": email,
                "password": password
            }).json()
            if 'user' in repsonse:
                user = repsonse['user']
                st.session_state['user'] = user
                st.success("Login successful!")
                st.rerun()
            else:
                st.error(repsonse.get('message', 'Login failed.'))
    with col2:
        st.header("Register")
        name = st.text_input("Name", key="reg_name")
        reg_email = st.text_input("Email", key="reg_email")
        reg_password = st.text_input("Password", type="password", key="reg_password")
        if st.button("Register"):
            repsonse = requests.post("http://127.0.0.1:5000/add_employee", json={
                "name": name,
                "email": reg_email,
                "password": reg_password
            }).json()
            print(repsonse)
            if repsonse.get('message'):
                st.info(repsonse['message'])
if __name__ == "__main__":
    Login_registration_page()