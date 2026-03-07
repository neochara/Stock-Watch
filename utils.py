import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


def plot_streamlit( header, plot_title, x_label, y_label, grid, legend, dataframe, data_plot,
                    label1, plot_marker, plot_linestyle, plot_color, dataframe2, data_plot2,
                    label2, plot_marker2, plot_linestyle2, plot_color2,):

    """Small helper to render a simple matplotlib line plot in Streamlit."""
    st.header(header)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(
        dataframe,
        data_plot,
        label=label1,
        marker=plot_marker,
        linestyle=plot_linestyle,
        color=plot_color,
    )

    if dataframe2 is not None and data_plot2 is not None:
        ax.plot(
            dataframe2,
            data_plot2,
            label=label2,
            marker=plot_marker2,
            linestyle=plot_linestyle2,
            color=plot_color2,
        )

    ax.set_title(plot_title, fontsize=16)
    ax.set_xlabel(x_label, fontsize=12)
    ax.set_ylabel(y_label, fontsize=12)

    if grid == "YES":
        ax.grid(True)
    if legend == "YES":
        ax.legend()

    st.pyplot(fig)
    plt.close(fig)


def bollinger_bands(price: pd.Series, window: int = 20, num_std: float = 2.0) -> pd.DataFrame:
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
