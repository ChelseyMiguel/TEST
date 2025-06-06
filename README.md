# TEST

This repository contains a utility function that queries the WISE catalog via
`astroquery`.

## Usage

```python
from astroquery_wise import query_wise_magnitudes

# Query 0.5 deg around RA=100 deg, Dec=22.5 deg
df = query_wise_magnitudes()
print(df.head())
```

The function requires the `astroquery` package to be installed.
