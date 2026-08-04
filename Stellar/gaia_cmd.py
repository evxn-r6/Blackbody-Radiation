import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from astroquery.gaia import Gaia

base_dir = Path(__file__).resolve().parent
data_dir = base_dir / "data"

data_dir.mkdir(exist_ok=True)

# Query the Gaia Archive for relevant data
query = """ SELECT source_id, ra, parallax, parallax_error, phot_g_mean_mag, bp_rp, phot_bp_mean_mag, phot_rp_mean_mag
            FROM gaiadr3.gaia_source
            WHERE 1=CONTAINS(
                POINT('ICRS', ra, dec),
                CIRCLE('ICRS', 56.75, 24.12, 2))
            AND parallax BETWEEN 6.5 AND 8.5
            AND parallax_over_error > 5
            AND phot_g_mean_mag < 18
            """

job = Gaia.launch_job(query)
df = job.get_results().to_pandas()
df.to_csv(data_dir / "gaia_data.csv", index=False)
print(len(df), "candidate Pleidaes members found in Gaia DR3 data.")

# Calculating Absolute Magnitude

df['abs_mag'] = df['phot_g_mean_mag'] + 5 * (np.log10(df['parallax'] / 1000) + 1)

# Plotting the Color-Magnitude Diagram (CMD)

plt.figure(figsize=(8, 6))
plt.scatter(df['bp_rp'], df['abs_mag'], s=10, color='blue', alpha=0.5)
plt.gca().invert_yaxis()  # Invert y-axis for magnitude
plt.xlabel('BP - RP Color (mag)')
plt.ylabel('Absolute Magnitude (G) (mag)')
plt.title('Color-Magnitude Diagram of Candidate Pleiades Members')
plt.savefig(data_dir / "pleiades_cmd.png", dpi=300)
plt.show()
