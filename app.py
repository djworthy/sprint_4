#import libraries
import streamlit as st
import pandas as pd
import plotly.express as px


primaryColor="#F63366"
backgroundColor="#FFFFFF"
secondaryBackgroundColor="#F0F2F6"
textColor="#262730"
font="sans serif"


#read in csv file to new dataframe 
df = pd.read_csv("vehicles_new_df.csv")
df = df.drop(df.columns[0], axis=1)

#### TEXT FOR TITLE AND INTITAL PROJECT POINTS### 
st.title('Analyzing Used Car Market Trends')
st.markdown("***")
st.markdown('In this project, we aim to gain insights into the trends and characterstics of the used car market. By analyzing various factors in pricing, transmission type, cylinder counts, car types, condition, relationship between age and odomter readings. In order to understand the how these influence the customer and the market')
st.markdown('****Key Questions:****')

st.markdown('*Pricing Trends:*')
st.markdown('- What is the distribution of car prices in our inventory?')
st.markdown('- How does the price range vary across different categories and conditions?')

st.markdown('*Transmission Preferences:*')
st.markdown('- What is the proportion of automatic versus manual transmissions in our stock?')
st.markdown('- Are there notable differences in pricing based on transmission type?')

st.markdown('*Cylinder Type:*')
st.markdown('- How are cars distributed among various cylinder counts?')
st.markdown('- Does the cylinder count impact pricing, and if so, how?')

st.markdown('*Car Type Popularity:*')
st.markdown('- Which car types (SUVs, sedans, pickups) are most popular among buyers?')
st.markdown('- Are there pricing variations based on the type of car?')

st.markdown('*Condition Classification:*')
st.markdown("- What percentage of our inventory falls under the 'good' condition category?")
st.markdown('- How does condition classification correlate with pricing?')

st.markdown('*Age and Odometer Relationships:*')

st.markdown("- What is the relationship between a car's age, odometer reading, and pricing?")
            
st.markdown('- How do older cars with higher odometer readings compare in terms of costs?')

st.markdown('*Pricing Trends:*')
st.markdown('- How do car prices evolve as vehicles age, and what role does odometer reading play?')

st.markdown("***")



#Create table of data from our df 
st.header('Used Car Market Data Table')
st.markdown('Filter Data Based on Manufacturers, Year Range, and Manual Transmission Cars')

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


st.markdown("***")

#Create Histogram Price Analysis by 'transmission','cylinders','type','condition'
st.header('Price Analysis of Inventory')
st.subheader('Key Insights from Our Inventory:')
st.text('1. The majority of our vehicles fall within the 5K - 10K price range.')
st.text('2. Automatic transmission is the prevailing choice over manual.')
st.text('3. Cars with 8, 6, or 4 cylinders dominate, with the 6-cylinder category being the most prominent.')
st.text('4. SUVs rank as the most popular car type, closely followed by sedans and pickups.')
st.text('5. The majority of our inventory has been classified as being in good condition.')





#create list of options
list_for_hist=['transmission','cylinders','type','condition']

#creae select box for list of options
choice_for_hist = st.selectbox('split for price distribution', list_for_hist)

#create histogram
fig = px.histogram(df, x='price', color= choice_for_hist)
fig.update_layout( title='<b>Split of Price by {}</b>'.format(choice_for_hist),
                height=600,  # Set the desired height
                width=800    # Set the desired width
                )

#create the chart
st.plotly_chart(fig, theme="streamlit")


st.markdown("***")


#Create Chart of Odometer Readings for price and age
st.header('Scatter Plot: Price vs Odometer, Grouped by Car Age')
st.markdown("As vehicles surpass the 5-year mark, those with higher odometer readings tend to exhibit lower costs.")
#create age of car in years into new column in df
df['age']=2023-df['model_year']


#create funtion to get age range of row
def age_category(x):
    if x<5: return '<5'
    elif x>=5 and x <10: return '5-10'
    elif x>=10 and x< 20: return '10-20'
    else: return '> 20'

#create new column in df for the age category calling the age_category function
df['age_category'] =  df['age'].apply(age_category)

#create scatter chart
fig2 = px.scatter(df, x='price', y='odometer', color='age_category')
st.plotly_chart(fig2)



st.markdown("***")



#Create Line Chart#
st.header('Comparison of Model Year to Avg Price')
st.markdown("As cars age, their prices generally decrease until reaching classic status")

#create datbase query to get mean price by model year 
mean_df = df.groupby('model_year')['price'].mean().reset_index()

#Create line plot
fig3 = px.line(mean_df, x='model_year', y='price')
fig3.update_layout(xaxis_title='Model Year', yaxis_title='Price')
st.plotly_chart(fig3)



###TEXT FOR FINAL CONCLUSION AND TAKEAWAYS####

st.markdown("***")
st.header('Final Conculsions:')
st.markdown("1. Our inventory predominantly consists of vehicles priced between 5K and 10K.")
st.markdown("2. Automatic transmission is the preferred choice over manual among our customers.")
st.markdown("3. Cars equipped with 8, 6, or 4 cylinders dominate our stock, with 6-cylinder models being particularly popular.")
st.markdown("4. SUVs stand out as the top choice, closely followed by sedans and pickups.")
st.markdown("5. The majority of our vehicles are classified as being in good condition.")
st.markdown("6. As vehicles age beyond 5 years, those with higher odometer readings tend to have lower costs.")
st.markdown("7. Over time, car prices generally decrease until they achieve classic status.")