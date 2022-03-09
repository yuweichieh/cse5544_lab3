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
data.replace({'..': '0'}, inplace=True)
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
st.subheader("Heatmap1: With Scheme \"spectral\"")
heatmap1 = alt.Chart(chart_data).mark_rect().encode(
    x=alt.X('country:N', title = 'country'),
    y=alt.Y('year:O', title = 'year'),
    color = alt.Color('emission:Q', scale=alt.Scale(scheme='spectral')),
    tooltip=['country', 'year', 'emission']
)

st.altair_chart(heatmap1, use_container_width = True)


st.subheader("Heatmap2: With Scheme \"accent\"")
heatmap2 = alt.Chart(chart_data).mark_rect().encode(
    x=alt.X('country:N', title = 'country'),
    y=alt.Y('year:O', title = 'year'),
    color = alt.Color('emission:Q', scale=alt.Scale(scheme='greenblue')),
    tooltip=['country', 'year', 'emission']
)

st.altair_chart(heatmap2, use_container_width = True)

st.header("Analysis")
st.text("I use the Climate Data (same as Lab1 and Lab2) for this lab. And the two schemes I choose are “spectral” and “accent”. Since missing data creates some black blocks in the heatmap, which sometimes makes it difficult to compare the neighbor colors. Therefore, I set those missing data values to 0 and the result is shown as above. And for comparison, I prefer scheme spectral for this dataset. Because OECD rows are significantly larger than others, using accent which only has green and blue is hard to differ those light green colors from other. However, in scheme spectral, you can distinguish those red and orange easier. So I will say spectral is slightly better for me.")