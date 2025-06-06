import pandas as pd
from pathlib import Path
from astroquery.skyview import SkyView
import astropy.units as u
import matplotlib.pyplot as plt


def fetch_ps1_cutouts(df: pd.DataFrame, out_dir: str = "cutouts") -> pd.DataFrame:
    """Download 2'×2' Pan-STARRS cutouts for outlier rows.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with columns ``ra``, ``dec`` and ``is_outlier``.
    out_dir : str
        Directory where the images are saved.

    Returns
    -------
    pandas.DataFrame
        DataFrame with an added ``cutout_path`` column containing file paths
        to the saved images. Non-outliers will have ``None``.
    """
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    df = df.copy()
    df["cutout_path"] = None

    for idx, row in df[df["is_outlier"]].iterrows():
        position = f"{row['ra']} {row['dec']}"
        try:
            images = SkyView.get_images(position=position,
                                        survey=["PanSTARRS g"],
                                        radius=1 * u.arcmin)
        except Exception as exc:
            print(f"Failed to download cutout for row {idx}: {exc}")
            continue

        if images:
            hdulist = images[0]
            data = hdulist[0].data
            fig, ax = plt.subplots(figsize=(4, 4), dpi=100)
            ax.imshow(data, origin="lower", cmap="gray")
            ax.axis("off")
            file_path = out_path / f"cutout_{idx}.png"
            fig.savefig(file_path, bbox_inches="tight", pad_inches=0)
            plt.close(fig)
            df.at[idx, "cutout_path"] = str(file_path)

    return df
