import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import h,c, k

# This module provides functions to calculate the properties of stars based on their temperature and radius.

# Calculate the intensity of a blackbody at a given wavelength and temperature using Planck's law.

def blackbody(wavelength, temperature):

    intensity = (2 * h * c**2) / (wavelength**5 * (np.exp((h * c) / (wavelength * k * temperature)) - 1))
    return intensity

# Wavelengths from 1 nm to 3 µm

wavelength = np.linspace(1e-9, 3e-6, 1000) 

# Define a dictionary of stars with their temperatures in Kelvin

stars = {
    "Sun": 5778,
    "Sirius": 9940,
    "Betelgeuse": 3500,
    "Rigel": 12100,
    "Vega": 9602
}

plt.figure(figsize=(10, 6))

# Calculate and plot the blackbody spectra for each star

for name, temperature in stars.items():

    spectrum = blackbody(wavelength, temperature)  
    plt.plot(wavelength * 1e9, spectrum, label=f'{name}')

plt.xlabel('Wavelength (nm)')
plt.ylabel('Relative Intensity (W/m²/nm/sr)')
plt.title('Blackbody Spectra of Different Stars')
plt.legend()
plt.grid()
plt.show()