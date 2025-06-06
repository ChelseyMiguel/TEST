# Utilities for filtering WISE data and querying Gaia DR3
import pandas as pd
import numpy as np
from astropy.coordinates import SkyCoord
import astropy.units as u
from astroquery.gaia import Gaia


def query_gaia_source(ra, dec, radius_arcsec=1.0):
    """Query Gaia DR3 around (ra, dec) and return parallax and G magnitude.

    Parameters
    ----------
    ra, dec : float
        Position in decimal degrees.
    radius_arcsec : float, optional
        Search radius in arcseconds, by default 1.0

    Returns
    -------
    tuple of (parallax, phot_g_mean_mag) or (np.nan, np.nan) if not found.
    """
    coord = SkyCoord(ra=ra, dec=dec, unit="deg")
    radius = radius_arcsec * u.arcsec
    try:
        job = Gaia.cone_search_async(coord, radius)
        results = job.get_results()
    except Exception:
        return np.nan, np.nan
    if len(results) == 0:
        return np.nan, np.nan
    # take closest match
    closest = results[0]
    return float(closest["parallax"]), float(closest["phot_g_mean_mag"])


def clean_merge_gaia(df, radius_arcsec=1.0):
    """Filter the DataFrame and merge Gaia information.

    Parameters
    ----------
    df : pandas.DataFrame
        Must contain columns 'w1mpro', 'w2mpro', 'w3mpro', 'w1snr', 'w2snr',
        'w3snr', 'ra', 'dec'.
    radius_arcsec : float, optional
        Search radius used when querying Gaia, by default 1.0

    Returns
    -------
    pandas.DataFrame
        DataFrame with additional columns 'w1w2', 'w2w3', 'parallax',
        'phot_g_mean_mag'.
    """
    required = ["w1mpro", "w2mpro", "w3mpro", "w1snr", "w2snr", "w3snr", "ra", "dec"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    mask = (df["w1snr"] > 5) & (df["w2snr"] > 5) & (df["w3snr"] > 5)
    out = df.loc[mask].copy()
    out["w1w2"] = out["w1mpro"] - out["w2mpro"]
    out["w2w3"] = out["w2mpro"] - out["w3mpro"]

    gaia_parallax = []
    gaia_gmag = []
    for _, row in out.iterrows():
        parallax, gmag = query_gaia_source(row["ra"], row["dec"], radius_arcsec)
        gaia_parallax.append(parallax)
        gaia_gmag.append(gmag)

    out["parallax"] = gaia_parallax
    out["phot_g_mean_mag"] = gaia_gmag
    return out
