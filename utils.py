import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

#def plot_streamlit(header, plot_title, x_label, y_label, dataframe, df_column, plot_marker, plot_linestyle, plot_color):
def plot_streamlit(header, plot_title, x_label, y_label, grid, legend,
                   dataframe, data_plot, label1, plot_marker, plot_linestyle, plot_color,
                   dataframe2, data_plot2, label2, plot_marker2, plot_linestyle2, plot_color2):

    st.header(header)
    plt.figure(figsize=(10, 6))
    plt.plot(dataframe, data_plot, label=label1, marker=plot_marker, linestyle=plot_linestyle, color=plot_color)
    plt.title(plot_title, fontsize=16)
    plt.xlabel(x_label, fontsize=12)
    plt.ylabel(y_label, fontsize=12)

    if grid == 'YES':
        plt.grid(True)
    
    if legend == 'YES':
        plt.legend()

    if dataframe2 is not None and data_plot2 is not None:
        plt.plot(dataframe2, data_plot2, label=label2, marker=plot_marker2, linestyle=plot_linestyle2, color=plot_color2)
    
    st.pyplot(plt)


def bollinger_bands(df, window=20, num_std=2):
    # Calculate rolling mean and rolling standard deviation
    df['Rolling Mean'] = df.rolling(window=window).mean()
    df['Rolling Std'] = df.rolling(window=window).std()

    # Calculate Bollinger Bands
    df['Upper Band'] = df['Rolling Mean'] + (df['Rolling Std'] * num_std)
    df['Lower Band'] = df['Rolling Mean'] - (df['Rolling Std'] * num_std)
    return df