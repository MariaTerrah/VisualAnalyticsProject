#Common part
import pandas as pd
import streamlit as st
import altair as alt
from vega_datasets import data

df=pd.read_csv('data_final.csv')
df.fillna(0,inplace=True)
control_dataset = df

    
# ------------------------------Poverty----------------------------------------------------------------------------

def poverty():

    df['Population living under $1.90 per day']=(df['Population']*df['Population with less than $1.90 per day'])/100
    df['Population living under $5.90 per day']=(df['Population']*df['Population with less than $5.90 per day'])/100
    
    
    years = df['Year'].unique() # get unique field values
    years = list(filter(lambda d: d is not None, years)) # filter out None values
    years.sort()
    
    
    
    selectYear = alt.selection_single(
        name='Select', # name the selection 'Select'
        fields=['Year'], # limit selection to the Major_Genre field
        init={'Year': years[0]}, # use first genre entry as initial value
        bind=alt.binding_select(options=years) # bind to a menu of unique genre values
    )
    
    
    
    
    countries = df['Country'].unique() # get unique field values
    countries = list(filter(lambda d: d is not None, countries)) # filter out None values
    countries.sort() #
    
    minyear = df.loc[:, 'Year'].min()
    maxyear = df.loc[:, 'Year'].max()
    
    
    data2=df[(df['Population with less than $1.90 per day']!=0)  & (df['Population with less than $5.90 per day']!=0)]
    data2.rename(columns={'Population with less than $1.90 per day':'per_pop_190','Population with less than $5.90 per day':'per_pop_590','Population living under $1.90 per day':'pop190','Population living under $5.90 per day':'pop590'},inplace=True)
    
    
    st.header('A major indicator : Poverty ')
    
    '''Poverty is influenced by and influences population dynamics, including population growth, age structure, and rural-urban distribution. All of this has a critical impact on a country's development prospects and prospects for raising living standards for the poor.
    '''
    
    countries = data2['Country'].unique().tolist()
    countries.remove("Angola")
    cty = st.selectbox("Select country:",countries)
    
    st.header(f" Evolution of poor population in {cty}")
    
    pop = alt.Chart(data2[data2["Country"] == cty]).mark_area(color="#F6DE74").encode(
        x="Year:N",
        y="Population",
        tooltip=["Year", "Population"]
    
    ).properties(
        width=700, # set the chart width to 400 pixels
        height=450  # set the chart height to 50 pixels
    ).interactive()
    
    pop190 = alt.Chart(data2[data2["Country"] == cty]).mark_area(color="#4BAB57").encode(
        x="Year:N",
        y="pop190",
        tooltip=["Year", "pop190"]
    
    ).properties(
        width=700, # set the chart width to 400 pixels
        height=450  # set the chart height to 50 pixels
    ).interactive()
    
    pop590 = alt.Chart(data2[data2["Country"] == cty]).mark_area(color="#CBD24B").encode(
        x="Year:N",
        y="pop590",
        tooltip=["Year", "pop590"]
    
    ).properties(
        width=700, # set the chart width to 400 pixels
        height=450  # set the chart height to 50 pixels
    ).interactive()
    
    opt = st.radio(
        "Select option:",
        ('Total population', 'Population living under 1.90$ a day','Population living under 5.90$ a day', 'Total population and population living under 1.90$ a day','Total population and population living under 5.90$ a day','All'))
    
    if opt == 'Total population':
        st.altair_chart(pop)
    elif opt == 'Population living under 1.90$ a day':
        st.altair_chart(pop190)
    elif opt == 'Population living under 5.90$ a day':
        st.altair_chart(pop590)
    elif opt == 'Total population and population living under 1.90$ a day':
        st.altair_chart(pop + pop190)
    elif opt == 'Total population and population living under 5.90$ a day':
        st.altair_chart(pop + pop590)
    else:
        st.altair_chart(pop + pop190 + pop590)
    
    ''' The share of people living in extreme poverty, as assessed by the international poverty line (IPL)
    estimated by the World Bank, has become one of the most prominent indicators for assessing
    progress in global economic development. It has been a central indicator for the Millennium
    Development Goals and is now an important indicator among the Sustainable Development
    Goals'''
    
    
    
    selectCountry = st.multiselect('Select country or countries:',
                            data2.groupby('Country').count().reset_index()['Country'].tolist(),
                            default=['Argentina', 'Brazil', 'Turkey'])
    
    select_period = st.slider('Select period:', int(str(minyear)), int(str(maxyear)), (2000, 2018))
    
    
    st.subheader('Share of population living under 5.90$')
    
    chart1 = alt.Chart(data2).mark_line().encode(
        alt.X('Year:O'),
        alt.Y('per_pop_590:Q',axis=alt.Axis(title='% of population living under 5.90$')),
        alt.Color('Country:N'),
    ).transform_filter(
        {'and': [{'field': 'Country', 'oneOf': selectCountry},
                {'field': 'Year', 'range': select_period}]}
        ).properties(
        width=700, # set the chart width to 400 pixels
        height=450  # set the chart height to 50 pixels
    )
    st.altair_chart(chart1)
    
    
    st.subheader('Share of population living under 1.90$')
    
    chart2 = alt.Chart(data2).mark_line().encode(
        alt.X('Year:O'),
        alt.Y('per_pop_190:Q',axis=alt.Axis(title='% of population living under 1.90$')),
        alt.Color('Country:N'),
    ).transform_filter(
        {'and': [{'field': 'Country', 'oneOf': selectCountry},
                {'field': 'Year', 'range': select_period}]}
        ).properties(
        width=700, # set the chart width to 400 pixels
        height=450  # set the chart height to 50 pixels
    )
    st.altair_chart(chart2)

