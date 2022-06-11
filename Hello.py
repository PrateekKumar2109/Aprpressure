import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋"
)


st.title(" Multi-Page Streamlit Web Application")
st.header(" Welcome to O & G Made Easy! 👋")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    We are here to make Oil and Gas Engineer life easy 
    
"""
)


activities=['Login','About']
choice=st.sidebar.selection("Select Activity", activities)
if choice=='Login':
    st.subheader('Login')
    username=st.text_input("Enter Username")
    password=st.text_input("Enter Password", type='password')
    if st.button("Submit"):
        if password=='12345':
            st.balloons()
            st.write("Hello {}".format(username))
        else:
            st.warning('Wrong Password')
            
expander = st.expander("Domain Knowledge of Oil & Gas ")
expander.write("""
     Pressure & Temperature hole Surveys are carried out in the well frequently. Shut-in & flowing 
     pressure & temp. surveys are recorded to analyze the pressures, well flowing behaviour.
 """)
