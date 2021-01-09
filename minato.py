#Common part
import pandas as pd
import streamlit as st
import altair as alt
from vega_datasets import data

df=pd.read_csv('data_final.csv')
df.fillna(0,inplace=True)
control_dataset = df

####### Dashboard

st.title("Population Analytics")

st.header("How are population , density and poverty are spread across the world. ")

'''
The following analysis is based on the evaluation made by World Health Organization (WHO) 
to country policies against Tobacco. A score from 1 to 5 is assigned depending on the intensity 
of a country to deal with Tobacco issues being 1 the worst and 5 the best
'''
years = df['Year'].unique()
# years
# type(years)
####### Control Measures given by WHO

control_metrics = ["Population",
                   "Density",
                   "LifeExp",
                   "GDPCapita",
                   "FertilityRate",
                   "PopUrban1M",
                   "RuralPop",
                   # "Poverty190",
                   # "Poverty590",
                   "Unemployment",
                   "Pop0-14",
                   "Pop15-64",
                   "Pop65"
                   ]
# year=years
# years=['2000', '2001', '2002', '2003', '2004', '2004','2005','2006','2007','2008','2009','2010','']

cols = st.selectbox('Select parameter to visualize: ', control_metrics)
    # cols

if cols in control_metrics:
    metric_to_show_in_covid_Layer = cols + ":Q"
    metric_name = cols
    metric_name

st.header("A global view of the parameters spread around the world.")

'''
    In the following map, we can identify the intensity of a specific parameter for each country. 
    We can also see the evolution of these parameters from 2000 to 2018
'''
####### Map Visualization


# -------------------------------------------------------------------------------------------------------------------------------------
source = alt.topo_feature(data.world_110m.url, "countries")
geoshape = alt.Chart(source).mark_geoshape(fill="white")

user_input = st.text_input("Type year within 2000 to 2010", 2000)
user_input = int(user_input)
data_selected = df[df["Year"] == user_input]
# data_selected

chart = (
    alt.Chart(source)
        .mark_geoshape(stroke="black", strokeWidth=0.15)
        .encode(
        color=alt.Color(
            # "population:N", scale=alt.Scale(scheme="lighttealblue"), legend=None,
            metric_to_show_in_covid_Layer, scale=alt.Scale(scheme="lighttealblue"), legend=None
        ),
        tooltip=[
            alt.Tooltip("Country:N", title="Country"),
            alt.Tooltip(metric_to_show_in_covid_Layer, title=metric_name),
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
            .properties(width=700, height=400)
            .project("naturalEarth1")
    )
st.altair_chart(map)

# -----------------------------------------------------------------------------------------------------------------
st.header("Most Densly populated countries across the world! ")

# data_selected
# Year Selection:

base = alt.Chart(source).mark_geoshape(
    fill='lightgray',
    stroke='white'
).properties(
    width=700,
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
    tooltip=['Country:N', 'Density:Q', 'Population:Q', 'GDPCapita:Q', 'Year:N']
)
final = chro + points
# final1=background+chart+points


c = alt.layer(base, final, data=data_selected).facet(
    facet='Year:N',
    columns=2,
    title='The Most Populous countries in the World'
)
st.altair_chart(c)

# ------------------------------Bubble Plot----------------------------------------------------------------------------
st.header("GDPCapita and LifeExp Plot! ")
select_year = alt.selection_single(
    name='select', fields=['Year'], init={'Year': 2000},
    bind=alt.binding_range(min=2000, max=2018, step=1)
)

chart = alt.Chart(df).mark_point(filled=True).encode(
    alt.X('LifeExp', scale=alt.Scale(domain=(20, 85))),
    alt.Y('GDPCapita', scale=alt.Scale(type='log', base=10, domain=(100, 80000))),
    # alt.Tooltip('Country'),
    tooltip=[alt.Tooltip('Country:N'),
             alt.Tooltip('GDPCapita:Q'),
             alt.Tooltip('LifeExp:Q'),
             alt.Tooltip('Population:Q')
             ],
    size=alt.Size('Population', scale=alt.Scale(range=[100, 2000])),
    color=alt.Color('Country', legend=None)
).properties(height=600, width=800).add_selection(select_year).transform_filter(select_year)

st.altair_chart(chart)

#Constrcution of selectors (!!!!!!! Common part)
slider = alt.binding_range(min=2000, max=2018, step=1, name='Years')
selector = alt.selection_single(name="Years", fields=['Years'],
                                bind=slider, init={'Years': 2000})

features=['Population','Density','Poverty190','Poverty590','GiniIndex',
           'LifeExp','GDPCapita','LiteracyRate','FertilityRate','PopUrban1M','RuralPop','Unemployment',
               'Pop0-14','Pop15-64','Pop65']
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

#COMPARISON OF TWO COUNTRIES FOR POP STATUS
c1=alt.Chart(df).transform_fold(
    ['PopUrban1M','RuralPop','Unemployment'],
    as_=['Population Status', 'Proportion (%)']
).mark_area(
    opacity=0.3
).encode(
    alt.X('Year:O'),
    alt.Y('Proportion (%):Q', stack=None),
    alt.Color('Population Status:N',scale=alt.Scale(domain=['PopUrban1M','RuralPop','Unemployment'],
                      range=['red', 'gold','blue'])),
).add_selection(
        selectCountry
    ).transform_filter(
    selectCountry)

c2=alt.Chart(df).transform_fold(
    ['PopUrban1M','RuralPop','Unemployment'],
    as_=['Population Status', 'Proportion (%)']
).mark_area(
    opacity=0.3
).encode(
    alt.X('Year:O'),
    alt.Y('Proportion (%):Q', stack=None),
    alt.Color('Population Status:N')
).add_selection(
        selectCountry2
    ).transform_filter(
    selectCountry2)

st.altair_chart(c1 | c2)

#COMPARISON OF TWO COUNTRIES FOR POP AGE
c3=alt.Chart(df).transform_fold(
    ['Pop0-14','Pop15-64','Pop65'],
    as_=['Age Distribution', 'Proportion (%)']
).mark_area(
    opacity=0.3
).encode(
    alt.X('Year:O'),
    alt.Y('Proportion (%):Q', stack=None),
    alt.Color('Age Distribution:N',scale=alt.Scale(domain=['Pop0-14','Pop15-64','Pop65'],
                      range=['green', 'silver','purple'])),
).add_selection(
        selectCountry
    ).transform_filter(
    selectCountry)

c4=alt.Chart(df).transform_fold(
    ['Pop0-14','Pop15-64','Pop65'],
    as_=['Age Distribution', 'Proportion (%)']
).mark_area(
    opacity=0.3
).encode(
    alt.X('Year:O'),
    alt.Y('Proportion (%):Q', stack=None),
    alt.Color('Age Distribution:N')
).add_selection(
        selectCountry2
    ).transform_filter(
    selectCountry2)

st.altair_chart(c3 | c4)


df['Pop_under_190']=(df['Population']*df['Poverty190'])/100
df['Pop_under_590']=(df['Population']*df['Poverty590'])/100


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


data2=df[(df['Poverty190']!=0)  & (df['Poverty590']!=0)]



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
    y="Pop_under_190",
    tooltip=["Year", "Pop_under_190"]

).properties(
    width=700, # set the chart width to 400 pixels
    height=450  # set the chart height to 50 pixels
).interactive()

pop590 = alt.Chart(data2[data2["Country"] == cty]).mark_area(color="#CBD24B").encode(
    x="Year:N",
    y="Pop_under_590",
    tooltip=["Year", "Pop_under_590"]

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


st.subheader('Share of population living under 1.90$')

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

