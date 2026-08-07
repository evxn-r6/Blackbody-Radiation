from astropy.coordinates import SkyCoord
from astroquery.gaia import Gaia
import matplotlib.pyplot as plt
import numpy as np

# This module provides functions to query the Gaia Archive for star cluster data and visualize the results.

# Input the name of the star cluster you want to analyze

cluster_name = input("Enter a cluster name (e.g M44, Pleiades):")
coord = SkyCoord.from_name(cluster_name)

# Get the RA and Dec of the cluster

ra = coord.ra.deg
dec = coord.dec.deg
print(f"Coordinates of {cluster_name}: RA = {ra:.2f} deg, Dec = {dec:.2f} deg")

# Query the Gaia Archive for relevant data

query = f"""
SELECT TOP 1000 source_id, ra, dec, parallax, parallax_error, phot_g_mean_mag, bp_rp, pmra, pmdec
FROM gaiadr3.gaia_source
WHERE 1=CONTAINS(
    POINT('ICRS', ra, dec),
    CIRCLE('ICRS', {ra}, {dec}, 1.5))
    AND phot_g_mean_mag < 17
    AND parallax > 0
"""
# Prints the query being executed for debugging purposes and prints the number of stars found in the cluster after executing the query.

print(f"Querying Gaia DR3 for stars in the {cluster_name} cluster...")
job = Gaia.launch_job_async(query, verbose=True)
print("Query completed. Processing results...")
df = job.get_results().to_pandas()
print(f"Found {len(df)} stars in the {cluster_name} cluster.")

counts, bin_edges = np.histogram(df['parallax'], bins=100)

peak_index = np.argmax(counts)
parallax_center = (bin_edges[peak_index] + bin_edges[peak_index + 1]) / 2
print(f"Peak parallax value: {parallax_center:.3f} mas")

df_clean = df[(df['parallax'] > parallax_center - 0.5) & (df['parallax'] < parallax_center + 0.5)]

# Plotting the parallax distribution 

plt.figure(figsize=(8, 6))
plt.hist(df['parallax'], bins=100, color='blue', alpha=0.7)
plt.axvline(parallax_center, color='red', linestyle='dashed', linewidth=1, label=f'Peak Parallax: {parallax_center:.3f} mas')
plt.xlim(parallax_center - 1, parallax_center + 8)
plt.xlabel('Parallax (mas)')
plt.ylabel('Frequency')
plt.title('Distribution of Parallax Values')
plt.legend()
plt.show()

# Plotting the proper motion distribution of all stars and highlighting the cluster members

pmra_center = df_clean['pmra'].median()
pmdec_center = df_clean['pmdec'].median()

pm_distance = np.sqrt((df_clean['pmra'] - pmra_center)**2 + (df_clean['pmdec'] - pmdec_center)**2)

df_final = df_clean[pm_distance < 4.0]
print(f"{len(df)} total stars found, {len(df_clean)} stars within parallax range, and {len(df_final)} stars identified as cluster members based on proper motion.")

plt.figure(figsize=(8, 6))
plt.scatter(df['pmra'], df['pmdec'], alpha=0.7)
plt.scatter(df_clean['pmra'], df_clean['pmdec'], color='red', alpha=0.7, label='Cluster Members')
plt.xlabel('Proper Motion in RA (mas/yr)')
plt.ylabel('Proper Motion in Dec (mas/yr)')
plt.title('Proper Motion Distribution')
plt.legend()
plt.show()

