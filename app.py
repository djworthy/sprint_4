#import libraries
import streamlit as st
import pandas as pd
import plotly.express as px

#read in csv file to new dataframe 
df = pd.read_csv("vehicles_new_df.csv")
df = df.drop(df.columns[0], axis=1)


#Create table of data from our df 
st.header('Market of used Cars fixed data')

#create option to choose car maker
make = df['make'].unique() 
name_make = st.selectbox("Select manufacturers:", make)

#Create slide bar to choose date range
min_year, max_year = (df['model_year'].min(),df['model_year'].max())
year_range = st.slider("Choose years:", value=(int(min_year),int(max_year)), min_value=int(min_year), max_value=int(max_year))
actual_range = list(range(year_range[0], year_range[1]+1))

#create checkbox to only show manuel transmission vehicles
manual_cars = st.checkbox('See Only Manual Cars', value=False)

#use manual_cars value to choose which database query to run
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

#create the table    
st.table(filtered_df.head(100))




#Create Histogram Price Analysis by 'transmission','cylinders','type','condition'
st.header('Price Analysis')

#create list of options
list_for_hist=['transmission','cylinders','type','condition']

#creae select box for list of options
choice_for_hist = st.selectbox('split for price distribution', list_for_hist)

#create histogram
fig = px.histogram(df, x='price', color= choice_for_hist)
fig.update_layout( title='<b>Splt of Price by {}</b>'.format(choice_for_hist),
                height=800,  # Set the desired height
                width=1000    # Set the desired width
                )

#create the chart
st.plotly_chart(fig, theme="streamlit")




#Create Chart of Odometer Readings for price and age
st.header('Scatterplot of Price on Odometer Reading on Grouped on the Age of the Car')

#create age of car in years into new column in df
df['age']=2023-df['model_year']


#create funtion to get age range of row
def age_category(x):
    if x<5: return '<5'
    elif x>=5 and x <10: return '5-10'
    elif x>=10 and x<10: return '10-20'
    else: return '>20'

#create new column in df for the age category calling the age_category function
df['age_category'] =  df['age'].apply(age_category)

#create scatter chart
fig2 = px.scatter(df, x='price', y='odometer', color='age_category')
st.plotly_chart(fig2)


