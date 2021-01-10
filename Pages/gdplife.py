#Common part
import pandas as pd
import streamlit as st
import altair as alt
from vega_datasets import data

df=pd.read_csv('data_final.csv')


# ------------------------------Bubble Plot: GDP/Life----------------------------------------------------------------------------
def write():
    st.header(":money_with_wings: How GDP per Capita and Life Expectancy with population of countries are related?")
    st.markdown('''
        In the following bubble plot, we can identify GDP Capita on X-axis and Life Expectancy (LifeExp) on Y-axis.
        The bubbles shows countries and shape of the bubbles shows their population values. So, bubbles are plotted on perticular values of X-axis and Y-axis.''')
    myexpander = st.beta_expander('Usage')
    myexpander.write('''Please select year to see bubble plot visualization of three parameters GDP per Capita, Life Expectancy and Population for countries. 
            Size of the bubble shows population, bigger is the bubble, higher is the size.
            Please hover on the bubbles to see values of GDP per Capita, Life Expectancy and Population with country names.''')
    myExpander = st.beta_expander('Explanation')
    myExpander.write('''Life expectancy at birth is defined as the average number of years that a newborn could expect to live if he or she were to pass through life subject to the age-specific mortality rates of a given period.
                GDP per capita is gross domestic product divided by midyear population. GDP is the sum of gross value added by all resident producers in the economy plus any product taxes and minus any subsidies not included in the value of the products.
                Bubble plot shows the improvement in GDP per Capita increases Life Expectancy. And plot is shifting to the right as we shift in the year.
    
    ''')
        
           
    select_year = st.slider('Select one year:', 2000, 2018, 2000)
    df.rename(columns={'GDP per Capita':'GDPCapita','Life Expectancy':'LifeExp'})
    years = df['Year'].unique() # get unique field values
    years = list(filter(lambda d: d is not None, years)) # filter out None values
    years.sort()

    selectYear = alt.selection_single(
        name='Select', # name the selection 'Select'
        fields=['Year'], # limit selection to the Major_Genre field
        init={'Year': years[0]}, # use first genre entry as initial value
        bind=alt.binding_select(options=years) # bind to a menu of unique genre values
    )
    chart = alt.Chart(df).mark_point(filled=True).encode(
        alt.X('Life Expectancy ', scale=alt.Scale(domain=(0, 85))),
        alt.Y('GDP per Capita', scale=alt.Scale(type='log', base=10, domain=(100, 80000))),
        # alt.Tooltip('Country'),
        tooltip=[alt.Tooltip('Country:N'),
                 alt.Tooltip('GDP per Capita:Q'),
                 alt.Tooltip('Life Expectancy :Q'),
                 alt.Tooltip('Population:Q')
                 ],
        size=alt.Size('Population', scale=alt.Scale(range=[100, 2000])),
        color=alt.Color('Country', legend=None)
    ).properties(height=600, width=800).add_selection(select_year).transform_filter(select_year)
    
    st.altair_chart(chart)
    
    st.altair_chart(chart)
