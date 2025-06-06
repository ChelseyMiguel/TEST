import numpy as np
import pandas as pd

# WISE zero-point fluxes in Jy for the profile-fit magnitudes
WISE_ZERO_JY = {
    'w1mpro': 309.540,
    'w2mpro': 171.787,
    'w3mpro': 31.674,
    'w4mpro': 8.363,
}

# central wavelengths (micron) for the WISE bands
WISE_WAVELENGTHS = np.array([3.4, 4.6, 12.0, 22.0])

# speed of light (m/s)
C = 2.99792458e8

# parsec in meters
PC = 3.08567758128e16

# solar luminosity in watts
L_SUN = 3.828e26

def wise_mags_to_flux_jy(df: pd.DataFrame) -> pd.DataFrame:
    """Convert WISE magnitudes to flux in Jy."""
    for band, zero in WISE_ZERO_JY.items():
        flux_col = band.replace('mpro', '_flux_jy')
        df[flux_col] = zero * 10 ** (-0.4 * df[band])
    return df

def estimate_luminosity(df: pd.DataFrame) -> pd.DataFrame:
    """Estimate bolometric luminosity in solar units using WISE photometry."""
    df = wise_mags_to_flux_jy(df.copy())

    # convert fluxes from Jy to W/m^2/Hz
    flux_cols = [band.replace('mpro', '_flux_jy') for band in WISE_ZERO_JY]
    fluxes = df[flux_cols].values * 1e-26

    # frequencies for each band
    nu = C / (WISE_WAVELENGTHS * 1e-6)

    # nu * F_nu at each band
    nu_f_nu = fluxes * nu

    # approximate bolometric flux via trapezoidal integration in log nu
    bolometric_flux = np.trapz(nu_f_nu, x=np.log(nu), axis=1)

    # convert parallax (mas) to distance in meters
    distance_m = (1e3 / df['parallax'].values) * PC

    # luminosity in watts
    luminosity_w = 4 * np.pi * distance_m ** 2 * bolometric_flux

    # scale to solar units
    df['luminosity'] = luminosity_w / L_SUN
    return df

__all__ = ["estimate_luminosity"]
