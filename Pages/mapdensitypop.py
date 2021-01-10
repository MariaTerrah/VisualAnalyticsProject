#Common part
import pandas as pd
import streamlit as st
import altair as alt
from vega_datasets import data

df=pd.read_csv('data_final.csv')
df.fillna(0,inplace=True)
control_dataset = df

# ------------------------------Density and Population----------------------------------------------------------------------------
def write():
    st.header("Most Densly populated countries across the world! ")
    st.markdown('''In the following choropleth map, we can identify the population of each country which is encoded by color intensity. 
        We can also see the evolution of density encoded with shape of red colored bubbles. The evolution of data is from 2000 to 2018.''')
    mexpander = st.beta_expander('Usage')
    mexpander.write('''Please hover on red bubbles and on countries to see data values for population and density. Bigger shape of the bubbles shows the highly dense value.''') 

    # data_selected
    # Year Selection:
    user_input_1 = st.text_input("Please TYPE the year (between 2000 to 2018) to visualize densely populated countries for selected year, default year is 2000.", 2000)
    user_input_1=int(user_input_1)
    data_selected=df[df["Year"]==user_input_1]
    source = alt.topo_feature(data.world_110m.url, "countries")

    base = alt.Chart(source).mark_geoshape(
        fill='lightgray',
        stroke='white'
    ).properties(
        width=800,
        height=400
    )
    
    chro = alt.Chart(source).mark_geoshape().encode(
        color='Population:Q',
        # strokeDash='Density:Q',
        # stroke='GDPCapita:Q',
        tooltip=[
            alt.Tooltip("Country:N", title="Country"),
            alt.Tooltip("Population:Q", title="population"),
            alt.Tooltip("Year:Q", title="Year"),
    
        ]
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(data_selected, 'id', ['Country', 'Population', 'Year'])
    ).project(
        type='naturalEarth1'
    ).properties(
        width=500,
        height=300
    )
    # chro
    
    points = alt.Chart().mark_circle(filled=True,
                                     opacity=0.4).encode(
        latitude='Latitude:Q',
        longitude='Longitude:Q',
        size=alt.Size('Density:Q', scale=alt.Scale(range=[0, 1000]), legend=alt.Legend(title="Density")),
        color='Density:Q',
        fill=alt.value('red'),
        stroke=alt.value('white'),
        tooltip=['Country:N', 'Density:Q', 'Population:Q', 'GDP per Capita:Q', 'Year:N']
    )
    final = chro + points
    
    
    c = alt.layer(base, final, data=data_selected).facet(
        facet='Year:N',
        columns=2,
        title='The Most Populous countries in the World'
    )
    st.altair_chart(c)
