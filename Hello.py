import streamlit as st
st.set_page_config(
    page_title="Hello",
    page_icon="👋"
)
#st.title(" Multi-Page Streamlit Web Application")
st.title(" Saas(Software As A Service ) Application for PetroPhysics")
#st.header(" Welcome to O & G Made Easy! 👋")
st.header(" Welcome  👋")
st.sidebar.success("Select a demo above.")
st.markdown(
    """
    We are here to make Oil and Gas Engineer life easy   
""")
activities=['Login','About']
choice=st.sidebar.selectbox("Select Activity", activities)
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
    
elif choice=='About':   
    st.write(
        """Web Based Software as a Service(Saas) is accessible on our web browser enabling scalibility. These applications
        are easy to update & manage. In our day to day work, the SaaS provides us with great Automation Oppurtunities as it eliminates 
        the need for any upfront investments. We 
             are Energy professionals &  our aim is to reduce the complexitiy of O & G Industy. 
             """)
    #st.write(
    #    """With the Release Streamlit Version 1.10.0 it is now possible to make a Multi-Page application 
    # eliminating need of third party plugins. In this Web application we are working on Pressure & Temperature Survey Data
    # which is used to make decision in day to day life of a well. We 
    #         are Energy professionals &  our aim is to reduce the complexitiy of O & G Industy. 
    #         """)
expander = st.expander("Domain Knowledge of Oil & Gas ")
#expander.write("""
#     Pressure & Temperature hole Surveys are carried out in the well frequently. Shut-in & flowing 
#     pressure & temp. surveys are recorded to analyze the pressures, well flowing behaviour.
# """)
expander.write("""
     In the field development activities wells are drilled. During drilling we record MDT/RFT meaning formation testing.
     MDT/RFT provides us with fast estimation of pressure of the formation & are also used for collecting formation samples.
     The operator has to provide the depths on which the MDT sampling & pressure has to be recorded on the basis of the LWD logs 
     recorded during driiling.
     
 """)
    
