import sys
import os
import pandas as pd
import numpy as np
import datetime as datetime
from pandas.core.series import Series
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.graph_objs import Figure
from loguru import logger
from fx_analytics.main_functions import setup_logging
from fx_analytics import config
from typing import List, Dict, Any

# functions!

def get_portfolio_growth(df: pd.DataFrame, profit = True) -> pd.DataFrame:

    # create a copy of the dataframe
    df = df.copy()
    # extracting orders from the dataframe!
    # df['date'] = pd.to_datetime(df['date'])
    # result_df = df.loc[df['type'] != 2]
    # result_df.loc[:, 'total_profit'] = result_df['profit'] + result_df['swap'] + result_df['commission'] + result_df['fee']
    # result_df = result_df.groupby('date')['total_profit'].sum().reset_index()

    # extracting orders from the dataframe!
    df['date'] = pd.to_datetime(df['date'])

    # Use .loc with a condition for assignment
    df.loc[df['type'] != 2, 'total_profit'] = df['profit'] + df['swap'] + df['commission'] + df['fee']

    # Now, create result_df for grouping
    result_df = df[df['type'] != 2].copy()  # Explicit copy here
    result_df = result_df.groupby('date')['total_profit'].sum().reset_index()
    
    if profit == True:
        result_df.columns = ['date', 'growth']
    else:
        deposit  =sum(df.loc[df.type == 2].profit.tolist())
        result_df.loc[:, 'daily_balance'] =  deposit + result_df['total_profit'].cumsum()
        result_df.columns = ['date', 'daily_profit','growth']
    result_df = result_df.sort_values(by='date', ascending = False )
    return result_df

def plot_growth_over_time(dataframe: pd.DataFrame,
                        x_column: str,
                        y_column: str,
                        title: str = "Profit Over Time",
                        yaxis_title: str = "Growth") -> go.Figure:
    """
    Create a line plot with optional scatter points to visualize growth over time.

    Args:
        dataframe (pd.DataFrame): A DataFrame containing the data to be plotted.
        x_column (str): The name of the column to be used as the x-axis.
        y_column (str): The name of the column to be used as the y-axis.
        title (str, optional): The title of the plot. Default is "Profit Over Time".
        yaxis_title (str, optional): The title of the y-axis. Default is "Growth".

    Returns:
        go.Figure: A Plotly figure representing the line plot with optional scatter points.

    Example:
        df = pd.DataFrame({
            'Date': ['2023-09-01', '2023-09-02', '2023-09-03'],
            'Profit': [100, 150, 120]
        })

        fig = plot_growth_over_time(df, x_column='Date', y_column='Profit', title='Profit Over Time', yaxis_title='Profit')
        fig.show()

    Output:
        (Line plot visualization of growth over time with optional scatter points)
    """
    # Create a new Plotly figure
    fig = go.Figure()

    # Create a line plot
    fig.add_trace(go.Scatter(x=dataframe[x_column], y=dataframe[y_column], mode='lines', name='Line'))

    # Add scatter points
    fig.add_trace(go.Scatter(x=dataframe[x_column], y=dataframe[y_column], mode='markers', name='Scatter'))

    # Customize the layout
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title=yaxis_title,
        showlegend=True,
    )

    return fig

def profit_over_time(dataframe: pd.DataFrame,
                        x_column: str,
                        y_column: str,
                        title: str = "Profit Over Time",
                        yaxis_title: str = "Growth") -> go.Figure:
    """
    Create a bar plot to visualize growth over time. Bars with positive y-values are colored green, 
    while bars with negative y-values are colored red.

    Args:
        dataframe (pd.DataFrame): A DataFrame containing the data to be plotted.
        x_column (str): The name of the column to be used as the x-axis.
        y_column (str): The name of the column to be used as the y-axis.
        title (str, optional): The title of the plot. Default is "Profit Over Time".
        yaxis_title (str, optional): The title of the y-axis. Default is "Growth".

    Returns:
        go.Figure: A Plotly figure representing the bar plot.

    Example:
        df = pd.DataFrame({
            'Date': ['2023-09-01', '2023-09-02', '2023-09-03'],
            'Profit': [100, -50, 120]
        })

        fig = plot_growth_over_time(df, x_column='Date', y_column='Profit', title='Profit Over Time', yaxis_title='Profit')
        fig.show()

    Output:
        (Bar plot visualization of growth over time with colors based on y-values)
    """
    # Determine bar colors based on y-values
    colors = ['green' if value >= 0 else 'red' for value in dataframe[y_column]]

    # Create a new Plotly figure
    fig = go.Figure()

    # Create a bar plot with conditional colors
    fig.add_trace(go.Bar(x=dataframe[x_column], y=dataframe[y_column], marker_color=colors, name='Growth'))

    # Customize the layout
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title=yaxis_title,
        showlegend=True,
        width=550,
        height=400
    )

    return fig

