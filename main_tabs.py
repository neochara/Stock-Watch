import matplotlib.pyplot as plt
import mplfinance as mpf
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st

from constants import END_DATE, START_DATE, STOCK_DATA_DICT, STOCK_IND_LIST
from data_analysis import get_clean_data, get_description  # get_nl_summary optional
from utils import plot_streamlit

sns.set_style("whitegrid")


# ----------------------------
# Helpers
# ----------------------------
def compute_bollinger_bands(price: pd.Series, window: int = 20, num_std: float = 2.0) -> pd.DataFrame:
    """Return a DF with columns: Price, Rolling Mean, Upper Band, Lower Band."""
    out = pd.DataFrame({"Price": price.astype(float)})
    rolling_mean = out["Price"].rolling(window=window).mean()
    rolling_std = out["Price"].rolling(window=window).std()

    out["Rolling Mean"] = rolling_mean
    out["Upper Band"] = rolling_mean + num_std * rolling_std
    out["Lower Band"] = rolling_mean - num_std * rolling_std
    return out


# ----------------------------
# Terminology subtab (Stock Data)
# ----------------------------
def render_terminology_tab():
    st.header("Terminology (A–Z)")
    st.caption("Quick lookup of terms we’ve touched in this project. Educational only — not financial advice.")

    TERMINOLOGY = {
        "Finance & Markets": [
            ("Alpha", "Return above a benchmark after adjusting for risk.", "Evaluating manager/strategy skill."),
            ("Arbitrage", "Low-risk profit from price differences across markets.", "Explaining why mispricings usually disappear."),
            ("Asset", "Anything with economic value (stocks, bonds, cash, real estate).", "Portfolio building."),
            ("Asset allocation", "How you split a portfolio across asset classes.", "Controlling risk/return profile."),
            ("Benchmark", "Reference index to compare performance (e.g., S&P 500).", "Measuring relative performance."),
            ("Bond", "A loan you make to an issuer; pays interest (coupon).", "Lower-volatility income allocation."),
            ("Bull market", "Broad market trend of rising prices.", "Context for long-run performance."),
            ("Bear market", "Broad market trend of falling prices.", "Risk context and drawdowns."),
            ("Capital gains", "Profit from selling an asset above purchase price.", "Tax/return planning."),
            ("Commodity", "Raw materials (gold, oil, wheat) traded in markets.", "Diversification/inflation hedges."),
            ("Correlation", "How two series move together (from -1 to +1).", "Diversification and risk management."),
            ("Covariance", "Unscaled correlation; depends on units.", "Building covariance matrices and portfolio math."),
            ("Dividend", "Cash payment from a company to shareholders.", "Income investing; total return."),
            ("Earnings", "Company profit; often reported quarterly.", "Valuation and sentiment."),
            ("ETF", "Exchange-Traded Fund: a basket of assets trading like a stock.", "Easy diversification, low-cost access."),
            ("Expense ratio", "Annual fund fee as a percent of assets.", "Comparing ETFs/funds."),
            ("Index", "A rules-based basket representing a market segment.", "Benchmarks and passive investing."),
            ("Index fund", "Fund that tracks an index (often via ETF or mutual fund).", "Low-cost passive exposure."),
            ("Inflation", "General rise in prices; reduces purchasing power.", "Real vs nominal returns."),
            ("Liquidity", "How easily you can trade without moving price much.", "Order choice and slippage awareness."),
            ("Market capitalization", "Company value = share price × shares outstanding.", "Sizing companies (small/large cap)."),
            ("Mutual fund", "Pooled investment priced once daily (NAV).", "Long-term investing vehicles."),
            ("NAV", "Net Asset Value; per-share value of a fund’s holdings.", "Understanding fund pricing."),
            ("Real return", "Return after inflation.", "Purchasing-power-aware performance."),
            ("Sector", "Industry group (tech, healthcare, energy, etc.).", "Diversifying exposures."),
            ("Spread", "Difference between two prices (often bid–ask).", "Transaction cost intuition."),
            ("Ticker", "Short symbol for a traded asset (e.g., NVDA).", "Selecting assets in the app."),
        ],
        "Trading & Orders": [
            ("Ask price", "Lowest price a seller will accept.", "Understanding execution cost."),
            ("Bid price", "Highest price a buyer will pay.", "Understanding execution cost."),
            ("Bid–ask spread", "Ask minus bid (a key trading friction).", "Estimating slippage/fees."),
            ("Day trading", "Short-horizon trading (intraday).", "Contrasts with investing; risk awareness."),
            ("Limit order", "Order that only fills at your price (or better).", "Controlling execution price."),
            ("Long position", "You profit if price rises (buy/hold).", "Basic directional exposure."),
            ("Market order", "Fill immediately at best available price.", "Fast execution; can pay spread/slippage."),
            ("Position sizing", "How big a trade is relative to portfolio.", "Risk control."),
            ("Short selling", "Borrow and sell now, buy later; profit if price falls.", "Hedging or bearish bets."),
            ("Stop-loss", "Auto-sell if price drops to a set level.", "Limiting downside (with caveats)."),
            ("Take-profit", "Auto-sell if price rises to a set level.", "Locking gains systematically."),
            ("Volatility", "How much price moves around; “wiggliness.”", "Sizing and risk planning."),
            ("Volume", "Shares/contracts traded in a period.", "Liquidity and market interest."),
        ],
        "Portfolio & Retirement": [
            ("401(k)", "Employer-sponsored retirement account (US).", "Tax-advantaged long-term saving."),
            ("Asset allocation", "Portfolio split across assets/classes.", "Risk/return design."),
            ("Diversification", "Spreading investments to reduce risk.", "Reducing single-asset blowups."),
            ("Rebalancing", "Resetting allocations back to targets.", "Keeping risk consistent over time."),
            ("Roth IRA", "After-tax contributions; qualified withdrawals tax-free.", "Long-horizon tax planning."),
            ("SEP IRA", "IRA for self-employed/small business; employer contributions.", "Higher contribution potential for some."),
            ("Tax-advantaged account", "Account with tax benefits (IRA/401k/HSA, etc.).", "Keeping more of returns."),
        ],
        "Time Series & Technical Analysis": [
            ("Bollinger Bands", "Rolling mean ± k×rolling std of price.", "Visualizing volatility; mean-reversion ideas."),
            ("Candlestick", "OHLC visualization (open/high/low/close).", "Price action and trend inspection."),
            ("Close", "Last traded price in a trading day/period.", "Return calculations and charts."),
            ("EWMA / EMA", "Exponentially weighted moving average (recent data matters more).", "Smoothing; trend/level estimation."),
            ("Half-life", "EWMA parameter: time for weight to drop by half.", "Choosing smoothing strength."),
            ("High", "Highest price in a trading day/period.", "Range/volatility views."),
            ("Low", "Lowest price in a trading day/period.", "Range/volatility views."),
            ("Log return", "Return as log(P_t / P_{t-1}).", "Additive over time; common in finance."),
            ("Moving average (SMA)", "Simple average over a rolling window.", "Trend smoothing."),
            ("OHLC", "Open/High/Low/Close prices for a period.", "Candles and basic price features."),
            ("Open", "First traded price in a trading day/period.", "Intraday comparisons vs close."),
            ("Rolling window", "Compute stats on a sliding time window.", "Moving averages, rolling std, bands."),
            ("Time series", "Data indexed by time (prices, returns).", "Everything in charting/returns."),
        ],
        "Risk & Performance": [
            ("Drawdown", "Peak-to-trough decline in portfolio/price.", "Worst-case pain measurement."),
            ("Hedging", "Reducing risk by taking an offsetting position.", "Lowering exposure to specific risks."),
            ("Risk premium", "Extra return expected for taking risk.", "Why stocks often beat cash long-term."),
            ("Risk-free rate", "Return with minimal default risk (often T-bills proxy).", "Sharpe/CAPM style metrics."),
            ("Sharpe ratio", "(Return − risk-free) / volatility.", "Risk-adjusted performance comparison."),
            ("Systematic risk", "Market-wide risk you can’t diversify away.", "Explains beta-like exposure."),
            ("Unsystematic risk", "Asset-specific risk; diversifiable.", "Reason to diversify."),
            ("Value at Risk (VaR)", "Loss threshold not exceeded with some probability.", "Risk reporting (with assumptions)."),
        ],
        "Statistics & Probability": [
            ("Central limit theorem", "Averages tend toward normality as sample size grows.", "Why normal approximations sometimes work."),
            ("Confidence interval", "Range likely containing a parameter.", "Uncertainty quantification."),
            ("Distribution", "How values are spread/probabilities assigned.", "Modeling returns, errors, outcomes."),
            ("Histogram", "Binned frequency plot.", "Seeing shape, skew, outliers."),
            ("Independence", "One variable doesn’t inform the other.", "Model assumptions."),
            ("Mean", "Average value.", "Expected level/return."),
            ("Median", "Middle value.", "Robust center measure."),
            ("Normal distribution", "Bell-curve distribution.", "Baseline model; Q–Q checks."),
            ("Outlier", "Point far from typical values.", "Data cleaning; robust modeling."),
            ("p-value", "How surprising data is under a null hypothesis.", "Hypothesis testing (carefully)."),
            ("Q–Q plot", "Quantile–quantile plot comparing data to a reference distribution.", "Checking normality/heavy tails."),
            ("Quantile", "Value below which a % of data falls.", "Risk percentiles, Q–Q plots."),
            ("Standard deviation", "Typical spread around the mean.", "Volatility and uncertainty."),
            ("Stationarity", "Statistical properties stable over time.", "Time-series modeling assumptions."),
            ("Variance", "Squared spread; std^2.", "Risk/volatility math."),
        ],
        "Machine Learning & Sketching": [
            ("Block-diagonal sketch", "Sketch matrix applied in blocks (distributed-friendly).", "Speeding up large linear algebra."),
            ("CIFAR-10", "Image classification dataset (10 classes).", "Benchmarking classification experiments."),
            ("Embedding (subspace)", "Mapping that preserves geometry of a subspace.", "Fast approximate regression/LS."),
            ("Frobenius norm", "Matrix size measure: sqrt(sum of squares).", "Error metrics and bounds."),
            ("Johnson–Lindenstrauss (JL)", "Random projections preserve distances approximately.", "Dimensionality reduction."),
            ("Leverage scores", "Row/column importance scores for sampling.", "Smarter sketching/sampling."),
            ("Linear regression", "Predict y with linear model; minimize squared error.", "Baseline modeling; sketching tests."),
            ("Logistic regression", "Classification model for probabilities via sigmoid/softmax.", "MNIST/classification experiments."),
            ("MNIST", "Handwritten digit dataset.", "Classification benchmarks."),
            ("Rademacher matrix", "Random ±1 entries used for projections.", "Fast randomized sketches."),
            ("ResNet", "Deep residual network architecture.", "Image classification experiments."),
            ("SJLT", "Sparse Johnson–Lindenstrauss Transform.", "Fast sketching with sparsity."),
            ("SRHT", "Subsampled Randomized Hadamard Transform.", "Fast structured random projection."),
            ("Subsampling", "Using a subset of data/rows.", "Speed/approximation tradeoffs."),
        ],
        "Programming & Data (Python/Pandas)": [
            ("DataFrame", "2D labeled table (rows/columns) in pandas.", "Core structure for your CSV market data."),
            ("deque", "Double-ended queue (fast pops from both ends).", "BFS/tree problems; queues."),
            ("iloc", "pandas integer-location indexing.", "Selecting by row/col positions."),
            ("loc", "pandas label-based indexing.", "Selecting by index labels/dates."),
            ("parse_dates", "pandas option to parse date strings into datetimes.", "Correct time indexing."),
            ("ravel / flatten", "Convert arrays to 1D.", "Stats functions expecting 1D arrays."),
            ("shift", "pandas method to offset data by periods.", "Computing returns from prices."),
            ("Stack", "LIFO data structure.", "Algorithm practice; merges/compression tasks."),
            ("Vectorization", "Using array operations instead of Python loops.", "Speed in data processing."),
        ],
        "App & Data Sources (Streamlit/YFinance/Config)": [
            ("API key", "Secret token to authenticate to an API.", "Accessing paid services safely."),
            ("Config file", "A settings file (often JSON) read by the app.", "Centralizing parameters without hardcoding."),
            ("JSON", "Text format for structured data (language-agnostic).", "App configuration and settings."),
            ("Rate limit", "Service throttling when too many requests occur.", "Why yfinance/downloads can fail temporarily."),
            ("Streamlit", "Python framework for data apps with interactive UI.", "Your Stock Watch interface."),
            ("yfinance", "Python wrapper for Yahoo Finance data.", "Downloading historical prices quickly."),
        ],
    }

    # Flatten + sort for filtering
    flat = []
    for cat, entries in TERMINOLOGY.items():
        for term, definition, used_for in entries:
            flat.append({"category": cat, "term": term, "definition": definition, "used_for": used_for})
    flat.sort(key=lambda x: x["term"].lower())

    query = st.text_input("Search (e.g., 'ETF', 'Q-Q', 'hedge')", value="").strip().lower()
    if query:
        flat = [x for x in flat if query in x["term"].lower() or query in x["definition"].lower()]

    letters = sorted({x["term"][0].upper() for x in flat if x["term"]})
    letter_choice = st.selectbox("Jump to letter", ["All"] + letters, index=0)

    if letter_choice != "All":
        flat = [x for x in flat if x["term"].upper().startswith(letter_choice)]

    # Regroup by category
    grouped = {}
    for x in flat:
        grouped.setdefault(x["category"], []).append(x)

    for cat in sorted(grouped.keys(), key=str.lower):
        with st.expander(cat, expanded=False):
            for x in sorted(grouped[cat], key=lambda z: z["term"].lower()):
                st.markdown(f"- **{x['term']}** — {x['definition']}\n  - *Used for:* {x['used_for']}")

    st.caption("Tip: use the search box to treat this like a mini dictionary.")


