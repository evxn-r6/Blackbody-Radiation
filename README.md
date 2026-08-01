# Astrophysics Projects

## <ins>Blackbody Radiation</ins>

This project models stellar radiation using Planck's Law. It calculates blackbody spectra, Wien displacement peaks and also calculates important properties about stars.

## <ins>Exoplanet Analysis</ins>
<details>
<summary> Exoplanet Analysis</summary>

## Introduction 
 A short data analysis project exploring patterns in exoplanets, using data from the NASA Exoplanet Archive.

This project was a good test to practice data cleaning, using real life data and visualising actual data used in research. Exoplanets were a clear choice due to my interest in astrophysics and especially since they're becoming more popular over time, the dataset is large and messy and has the possibility to find genuine physics behind the patterns.

Data was acquired from the NASA Exoplanet Archive, using the `pscomppars` (Planetary Systems Composite Parameters) table via `astroquery`. In my first iteration, only certain columns have been used due to me wanting to gain experience and not overwhelming myself.

## Data Cleaning
The raw data acquired from the exoplanet archive had to be cleaned before analysis:
- **Duplicates**: Duplicate planet entries were removed, keeping only the first occurrence.
- **Invalid Values**: Rows that had impossible mass and radius values ($>0$) were removed.
- **Missing Values**: Rows with any missing fields were not removed as it was not an error and often meaningful:
  - Planets missing `pl_bmasse` or `pl_rade` are often detections where only either mass or radius could be measured (e.g transit-only detections give radius but not mass)
  - Planets missing `st_teff` or `st_rad` are overwhelmingly microlensing detections. This method characterises the planet from a one-off lensing event so the host star is unable to studied afterward.
- Rare Category Filtering: For the histogram, discovery methods with fewer than 20 total detections were excluded to keep the plot readable and not overwhelm the reader. 

 ## Analysis and Findings
### Mass-Radius Relationship by Discovery Method
Plotting the planet's mass against its radius, coloured by discovery method, shows the biases of different methods:
</details>