def plot_piechart(df):
    """
    Create a pie chart to visualize the distribution of symbols in a DataFrame.

    Args:
        df (pd.DataFrame): A DataFrame containing symbol information.

    Returns:
        Figure: A Plotly figure representing the pie chart.

    Example:
        df = pd.DataFrame({
            'symbol': ['AAPL', 'GOOGL', 'AAPL', 'MSFT', 'GOOGL', 'AAPL'],
            'type': [1, 2, 1, 1, 2, 1]
        })

        fig = plot_piechart(df)
        fig.show()

    Output:
        (Pie chart visualization of symbol distribution)
    """
    # create a copy of the dataframe
    df = df.copy()

    # Filter out rows where 'type' is not equal to 2
    df_sym = df.loc[df['type'] != 2]

    # Group symbols and count their occurrences
    commodity = df_sym.groupby(by=['symbol']).size().reset_index(name='count')

    # Create a pie chart using Plotly Express
    fig = px.pie(commodity, 
                values=commodity['count'], 
                names=commodity['symbol'], 
                color_discrete_sequence=px.colors.sequential.RdBu,
                title="Commodities/Currency Trade Distribution")

    return fig


def daily_commodities_trade_pie_chart(df: pd.DataFrame, create_symbol_count_dataframe):
    """
    Generate a pie chart visualizing the distribution of commodities trade.

    This function takes a DataFrame containing commodities trade data, processes it to obtain
    the necessary statistics, and then uses these statistics to generate a pie chart.

    Parameters:
    df (pd.DataFrame): A DataFrame containing the commodities trade data. It must contain at least
                    the columns 'type', 'date', and 'symbol'.
    create_symbol_count_dataframe: A function that processes the data for the pie chart.

    Returns:
    px.Figure: A plotly express Figure object representing the pie chart.

    """
    # Ensure not to modify the original dataframe
    df = df.copy()

    # Filter out specific rows based on 'type'
    df_sym = df.loc[df['type'] == 0]

    # Group by 'date' and 'symbol' and count occurrences
    commodity = df_sym.groupby(by=['date','symbol']).size().reset_index(name='count')

    # Further group by 'date' and create lists of 'symbols' and their corresponding 'count'
    commodity = commodity.groupby('date').agg({'symbol': list, 'count': list}).reset_index()

    # Sort values by 'date' in descending order and reset index
    result_ord = commodity.sort_values(by=['date'], ascending=False).reset_index()

    # Drop the old index column
    result_ord = result_ord.drop(columns=['index'])

    # Process the dataframe for the pie chart
    symbol_count_df = create_symbol_count_dataframe(result_ord, row_index=0)

    # Create the pie chart using plotly express
    fig = px.pie(symbol_count_df,
                 values=symbol_count_df['count'],
                 names=symbol_count_df['symbol'],
                 color_discrete_sequence=px.colors.sequential.RdBu,
                 title="Daily Commodities Trade Distribution")
    
    return fig