# ----------------------------
# App
# ----------------------------
st.title("Stock Watch 😎")

# Load local CSV data once (no yfinance downloads in this file)
stocks_dfs_dict = get_clean_data()

# Build a ticker->name mapping from constants.py (STOCK_DATA_DICT is name -> ticker)
ticker_to_name = {ticker: name for name, ticker in STOCK_DATA_DICT.items()}

# Build dropdown labels like "Apple (AAPL)" for tickers in STOCK_IND_LIST
ticker_options = []
for ticker in STOCK_IND_LIST:
    name = ticker_to_name.get(ticker)
    label = f"{name} ({ticker})" if name else ticker
    ticker_options.append((label, ticker))

ticker_options.sort(key=lambda x: x[0].lower())

selected_label = st.selectbox(
    "Select a stock/index:",
    [lbl for (lbl, _tkr) in ticker_options],
)
selected_ticker = dict(ticker_options)[selected_label]

st.write(f"Time period configured: {START_DATE} to {END_DATE}")

idx_of_interest = selected_ticker.lower()
if idx_of_interest not in stocks_dfs_dict:
    st.error(f"Could not find local CSV data for '{selected_ticker}'. Expected key '{idx_of_interest}'.")
    st.stop()

idx_df = stocks_dfs_dict[idx_of_interest]

