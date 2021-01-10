#Common part
import pandas as pd
import streamlit as st
import altair as alt
from vega_datasets import data

df=pd.read_csv('data_final.csv')
df.fillna(0,inplace=True)
control_dataset = df

# ------------------------------Maps----------------------------------------------------------------------------
   
def write():
    st.header("A global view of the parameter spread around the world by using map.")
        
    years = df['Year'].unique()
    
    control_metrics = ["Population",
                       "Density",
                       "Life Expectancy ",
                       "GDP per Capita",
                       "Fertility Rate",
                       "Population living in a city of +1M inhabitants",
                       "Population living in a rural area",
                       "Unemployment Rate",	
                       "Population aged between 0-14",	
                       "Population aged between 15-64",	
                       "Population aged +65"	
                       ]
    st.markdown('In the following map, we can identify the intensity of a specific parameter for each country. We can also see the evolution of these parameters from 2000 to 2018.')
    my_expander = st.beta_expander('Usage')
    my_expander.write('''Please select parameter to be analysed by using drop down menu.
            And then please TYPE the year (between 2000 to 2018) to visualize selected parameter across the world.
            After mouse hover, you will be able to read the country name, parameter value and year for each country in the world map.''') 
    cols = st.selectbox('Select parameter to visualize: ', control_metrics)
    
    if cols in control_metrics:
        metric_to_show = cols + ":Q"
        metric_name = cols
        metric_name
               

    ####### Map Visualization
    
    source = alt.topo_feature(data.world_110m.url, "countries")
    geoshape = alt.Chart(source).mark_geoshape(fill="white")
    
    user_input = st.text_input("Type year within 2000 to 2018", 2000)
    user_input = int(user_input)
    data_selected = df[df["Year"] == user_input]
    # data_selected
    
    chart = (
        alt.Chart(source)
            .mark_geoshape(stroke="black", strokeWidth=0.15)
            .encode(
            color=alt.Color(
                # "population:N", scale=alt.Scale(scheme="lighttealblue"), legend=None,
                metric_to_show, scale=alt.Scale(scheme="lighttealblue"), legend=None
            ),
            tooltip=[
                alt.Tooltip("Country:N", title="Country"),
                alt.Tooltip(metric_to_show, title=metric_name),
                alt.Tooltip("Year:O", title="Year")
            ]
        )
            .transform_lookup(
            lookup="id",
            from_=alt.LookupData(data_selected, "id", [metric_name, "Country", "Year"]),
        )
    
    )
    
    map = (
            (geoshape + chart)
                .configure_view(strokeWidth=0)
                .properties(height=400)
                .project("naturalEarth1")
        )
    st.altair_chart(map)
