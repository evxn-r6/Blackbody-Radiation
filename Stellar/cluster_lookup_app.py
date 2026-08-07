import streamlit as st
from cluster_lookup import (get_cluster_coordinates, query_cluster_data, estimate_parallax_peak, identify_cluster_members, plot_parallax_distribution, plot_proper_motion_distribution)

st.set_page_config(page_title="Stellar Cluster Lookup", layout="wide")
st.title("Stellar Cluster Lookup Application")


cluster_name = st.text_input("Enter the name of the stellar cluster (e.g., Pleiades, Hyades):", "Pleiades")
radius = st.slider("Search radius (degrees):", min_value=0.1, max_value=5.0, value=1.5, step=0.1)
mag_limit = st.slider("Magnitude limit:", min_value=10, max_value=20, value=17, step=1)

if st.button("Analyze Cluster"):
    with st.spinner("Querying data and analyzing cluster..."):
        ra, dec = get_cluster_coordinates(cluster_name)
        df = query_cluster_data(ra, dec, radius, mag_limit)
        parallax_center = estimate_parallax_peak(df)

        df_final, df_clean = identify_cluster_members(df, parallax_center, parallax_width=0.5, pm_threshold=4.0)

        st.success(f"Found {len(df_final)} potential members of the {cluster_name} cluster.")

        fig1 = plot_parallax_distribution(df, parallax_center)
        fig2 = plot_proper_motion_distribution(df, df_clean, df_final)

        col1, col2 = st.columns(2)

        with col1:
            st.pyplot(fig1)

        with col2:
            st.pyplot(fig2)