import streamlit as st

import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter

import plotly.express as px
from plotly import graph_objects as go
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.transform import factor_cmap
from bokeh.palettes import Category20

st.set_page_config(
    page_title="Habits",
)

# Sidebar customization
with st.sidebar:
    st.write("Author:")
    st.write("Emma DESTE")
    st.write("Efrei Paris - Promo 2025")
    st.write('<span style="color: red; font-size: 20px;"> #datavz2023efrei </span>',
             unsafe_allow_html=True)

    # Link to my other works
    image_path = "github.png"
    left_co, cent_co, last_co = st.columns(3)  # to center the logo (https://discuss.streamlit.io/t/how-can-i-center-a-picture/30995/3)
    with cent_co:
        st.image(image_path, width=50)
    st.write('<span style="color: gray; font-size: 13px;"> https://github.com/EmmaDeste </span>',
             unsafe_allow_html=True)

    image_path = "linkedin.png"
    left_co, cent_co, last_co = st.columns(3)  # to center the logo
    with cent_co:
        st.image(image_path, width=50)
    st.write('<span style="color: gray; font-size: 13px;"> www.linkedin.com/in/emmadeste/ </span>',
             unsafe_allow_html=True)

# -----------------------------------------------------
st.title("Discover the French habits about food")

conso = pd.read_csv('consommation_fr.csv')


# -- 1. Wordcloud of the most consumed foods (Matplotlib)

st.write('<span style="color: green; font-size: 25px;"> 🔝 - Overview of the most eaten foods </span>',
             unsafe_allow_html=True)

word_freq = Counter(conso['occ_alim_libelle'].str.cat(sep=' ').split())

wordcloud = WordCloud(width=800, height=400, max_words=50, background_color='white', colormap='plasma').generate_from_frequencies(word_freq)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
# warning: avoid calling sm.pyplot() without argument
st.set_option('deprecation.showPyplotGlobalUse', False)
st.pyplot()

st.text("\n")


# -- 2. Pie of most consumed foods (Plotly)

st.write('<span style="color: green; font-size: 25px;"> ‍🔥 - Statistical repartition of the most eaten foods </span>',
             unsafe_allow_html=True)

aliment = {'occ_alim_libelle': list(conso['occ_alim_libelle'].value_counts().head(20).index),
        'freq': list(conso['occ_alim_libelle'].value_counts().head(20))}
conso_counts = pd.DataFrame(aliment)

fig = px.pie(conso_counts, names='occ_alim_libelle', values='freq')

st.plotly_chart(fig)

st.write("There's no question about it: we are facing French population.")
st.write("Top 15: 🥖, 🧀 and 🍷 represents almost 1/4 (22.6%) of the total diet.")

st.text("\n")

if st.button('You want to know the whole list of foods?'):
    values_head = conso['occ_alim_libelle'].value_counts().head(40)
    st.write("Top 40")
    st.table(values_head)
    values_tail = conso['occ_alim_libelle'].value_counts().tail(40)
    st.write("Last 40")
    st.table(values_tail)  # use table sinon .write affiche que les 10 premiers

    if st.button('Hide'):
        st.empty()  # réinitialise le conteneur de la table

st.text("\n")
st.text("\n")
st.text("\n")


# -- 3. Density Heatmap of quantity eaten throughout the day (Plotly)

st.write('<span style="color: green; font-size: 25px;"> 🍽️ - Quantity eaten through the day </span>',
             unsafe_allow_html=True)

fig = px.density_heatmap(conso, x='occ_hdeb', y='qte_conso', color_continuous_scale='Plasma')

fig.update_layout(
    xaxis_title="Hour of the day",
    xaxis_tickformat='%H:%M',
    yaxis_title="Quantity",
    yaxis_range=[0, 300]
)

st.plotly_chart(fig)

st.write("We recognize French mealtimes 🕒:")
st.markdown("Breakfast 6:30-10:00 | Lunch 12:00-14:00 | Snack 16:00-17:30 | Dinner 19:00-21:30")
st.text("\n")
st.write("Frenchies are not early birds, breakfast is the lightest meal, while Lunch is the main one.")

st.text("\n")
st.text("\n")
st.text("\n")


