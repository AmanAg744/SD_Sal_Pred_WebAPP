import pickle
import streamlit as st
import numpy as np

def load_model():
    with open('saved_steps.pkl','rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

regressor = data['model']
le_count = data['le_country']
le_edu = data["le_education"]

def show_prediction():
    st.title("Software Developer Salary Prediction")

    st.write(""" ### We need some data to make predictions of the salary.""")

    countries = ("United States of America","Germany",
               "United Kingdom of Great Britain and Northern Ireland","Canada",
               "India","France","Netherlands",                                              
                "Australia","Brazil","Spain",                                                    
                "Sweden","Italy","Poland",                                                   
                "Switzerland","Denmark","Norway","Israel")
    
    education = ('Bachelors Degree', 'Less than a Bachelor', 'Masters Degree',
       'Doctoral Degree')
    
    country = st.selectbox("Country",countries)
    edu = st.selectbox('Education',education)
    experience = st.slider("years of experience",0,50,3)
    
    ok = st.button("Calculate Salary")
    if ok:
        x = np.array([[country, edu, experience]])
        x[:,0] = x[:,0].astype(object)
        x[:,1] = x[:,1].astype(object)
        x[:,0] = le_count.transform(x[:,0])
        x[:,1] = le_edu.transform(x[:,1])
        x = x.astype(float)

        salary = regressor.predict(x)
        st.subheader(f"The estimated salary is ${salary[0]:.2f}")
    