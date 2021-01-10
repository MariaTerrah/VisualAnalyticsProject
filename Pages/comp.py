#Common part
import pandas as pd
import streamlit as st
import altair as alt
from vega_datasets import data

df=pd.read_csv('data_final.csv')
df.fillna(0,inplace=True)
countries = df['Country'].unique()

# ------------------------------Comparison of pop status for two countries----------------------------------------------------------------------------
def write():
    st.header("Compare two countries! Population status")
    st.markdown('''
        Here you can choose two countries and compare their populations over three parameters : the percentage of people living in a city that has over 1 million inhabitants, percentage of people living in a rural area and unemployment rate. 
        This tool help us not only compare countries but it challenges also the idea that countries with large cities have less unemployment. Rural countries are not always the one suffering from inactivity.
    ''')
    mYexpander = st.beta_expander('Usage')
    mYexpander.write('''Please select two different countries to visualize their different proportions for urban and rural population and unemployment rate. Note that urban people means here people living in a city with +1M inhabitants.''')
    mYExpander = st.beta_expander('Explanation')
    mYExpander.write('''It is very interesting to see that unemployment is not a rural country issue. In fact countries with high urban rates suffer also, even more, than rural countries.
    ''')
    coll1, coll2 = st.beta_columns(2)
    country1 = coll1.selectbox("Select a country:",countries)
    country2 = coll2.selectbox("Select another country:",countries)
    
    c1=alt.Chart(df[df["Country"]==country1]).transform_fold(
        ["Population living in a city of +1M inhabitants","Population living in a rural area","Unemployment Rate"],
        as_=['Population Status', 'Proportion (%)']
    ).mark_area(
        opacity=0.3
    ).encode(
        alt.X('Year:O'),
        alt.Y('Proportion (%):Q', stack=None),
        alt.Color('Population Status:N',scale=alt.Scale(domain=["Population living in a city of +1M inhabitants","Population living in a rural area","Unemployment Rate"],
                          range=['red', 'gold','blue']),legend=None),
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
        alt.Color('Population Status:N',scale=alt.Scale(domain=["Population living in a city of +1M inhabitants","Population living in a rural area","Unemployment Rate"],
                          range=['red', 'gold','blue']),legend=None),
        alt.Tooltip(['Country:N','Population Status:N','Proportion (%):Q'])
    ).interactive()
    

    coll1.header(country1)
    coll1.altair_chart(c1)

    coll2.header(country2)
    coll2.altair_chart(c2)
    
    # ------------------------------Comparison of age distribution for two countries----------------------------------------------------------------------------
    st.header("Compare two countries! Age Distribution")
    st.markdown('''
         Here you can choose two countries and compare their age distribution between three segments : under 14 years old, between 15 and 64 years old (this segment is considered as the labor force) and over 65 years old. 
         This is a very interesting tool because you can clearly see the difference between aging countries in the west and younger one in Africa.    
    ''')
    MYexpander = st.beta_expander('Usage')
    MYexpander.write('''Please select two different countries to visualize their different age distribution.''')
    MYExpander = st.beta_expander('Explanation')
    MYExpander.write('''The difference between developping countries and Western countries in quite stricking. Try comparing the percentage of young people of an African country like Niger with an aging country like Belgium.''')
    
    coll3, coll4 = st.beta_columns(2)
    country3 = coll3.selectbox("Select the first country:",countries)
    country4 = coll4.selectbox("Select the second country:",countries)
    
    c3=alt.Chart(df[df["Country"]==country3]).transform_fold(
        ["Population aged between 0-14","Population aged between 15-64","Population aged +65"],
        as_=['Age Distribution', 'Proportion (%)']
    ).mark_area(
        opacity=0.3
    ).encode(
        alt.X('Year:O'),
        alt.Y('Proportion (%):Q', stack=None),
        alt.Color('Age Distribution:N',scale=alt.Scale(domain=["Population aged between 0-14","Population aged between 15-64","Population aged +65"],
                          range=['green', 'silver','purple']),legend=None),
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
        alt.Color('Age Distribution:N',scale=alt.Scale(domain=["Population aged between 0-14","Population aged between 15-64","Population aged +65"],
                          range=['green', 'silver','purple']),legend=None),
        alt.Tooltip(['Country:N','Age Distribution:N','Proportion (%):Q'])
    ).interactive()
    
    coll3.header(country3)
    coll3.altair_chart(c3)

    coll4.header(country4)
    coll4.altair_chart(c4)
