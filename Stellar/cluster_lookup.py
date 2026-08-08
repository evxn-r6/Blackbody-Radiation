from astropy.coordinates import SkyCoord
from astroquery.gaia import Gaia
import matplotlib.pyplot as plt
import numpy as np

# This module provides functions to query the Gaia Archive for star cluster data and visualize the results.


# A function to get the coordinates of a star cluster from its name using the SkyCoord class from astropy.coordinates. It raises a ValueError if the cluster name cannot be resolved.

def get_cluster_coordinates(cluster_name):
    try:
        coord = SkyCoord.from_name(cluster_name)
    except Exception as exc:
        raise ValueError(f"Could not resolve cluster name '{cluster_name}'.") from exc

    ra = coord.ra.deg
    dec = coord.dec.deg
    print(f"Coordinates for {cluster_name}: RA = {ra:.3f} deg, Dec = {dec:.3f} deg")
    return ra, dec


# Query the Gaia Archive for relevant data and prints the query being executed for debugging purposes and prints the number of stars found in the cluster.

def query_cluster_data(ra, dec, radius_deg=1.5, mag_limit=17):
    query = f"""
    SELECT TOP 100 source_id, ra, dec, parallax, parallax_error, phot_g_mean_mag, bp_rp, pmra, pmdec
    FROM gaiadr3.gaia_source
    WHERE 1=CONTAINS(
        POINT('ICRS', ra, dec),
        CIRCLE('ICRS', {ra}, {dec}, {radius_deg}))
        AND phot_g_mean_mag < {mag_limit}
        AND parallax > 0
    ORDER BY source_id
"""

    print(f"Querying Gaia DR3 for stars near the cluster.", flush=True)
    job = Gaia.launch_job_async(query, verbose=True)
    df = job.get_results().to_pandas()
    print(f"Found {len(df)} stars in the specified region.")
    return df


# Estimate the cluster parallax peak from the histogram.

def estimate_parallax_peak(df):
    counts, bin_edges = np.histogram(df['parallax'], bins=100)

    if len(counts) == 0:
        raise ValueError("No parallax data available to estimate peak.")
    
    peak_index = int(np.argmax(counts))
    parallax_center = (bin_edges[peak_index] + bin_edges[peak_index + 1]) / 2
    print(f"Peak parallax value: {parallax_center:.3f} mas")
    return parallax_center


# Select stars close to the parallax peak and propermotion center.

def identify_cluster_members(df, parallax_center, parallax_width=0.5, pm_threshold=4.0):
    df_clean = df[(df['parallax'] > parallax_center - parallax_width) & (df['parallax'] < parallax_center + parallax_width)]

    pmra_center = df_clean['pmra'].median()
    pmdec_center = df_clean['pmdec'].median()

    pm_distance = np.sqrt((df_clean['pmra'] - pmra_center)**2 + (df_clean['pmdec'] - pmdec_center)**2)
    df_final = df_clean[pm_distance < pm_threshold]

    print(f"{len(df)} total stars found, {len(df_clean)} stars within parallax range, and {len(df_final)} stars identified as cluster members based on proper motion.")
    return df_final, df_clean


# Plotting the parallax distribution 

def plot_parallax_distribution(df, parallax_center):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.hist(df['parallax'], bins=100, color='blue', alpha=0.7)
    ax.axvline(parallax_center, color='red', linestyle='dashed', linewidth=1, label=f'Parallax Peak: {parallax_center:.3f} mas')
    ax.set_xlabel('Parallax (mas)')
    ax.set_ylabel('Frequency')
    ax.set_title('Parallax Distribution of Stars in the Cluster Region')
    ax.legend()
    return fig

# Plotting the proper motion distribution of all stars and highlighting the cluster members

def plot_proper_motion_distribution(df, df_clean, df_final):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(df['pmra'], df['pmdec'], alpha=0.7, label='All Stars')
    ax.scatter(df_clean['pmra'], df_clean['pmdec'], color='red', alpha=0.7, label='Cluster Members')
    ax.set_xlabel('Proper Motion in RA (mas/yr)')
    ax.set_ylabel('Proper Motion in Dec (mas/yr)')
    ax.set_xlim(-200, 200)
    ax.set_ylim(-200, 200)
    ax.set_title('Proper Motion Distribution')
    ax.legend()
    return fig


# 

def analyse_cluster(cluster_name, radius_deg=1.5, mag_limit=17):
    ra, dec = get_cluster_coordinates(cluster_name)
    df = query_cluster_data(ra, dec, radius_deg, mag_limit)
    parallax_center = estimate_parallax_peak(df)
    df_final, df_clean = identify_cluster_members(df, parallax_center, parallax_width=0.5, pm_threshold=4.0)

    plot_parallax_distribution(df, parallax_center)
    plot_proper_motion_distribution(df, df_clean, df_final)


def main():
    cluster_name = input("Enter the name of the star cluster (e.g Pleiades, M44): ").strip()
    analyse_cluster(cluster_name)

if __name__ == "__main__":
    main()