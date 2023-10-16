import streamlit as st

import pandas as pd

import plotly.express as px

st.set_page_config(
    page_title="Health & Nutrition",
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
st.title('Food is also about 🩺 Health')
st.title('and 🧬 Nutrition')

sante = pd.read_csv('sante_fr.csv')

st.text("\n")
st.text("\n")
st.text("\n")

# -- . Interactive curve for macronutriments

st.write('<span style="color: green; font-size: 25px;"> 📈 - Nutrition consumption along the day </span>',
             unsafe_allow_html=True)
st.text("\n")

# To visualize average of ... for plage of 10 minutes
sante['occ_hdeb'] = pd.to_datetime(sante['occ_hdeb'], format='%Y-%m-%d %H:%M:%S')
sante['occ_10min'] = sante['occ_hdeb'].dt.round('10min')
mean10_df = sante.groupby('occ_10min').agg('mean').reset_index()

#mean10_df['occ_hdeb'] = sante['occ_hdeb']
mean10_df = mean10_df.sort_values(by='occ_10min')

sante_curve = mean10_df.copy()
sante_curve['preparation_style'] = sante['preparation_style']
#print(mean10_df.columns)


# selection of column
mean10_df_col = mean10_df.drop(columns='occ_10min')
selected_column = st.selectbox('Choose a nutriment or vitamine:', mean10_df_col.columns)

# selected range
selected_range = st.slider('Select a period range:', min_value=0.0, max_value=23.0, value=(0.0, 23.0))

# # sante['occ_hdeb'] = pd.to_datetime(sante['occ_10min'], format='%Y-%m-%d %H:%M:%S')
filtered_df = mean10_df[(mean10_df['occ_10min'].dt.hour >= selected_range[0]) & (mean10_df['occ_10min'].dt.hour <= selected_range[1])]

fig = px.line(filtered_df, x='occ_10min', y=selected_column, title=f'Consumption of - {selected_column} - daily')

fig.update_yaxes(range=[0, filtered_df[selected_column].max() + 10])  # adjust for each graph (not same prop for all)

st.plotly_chart(fig)

st.text("\n")

st.write("⁉️ FAQ - Benefits and Issues associated to the various Nutrients and Vitamins.")

expander = st.expander("Aet")
expander.write("aet = Energy in calories")

expander = st.expander("Ags")
expander.write("ags = Saturated fatty acids")
expander.write("🔴 Promotes cholesterol, cardiovascular diseases, and weight gain")

expander = st.expander("Proteines")
expander.write("= Proteins")
expander.write("🟢 Growth and development, Immune support, Nutrient transport")
expander.write("🔴 Harder digestion, Quick imbalance in case of excess")

expander = st.expander("Glucides")
expander.write("= Carbohydrate")
expander.write("🟢 Long-term energy intake")
expander.write("🔴 Blood sugar increase due to added sugars")

expander = st.expander("Lipides")
expander.write("= Lipid")
expander.write("🟢 Organ protection, Facilitation of cellular function, Energy intake")
expander.write("🔴 Cholesterol and Calories increase")

expander = st.expander("Sucres")
expander.write("= Sugar")
expander.write("🟢 Body and Brain energy")
expander.write("🔴 Diabetes, Overweight, Cavities")

expander = st.expander("Amidons")
expander.write("= Starch")
expander.write("🟢 Steady energy, Vitamins, Fiber brought")
expander.write("🔴 Harder digestion, Blood sugar increase")
expander.write("⚠️ High risk for gluten allergy")

expander = st.expander("Fibres")
expander.write("= Fibre")
expander.write("🟢 Good heart health, Reduced cholesterol, Easy digestion")

expander = st.expander("Alcool")
expander.write("= Alcohol")
expander.write("🟢 Relaxation and Sociability easier")
expander.write("🔴 Onset of dependencies, Issues with the liver and nervous system")


