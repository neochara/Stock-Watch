import streamlit as st

def render_terminology_tab():
    st.header("Terminology (A–Z)")
    st.caption("Comprehensive lookup of financial, quantitative, and trading terms. Educational only — not financial advice.")

    # --- Data: category -> list of entries (term, short_def, used_for) ---
    TERMINOLOGY = {
        "Finance & Markets": [
            ("Alpha", "The excess return of an investment relative to the return of a benchmark index.", "Measuring the value added by an active portfolio manager."),
            ("Arbitrage", "The simultaneous purchase and sale of the same asset in different markets to profit from tiny price differences.", "Risk-free profit strategies (theoretical); ensuring market efficiency."),
            ("Asset Class", "A grouping of investments that exhibit similar characteristics and are subject to the same laws and regulations (e.g., Equities, Fixed Income, Commodities).", "Strategic asset allocation and diversification."),
            ("Bear Market", "A market condition in which securities prices fall 20% or more from recent highs.", "Understanding market cycles and sentiment."),
            ("Benchmark", "A standard against which the performance of a secutiy, mutual fund, or investment manager can be measured (e.g., S&P 500).", "Evaluating performance and calculating Alpha/Beta."),
            ("Beta", "A measure of the volatility (or systematic risk) of a security or portfolio in comparison to the market as a whole.", "Assessing risk; High beta (>1) means more volatile than market."),
            ("Bull Market", "A market condition in which prices are rising or are expected to rise.", "Identifying growth opportunities."),
            ("Capital Gains", "The profit realized on the sale of a non-inventory asset that was purchased at a cost lower than the amount realized on the sale.", "Tax planning; Total return calculations."),
            ("Correlation", "A statistic that measures the degree to which two securities move in relation to each other (-1 to +1).", "Portfolio diversification; Lower correlation reduces overall risk."),
            ("Dividend Yield", "A financial ratio (dividend/price) that shows how much a company pays out in dividends each year relative to its stock price.", "Income investing; Comparing income-generating assets."),
            ("Earnings Per Share (EPS)", "The portion of a company's profit allocated to each outstanding share of common stock.", "Fundamental analysis; Calculating P/E ratio."),
            ("Equity", "The value of the shares issued by a company (stock).", "Capital appreciation and ownership."),
            ("ETF (Exchange-Traded Fund)", "A type of pooled investment security that operates much like a mutual fund but trades on an exchange like a stock.", "Low-cost diversification; Access to specific sectors/indices."),
            ("Liquidity", "The efficiency or ease with which an asset or security can be converted into ready cash without affecting its market price.", "Risk management; ease of entry/exit."),
            ("Market Capitalization", "The total market value of a company's outstanding shares of stock (Share Price × Outstanding Shares).", "Classifying company size (Small, Mid, Large Cap)."),
            ("P/E Ratio", "The Price-to-Earnings ratio; measures its current share price relative to its per-share earnings.", "Valuation; Determining if a stock is over/undervalued."),
            ("Spread", "The difference between the bid (sell) and ask (buy) prices of a security/asset.", "Transaction efficiency; measure of liquidity."),
            ("Yield Curve", "A line that plots yields (interest rates) of bonds having equal credit quality but differing maturity dates.", "Forecasting economic state (inverted curve often predicts recession)."),
        ],

        "Trading & Execution": [
            ("Ask Price", "The lowest price a seller is willing to accept for a security.", "Buying; assessing immediate liquidity."),
            ("Bid Price", "The highest price a buyer is willing to pay for a security.", "Selling; assessing immediate liquidity."),
            ("Bid-Ask Spread", "The amount by which the ask price exceeds the bid price.", "Transaction cost; Indicator of market liquidity."),
            ("Day Trading", "Buying and selling the same security on the same day to capitalize on short-term price movements.", "Speculative execution."),
            ("Execution Strategy", "The method used to buy or sell a large order (e.g., TWAP, VWAP) to minimize market impact.", "Reducing slippage and transaction costs."),
            ("High-Frequency Trading (HFT)", "A method of trading that uses powerful computer programs to transact a large number of orders in fractions of a second.", "Market making; Arbitrage."),
            ("Limit Order", "An order to buy or sell a security at a specific price or better.", "Controlling the execution price, at the risk of non-fill."),
            ("Long Position", "Buying a security with the expectation that it will rise in value.", "Bullish strategy."),
            ("Market Order", "An order to buy or sell a security immediately at the best available current price.", "Guaranteed execution, but price may slip."),
            ("Scalping", "A trading strategy attempting to make many small profits on small price changes.", "High-volume, short-term trading."),
            ("Short Selling", "Selling a security that is not owned by the seller, usually borrowed, with the intent to buy it back later at a lower price.", "Profiting from price declines; Hedging."),
            ("Slippage", "The difference between the expected price of a trade and the price at which the trade is executed.", "Transaction cost analysis."),
            ("Stop-Loss Order", "An order placed to buy or sell a security when it reaches a certain price.", "Risk management; Limiting potential losses."),
            ("VWAP (Volume Weighted Average Price)", "The average price a security has traded at throughout the day, based on both volume and price.", "Benchmark for execution efficiency."),
        ],

        "Quantitative Finance & Risk": [
            ("Black-Scholes Model", "A mathematical model for pricing an options contract. Estimates the variation over time of financial instruments.", "Option pricing; Risk management."),
            ("Conditional Value at Risk (CVaR)", "Also known as Expected Shortfall; the expected loss given that the loss is greater than the VaR threshold.", "Tail-risk measurement; more robust than VaR."),
            ("Covariance Matrix", "A matrix displaying the covariance between pairs of elements in a random vector.", "Portfolio optimization (Modern Portfolio Theory)."),
            ("Drawdown", "The peak-to-trough decline during a specific recorded period of an investment.", "Assessing historical risk and recovery time."),
            ("Efficient Frontier", "The set of optimal portfolios that offer the highest expected return for a defined level of risk.", "Portfolio Optimization."),
            ("Factor Investing", "An investment strategy in which securities are chosen based on attributes (factors) that are associated with higher returns (e.g., Value, Momentum, Size).", "Systematic active management."),
            ("Greeks", "Terms (Delta, Gamma, Theta, Vega, Rho) used to measure the sensitivity of an option's price to various factors.", "Hedging options portfolios."),
            ("Hedging", "An investment to reduce the risk of adverse price movements in an asset (like insurance).", "Risk mitigation."),
            ("Information Ratio", "A measure of portfolio returns above the returns of a benchmark to the volatility of those returns (tracking error).", "Evaluating manager skill/consistency."),
            ("Kurtosis", "A statistical measure that defines how heavily the tails of a distribution differ from the tails of a normal distribution.", "Assessing 'tail risk' or extreme events."),
            ("Leverage", "The use of borrowed capital for (an investment), expecting the profits made to be greater than the interest payable.", "Amplifying potential returns (and losses)."),
            ("Maximum Drawdown (MDD)", "The maximum observed loss from a peak to a trough of a portfolio, before a new peak is attained.", "Worst-case historical scenario."),
            ("Mean Reversion", "The theory that asset prices and historical returns eventually return to their long-term mean or average level.", "Pairs trading; Contra-trend strategies."),
            ("Monte Carlo Simulation", "A mathematical technique that generates random variables for modeling risk or uncertainty.", "Forecasting/Risk analysis under uncertainty."),
            ("Sharpe Ratio", "The average return earned in excess of the risk-free rate per unit of volatility or total risk.", "Comparing risk-adjusted performance of assets."),
            ("Skewness", "A measure of the asymmetry of the probability distribution of a real-valued random variable about its mean.", "Identifying bias towards positive or negative returns."),
            ("Sortino Ratio", "A variation of the Sharpe ratio that differentiates harmful volatility from total overall volatility by using the asset's standard deviation of negative portfolio returns.", "Focusing on downside risk."),
            ("Value at Risk (VaR)", "A statistic that quantifies the extent of possible financial losses within a firm, portfolio, or position over a specific time frame.", "Regulatory risk reporting."),
            ("Volatility Clustering", "The tendency for large changes in asset prices (of either sign) to follow large changes, and small changes to follow small changes.", "GARCH modeling; Risk forecasting."),
        ],

        "ML for Trading": [
            ("Alternative Data", "Non-traditional data used in finance (e.g., satellite imagery, credit card transactions, social media sentiment) to gain an edge.", "Generating unique alpha signals."),
            ("Backtesting", "Testing a predictive model or strategy on historical data.", "Validating strategy viability before live trading."),
            ("Feature Engineering", "The process of using domain knowledge to extract features (characteristics) from raw data for ML algorithms.", " improving model predictive performance."),
            ("Gradient Boosting", "An ML technique for regression and classification problems, which produces a prediction model in the form of an ensemble of weak prediction models (decision trees).", "Predicting price direction or returns."),
            ("LSTM (Long Short-Term Memory)", "A type of Recurrent Neural Network (RNN) capable of learning order dependence in sequence prediction problems.", "Time-series forecasting."),
            ("Natural Language Processing (NLP)", "A field of AI giving computers the ability to understand text and spoken words.", "Sentiment analysis of news/tweets."),
            ("Overfitting", "A modeling error involved when a function is too closely fit to a limited set of data points.", "Strategy failing in 'out of sample' (live) trading."),
            ("Random Forest", "An ensemble learning method that constructs a multitude of decision trees at training time.", "Robust classification/regression; Reducing overfitting."),
            ("Reinforcement Learning", "An area of ML concerned with how intelligent agents ought to take actions in an environment to maximize the notion of cumulative reward.", "Dynamic portfolio optimization; Execution agents."),
            ("Supervised Learning", "The machine learning task of learning a function that maps an input to an output based on example input-output pairs.", "Predicting returns (Regression) or Direction (Classification)."),
            ("Train-Test Split", "Separating data into a training set to build the model and a test set to validate it.", "Preventing overfitting; Simulating out-of-sample performance."),
            ("Unsupervised Learning", "A type of ML algorithm used to draw inferences from datasets consisting of input data without labeled responses.", "Clustering similar assets; Regime detection."),
            ("Walk-Forward Optimization", "A method used in finance to determine the best parameters for a trading strategy by moving a window of time forward.", "Robust backtesting."),
        ],

        "Time Series & Technical Analysis": [
            ("Autocorrelation", "The correlation of a time series with a delayed copy of itself.", "Detecting patterns/trends in time series."),
            ("Bollinger Bands", "A volatility indicator defined by a set of trendlines plotted two standard deviations (positively and negatively) away from a simple moving average (SMA).", "Identifying overbought/oversold conditions."),
            ("Candlestick Chart", "A style of financial chart used to describe price movements of a security, derivative, or currency.", "Visualizing price action (OHLC)."),
            ("Cointegration", "A statistical property of a collection of time series variables that indicates if a linear combination of them is stationary.", "Pairs Trading (identifying spreads that mean-revert)."),
            ("Exponential Moving Average (EMA/EWMA)", "A type of moving average that places a greater weight and significance on the most recent data points.", "Trend identification; faster reaction than SMA."),
            ("Momentum", "The rate of acceleration of a security's price or volume.", "Trend-following strategies."),
            ("Moving Average Crossover", "A point on a chart where a shorter-term moving average crosses a longer-term moving average.", "Technical buy/sell signals (Golden Cross/Death Cross)."),
            ("RSI (Relative Strength Index)", "A momentum indicator used in technical analysis that measures the magnitude of recent price changes to evaluate overbought or oversold conditions.", "Timing entries and exits."),
            ("Stationarity", "A property of a time series where statistical properties like mean and variance are constant over time.", "Prerequisite for many time-series models (e.g., ARIMA)."),
            ("Support & Resistance", "Price levels where a stock has historically had difficulty falling below (support) or rising above (resistance).", "Setting entry/exit/stop-loss levels."),
        ],

        "Statistics & Probability": [
            ("Confidence Interval", "A range of values so defined that there is a specified probability that the value of a parameter lies within it.", "Estimating true mean return."),
            ("Distribution", "A function that shows the possible values for a variable and how often they occur.", "Modeling asset returns (often assumed Normal, but rarely are)."),
            ("Hypothesis Testing", "A formal procedure for investigating our ideas about the world using statistics.", " verifying if a strategy's returns are significantly > 0."),
            ("Normal Distribution", "A bell-shaped frequency distribution curve. Most data clusters around the mean.", "Baseline assumption for many models (CAPM, Black-Scholes)."),
            ("Outlier", "An observation point that is distant from other observations.", "Data cleaning; Anomaly detection."),
            ("P-Value", "The probability of obtaining test results at least as extreme as the results actually observed, assuming that the null hypothesis is correct.", "Statistical significance testing."),
            ("Q-Q Plot (Quantile-Quantile)", "A graphical tool to help us assess if a set of data plausibly came from some theoretical distribution such as a Normal or exponential.", "Checking normality of returns."),
            ("Standard Deviation", "A measure of the amount of variation or dispersion of a set of values.", "Proxy for volatility/risk."),
            ("Variance", "The expectation of the squared deviation of a random variable from its mean.", "Component of volatility calculations."),
            ("Z-Score", "The number of standard deviations a data point is from the mean.", "Standardizing data; Detecting outliers."),
        ],
    }

    # --- Build a flat list and sort by term for filtering ---
    flat = []
    for cat, entries in TERMINOLOGY.items():
        for term, definition, used_for in entries:
            flat.append({"category": cat, "term": term, "definition": definition, "used_for": used_for})

    flat.sort(key=lambda x: x["term"].lower())

    query = st.text_input("Search (e.g., 'Alpha', 'LSTM', 'Hedging')", value="").strip().lower()
    if query:
        flat = [x for x in flat if query in x["term"].lower() or query in x["definition"].lower()]

    letters = sorted({x["term"][0].upper() for x in flat if x["term"]})
    letter_choice = st.selectbox("Jump to letter", ["All"] + letters, index=0)

    if letter_choice != "All":
        flat = [x for x in flat if x["term"].upper().startswith(letter_choice)]

    # --- Regroup by category (and keep terms alphabetical) ---
    grouped = {}
    for x in flat:
        grouped.setdefault(x["category"], []).append(x)

    # Sort categories specifically to keep related ones together if desired, or just alphabetical
    for cat in sorted(grouped.keys()):
        with st.expander(cat, expanded=False):
            for x in sorted(grouped[cat], key=lambda z: z["term"].lower()):
                st.markdown(
                    f"- **{x['term']}**\n"
                    f"  - *Definition:* {x['definition']}\n"
                    f"  - *Used for:* {x['used_for']}"
                )

    st.caption("Tip: use the search box to treat this like a mini dictionary.")
