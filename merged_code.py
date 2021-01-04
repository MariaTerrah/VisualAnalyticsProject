import pandas as pd
import streamlit as st
import altair as alt
import numpy as np
from vega_datasets import data

'''This app is to give insight about populations' growth and evolution , poverty in population'''

'''The world’s population is always changing drastically, with some countries growing rapidly and others shrinking in population size.Thiss map shows which countries are growing faster and which have the most negative growth. There is indeed a trend of countries with higher GDPs growing slower or stagnating, while the poorest countries are often the ones growing most rapidly.

This is largely due to the remaining high fertility rates in developing countries even as mortality rates are falling, resulting in enormous population growth. Africa has the most countries with high growth, while Eastern Europe, Russia, and Japan all have shrinking populations'''


data1=pd.read_csv('final_data.csv')
data1['Pop_under_190']=(data1['Population']*data1['Poverty190'])/100
data1['Pop_under_590']=(data1['Population']*data1['Poverty590'])/100


years = data1['Year'].unique() # get unique field values
years = list(filter(lambda d: d is not None, years)) # filter out None values
years.sort()



selectYear = alt.selection_single(
    name='Select', # name the selection 'Select'
    fields=['Year'], # limit selection to the Major_Genre field
    init={'Year': years[0]}, # use first genre entry as initial value
    bind=alt.binding_select(options=years) # bind to a menu of unique genre values
)

source = alt.topo_feature(data.world_110m.url, "countries")

background = alt.Chart(source).mark_geoshape(fill="white")

foreground = (
    alt.Chart(source)
    .mark_geoshape(stroke="black", strokeWidth=0.15)
    .add_selection(
        selectYear
    )
        .encode(
        color=alt.Color(
            "Poverty190:N", scale=alt.Scale(scheme="lightgreyred"), legend=None,
        ),
        tooltip=[
            alt.Tooltip("Country:N", title="Country"),
            alt.Tooltip("Poverty190:Q", title="% of population living under 1.90$ a day"),
            alt.Tooltip("Year:O", title="Year")
        ],
        opacity=alt.condition(selectYear, alt.value(0.80), alt.value(0.40))
    )
    .transform_lookup(
        lookup="id",
        from_=alt.LookupData(data1, "id", ["Poverty190", "Country","Year"]),
    )
)

final_map = (
    (background + foreground)
    .configure_view(strokeWidth=0)
    .properties(width=700, height=400)
    .project("naturalEarth1")
)

st.write(final_map)

'''Poverty is influenced by and influences population dynamics, including population growth, age structure, and rural-urban distribution. All of this has a critical impact on a country's development prospects and prospects for raising living standards for the poor.
'''

countries = data1['Country'].unique() # get unique field values
countries = list(filter(lambda d: d is not None, countries)) # filter out None values
countries.sort() #

minyear = data1.loc[:, 'Year'].min()
maxyear = data1.loc[:, 'Year'].max()

''' bla bla '''

data2=data1[(data1['Poverty190']!=0)  & (data1['Poverty590']!=0)]



st.header('Poverty rates evolution in countries')

countries = data2['Country'].unique()
cty = st.selectbox("Select country",countries)

st.header(f" for {cty}")

pop = alt.Chart(data2[data2["Country"] == cty]).mark_area(color="blue").encode(
    x="Year:N",
    y="Population",
    tooltip=["Year", "Population"]

).properties(
    width=700, # set the chart width to 400 pixels
    height=450  # set the chart height to 50 pixels
).interactive()

pop190 = alt.Chart(data2[data2["Country"] == cty]).mark_area(color="green").encode(
    x="Year:N",
    y="Pop_under_190",
    tooltip=["Year", "Pop_under_190"]

).properties(
    width=700, # set the chart width to 400 pixels
    height=450  # set the chart height to 50 pixels
).interactive()

pop590 = alt.Chart(data2[data2["Country"] == cty]).mark_area(color="yellow").encode(
    x="Year:N",
    y="Pop_under_590",
    tooltip=["Year", "Pop_under_590"]

).properties(
    width=700, # set the chart width to 400 pixels
    height=450  # set the chart height to 50 pixels
).interactive()

opt = st.radio(
    "Select the option",
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

''' bla blou'''


selectCountry = st.multiselect('Select country or countries:',
                        data2.groupby('Country').count().reset_index()['Country'].tolist(),
                        default=['Argentina', 'Brazil', 'Turkey'])

select_period = st.slider('Select a period to plot', int(str(minyear)), int(str(maxyear)), (2000, 2018))




chart1 = alt.Chart(data2).mark_line().encode(
    alt.X('Year:O'),
    alt.Y('Poverty590:Q',axis=alt.Axis(title='% of population living under 5.90$')),
    alt.Color('Country:N'),
).transform_filter(
    {'and': [{'field': 'Country', 'oneOf': selectCountry},
            {'field': 'Year', 'range': select_period}]}
    ).properties(
    width=700, # set the chart width to 400 pixels
    height=450  # set the chart height to 50 pixels
)
st.altair_chart(chart1)




chart2 = alt.Chart(data2).mark_line().encode(
    alt.X('Year:O'),
    alt.Y('Poverty190:Q',axis=alt.Axis(title='% of population living under 1.90$')),
    alt.Color('Country:N'),
).transform_filter(
    {'and': [{'field': 'Country', 'oneOf': selectCountry},
            {'field': 'Year', 'range': select_period}]}
    ).properties(
    width=700, # set the chart width to 400 pixels
    height=450  # set the chart height to 50 pixels
)
st.altair_chart(chart2)





