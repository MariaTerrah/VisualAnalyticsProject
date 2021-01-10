#Common part
import pandas as pd
import streamlit as st
import altair as alt
from vega_datasets import data

df=pd.read_csv('data_final.csv')
df.fillna(0,inplace=True)
control_dataset = df

# ------------------------------CHECK IF USEFUL !!!!!----------------------------------------------------------------------------

slider = alt.binding_range(min=2000, max=2018, step=1, name='Years')
selector = alt.selection_single(name="Years", fields=['Years'],
                                bind=slider, init={'Years': 2000})

features=['Population','Density',"Population with less than $1.90 per day","Population with less than $5.90 per day",	
          "Gini Index","Life Expectancy","GDP per Capita","Literacy Rate","Fertility Rate",	
              "Population living in a city of +1M inhabitants","Population living in a rural area",
              "Unemployment Rate","Population aged between 0-14","Population aged between 15-64","Population aged +65"]

selectFeature = alt.selection_single(
    name='Select ', 
    init={'Features': features[0]}, 
    bind=alt.binding_select(options=features) )

countries = df['Country'].unique()

selectCountry = alt.selection_single(
    name='Select', 
    fields=['Country'], 
    init={'Country': countries[0]}, 
    bind=alt.binding_select(options=countries) 
)

selectCountry2 = alt.selection_single(
    name='Select2', 
    fields=['Country'], 
    init={'Country': countries[0]}, 
    bind=alt.binding_select(options=countries) 
)

years = df['Year'].unique()

selectYear = alt.selection_single(
    name='Select', 
    fields=['Year'], 
    init={'Year': years[0]}, 
    bind=alt.binding_select(options=years) 
)
# ------------------------------Comparison of pop status for two countries----------------------------------------------------------------------------
def write():
    st.header("Compare two countries! Population status")
    '''
        Here you can choose two countries and compare their populations over three parameters : the percentage of people living in a city that has over 1 million inhabitants, percentage of people living in a rural area and unemployment rate. 
        This tool help us not only compare countries but it challenges also the idea that countries with large cities have less unemployment. Rural countries are not always the one suffering from inactivity.
    '''
    country1 = st.selectbox("Select a country:",countries)
    country2 = st.selectbox("Select another country:",countries)
    
    c1=alt.Chart(df[df["Country"]==country1]).transform_fold(
        ["Population living in a city of +1M inhabitants","Population living in a rural area","Unemployment Rate"],
        as_=['Population Status', 'Proportion (%)']
    ).mark_area(
        opacity=0.3
    ).encode(
        alt.X('Year:O'),
        alt.Y('Proportion (%):Q', stack=None),
        alt.Color('Population Status:N',scale=alt.Scale(domain=["Population living in a city of +1M inhabitants","Population living in a rural area","Unemployment Rate"],
                          range=['red', 'gold','blue'])),
        alt.Tooltip(['Country:N','Population Status:N','Proportion (%):Q'])
    ).interactive()
    
    c2=alt.Chart(df[df["Country"]==country2]).transform_fold(
        ["Population living in a city of +1M inhabitants","Population living in a rural area","Unemployment Rate"],
        as_=['Population Status', 'Proportion (%)']
    ).mark_area(
        opacity=0.3
    ).encode(
        alt.X('Year:O'),
        alt.Y('Proportion (%):Q', stack=None),
        alt.Color('Population Status:N'),
        alt.Tooltip(['Country:N','Population Status:N','Proportion (%):Q'])
    ).interactive()
    
    st.altair_chart(c1 | c2)
    
    # ------------------------------Comparison of age distribution for two countries----------------------------------------------------------------------------
    st.header("Compare two countries! Age Distribution")
    '''
         Here you can choose two countries and compare their age distribution between three segments : under 14 years old, between 15 and 64 years old (this segment is considered as the labor force) and over 65 years old. 
         This is a very interesting tool because you can clearly see the difference between aging countries in the west and younger one in Africa.    
    '''
    country3 = st.selectbox("Select the first country:",countries)
    country4 = st.selectbox("Select the second country:",countries)
    
    c3=alt.Chart(df[df["Country"]==country3]).transform_fold(
        ["Population aged between 0-14","Population aged between 15-64","Population aged +65"],
        as_=['Age Distribution', 'Proportion (%)']
    ).mark_area(
        opacity=0.3
    ).encode(
        alt.X('Year:O'),
        alt.Y('Proportion (%):Q', stack=None),
        alt.Color('Age Distribution:N',scale=alt.Scale(domain=["Population aged between 0-14","Population aged between 15-64","Population aged +65"],
                          range=['green', 'silver','purple'])),
        alt.Tooltip(['Country:N','Age Distribution:N','Proportion (%):Q'])
    ).interactive()
    
    c4=alt.Chart(df[df["Country"]==country4]).transform_fold(
        ["Population aged between 0-14","Population aged between 15-64","Population aged +65"],
        as_=['Age Distribution', 'Proportion (%)']
    ).mark_area(
        opacity=0.3
    ).encode(
        alt.X('Year:O'),
        alt.Y('Proportion (%):Q', stack=None),
        alt.Color('Age Distribution:N'),
        alt.Tooltip(['Country:N','Age Distribution:N','Proportion (%):Q'])
    ).interactive()
    
    st.altair_chart(c3 | c4)