def create_symbol_count_dataframe(dataframe, row_index= 0):
    """
    Converts symbol and count data from a specific row of a DataFrame
    into a pandas DataFrame.

    Args:
        dataframe (pd.DataFrame): The DataFrame containing the data.
        row_index (int): The index of the row to process.

    Returns:
        pd.DataFrame: A DataFrame containing symbol-count pairs.
    """
    # Create an empty dictionary to store symbol-count pairs
    symbol_dict = {}  

    # create a copy of the dataframe
    dataframe = dataframe.copy()

    # Iterate over each symbol-count pair in the specified row
    for i in range(len(dataframe.loc[row_index, 'symbol'])):
        symbol = dataframe.loc[row_index, 'symbol'][i]
        count = dataframe.loc[row_index, 'count'][i]

        # Update the symbol_dict with the symbol-count pair
        symbol_dict[symbol] = count

    # Convert the dictionary into a DataFrame
    df = pd.DataFrame.from_dict(symbol_dict, orient='index', columns=['count']).reset_index()
    # Rename the 'index' column to 'symbol'
    df.rename(columns={'index': 'symbol'}, inplace=True)

    return df

def total_trades(df: pd.DataFrame) -> int:
    """
    Calculate the total number of unique trades in a DataFrame.

    Args:
        df (pd.DataFrame): A DataFrame containing trading data with a 'type' column.

    Returns:
        int: The total number of unique trades.

    Example:
        df = pd.DataFrame({
            'position_id': [1, 2, 3, 4, 5],
            'type': [0, 1, 0, 0, 1]
        })

        total = total_trades(df)
        print(total)

    Output:
        3
    """
    # create a copy of the dataframe
    df = df.copy()

    # Filter rows where 'type' is equal to 0 (assuming 'type' 0 represents trades)
    df_sys = df.loc[df['type'] == 0]

    # Calculate the total number of unique trades based on 'position_id'
    total_trades = df_sys['position_id'].nunique()

    return total_trades