# -- 4. Histogram of the breakfast habits (Bokeh)

st.write('<span style="color: green; font-size: 25px;"> 🌅 - Breakfast French habits </span>',
             unsafe_allow_html=True)

# replace invalid values with NaT, to drop them
morning = pd.read_csv('morning_conso.csv')
morning['occ_hdeb'] = pd.to_datetime(morning['occ_hdeb'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
morning = morning.dropna(subset=['occ_hdeb'])

# Extract 6h-10h30 data
mask = (morning['occ_hdeb'].dt.hour >= 6) & (morning['occ_hdeb'].dt.hour < 10) & (morning['occ_hdeb'].dt.minute <= 30)
morning_data = morning[mask]

# Get value counts for 'occ_alim_libelle'
food_counts = morning_data['occ_alim_libelle'].value_counts()

# Select top 15 for clearer histogram
top_15 = food_counts.head(14)
aliments_liste = top_15.index.tolist()

# Data source for Bokeh to proceed
source = ColumnDataSource(data=dict(aliment=aliments_liste, occurrences=top_15.values))

h = figure(x_range=aliments_liste, plot_height=350,
           toolbar_location=None, tools='')
# add bars
bars = h.vbar(x='aliment', top='occurrences', width=0.9, source=source,
              line_color='white', fill_color=factor_cmap('aliment', palette=Category20[10], factors=aliments_liste))

# give more interactivity to the user
tooltips = [("Aliment", "@aliment"), ("Occurrences", "@occurrences")]
h.add_tools(HoverTool(renderers=[bars], tooltips=tooltips))

h.xgrid.grid_line_color = None
h.y_range.start = 0
h.y_range.end = top_15.max() + 1
h.xaxis.major_label_orientation = 1.2  # rotation for lisibility

st.bokeh_chart(h)

st.write("Timeless: ☕, 🫖,🧃, 🥛 & 🥣")
st.write("French recognizable products at the top: 🥖, 🍞, 🥐")

st.text("\n")
st.text("\n")
st.text("\n")


# -- 5. Organic food production (Plotly)
# thanks to https://plotly.com/python/funnel-charts/

st.write('<span style="color: green; font-size: 25px;"> 🚜 - Organic food consumption </span>',
             unsafe_allow_html=True)

eco_package = conso
eco_package['aliment_marque_bio'].dropna() # to avoid inconsistent data

# add legend to visualize more clearly
eco_package['aliment_marque_bio'] = eco_package['aliment_marque_bio'].replace(
    {0: 'Non Bio', 1: 'Bio', 2: 'Bio & Durable'})

fig = go.Figure(go.Funnelarea(
    text=eco_package['aliment_marque_bio'].value_counts().index,
    values=eco_package['aliment_marque_bio'].value_counts().values
))

st.plotly_chart(fig)

st.write("Most of French population doesn't buy organic products for now")
st.write("but attitudes change 🔄 and tend to turn the situation around. ")

st.write("-> 📖 You want to learn further about the government AB certification: https://agriculture.gouv.fr/la-certification-en-agriculture-biologique")

st.text("\n")
st.text("\n")
st.text("\n")


# -- 6. Heatmap of delivery habits (Plotly)

st.write('<span style="color: green; font-size: 25px;"> 🧑‍🍳  - Preparation style through the day </span>',
             unsafe_allow_html=True)

data_style = pd.read_csv('prep_style.csv')

# replace invalid values with NaT, to drop them
data_style['occ_hdeb'] = pd.to_datetime(data_style['occ_hdeb'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
data_style = data_style.dropna(subset=['occ_hdeb'])

data_style.loc[:, 'hour'] = data_style['occ_hdeb'].dt.hour

heatmap_data = data_style.pivot_table(index='hour', columns='preparation_style', aggfunc='size', fill_value=0)

fig = px.imshow(heatmap_data, labels=dict(x='Preparation Style', y='Hour', color='Occurrences'))
fig.update_layout(title='Preparation Style throughout the day')

st.plotly_chart(fig)

st.write("Industrialized foods are 🥇 for all meals.")
st.write("Homemade comes 🥈, showing French are food lovers but courageous")

