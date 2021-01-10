#Common part
import pandas as pd
import streamlit as st
import altair as alt
from vega_datasets import data
import Pages.home as home
import Pages.mapfeatures as mapfeatures
import Pages.mapdensitypop as mapdensitypop
import Pages.gdplife as gdplife
import Pages.comp as comp
import Pages.poverty as poverty


df=pd.read_csv('data_final.csv')
df.fillna(0,inplace=True)
control_dataset = df

# ------------------------------Navigation Menu----------------------------------------------------------------------------


PAGES = {
    "Homepage": home,
    "Maps": mapfeatures,
    "Density and Population": mapdensitypop,
    "GDP and Life Expectancy": gdplife,
    "Comparators": comp,
    "Poverty": poverty,
}
def main():
    st.sidebar.title('Population Analytics')
    selection = st.sidebar.radio("Choose a topic", list(PAGES.keys()))
    page = PAGES[selection]
    page.write()


if __name__ == "__main__":
	main()
