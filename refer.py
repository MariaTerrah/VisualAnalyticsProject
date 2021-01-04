import streamlit as st
import pandas as pd
import altair as alt
import json
import requests
import numpy as np
from IPython.display import display, HTML
from altair import datum
from vega_datasets import data


####### Datasets
path="final_data.csv"
df = pd.read_csv(path)
df=df[(df['Poverty190']!=0)  & (df['Poverty590']!=0)]
#df
#control_dataset = 'https://raw.githubusercontent.com/JulioCandela1993/VisualAnalytics/master/data/control_policy.csv'
#control_dataset="C:\\Users\\POOJA\\Visual_Analytics\\final_data.csv"
control_dataset=df
control_dataset
####### Dashboard

st.title("Population Analytics")


st.header("How are population , density and poverty are spread across the world. ")


years = df['Year'].unique()
years
type(years)
####### Control Measures given by WHO

control_metrics = ["Population",	
           "Density",	
           "Poverty190",
           "Poverty590",
           "LifeExp",
           "GDPCapita"           
]
#year=years
#years=['2000', '2001', '2002', '2003', '2004', '2004','2005','2006','2007','2008','2009','2010','']
#container_map = st.beta_container()
#with container_map:

cols = st.selectbox('Select parameter to visualize: ', control_metrics)
    #cols
    
if cols in control_metrics:
    metric_to_show_in_map_Layer = cols +":Q"
    metric_name = cols

    
st.header("A global view of the parameters spread around the world.")




####### Map Visualization


#-------------------------------------------------------------------------------------------------------------------------------------

slider = alt.binding_range(min=2000, max=2018, step=1)
select_year = alt.selection_single(name='Year', fields=['Year'],
                                   bind=slider, init={'Year': 2000})
years = df['Year'].unique() # get unique field values
s_year = st.selectbox('Year',years)

#years
#years = list(filter(lambda x: x is not None, years)) # filter out None values
#years.sort()
#years[0]
selectYear = alt.selection_single(
    name='Select',
    fields=['Year'],
    init={'Year': years[0]},
    bind=alt.binding_select(options=years)
)

source = alt.topo_feature(data.world_110m.url, "countries")

geoshape = alt.Chart(source).mark_geoshape(fill="white")

chart = (
    alt.Chart(source)
    .mark_geoshape(stroke="black", strokeWidth=0.15)
        .encode(
        color=
            #"population:N", scale=alt.Scale(scheme="lighttealblue"), legend=None,
            metric_to_show_in_map_Layer
        ,
        tooltip=[
            alt.Tooltip("Country:N", title="Country"),
            alt.Tooltip(metric_to_show_in_map_Layer, title=metric_name),
            alt.Tooltip("Year:O", title="Year")
        ],
        opacity=alt.condition(select_year, alt.value(0.80), alt.value(0.50))
    )
    .transform_lookup(
        lookup="id",
        from_=alt.LookupData(df, "id", [metric_name, "Country","Year"]),
    ).transform_calculate(
    year='parseInt(datum.Year)',
).transform_filter(
    alt.FieldEqualPredicate(field='year', equal=s_year)
)
)
map = (
        (geoshape + chart)
        .configure_view(strokeWidth=0)
        .properties(width=800, height=600)
        .project("naturalEarth1")
    )
st.altair_chart(map)



