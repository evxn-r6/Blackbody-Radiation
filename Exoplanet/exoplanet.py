from astroquery.ipac.nexsci.nasa_exoplanet_archive import NasaExoplanetArchive
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Folder to save the data
base_dir = Path(__file__).resolve().parent
data_dir = base_dir / "data"

data_dir.mkdir(exist_ok=True)

# Query the NASA Exoplanet Archive for relevant data
table = NasaExoplanetArchive.query_criteria(
    table="pscomppars",
    select="pl_name, hostname, pl_bmasse, pl_rade, pl_orbper, discoverymethod, disc_year, st_teff, st_rad"
)
df = table.to_pandas()
df.to_csv(data_dir / "exoplanet_data.csv", index=False)
print(df.shape)

# Clean the data
cols = ["pl_name", "hostname", "pl_bmasse", "pl_rade", "pl_orbper", "discoverymethod", "disc_year", "st_teff", "st_rad"]
df_clean=df[cols].copy()

# Drop duplicate planet entries
df_clean = df_clean.drop_duplicates(subset='pl_name', keep='first')

# Remove impossible values
df_clean = df_clean[df_clean['pl_bmasse'] > 0]
df_clean = df_clean[df_clean['pl_rade'] > 0]

print(f"Started with {len(df)} rows, after cleaning we have {len(df_clean)} rows.")

df_clean.to_csv(data_dir / "exoplanet_data_cleaned.csv", index=False)

# Plotting the cleaned data, showing bias in discovery methods
plt.figure(figsize=(8, 6))
for method, group in df_clean.groupby('discoverymethod'):
    plt.scatter(group['pl_rade'], group['pl_bmasse'], label=method, alpha=0.7, s=15)

plt.xlabel('Planet Radius (Earth Radii)')
plt.ylabel('Planet Mass (Earth Masses)')
plt.title('Exoplanet Properties by Discovery Method')
plt.xscale('log')
plt.yscale('log')
plt.legend(fontsize=8)
plt.show()

# Stacked histogram of discovery methods over the years
plt.figure(figsize=(10, 6))
methods = df_clean['discoverymethod'].unique()

# Keeping meaningful discovery methods for the histogram to reduce clutter
counts_by_method = df_clean['discoverymethod'].value_counts()
meaningful_methods = counts_by_method[counts_by_method > 20].index.tolist()

df_plot =df_clean[df_clean['discoverymethod'].isin(meaningful_methods)]
pivot = df_plot.groupby(['disc_year', 'discoverymethod']).size().unstack(fill_value=0)
pivot.plot(kind='bar', stacked=True, figsize=(12, 6))

plt.xlabel('Discovery Year')
plt.ylabel('Number of Exoplanets Discovered')
plt.title('Exoplanet Discoveries by Method Over Time')
plt.legend(title='Discovery Method', fontsize=8)
plt.tight_layout()
plt.show()