def calculating_pip_growth(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate pip growth based on input data.

    Args:
        data (pd.DataFrame): A DataFrame containing trading data with columns 'type', 'commission', 'swap',
                                'profit', 'date', 'position_id', 'symbol', and 'volume'.

    Returns:
        pd.DataFrame: A DataFrame containing calculated pip growth grouped by date and symbol.
    """
    # create a copy of the dataframe
    data = data.copy()

    # Filter out rows with 'type' equal to 2
    df_pip = data.loc[data.type != 2]

    # Calculate 'total_profit' as the sum of 'commission', 'swap', and 'profit'
    df_pip.loc[:, 'total_profit'] = df['commission'] + df['swap'] + df['profit']

    # Group by 'date', 'position_id', 'symbol', and 'volume', and sum 'total_profit'
    df_pip_gb = df_pip.groupby(by=['date','position_id','symbol','volume'])['total_profit'].sum().reset_index()

    # Group by 'date' and 'symbol', and sum 'volume' and 'total_profit'
    df_pip_daily_gb = df_pip_gb.groupby(['date', 'symbol'])[['volume','total_profit']].sum().reset_index()
    
    return df_pip_daily_gb


# Define a function to calculate pip_growth based on the symbol
def calculate_pip_growth(row: Series) -> float:
    """
    Calculates pip_growth based on the symbol.

    Args:
        row (pandas.Series): A row from the DataFrame containing 'symbol', 'volume', and 'total_profit'.

    Returns:
        float: The calculated pip_growth value.
    """
    if row['symbol'] == 'XAUUSD':
        return round(row['total_profit'] / (row['volume'] * 100 * 0.095), 1)
    elif row['symbol'] == 'GBPJPY':
        return round(row['total_profit'] / (row['volume'] * 100 * 0.063), 1)
    else:
        return None


def extract_latest_pip_growth(data: pd.DataFrame) -> pd.DataFrame:
    """
    Extract the rows with the latest date from a DataFrame containing pip growth data.

    Args:
        data (pd.DataFrame): A DataFrame containing pip growth data with a 'date' column.

    Returns:
        pd.DataFrame: A DataFrame containing only the rows with the latest date.
    """
    # create a copy of the dataframe
    data = data.copy()
    # Sort the DataFrame by date in descending order (latest date first)
    data = data.sort_values('date', ascending=False)

    # Extract the rows with the latest date
    df_pip_latest = data.loc[data.date == data['date'].max()]

    return df_pip_latest


def create_growth_chart(df: pd.DataFrame, weeklygrowth: bool = True) -> Figure:
    """
    Create and display a weekly and monthly growth bar chart from a DataFrame.

    Args:
        df (DataFrame): The DataFrame containing the data with 'date', 'type', and 'profit' columns.

    Returns:
        Figure: A Plotly Figure object representing the weekly growth chart.
    """
    # create a copy of the dataframe
    df = df.copy()
    # Convert the 'date' column to DateTime
    df['date'] = pd.to_datetime(df['date'])

    # Filter the DataFrame by 'type' column
    result_df = df.loc[df['type'] != 2]

    # Calculating total profit 
    result_df.loc[:, 'total_profit'] = result_df['profit'] + result_df['swap'] + result_df['commission'] + result_df['fee']
    # Extract week and month
    result_df.loc[:,'week'] = result_df['date'].dt.isocalendar().week
    result_df['week'] = result_df['week'].astype('int32')
    result_df.loc[:,'month'] = result_df['date'].dt.month
    result_df.loc[:,'year'] = result_df['date'].dt.year
    result_df.loc[:,'week-year'] = result_df['week'].astype(str) + '-' + result_df['year'].astype(str)
    result_df.loc[:,'month-year'] = result_df['month'].astype(str) + '-' + result_df['year'].astype(str)

    if weeklygrowth == True:
        # Calculate weekly growth
        weekly_growth = result_df.groupby(by=['week-year','month','year'])['total_profit'].sum().reset_index()
        weekly_growth.loc[:,'color'] = weekly_growth['total_profit'].apply(lambda x: 'green' if x >= 0 else 'red')
        weekly_growth = weekly_growth.sort_values(by=['year','month'], ascending=True)

        # Create the bar chart
        fig = go.Figure(data=[go.Bar(
            x=weekly_growth['week'],
            y=weekly_growth['total_profit'],
            marker_color=weekly_growth['color'],  # Set the bar color based on the 'color' column
        )])
            # Customize the chart appearance
        fig.update_layout(
            title="Weekly Growth",
            xaxis_title="Week",
            yaxis_title="Profit",
            width=475,
            height=375
        )

    else:
        # Calculate monthly growth
        monthly_growth = result_df.groupby(by=['month-year','month','year'])['total_profit'].sum().reset_index()
        monthly_growth.loc[:,'color'] = monthly_growth['total_profit'].apply(lambda x: 'green' if x >= 0 else 'red')
        monthly_growth = monthly_growth.sort_values(by=['year','month'], ascending=True)

        # Create the bar chart
        fig = go.Figure(data=[go.Bar(
            x=monthly_growth['month'],
            y=monthly_growth['total_profit'],
            marker_color=monthly_growth['color'],  # Set the bar color based on the 'color' column
        )])
        # Customize the chart appearance
        fig.update_layout(
            title="Monthly Growth",
            xaxis_title="month",
            yaxis_title="Profit",
            width=475,
            height=375
        )

    return fig

def weekly_percentage_growth(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate weekly percentage growth and various related metrics.

    Parameters:
    - df (pandas.DataFrame): DataFrame containing at least the columns ['date', 'type', 'profit', 'swap', 'commission', 'fee']

    Returns:
    - pandas.DataFrame: DataFrame with weekly percentage growth and related metrics.
    """
        # create a copy of the dataframe
    df = df.copy()
    
    # Convert 'date' column to datetime format
    df['date'] = pd.to_datetime(df['date'])

    # Calculate total deposits based on type==2 and store in variable
    deposit  = sum(df.loc[df.type == 2].profit.tolist())
    
    # Filter out rows where type is 2
    df = df.loc[df['type'] != 2]
    
    # Add a 'week' column with the week number of the year
    df['week'] = df['date'].dt.isocalendar().week
    
    # Add a 'month' column with the month of the date
    df['month'] = df['date'].dt.month
    
    # Add a 'year' column with the year of the date
    df['year'] = df['date'].dt.year
    
    # Calculate the total profit by adding the profit, swap, commission, and fee columns
    df.loc[:, 'total_profit'] = df['profit'] + df['swap'] + df['commission'] + df['fee']
    
    # Group by week, month, and year and sum the total profit for each group
    df_weekly_percentage_growth = df.groupby(by=['week', 'month', 'year'])['total_profit'].sum().reset_index()
    
    # Calculate the cumulative weekly growth
    df_weekly_percentage_growth.loc[:, 'cummulative_weekly_growth'] = df_weekly_percentage_growth['total_profit'].cumsum()
    
    # Calculate the daily balance by adding deposit to cumulative weekly growth
    df_weekly_percentage_growth.loc[:, 'weekly_balance'] =  deposit + df_weekly_percentage_growth['cummulative_weekly_growth']

    # Sort the DataFrame by year, month, and week in descending order
    df_weekly_percentage_growth = df_weekly_percentage_growth.sort_values(by=['year', 'month', 'week'], ascending=False)

    # shifting the dataframe by 1 week to calculate weekly growth
    df_weekly_percentage_growth['weekly_profit_shift1'] = df_weekly_percentage_growth['total_profit'].shift(1)

    # after shifting the dataframe by week 1, the first row contains NaN value , so we need to drop it
    df_weekly_percentage_growth = df_weekly_percentage_growth.dropna()

    # calculating weekly growth by taking ratio of weekly profit to last week revenue!
    df_weekly_percentage_growth['weekly_growth_%'] = round((df_weekly_percentage_growth['weekly_profit_shift1'] / df_weekly_percentage_growth['weekly_balance']),3)*100

    # Slice the DataFrame to get the first two rows
    df_weekly_percentage_growth = df_weekly_percentage_growth.iloc[:2]

    return df_weekly_percentage_growth

def monthly_percentage_growth(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate monthly percentage growth and related metrics from a given DataFrame.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame containing at least the columns ['date', 'type', 'profit', 'swap', 'commission', 'fee'].

    Returns:
    - pandas.DataFrame: A DataFrame with monthly percentage growth and related metrics.
    """
    # create a copy of the dataframe
    df = df.copy()
    
    # Convert 'date' column to datetime format
    df['date'] = pd.to_datetime(df['date'])
    
    # Calculate total deposits based on type==2 and store in variable
    deposit = sum(df.loc[df.type == 2].profit.tolist())
    
    # Filter out rows where type is 2
    df = df.loc[df['type'] != 2].copy()  # using .copy() to avoid SettingWithCopyWarning
    
    # Extract month and year from the 'date' column and create respective columns
    df.loc[:,'month'] = df['date'].dt.month
    df.loc[:,'year'] = df['date'].dt.year
    
    # Calculate the total profit by adding the profit, swap, commission, and fee columns
    df.loc[:, 'total_profit'] = df['profit'] + df['swap'] + df['commission'] + df['fee']
    
    # Group by month and year, then sum the total profit for each group
    df_month_percentage_growth = df.groupby(by=['month', 'year'])['total_profit'].sum().reset_index()
    
    # Calculate the cumulative monthly growth
    df_month_percentage_growth.loc[:, 'cummulative_monthly_growth'] = df_month_percentage_growth['total_profit'].cumsum()
    
    # Calculate the daily balance by adding deposit to cumulative monthly growth
    df_month_percentage_growth.loc[:, 'monthly_balance'] =  deposit + df_month_percentage_growth['cummulative_monthly_growth']
    
    # Sort the DataFrame by year and month in descending order
    df_month_percentage_growth = df_month_percentage_growth.sort_values(by=['year', 'month'], ascending=False)

    # shifting the dataframe by 1 month to calculate weekly growth
    df_month_percentage_growth['monthly_profit_shift1'] = df_month_percentage_growth['total_profit'].shift(1)

    # after shifting the dataframe by month 1, the first row contains NaN value , so we need to drop it
    df_month_percentage_growth = df_month_percentage_growth.dropna()
    
    # calculating weekly growth by taking ratio of weekly profit to last week revenue!
    df_month_percentage_growth['monthly_growth_%'] = round((df_month_percentage_growth['monthly_profit_shift1'] / df_month_percentage_growth['monthly_balance']),3)*100

    # Slice the DataFrame to get the first two rows
    df_month_cum_growth = df_month_percentage_growth.iloc[:2]

    return df_month_cum_growth

def main(data_file_path:str):
    
    #settingup loggin file!
    setup_logging(config.LOG_PATH)
    logger.info("Connection to dashboard is established!")

    # setting the page configuration
    base="dark"
    primaryColor="purple"
    # Setting the page config first
    st.set_page_config(
        page_title="Real-Time Forex Dashboard",
        page_icon="icon.jpg",
        layout="wide"
    )

    # displaying on the app

    st.caption('For better view on Mobile devices, switch to landscape mode!')
    st.title('My Forex Dashboard 2023')
    # reading the csv file!
    
    
    df = pd.read_csv(data_file_path)

    # creating tabs for displaying daily and total metrics!
    tab1, tab2 = st.tabs(["Daily", "Total"])

    with tab1:

        with st.container():
        # Portfolio growth calculation!
            
            Deposit, Current_Portfolio_Value, Profit_Loss, Commission, DailySwaps, DailyTradesTaken, Weekly_growth, Monthly_growth= st.columns(8)

            with Deposit:
                df = df.copy()
                deposit  =sum(df.loc[df.type == 2].profit.tolist())
                st.metric(label="Deposit", value=f"{deposit} €")

            with Current_Portfolio_Value:
                df_growth = get_portfolio_growth(df,profit = False)
                df_profit = get_portfolio_growth(df)
                current_portfolio_value = df_growth.sort_values(by = 'date', ascending = False)['growth'].to_list()[0]
                profit_or_Loss = df_profit.sort_values(by = 'date', ascending = False)['growth'].to_list()[0]
                st.metric(label="Portfolio Value:", value=f"{round(current_portfolio_value,1)} €", delta=f"{round(profit_or_Loss,2)} €")

            with Profit_Loss:
                if profit_or_Loss < 0:
                    Percentage_Gain_or_Loss = round(profit_or_Loss/(current_portfolio_value + abs(profit_or_Loss))*100,1)
                else:
                    Percentage_Gain_or_Loss = round(profit_or_Loss/(current_portfolio_value - abs(profit_or_Loss))*100,1)
                st.metric(label="% Gain/Loss:", value=f"{Percentage_Gain_or_Loss} %")

            with Commission:
                df = df.copy()
                df_commission = df.groupby(by='date')['commission'].sum().reset_index()
                df_commission = df_commission.sort_values(by='date', ascending = False).reset_index()
                df_commission = df_commission.drop(columns = ['index'])
                commissions = round(df_commission.commission.to_list()[0],2)
                st.metric(label="Daily Commissions", value=f"{round(commissions,2)} €")

            with DailySwaps:
                df = df.copy()
                df_swaps = df.groupby(by='date')['swap'].sum().reset_index()
                df_swaps = df_swaps.sort_values(by=['date'], ascending = False)
                swaps = df_swaps['swap'][0]
                st.metric(label="Swaps", value=f"{round(swaps,2)} €")

            with DailyTradesTaken:
                df = df.copy()
                df_trade = df.loc[df['type'] == 0]
                df_trade = df_trade.groupby(by = 'date').size().reset_index(name='count')
                trades_taken_yesturday = df_trade.sort_values(by='date', ascending = False)['count'].to_list()[0]
                st.metric(label="# Trades", value=f"{trades_taken_yesturday}")
            
            with Weekly_growth:
                df_weekly_cum_growth = weekly_percentage_growth(df)
                weekly_growth_list = df_weekly_cum_growth['weekly_growth_%'].to_list()
                if len(weekly_growth_list) > 1:
                    current_growth = df_weekly_cum_growth['weekly_growth_%'].to_list()[0]
                    previous_week_growth = df_weekly_cum_growth['weekly_growth_%'].to_list()[1]
                else:
                    current_growth = df_weekly_cum_growth['weekly_growth_%'].to_list()[0]
                    previous_week_growth = None
                st.metric(label = 'Weekly Growth', value = f"{current_growth} %", delta = f"{previous_week_growth} %" )

            with Monthly_growth:
                df_month_cum_growth = monthly_percentage_growth(df)
                monthly_growth_list = df_month_cum_growth['monthly_growth_%'].to_list()
                if len(monthly_growth_list) >1:
                    current_month_growth = df_month_cum_growth['monthly_growth_%'].to_list()[0]
                    previous_month_growth = df_month_cum_growth['monthly_growth_%'].to_list()[1]
                else:
                    current_month_growth = df_month_cum_growth['monthly_growth_%'].to_list()[0]
                    previous_month_growth = None
                st.metric(label = 'monthly_growth', value = f"{current_month_growth} %", delta = f"{previous_month_growth} %" )

    with tab2:

        with st.container():

            Deposit, total_profit_loss, Commission, Swaps, TotalTradesTaken = st.columns(5)

            with Deposit:
                df = df.copy()
                deposit  =sum(df.loc[df.type == 2].profit.tolist())
                st.metric(label="Deposit", value=f"{deposit} €")

            with total_profit_loss:
                df_growth = get_portfolio_growth(df,profit = False)
                current_portfolio_value = df_growth.sort_values(by = 'date', ascending = False)['growth'].to_list()[0]
                total_profit_or_Loss = round(current_portfolio_value/(deposit)*100,1) -100
                total_profit_or_Loss_eur = round((current_portfolio_value - deposit),2)
                st.metric(label="Total Portfolio Growth:", value=f"{total_profit_or_Loss_eur} €", delta=f"{round(total_profit_or_Loss,1)} %")

            with Commission:
                df = df.copy()
                df_commission = df.groupby(by='date')['commission'].sum().reset_index()
                total_commissions = df_commission.commission.sum()
                st.metric(label="Total Commissions", value=f"{round(total_commissions,2)} €", delta = f"{abs(round(commissions,2))} €")

            with Swaps:
                df = df.copy()
                df_swaps = df.groupby(by='date')['swap'].sum().reset_index()
                total_swaps = df_swaps.swap.sum()
                st.metric(label="Total Swaps", value=f"{round(total_swaps,2)} €", delta = f"{abs(round(swaps,2))} €")

            with TotalTradesTaken:
                trade = total_trades(df)
                st.metric(label = 'total trades', value = f"{trade}" ,delta = f"{trades_taken_yesturday}")

    with st.container():

        GrowthPlot, ProfitPlot = st.columns(2)
    
        with GrowthPlot:

            growthplot = plot_growth_over_time(get_portfolio_growth(df, profit = False), 'date', 'growth', title="Growth Over Time", yaxis_title= 'Daily_Portfolio (€)')
            st.plotly_chart(growthplot)
            
        with ProfitPlot:
            profitplot = profit_over_time(get_portfolio_growth(df), 'date', 'growth', title="Daily Profit", yaxis_title= 'Daily Profit (€)')
            st.plotly_chart(profitplot)

        DailyCommodityDeals, TotalCommodityDeals = st.columns(2)

        with DailyCommodityDeals:

            daily_commodity_deals = daily_commodities_trade_pie_chart(df, create_symbol_count_dataframe)
            st.plotly_chart(daily_commodity_deals)

        with TotalCommodityDeals:

            total_commodity_deals = plot_piechart(df)
            st.plotly_chart(total_commodity_deals)


        Trades, WeeklyGrowth, MonthlyGrowthProfit = st.columns(3, gap="medium")

        with Trades:

            df_trade = df.loc[df['type'] == 0]
            df_trade = df_trade.groupby(by = 'date').size().reset_index(name='count')
            plot_total_daily_trades =  profit_over_time(df_trade, 'date', 'count', title="Daily Number of Trade!", yaxis_title= 'Daily Number of Trades Taken')
            st.plotly_chart(plot_total_daily_trades)

        with WeeklyGrowth:

            weekly_growth = create_growth_chart(df, weeklygrowth = True)
            st.plotly_chart(weekly_growth)

        with MonthlyGrowthProfit:
            monthly_growth = create_growth_chart(df, weeklygrowth = False)
            st.plotly_chart(monthly_growth)

if __name__ == '__main__':
    data_file_path = 'fx_history.csv'
    main(data_file_path)
