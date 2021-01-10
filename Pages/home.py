
#Common part
import pandas as pd
import streamlit as st
import altair as alt
from vega_datasets import data
from PIL import Image

df=pd.read_csv('data_final.csv')
df.fillna(0,inplace=True)
control_dataset = df

# ------------------------------Home----------------------------------------------------------------------------

def write():
    
    image = Image.open('Pages/picture.jpeg')

    st.title(":earth_africa: Population Analytics :earth_africa:")
    st.header(':grey_question: How are population, density, poverty and other parameters spread across the world ?')

    st.markdown('When it comes to learning more about the population distribution over the world, one can certainly wonder first where are the most populated areas. However, this isn’t enough to know who lives there and how. Therefore, we decided to add some useful features, when available, like density, poverty, literacy rate, GDP per capita, GINI index, rural population, population living in a city of more than 1 million inhabitants, unemployment rate, life expectancy, fertility rate and distribution of the population in 3 segments (children, labor force, elder people). This enable us to know more about the status of each country : for example China may be a highy populated country as India but the difference is that India is a younger country.')
    st.image(image, caption='According to the UN, we will be more than 9 billion people by 2050', use_column_width=True)
    st.markdown(':information_source: All the data are coming from the **World Bank OpenData** website, you can find the original dataset and the metadata on the github.')

    #Disclaimers----------------------------------------------------------------------------
    st.header(':warning: Disclaimers')

    st.markdown('_The goal of this tool is to be able to learn more about the status of the 7 billion people living on earth. This tool tries to describe where and how people are living. The living conditions are described by life expectancy, density, etc. However, some data must be approached carefully: most of the values are calculated according to international standards but some may not reflect the entire reality. For example, GDP per capita is not a real measure of the wealth distribution. But, when confronted to other indicators it helps understand the actual distribution._') 
