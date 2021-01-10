#Common part
import pandas as pd
import streamlit as st
import altair as alt
from vega_datasets import data

df=pd.read_csv('data_final.csv')
df.fillna(0,inplace=True)
control_dataset = df

# ------------------------------Bubble Plot: GDP/Life----------------------------------------------------------------------------
def write():
    st.header("How GDP per Capita and Life Expectancy with population of countries are related.")
    '''
        In the following bubble plot, we can identify GDP Capita on Y-axis and Life Expectancy (LifeExp) on X-axis.
        The bubbles shows countries and shape of the bubbles shows their population values. So, bubbles are plotted on perticular values of X-axis and Y-axis.
        
        Usage:
        
            Please select year to see bubble plot visualization of three parameters GDPCapita (GDP capitalization), LifeExp (Life Expectancy ) and population for countries.
            Size of the bubble shows population, bigger is the bubble, higher is the size.
            Please hover on the bubbles to see values of GDPCapita, LifeExp and population with country names.
            
            Explanation:            
                Life expectancy at birth is defined as the average number of years that a newborn could expect to live if he or she were to pass through life subject to the age-specific mortality rates of a given period.
                GDP per capita is gross domestic product divided by midyear population. GDP is the sum of gross value added by all resident producers in the economy plus any product taxes and minus any subsidies not included in the value of the products.
                Bubble plot shows the improvement in GDP Capita increases life expectancy. And plot is shifting to the right as we shift in the year.
    
    '''
    select_year = alt.selection_single(
        name='select', fields=['Year'], init={'Year': 2000},
        bind=alt.binding_range(min=2000, max=2018, step=1)
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