# imports
import pandas as pd
import streamlit as st
import seaborn as sns
from haversine import haversine
import folium
from streamlit_folium import folium_static
import matplotlib.pyplot as plt
from io import StringIO
from sklearn.cluster import BisectingKMeans, KMeans, MiniBatchKMeans
from g_util import get_geocoder, plot_map, colors
from mst_utils import gen_mst

st.header('Generating Metro Network')

# globals
cityname = st.text_input('City Name')
df = pd.DataFrame()
method = st.selectbox(
     'Which clustering method to ue?',
     ('Bisecting K-means Clustering', 'K means Clustering', 'Minibatch K means Clustering'))

# inputs
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:

    # Reading the .csv file
    bytes_data = uploaded_file.getvalue() # To read file as bytes
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8")) # To convert to a string based IO
    string_data = stringio.read() # To read file as string
    df = pd.read_csv(uploaded_file) # Can be used wherever a "file-like" object is accepted

    # Fromatting the dataframe
    df = df.reset_index().rename(columns = {
        "index": "id"
    })
    df.drop(columns=["ID"], inplace=True)
    ptype = []
    for i in df['Population']:
        if(0 <= i <= 15000):
            ptype.append("Low")
        elif(15001 <= i <= 30000):
            ptype.append("Mid")
        else:
            ptype.append("High")
    df["Population Density"] = ptype

    st.subheader('Input DataFrame')
    # Write: dataframe
    st.write(df.head())

    st.subheader('Popluation Plot')
    # Write: seaborn plot
    fig = plt.figure(figsize=(10, 4))
    sns.histplot(df, x = "Population")
    st.pyplot(fig)

    # Fetching location data
    location = get_geocoder(address = cityname)

    # Creating the map 
    map_ = plot_map(df, x = "Latitude", y = "Longitude", start = location, zoom = 11, 
                tiles = "cartodbpositron", popup = "Name", 
                size = "Area (km)", color = "Population Density", lst_colors = ["red","green","orange"], legend = True,
                marker = None)
    
    st.subheader('Population Cluster Map')
    # Write: folium map
    folium_static(map_)

    # k_best = find_best_k(df[["Latitude","Longitude"]], max_k = 50)
    # Fecting the k from the user
    k = st.text_input('K in K-means clustring')
    if k != '':
        k = int(k)

        # Setting up the models
        if(method == 'Bisecting K-means Clustering'):
            model = BisectingKMeans(n_clusters = k, init = 'k-means++', random_state = 1729)
        elif(method == 'K means Clustering'):
            model = KMeans(n_clusters = k, init = 'k-means++', random_state = 1729)
        else:
            model = MiniBatchKMeans(n_clusters = k, random_state = 1729, batch_size = 1)

        # fitting the model
        model.fit(df[["Latitude","Longitude"]])

        # finding all the clusters
        coord_clusters = model.cluster_centers_

        # all cluster vals
        cluster_vals = model.predict(df[["Latitude","Longitude"]])

        # setting up data for dataframe for clusters
        cluster_lat, cluster_long = [], []
        dist = []
        idx = 0
        point_lat = df['Latitude'].to_numpy()
        point_long = df['Longitude'].to_numpy()
        for cluster_val in cluster_vals:
            (x, y) = coord_clusters[cluster_val]
            cluster_lat.append(x)
            cluster_long.append(y)
            dist.append(haversine((x, y), (point_lat[idx], point_long[idx])))
            idx += 1
        df['Cluster Latitude'] = cluster_lat
        df['Cluster Longitude'] = cluster_long
        df['Cluster'] = cluster_vals
        df['Cluster Distance'] = dist

        # Write: dataframe
        # st.write(df.head())

        # made the cluster dataframe
        cdf = df = df.groupby('Cluster', as_index=False).agg({'Population':'sum', 'Cluster Distance':'sum', 'Area (km)': 'sum'})
        cdf[['Latitude', 'Longitude']] = coord_clusters
        cdf['Station Name'] = [f"{i + 1}" for i in range(k)]

        st.subheader('Cluster DataFrame')
        # Write: dataframe
        st.write(cdf.head())
        
        # rendering the map
        idx = 0
        for (x, y) in coord_clusters:
            # With-in-Sum-of-Squares (WSS): WSS is the total distance of data points from their respective cluster centroids.
            html=f"""
                <link href='http://fonts.googleapis.com/css?family=Roboto' rel='stylesheet' type='text/css'>
                <div style = "font-family: 'Roboto', sans-serif;">
                    <h4> Cluster {idx + 1}</h4>
                    <p>Details: </p>
                    <ul>
                        <li>Population: {cdf.iloc[idx, 1]}</li>
                        <li>WSS: {cdf.iloc[idx, 2]:.3f} km</li>
                        <li>Area: {cdf.iloc[idx, 3]:.3f} km^2</li>
                    </ul>
                    </p>
                <div>
                """
            iframe = folium.IFrame(html=html, width = 200, height = 200)
            popup = folium.Popup(iframe, max_width=2650)
            folium.Marker(
                location = [x, y],
                popup = popup,
                icon = folium.Icon(
                    color = colors[idx]
                )
            ).add_to(map_)
            idx += 1
        
        st.subheader('Population Cluster Map with More Information')
        # Write: folium map
        folium_static(map_)

        st.subheader('Proposed Metro Network')
        mst_map = gen_mst(cityname, cdf)
        # Write: folium map
        folium_static(mst_map)

        # adding data to map
        idx = 0
        for (x, y) in model.cluster_centers_:
            # With-in-Sum-of-Squares (WSS): WSS is the total distance of data points from their respective cluster centroids.
            html=f"""
                <link href='http://fonts.googleapis.com/css?family=Roboto' rel='stylesheet' type='text/css'>
                <div style = "font-family: 'Roboto', sans-serif;">
                    <h4> Station {idx + 1}</h4>
                    <p>Details: </p>
                    <ul>
                        <li>Population: {cdf.iloc[idx, 1]}</li>
                        <li>WSS: {cdf.iloc[idx, 2]:.3f} km</li>
                        <li>Area: {cdf.iloc[idx, 3]:.3f} km^2</li>
                    </ul>
                <div>
                """
            iframe = folium.IFrame(html=html, width = 200, height = 200)
            popup = folium.Popup(iframe, max_width=2650)
            folium.Marker(
                location = [x, y],
                popup = popup,
                icon = folium.Icon(
                    color = colors[idx]
                )
            ).add_to(mst_map)
            idx += 1
        
        st.subheader('Proposed Metro Network with Stations Data')
        # Write: folium map
        folium_static(mst_map)
