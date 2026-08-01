# Astrophysics Projects

## <ins>Blackbody Radiation</ins>

This project models stellar radiation using Planck's Law. It calculates blackbody spectra, Wien displacement peaks and also calculates important properties about stars.

## <ins>Exoplanet Analysis</ins>
<details>
<summary></summary>

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
1. ### Mass-Radius Relationship by Discovery Method
<img width="800" height="600" alt="Mass-Radius by Discovery Method" src="https://github.com/user-attachments/assets/a3a5bcb3-9e8a-4653-af12-d155fed45cd3" />

Plotting the planet's mass against its radius, coloured by discovery method, shows the biases of different methods:
- **Transit** detections cluster toward smaller radii and lower masses. This method needs the planet to pass in front of its star from our line of sight, which is easier to catch for planets in close-in orbits.
- **Radial Velocity** detections skew toward higher masses as this method measures the star's gravitational 'wobble' so it's more sensitive to massive planets.
- **Imaging** detections consist of the most massive and widest-separation planets since directly imaging a planet requires enough separation from its host star's glare.

2. ### Discoveries Over Time by Method
<img width="1200" height="600" alt="image" src="https://github.com/user-attachments/assets/23c8ada3-95eb-4d5e-bca9-ee374d796c05" />

- Before ~2013, discoveries were dominated by **Radial Velocity**.
- Two large spikes in **2014** and **2016** are dominated by **Transit** detections. These correspond to major **Kepler mission** data releases, where large batches of confirmed planets were published at once, rather than planets suddenly being found faster.
- From ~2018 onward, Transit remains the dominant method at a steadier rate, consistent with **TESS** taking over from Kepler alongside ground-based follow ups.

## What I learned
- Real datasets require deliberate decisions about missing data. The 'right' way to handle a gap depends on why it's missing, not just what is missing.
- Debugging: I had many errors especially since it was my first time cleaning data with pandas, choosing which columns to use and deciding which to remove was also a challenge.
- Visually seeing the detection bias was a good experience as it is an important concept in observational astrophysics and this dataset makes it visible.

## Possible Updates/Extensions
- Estimate stellar luminosity from `st_teff`/`st_rad` and check which planets fall in a rough habitable zone.
- Break the mass-radius plot down by discovery year to see how each method's typical detections have changed over time.

</details>