# ----------------------------
# Main tabs
# ----------------------------
StockData_main_tab, Portfolio_main_tab = st.tabs(["Stock Data", "Portfolio Management"])

# ----------------------------
# Stock Data (subtabs)
# ----------------------------
with StockData_main_tab:
    (
        Overview_tab,
        Terminology_tab,
        Data_TS_tab,
        Stats_tab,
        EWMA_tab,
        Candlesticks_tab,
        Bollinger_tab,
        Stocks_comp_tab,
    ) = st.tabs(
        [
            "Overview",
            "Terminology",
            "Data and Timeseries",
            "Statistics",
            "EWMA",
            "Candlesticks",
            "Bollinger Bands",
            "Stock Comparisons",
        ]
    )

    # ----------------------------
    # Overview subtab
    # ----------------------------
    with Overview_tab:
        st.header("Overview")

        st.markdown(
            f"""
- This app loads **locally stored CSV price data** (no live downloading inside these tabs).
- You pick a ticker from the dropdown at the top; all subtabs update to reflect that selection.
- Date range configured in `constants.py`: **{START_DATE}** to **{END_DATE}**.

**What each subtab contains**
- **Terminology**: A searchable A–Z mini dictionary (grouped by category).
- **Data and Timeseries**: raw data table + Open/Close time series plots, plus a year-over-year Close overlay (raw + normalized to start at 100).
- **Statistics**: descriptive statistics summary table for the selected instrument.
- **EWMA**: exponentially weighted moving average plots (half-life and alpha controls) + crossings visualization.
- **Candlesticks**: candlestick chart (with volume).
- **Bollinger Bands**: Bollinger bands with adjustable window and $k$ (std dev multiplier), shaded band region.
- **Stock Comparisons**: multi-ticker comparison over the last $X$ completed years (growth % + covariance heatmap) using local CSVs.
"""
        )

        st.subheader("Available tickers (from constants.py)")
        # STOCK_DATA_DICT is name -> ticker; print ticker -> name
        pairs = sorted(((ticker, name) for name, ticker in STOCK_DATA_DICT.items()), key=lambda x: x[0])
        st.markdown("\n".join([f"- **{ticker}** — {name}" for ticker, name in pairs]))

    # ----------------------------
    # Terminology subtab
    # ----------------------------
    with Terminology_tab:
        render_terminology_tab()

    # ----------------------------
    # Data & Timeseries subtab
    # ----------------------------
    with Data_TS_tab:
        st.header(f"{selected_ticker} Stock Data")
        st.dataframe(idx_df)

        # Opening
        plot_streamlit(
            header=f"Opening Price Time Series of {selected_ticker}",
            plot_title=f"{selected_ticker} Stock Opening Prices",
            x_label="Date",
            y_label="Opening Price (USD)",
            grid="YES",
            legend="NO",
            dataframe=idx_df.index,
            data_plot=idx_df["Open"],
            label1=None,
            plot_marker="x",
            plot_linestyle="-",
            plot_color="b",
            dataframe2=None,
            data_plot2=None,
            label2=None,
            plot_marker2=None,
            plot_linestyle2=None,
            plot_color2=None,
        )

        # Closing
        plot_streamlit(
            header=f"Closing Price Time Series of {selected_ticker}",
            plot_title=f"{selected_ticker} Stock Closing Prices",
            x_label="Date",
            y_label="Closing Price (USD)",
            grid="YES",
            legend="NO",
            dataframe=idx_df.index,
            data_plot=idx_df["Close"],
            label1=None,
            plot_marker="o",
            plot_linestyle="-",
            plot_color="r",
            dataframe2=None,
            data_plot2=None,
            label2=None,
            plot_marker2=None,
            plot_linestyle2=None,
            plot_color2=None,
        )

        # Both Opening & Closing
        plot_streamlit(
            header=f"Opening and Closing Price Time Series of {selected_ticker}",
            plot_title=f"{selected_ticker} Stock Prices",
            x_label="Date",
            y_label="Price (USD)",
            grid="YES",
            legend="NO",
            dataframe=idx_df.index,
            data_plot=idx_df["Open"],
            label1=None,
            plot_marker=None,
            plot_linestyle="-",
            plot_color="b",
            dataframe2=idx_df.index,
            data_plot2=idx_df["Close"],
            label2=None,
            plot_marker2=None,
            plot_linestyle2="-",
            plot_color2="r",
        )

        # Difference (Close - Open)
        plot_streamlit(
            header=f"Difference between Closing and Opening Price of {selected_ticker}",
            plot_title=f"{selected_ticker} Stock Close-Open Difference",
            x_label="Date",
            y_label="Price Difference (USD)",
            grid="YES",
            legend="NO",
            dataframe=idx_df.index,
            data_plot=idx_df["Close"] - idx_df["Open"],
            label1=None,
            plot_marker=None,
            plot_linestyle="-",
            plot_color="m",
            dataframe2=None,
            data_plot2=None,
            label2=None,
            plot_marker2=None,
            plot_linestyle2=None,
            plot_color2=None,
        )

        # ---- Two year-over-year plots at the end of this tab
        st.divider()
        st.subheader("Year-over-year Close comparison (selected instrument)")

        most_recent_completed_year = 2025  # per your current setup (Jan 2026)
        X = st.selectbox(
            "Select number of years (always includes 2025):",
            [1, 2, 3, 4, 5],
            index=2,
            key="yoy_years_in_first_tab",
        )
        years_to_plot = list(range(most_recent_completed_year - int(X) + 1, most_recent_completed_year + 1))
        st.caption(f"Years shown: {years_to_plot}")

        idx_df_local = idx_df.copy()
        idx_df_local.index = pd.to_datetime(idx_df_local.index)

        if "Close" not in idx_df_local.columns:
            st.error("This dataset does not contain a 'Close' column.")
        else:
            close_all = idx_df_local["Close"].dropna()

            per_year_close = {}
            skipped_years = []
            for y in years_to_plot:
                s = close_all[close_all.index.year == y]
                if s.empty:
                    skipped_years.append(y)
                else:
                    per_year_close[y] = s

            if skipped_years:
                st.warning(f"No Close data found for year(s): {skipped_years}. They will be skipped.")

            if not per_year_close:
                st.error("No year data available to plot for your selection.")
            else:
                max_len = max(len(s) for s in per_year_close.values())
                day_idx = np.arange(1, max_len + 1)

                comp_raw = pd.DataFrame(index=day_idx)
                comp_norm = pd.DataFrame(index=day_idx)

                for y, s in per_year_close.items():
                    vals = s.values
                    comp_raw[y] = pd.Series(vals, index=np.arange(1, len(vals) + 1))

                    base = float(s.iloc[0])  # first trading day of that year
                    comp_norm[y] = pd.Series((vals / base) * 100.0, index=np.arange(1, len(vals) + 1))

                fig1, ax1 = plt.subplots(figsize=(12, 6))
                for y in sorted(comp_raw.columns):
                    ax1.plot(comp_raw.index, comp_raw[y], label=str(y))
                ax1.set_title(f"{selected_ticker} — Close (raw), overlayed by trading day")
                ax1.set_xlabel("Trading day of year (1 = first trading day)")
                ax1.set_ylabel("Close (USD)")
                ax1.grid(True)
                ax1.legend(title="Year")
                st.pyplot(fig1)

                fig2, ax2 = plt.subplots(figsize=(12, 6))
                for y in sorted(comp_norm.columns):
                    ax2.plot(comp_norm.index, comp_norm[y], label=str(y))
                ax2.set_title(f"{selected_ticker} — Close (normalized), each year starts at 100")
                ax2.set_xlabel("Trading day of year (1 = first trading day)")
                ax2.set_ylabel("Indexed Close (Year start = 100)")
                ax2.grid(True)
                ax2.legend(title="Year")
                st.pyplot(fig2)

    # ----------------------------
    # Statistics subtab
    # ----------------------------
    with Stats_tab:
        description_dict = get_description()
        description_idx_df = description_dict[idx_of_interest]
        st.header(f"{selected_ticker} Stock Data Statistics")
        st.dataframe(description_idx_df)

    # ----------------------------
    # EWMA subtab
    # ----------------------------
    with EWMA_tab:
        half_life_short = st.number_input(
            "Enter a half-life of your EWMA in days, up to 3 years",
            min_value=1,
            max_value=1095,
            value=30,
            step=1,
        )
        alpha_hl_short = 1 - np.exp(-np.log(2) / half_life_short)
        st.write(f"For half-life = {half_life_short}, we get $\\alpha$ = {alpha_hl_short}")

        half_life_long = st.number_input(
            "Enter a longer half-life of your EWMA in days, up to 3 years",
            min_value=int(half_life_short),
            max_value=1095,
            value=100,
            step=1,
        )
        alpha_hl_long = 1 - np.exp(-np.log(2) / half_life_long)
        st.write(f"For the longer half-life = {half_life_long}, we get $\\alpha$ = {alpha_hl_long}")

        ewma_closing_hl_short = idx_df["Close"].ewm(halflife=half_life_short, adjust=False).mean()
        ewma_closing_hl_long = idx_df["Close"].ewm(halflife=half_life_long, adjust=False).mean()

        st.header(f"EWMA of Closing Price Time Series of {selected_ticker} — varying half-life")
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(idx_df.index, idx_df["Close"], label="Original Data", color="skyblue")
        ax.plot(idx_df.index, ewma_closing_hl_short, label=f"short half-life={half_life_short}", color="orange")
        ax.plot(idx_df.index, ewma_closing_hl_long, label=f"long half-life={half_life_long}", color="green")
        ax.set_title("Exponentially Weighted Moving Average (EWMA) — varying half-life", fontsize=16)
        ax.set_xlabel("Time", fontsize=12)
        ax.set_ylabel("Value", fontsize=12)
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

        alpha = st.number_input(
            "Enter a smoothing parameter $\\alpha$ between 0 and 1:",
            min_value=0.01,
            max_value=1.0,
            value=0.05,
            step=0.01,
        )
        ewma_instrument_closing = pd.Series(idx_df["Close"]).ewm(alpha=alpha, adjust=False).mean()

        plot_streamlit(
            header=f"EWMA of Closing Price Time Series of {selected_ticker}",
            plot_title="Exponentially Weighted Moving Average (EWMA), w/ choice of $\\alpha$",
            x_label="Time",
            y_label="Value",
            grid="NO",
            legend="YES",
            dataframe=idx_df.index,
            data_plot=idx_df["Close"],
            label1="Original Data",
            plot_marker=None,
            plot_linestyle="-",
            plot_color="skyblue",
            dataframe2=idx_df.index,
            data_plot2=ewma_instrument_closing,
            label2=f"EWMA (alpha={alpha})",
            plot_marker2=None,
            plot_linestyle2=None,
            plot_color2="orange",
        )

        st.header(f"EWMA of Closing Price Time Series of {selected_ticker} — crossings")
        fig2, ax2 = plt.subplots(figsize=(12, 6))
        ax2.plot(idx_df.index, idx_df["Close"], label="Original Data", color="skyblue")
        ax2.plot(idx_df.index, ewma_closing_hl_short, label=f"short half-life={half_life_short}", color="orange")
        ax2.plot(idx_df.index, ewma_closing_hl_long, label=f"long half-life={half_life_long}", color="magenta")

        cross_above = ewma_closing_hl_short > ewma_closing_hl_long
        cross_below = ewma_closing_hl_short < ewma_closing_hl_long

        ax2.fill_between(
            idx_df.index,
            idx_df["Close"],
            where=cross_above,
            color="green",
            alpha=0.5,
            label="short > long",
            interpolate=True,
        )
        ax2.fill_between(
            idx_df.index,
            idx_df["Close"],
            where=cross_below,
            color="red",
            alpha=0.5,
            label="long > short",
            interpolate=True,
        )

        ax2.set_title("EWMA — crossings", fontsize=16)
        ax2.set_xlabel("Time", fontsize=12)
        ax2.set_ylabel("Value", fontsize=12)
        ax2.legend()
        ax2.grid(True)
        st.pyplot(fig2)

    # ----------------------------
    # Candlesticks subtab
    # ----------------------------
    with Candlesticks_tab:
        st.header(f"Candlestick Chart (Close) for {selected_ticker}")
        fig, _ax = mpf.plot(
            idx_df,
            type="candle",
            style="charles",
            title=f"Candlestick Chart for {selected_ticker}",
            ylabel="Price",
            volume=True,
            returnfig=True,
        )
        st.pyplot(fig)

        st.write(
            "**Naked Price Action** — green candlesticks are **bullish** (increase), "
            "red candlesticks are **bearish** (decrease)."
        )

    # ----------------------------
    # Bollinger Bands subtab
    # ----------------------------
    with Bollinger_tab:
        st.header(f"Bollinger Bands for {selected_ticker}")

        window = st.number_input("Rolling window size (days):", min_value=2, max_value=300, value=20, step=1)
        k_choices = [1.0, 1.5, 2.0, 2.5, 3.0, 4.0]
        num_std = st.selectbox("Number of standard deviations ($k$):", k_choices, index=k_choices.index(2.0))
        price_col = st.selectbox("Price to use:", ["Close", "Open"], index=0)

        price_series = idx_df[price_col].dropna()
        if price_series.empty:
            st.error(f"No data available for {price_col} to compute Bollinger Bands.")
        else:
            bb = compute_bollinger_bands(price_series, window=int(window), num_std=float(num_std))

            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(bb.index, bb["Price"], label=f"{price_col} Price", color="blue")
            ax.plot(bb.index, bb["Upper Band"], color="red", linestyle="-", linewidth=1, label="_nolegend_")
            ax.plot(bb.index, bb["Lower Band"], color="green", linestyle="-", linewidth=1, label="_nolegend_")
            ax.plot(bb.index, bb["Rolling Mean"], color="orange", linestyle="-", linewidth=1, label="Rolling Mean")

            mask = bb["Upper Band"].notna() & bb["Lower Band"].notna()
            ax.fill_between(bb.index, bb["Lower Band"], bb["Upper Band"], where=mask, alpha=0.25, label="_nolegend_")

            ax.set_title(f"{selected_ticker} Bollinger Bands (window={int(window)}, k={num_std})", fontsize=16)
            ax.set_xlabel("Date")
            ax.set_ylabel("Price (USD)")
            ax.legend(loc="best")
            ax.grid(True)
            st.pyplot(fig)

    # ----------------------------
    # Stock Comparisons subtab (LOCAL CSVs; no yfinance)
    # Two figures: growth + covariance heatmap
    # ----------------------------
    with Stocks_comp_tab:
        st.header("Indices comparisons (local CSV data)")

        most_recent_completed_year = 2025
        number_of_years = st.selectbox(
            "Select the past how many completed years you want to compare:",
            [1, 2, 3, 4, 5],
            index=2,
            key="multi_ticker_years_last_tab",
        )

        start_year = most_recent_completed_year - int(number_of_years) + 1
        start_date = pd.Timestamp(f"{start_year}-01-01")
        end_date = pd.Timestamp(f"{most_recent_completed_year}-12-31")
        st.caption(f"Window: {start_date.date()} to {end_date.date()}")

        available = []
        skipped = []
        close_series = {}

        for symbol in STOCK_IND_LIST:
            sym_key = symbol.lower()
            if sym_key not in stocks_dfs_dict:
                skipped.append(symbol)
                continue

            df_sym = stocks_dfs_dict[sym_key].copy()
            df_sym.index = pd.to_datetime(df_sym.index)

            if "Close" not in df_sym.columns:
                skipped.append(symbol)
                continue

            s = df_sym["Close"].dropna()
            s = s[(s.index >= start_date) & (s.index <= end_date)].dropna()

            if s.empty:
                skipped.append(symbol)
                continue

            close_series[symbol] = s
            available.append(symbol)

        if skipped:
            st.warning("Skipping tickers with missing data in this window: " + ", ".join(skipped))

        if not available:
            st.error("No tickers had valid Close data for this period from local CSVs.")
        else:
            fig_growth, ax_growth = plt.subplots(figsize=(12, 6))
            for symbol in available:
                s = close_series[symbol]
                base = float(s.iloc[0])
                growth_pct = ((s / base) - 1.0) * 100.0
                ax_growth.plot(growth_pct.index, growth_pct.values, label=symbol)

            ax_growth.set_title("Stock Growth (Close) — cumulative return % since first day in window", fontsize=16)
            ax_growth.set_xlabel("Date", fontsize=12)
            ax_growth.set_ylabel("Cumulative Returns (%)", fontsize=12)
            ax_growth.grid(True)
            ax_growth.legend()
            st.pyplot(fig_growth)

            log_returns = pd.DataFrame()
            for symbol in available:
                s = close_series[symbol]
                log_returns[symbol] = np.log(s / s.shift(1))

            log_returns = log_returns.dropna(how="all")
            valid_cols = [c for c in available if c in log_returns.columns and not log_returns[c].dropna().empty]

            if len(valid_cols) < 2:
                st.info("Not enough valid tickers to compute a covariance matrix for this period.")
            else:
                cov = log_returns[valid_cols].dropna().cov()

                fig_cov, ax_cov = plt.subplots(figsize=(12, 10))
                sns.heatmap(1000 * cov, annot=True, cmap="cividis", fmt=".4f", linewidths=0.5, ax=ax_cov)
                ax_cov.set_title("Covariance Matrix of Log Returns (scaled by 10^3)", fontsize=16)
                st.pyplot(fig_cov)

# ----------------------------
# Portfolio Management (placeholder)
# ----------------------------
with Portfolio_main_tab:
    st.header("Portfolio Management")
    st.info("Placeholder: you'll add portfolio-related tabs/features here later.")