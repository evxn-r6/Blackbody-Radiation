import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy.constants import h, c, k

# This module provides functions to calculate the properties of blackbody radiation based on temperature and wavelength.

def blackbody(wavelength, temperature):
    """
    Calculate the spectral radiance of a blackbody at a given temperature.

    Wavelength: Metres (m) and temperature: Kelvin (K).

    """
    # Planck's law
    numerator = 2 * h * c**2
    denominator = (wavelength**5) * (np.exp((h * c) / (wavelength * k * temperature)) - 1)
    return numerator / denominator

wavelength = np.linspace(1e-9, 3e-6, 1000)  # Wavelengths from 1 nm to 3 µm
temperature = [3000, 4000, 5000]  # Temperatures in Kelvin

plt.figure(figsize=(10, 6))

for T in temperature:
    intensity = blackbody(wavelength, T)
    plt.plot(wavelength * 1e9, intensity, label=f'T = {T} K')

plt.title('Blackbody Radiation Curves')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Spectral Radiance (W/m²/nm/sr)')
plt.legend()
plt.grid()
plt.show()




