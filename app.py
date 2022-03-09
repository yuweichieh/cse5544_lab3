import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import altair as alt

st.title("OSU CSE5544 Lab3 Webpage")

st.header("Visualization Part")

st.subheader("Chosen data: Climate data that is used for Lab1 & Lab2")


df = pd.DataFrame({
    'c1':[1,2,3,4],
    'c2':[10,20,30,40]
})

data = pd.read_csv("https://raw.githubusercontent.com/CSE5544/data/main/ClimateData.csv")
data

#prepare the data
countries = data['Country\\year']
df_data_country = data.iloc[:,2:]
df_data_country = df_data_country.apply(pd.to_numeric, errors='coerce')
country_stats = pd.DataFrame({'country': countries, 'mean': df_data_country.mean(axis=1),
                       'std': df_data_country.std(axis=1)})

#render results
fig, ax = plt.subplots(figsize=(14, 6), dpi = 50)
ax.bar(countries, country_stats['mean'], yerr=country_stats['std'], capsize = 3)
ax.set_axisbelow(True)  #ensure the grid is under the graph elements
ax.margins(x=0.01) #set up the margin of graph
ax.grid(alpha = 0.3) #show the grid line
ax.set_xlabel('country')
ax.set_ylabel('emissions')
ax.set_title('The mean and std of emissions of countries')
xaxis = plt.xticks(rotation=90, ha='center', fontsize=8)
yaxis = plt.yticks(fontsize=8)

st.pyplot(fig)

st.subheader("altair chart")

chart_data = data.drop(columns=['Non-OECD Economies'])
chart_data = pd.melt(chart_data, id_vars=['Country\year'], var_name='year')
chart_data['value'] = chart_data['value'].apply(pd.to_numeric, errors='coerce')
chart_data.rename(columns={"Country\year": "country", "value":"emission"}, inplace = True)
chart_data

#render using altair
st.text("Heatmap1: With Scheme \"spectral\"")
heatmap1 = alt.Chart(chart_data).mark_rect().encode(
    x=alt.X('country:N', title = 'country'),
    y=alt.Y('year:O', title = 'year'),
    color = alt.Color('emission:Q', scale=alt.Scale(scheme='spectral')),
    tooltip=['country', 'year', 'emission']
)

st.altair_chart(heatmap1, use_container_width = True)


st.text("Heatmap2: With Scheme \"accent\"")
heatmap1 = alt.Chart(chart_data).mark_rect().encode(
    x=alt.X('country:N', title = 'country'),
    y=alt.Y('year:O', title = 'year'),
    color = alt.Color('emission:Q', scale=alt.Scale(scheme='greenblue')),
    tooltip=['country', 'year', 'emission']
)

st.altair_chart(heatmap2, use_container_width = True)