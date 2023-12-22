import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
#from matplotlib import pyplot as plt
#import seaborn as sns
#import streamlit-pandas as sp


#@st.cache(allow_output_mutation=True)

df = pd.read_csv("vehicles_new_df.csv")
df = df.drop(df.columns[0], axis=1)

st.header('Market of used Cars fixed data')

make = df['make'].unique() 
name_make = st.selectbox("Select manufacturers:", make)

min_year, max_year = (df['model_year'].min(),df['model_year'].max())
year_range = st.slider("Choose years:", value=(min_year,max_year), min_value=min_year, max_value=max_year)
actual_range = list(range(year_range[0], year_range[1]+1))

manual_cars = st.checkbox('See Only Manual Cars', value=False)


if manual_cars == True: 
    filtered_df = df[(df['make'] == name_make) 
                  & (df['model_year'].isin(actual_range)
                  & (df['transmission'] == 'manual')   
                     )
                ].sort_values(by='model_year', ascending=True).reset_index(drop=True)
else:
    filtered_df = df[(df['make'] == name_make) 
                  & (df['model_year'].isin(actual_range)  
                     )
                ].sort_values(by='model_year', ascending=True).reset_index(drop=True)
    
st.table(filtered_df.head(100))



st.header('Price Analysis')
list_for_hist=['transmission','cylinders','type','condition']
choice_for_hist = st.selectbox('split for price distribution', list_for_hist)

fig = px.histogram(df, x='price', color= choice_for_hist)
fig.update_layout( title='<b>Splt of Price by {}</b>'.format(choice_for_hist),
                height=800,  # Set the desired height
                width=1000    # Set the desired width
                )

st.plotly_chart(fig, theme="streamlit")





df['age']=2023-df['model_year']

def age_category(x):
    if x<5: return '<5'
    elif x>=5 and x <10: return '5-10'
    elif x>=10 and x<10: return '10-20'
    else: return '>20'
df['age_category'] =  df['age'].apply(age_category)

list_for_scatter=['odometer','cylinders','paint_color']
choice_for_scatter = st.selectbox('Price Dependancy on ', list_for_scatter)

fig2 = px.scatter(df, x='price', y=choice_for_scatter, color='age_category')
st.plotly_chart(fig2)


