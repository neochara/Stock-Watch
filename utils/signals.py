import pandas as pd


def bollinger_bands(
    price: pd.Series, window: int = 20, num_std: float = 2.0
) -> pd.DataFrame:
    """Compute Bollinger Bands for a price series.

    Returns a DataFrame with columns:
      - Price
      - Rolling Mean
      - Rolling Std
      - Upper Band
      - Lower Band
    """
    # Robust numeric coercion (handles strings like '1,234.56' or '$123.45')
    s = (
        price.astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("$", "", regex=False)
    )
    s = pd.to_numeric(s, errors="coerce")

    out = pd.DataFrame(index=price.index)
    out["Price"] = s
    out["Rolling Mean"] = s.rolling(window=window, min_periods=window).mean()
    out["Rolling Std"] = s.rolling(window=window, min_periods=window).std()
    out["Upper Band"] = out["Rolling Mean"] + num_std * out["Rolling Std"]
    out["Lower Band"] = out["Rolling Mean"] - num_std * out["Rolling Std"]

    return out
