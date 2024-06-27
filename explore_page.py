import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def shorten_cat(categories,cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]

        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map

def clean_expe(x):
    if x == 'More than 50 years':
        return 50.0
    if x == 'Less than 1 year':
        return 0.5
    
    return float(x)

def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelors Degree'
    if 'Master’s degree' in x:
        return 'Masters Degree'
    if 'Professional degree' in x or 'Associate degree' in x:
        return 'Doctoral Degree'
    
    return 'Less than a Bachelor'


@st.cache_data
def load_data():
    df = pd.read_csv('survey_results_public.csv')
    df = df[['Country','EdLevel','YearsCodePro','Employment','ConvertedCompYearly']]
    df = df.rename({'ConvertedCompYearly':'Salary'},axis=1)
    df = df[df['Salary'].notna()]
    df = df.dropna()
    df = df[df['Employment'] == 'Employed, full-time']
    df = df.drop('Employment',axis=1)
    t = df['Country'].value_counts()
    country_map = shorten_cat(t,400)
    df['Country'] = df['Country'].map(country_map)
    df = df[df['Salary']<= 250000]
    df = df[df['Salary'] >10000]
    df = df[df['Country'] != 'Other']
    df['YearsCodePro'] = df['YearsCodePro'].apply(clean_expe)
    df['EdLevel'] = df['EdLevel'].apply(clean_education)
    return df

df = load_data()

def show_explorations():
    st.title("Explore Software Developers Salary")

    st.write(""" 
            ## Stack Overflow Developer survey 2023
            """)
    
    data = df["Country"].value_counts()

    fig1,ax1 = plt.subplots()
    ax1.pie(data,labels = data.index, autopct = "%1.1f%%",shadow = True,startangle = 90)
    ax1.axis('equal')
    
    st.write("""#### Number of Data from Different Countries""")
    st.pyplot(fig1)

    st.write(""" ## Mean salary based on country""")

    data  = df.groupby(["Country"])['Salary'].mean().sort_values(ascending=True)

    st.bar_chart(data)
    st.write(""" ## Mean salary based on experience""")

    data  = df.groupby(["YearsCodePro"])['Salary'].mean().sort_values(ascending=True)
    st.line_chart(data)

