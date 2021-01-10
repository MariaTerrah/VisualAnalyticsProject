#Common part
import pandas as pd
import streamlit as st
import altair as alt
from vega_datasets import data

df=pd.read_csv('data_final.csv')
df.fillna(0,inplace=True)
control_dataset = df


####### Dashboard

st.set_page_config(layout="wide")
st.title("Population Analytics")

st.header("How are population , density, poverty and otehr parameters are spread across the world. ")

'''
When it comes to learning more about the population distribution over the world, one can certainly wonder first where are the most populated areas. However, this isn’t enough to know who lives there and how. 
Therefore, we decided to add some useful features, when available, like density, poverty, literacy rate, GDP per capita, GINI index, rural population, population living in a city of more than 1 million inhabitants, unemployment rate, life expectancy, fertility rate and distribution of the population in 3 segments (children, labor force, elder people). 
This enable us to know more about the status of each country : for example China may be a highy populated country as India but the difference is that India is a younger country.
All the data are coming from the World Bank OpenData website, you can find the original dataset and the metadata on the github.
'''
st.header("A global view of the parameter spread around the world by using map.")


years = df['Year'].unique()
# years
# type(years)
####### Control Measures given by WHO

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
# year=years
# years=['2000', '2001', '2002', '2003', '2004', '2004','2005','2006','2007','2008','2009','2010','']

cols = st.selectbox('Select parameter to visualize: ', control_metrics)
    # cols

if cols in control_metrics:
    metric_to_show_in_covid_Layer = cols + ":Q"
    metric_name = cols
    metric_name

#st.header("A global view of the parameter spread around the world.",metric_name)

'''
    In the following map, we can identify the intensity of a specific parameter for each country. 
    We can also see the evolution of these parameters from 2000 to 2018.
    
    Usage:
    
        Please select parameter to be analysed by using drop down menu.
        And then please TYPE the year (between 2000 to 2018) to visualize selected parameter across the world.
        After mouse hover, you will be able to read the country name, parameter value and year for each country in the world map.

'''
####### Map Visualization


# -------------------------------------------------------------------------------------------------------------------------------------
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
'''
    In the following choropleth map, we can identify the population of each country which is encoded by color intensity. 
    We can also see the evolution of density encoded with shape of red colored bubbles. The evolution of data is from 2000 to 2018.
    
    Usage:
    
        Please hover on red bubbles and on countries to see data values for population and density. Bigger shape of the bubbles shows the highly dense value.
'''
# data_selected
# Year Selection:
user_input_1 = st.text_input("Please TYPE the year (between 2000 to 2018) to visualize densely populated countries for selected year, default year is 2000.", 2000)
user_input_1=int(user_input_1)
data_selected=df[df["Year"]==user_input_1]
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
    tooltip=['Country:N', 'Density:Q', 'Population:Q', 'GDP per Capita:Q', 'Year:N']
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

#Constrcution of selectors (!!!!!!! Common part)
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

# ------------------------------Disclaimers----------------------------------------------------------------------------
st.header('Disclaimers')
''' 
The goal of this tool is to be able to learn more about the status of the 7 billion people living on earth. This tool tries to describe where and how people are living. 
The living conditions are described by life expectancy, density, etc. However, some data must be approached carefully: most of the values are calculated according to international standards but some may not reflect the entire reality. 
For example, GDP per capita is not a real measure of the wealth distribution. But, when confronted to other indicators it helps understand the actual distribution.
''' 