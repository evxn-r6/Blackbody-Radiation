import numpy as np
from scipy.constants import sigma, h, c, k, Wien

# This module provides functions to calculate the properties of stars based on their temperature and radius.

def peak_wavelength(temperature):
    """
    Calculate the peak wavelength of a star's emission using Wien's displacement law.

    Temperature: Kelvin (K).
    """
    wavelength = Wien / temperature

    return wavelength *1e9  # Convert to nanometers

def star_colour(wavelength):
    """
    Calculate the colour of a star based on its peak wavelength.
    """
    if wavelength < 400:
        return "Ultraviolet"
    elif wavelength < 450:
        return "Violet"
    elif wavelength < 495:
        return "Blue"
    elif wavelength < 570:
        return "Green"
    elif wavelength < 590:
        return "Yellow"
    elif wavelength < 610:
        return "Orange"
    elif wavelength < 750:
        return "Red"
    else:
        return "Infrared"

temperature = float(input("Enter the temperature of the star in Kelvin: "))
peak = peak_wavelength(temperature)

print(f"\nThe peak wavelength of the star's emission is: {peak:.2f} nm")
print(f"The approximate colour of the star is: {star_colour(peak)}")