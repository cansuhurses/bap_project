import pandas as pd
import streamlit as st
import folium
from streamlit_folium import folium_static
from sklearn.preprocessing import MinMaxScaler

df = pd.read_csv("df_deneme.csv")

# Filter
selected_filters = []
with st.expander("Haritayı bina işlevine göre filtreleyin"):
        islev_list = df['İşlev'].unique().tolist()
        islev = st.container()
        all_islev = st.checkbox("Hepsini seç.", value=True, key="1.1")
        if all_islev:
            islev.markdown("Hepsi seçildi.")
            selected_islev = islev_list
        else:
            selected = islev.multiselect(
                "İşlev:", [item for item in islev_list if not (pd.isnull(item)) == True], key="1.2")
            if len(selected) == 0:
                selected_islev = islev_list
            else:
                selected_islev = selected
        selected_filters.append(selected_islev)

# Create a Folium map centered at the mean latitude and longitude
m = folium.Map(location=[df['lat'].mean(), df['lon'].mean()], zoom_start=15, tiles = "CartoDB Positron")

# Create a mapping of categories to colors
category_colors = {
    2: 'blue',
    3: 'green',
    4: 'red',
    # Add more categories and corresponding colors as needed
}

# Add circles for each data point
for index, row in df[df["İşlev"].isin(selected_filters[0])].iterrows():
    category = row['bolge']
    color = category_colors.get(category, 'gray')
    folium.Circle(
        location=[row['lat'], row['lon']],
        radius=row['radius'],  # Adjust the radius to control the size of the circles
        color=color,  # You can change the color of the circles here
        fill=True,
        fill_color=color,  # You can change the fill color of the circles here
    ).add_to(m)

# Display the map using folium_static
folium_static(m)