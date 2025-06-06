import pandas as pd
from astropy.coordinates import SkyCoord
import astropy.units as u

try:
    from astroquery.irsa import Irsa
except ImportError:  # pragma: no cover - handle missing astroquery gracefully
    Irsa = None


def query_wise_magnitudes(ra=100.0, dec=22.5, radius=0.5):
    """Query WISE magnitudes around a position.

    Parameters
    ----------
    ra : float
        Right ascension in degrees.
    dec : float
        Declination in degrees.
    radius : float
        Search radius in degrees.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing RA, Dec, W1--W4 magnitudes and uncertainties.
    """
    if Irsa is None:
        raise ImportError(
            "astroquery is required for this function; please install it to proceed"
        )

    coord = SkyCoord(ra=ra * u.deg, dec=dec * u.deg, frame="icrs")
    tbl = Irsa.query_region(
        coord,
        catalog="allwise_p3as_psd",
        spatial="Cone",
        radius=radius * u.deg,
    )

    columns = [
        "ra",
        "dec",
        "w1mpro",
        "w1sigmpro",
        "w2mpro",
        "w2sigmpro",
        "w3mpro",
        "w3sigmpro",
        "w4mpro",
        "w4sigmpro",
    ]
    return tbl[columns].to_pandas()


__all__ = ["query_wise_magnitudes"]
