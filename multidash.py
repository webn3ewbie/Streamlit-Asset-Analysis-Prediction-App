import streamlit as st
import yfinance as yf

def intro():
    import streamlit as st
    
    st.write("# Welcome to ExtractAlpha! ")
    st.sidebar.success("Select an Analyzer above.")
    st.markdown(
        """
        ExtractAlpha is an open-source Streamlit app built specifically to analyze equities, bonds, commodities, currencies, and cryptos. ExtractAlpha supports any asset available on YahooFinance.com
        
       
        ExtractAlpha consists of multiple unique dashboards that feature Asset Returns, Asset Price Comparisons, Asset Price Predictions, and Monte Carlo Simulation. The Asset Price Prediction leverages Facebook Prophet to predict prices up to 5 years in the future. The model is trained from data of the assets daily opening and closing price based on the time period entered by the user .Please note this app is NOT financial advice,  nor are any dashboards intended to help guide financial decisions!

        A big shoutout to [Algovibes](https://www.youtube.com/c/Algovibes/featured) and [Python Engineer](https://www.youtube.com/c/PythonEngineer). Without their videos and blog posts this project would not have be been possible, much apperciate the inspiration. Make sure you check out their excellent content!
        
        Select a dashboard and see what ExtractAlpha can do!
        #### Want to learn more?
        - Check out the repo [Here](https://github.com/webn3ewbie/Equity-Currencies-Cryptos-Bonds-Analyzer)
        - Connect with me on [LinkedIn](https://www.linkedin.com/in/joseph-biancamano/)
        - Ask a question in the Streamlit community [forums](https://discuss.streamlit.io)
        #### Yahoo Finance Ticker Cheat Sheet
        - Crude Oil: CL=F 
        - Gold: GC=F 
        - Silver: SI=F  
        - U.S. 5 Year Treasury Yield: ^FVX
        - U.S. 10 Year Treasury Yield: ^TNX
        - U.S. 30 Year Treasury Yield: ^TYX
        - Dow Jones Industrial Average: ^DJI
        - S&P 500: ^GSPC
        - Nasdaq: ^IXIC
        - Nikkei 225: ^N225
        - USD/EUR: EURUSD=X
        - CBOE Volatility Index: ^VIX
    """
    )

def price_comparison():
    import streamlit as st
    import yfinance as yf
    import pandas as pd
     
    st.title('Asset Price Analyzer') 
    start = st.date_input('Start', value = pd.to_datetime('2000-01-01'))
    end = st.date_input('End',value = pd.to_datetime('today'))
    tickers = st.text_input("Tickers", "AAPL MSFT")
    tickers = tickers.split()
    tickers_data = yf.download(tickers, period="5y", interval="1d")
    st.header('Prices of {}'.format(tickers))
    st.line_chart(tickers_data.Close) 

def asset_return():

    import streamlit as st 
    import pandas as pd
    import yfinance as yf
 
    st.title('Asset Return Analyzer')
    
    tickers = ("Tickers",'TSLA','AAPL','MSFT','BTC-USD','ETH-USD','LMT','AMZN','SPY','BRK-B','META','UNH','V','NVDA','JNJ','WMT','XOM','JPM','PG','MA','GOOG', 'QQQ','CL=F','GC=F','SI=F','^TNX','EURUSD=X','^FVX','^TYX','^RUT','^IXIC','^GSPC','^DJI','^N225','^VIX')

    dropdown = st.multiselect('Select your assests', tickers)

    start = st.date_input('Start', value = pd.to_datetime('2000-01-01'))
    end = st.date_input('End',value = pd.to_datetime('today'))
    
    def relativeret(df):
        rel = df.pct_change()
        cumret = (1+rel).cumprod() - 1
        cumret = cumret.fillna(0)
        return cumret
    
    if len (dropdown) > 0:
        df = yf.download(dropdown,start,end)['Adj Close']
        st.header('Returns of {}'.format(dropdown))
        df = relativeret(yf.download(dropdown, start, end)['Adj Close'])
        st.line_chart(df)
 
def asset_price_prediction():
    import pandas as pd
    from prophet import Prophet
    from prophet.plot import plot_plotly
    from plotly import graph_objs as go
    
    st.title('Asset Price Prediction')
    st.write("""
             Use Facebook Prophet to predict asset prices up to 5 years in the future. The model is trained from data of the assets daily opening and closing price based on the time period entered by the user, therefore the start and end date selected are very import to the models accuracy. Be sure to experiment with a short time series and a long time time series to see the difference in the  prediction. Remember this is NOT financial advice!
             
             """)
    start = st.date_input('Start', value = pd.to_datetime('2000-01-01'))
    end = st.date_input('End',value = pd.to_datetime('today'))

    stocks = ('SPY','AAPL','MSFT','BTC-USD','ETH-USD','LMT','AMZN','TSLA','BRK-B','META','UNH','V','NVDA','JNJ','WMT','XOM','^VIX','JPM','PG','MA','GOOG','CL=F','GC=F','SI=F','^TNX','EURUSD=X','^FVX','^TYX','^RUT','^IXIC','^GSPC','^DJI')

    selected_stock = st.selectbox('Select dataset for prediction', stocks)

    n_years = st.slider('Years of prediction:', 1, 5)
    period = n_years * 365

    @st.cache
    def load_data(ticker):
        data = yf.download(ticker, start,end)
        data.reset_index(inplace=True)
        return data
 	
    data_load_state = st.text('Loading data...')
    data = load_data(selected_stock)
    data_load_state.text('Loading data... done!')

    # Plot raw data
    def plot_raw_data():
    	fig = go.Figure()
    	fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
    	fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
    	fig.layout.update(title_text='Time Series Data ', xaxis_rangeslider_visible=True)
    	st.plotly_chart(fig)
    	
    plot_raw_data()

    # Predict forecast with Prophet.
    df_train = data[['Date','Close']]
    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

    m = Prophet()
    m.fit(df_train)
    future = m.make_future_dataframe(periods=period)
    forecast = m.predict(future)
    
    # Show and plot forecast
    st.subheader('Forecast data')
    st.write(forecast.tail())
        
    st.write(f'Forecast plot for {n_years} years')
    fig1 = plot_plotly(m, forecast)
    st.plotly_chart(fig1)

    st.write("Forecast components")
    fig2 = m.plot_components(forecast)
    st.write(fig2)
    
def monte_carlo():
    
    import datetime
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import seaborn as sns
    import streamlit as st
    from pandas_datareader import data as wb
    from scipy.stats import norm
    import statistics as stat
    import yfinance as yf

    #<----------SETTING THE PAGE PARAMETERS----------->
   

    #<----------HEADING PAGE TITLE AND DESCRIPTION------------>
    st.title('Monte Carlo Simulator')
    st.write("""
        The Monte Carlo is a widely used tool to solve a variety of problems ranging from numerical integration to optimization
        of financial portfolios. It's an incredible tool that used across various industries. 

        The purpose of this application is calculate the probable outcomes of a given
        security using the Monte Carlo method.
        We will manipulate the number of scenarios and days we are looking to illustrate given our equity.
        This is a basic Monte Carlo simulator that utilizes Brownian motion to estimate probable rates of return. 

        Brownian motion has two main driving components. 
         1. Drift - The different directions that rates of return have had in the past.

         2. Volatility - Utilizing historical volatility and multiplying it by a standard variable.
        Using these components we can compute the daily return of any given security. We will run a number of simulations to simulate future trading days and the impact it will have on the portfolio. 
        """)

    #<----------SELECTING A VALID TICKER FOR THE MONTE CARLO SIMULATION---------->
    ticker = st.text_input("Input a Ticker", value="SPY")

    #<----------SELECTING A STARTING DATE FOR CALCULATING THE VOLATILITY AND DRIFT COMPONENTS------>
    st.write("""
    The start date is our basis for how far back we want to collect historical data to compute our volatility and drift.
    The end date will always be today's date. 
    """)
    startDate = st.date_input("Historical Start Date", datetime.date(2010,1,1))

    #<----------SELECTING NUMBER OF DAYS WE ARE LOOKING TO FORECAST----------->
    intDays = st.number_input("Number of Future Days to Simulate", min_value=5, max_value=None, value=50) + 1

    #<----------SELECTING THE NUMBER OF SIMULATIONS TO RUN-------------------->
    intTrials = st.number_input("Total Number of Simulations to Run", min_value=5, max_value=None, value=100)

    #<----------SETTING THE NUMBER OF TOTAL SHARES INVESTED WITHIN THE FUND----------->
    numShares = st.number_input("Number of " + ticker + " Shares Held", min_value=0, max_value=None, value=10)

    #<----------FULL NAME OF FUND----------->
    fullName = yf.Ticker(ticker).info['longName']

    #<--------IMPORTING DATA FROM YAHOO FINANCE------------>
    data = pd.DataFrame()
    data[ticker] = wb.DataReader(ticker, data_source = 'yahoo',
    start = startDate)['Close']

    #<-------COMPUTING LOG RETURN-------->
    log_return = np.log(1 + data.pct_change())
    simple_return = (data/data.shift(1)-1)

    #<-------CALCULATING DRIFT------>
    u = log_return.mean()
    var = log_return.var()
    drift = u - (0.5 * var)
    stdev = log_return.std()
    Z = norm.ppf(np.random.rand(intDays, intTrials))
    daily_returns = np.exp(drift.values + stdev.values * Z)

    #<----WILL ADD FEATURE FOR ADVANCED SETTINGS TO MANIPULATE STANDARD DEVIATION AND MEAN------>
    # st.sidebar.subheader("Advanced Settings")
    # newstdev = st.sidebar.number_input("Standard Deviation", value=stdev.item(), format="%.4f")

    #<-------CALCULATING STOCK PRICE-------->
    price_paths = np.zeros_like(daily_returns)
    price_paths[0] = data.iloc[-1]
    for t in range(1, intDays):
        price_paths[t] = price_paths[t-1]*daily_returns[t]
        endValue = numShares * price_paths[t]

    with st.expander('Monte Carlo - Results', expanded=True):
        st.write("""
        Standard Deviation: {}

        Mean: {}

        Variance: {}

        Drift: {}
        """.format(stdev.item(), u.item(), var.item(), drift.item()), format="%.4f")

        #<-----PLOT HISTORICAL DATA------>
        st.subheader("Historical Closing Price for " + fullName)
        tickerFigure = plt.figure(figsize=(7,3))
        plt.plot(data)
        plt.xlabel("Date")
        plt.ylabel(ticker + " Price (USD)")
        st.pyplot(tickerFigure)

        #<-----PLOTTING HISTORICAL RETURNS HISTOGRAM----->
        st.subheader("Historical Frequency of Daily Returns")
        tickerHisto = plt.figure(figsize=(7,3))
        sns.distplot(log_return.iloc[1:])
        plt.xlabel("Daily Return")
        plt.ylabel("Frequency")
        st.pyplot(tickerHisto)

        #<-----PLOTTING MONTE CARLO CHART RESULTS------>
        st.subheader("Monte Carlo Results for " + fullName)
        mcFigure = plt.figure(figsize=(7,4))
        plt.plot(price_paths)
        plt.xlabel("# of Days Into Future")
        plt.ylabel(ticker + " Price (USD)")
        st.pyplot(mcFigure)
        
        #<-----PLOTTING MONTE CARLO HISTOGRAM RESULTS----->
        st.subheader("Density of Terminal Monte Carlo Values")
        mcHisto = plt.figure(figsize=(7,3))
        sns.distplot(pd.DataFrame(price_paths).iloc[-1])
        plt.xlabel("Price After {} Days".format(intDays-1))
        st.pyplot(mcHisto)

        #Plotting Portfolio Value Results
        portMax = max(endValue)
        portMedian = stat.median(endValue)
        portMin = min(endValue)
        
        st.subheader("Portfolio Results")
        st.write("Maximum Ending Portfolio Value: ${:,.2f}".format(portMax))
        st.write("Median Ending Portfolio Value: ${:,.2f}".format(portMedian))
        st.write("Minimum Ending Portfolio Value: ${:,.2f}".format(portMin))
        
def equity_analysis():
 #import required libraries
 import streamlit as st
 import yfinance as yf
 from datetime import datetime


 #ticker search feature in sidebar
 st.title("""Equity Fundamental Analysis""")
 selected_stock = st.text_input("Enter a valid stock ticker...", "GOOG")


 #main function
 def main():
     st.subheader("""Daily **closing price** for """ + selected_stock)
     #get data on searched ticker
     stock_data = yf.Ticker(selected_stock)
     #get historical data for searched ticker
     stock_df = stock_data.history(period='1d', start='2010-01-01', end=None)
     #print line chart with daily closing prices for searched ticker
     st.line_chart(stock_df.Close)

     st.subheader("""Last **closing price** for """ + selected_stock)
     #define variable today 
     today = datetime.today().strftime('%Y-%m-%d')
     #get current date data for searched ticker
     stock_lastprice = stock_data.history(period='1d', start=today, end=today)
     #get current date closing price for searched ticker
     last_price = (stock_lastprice.Close)
     #if market is closed on current date print that there is no data available
     if last_price.empty == True:
         st.write("No data available at the moment")
     else:
         st.write(last_price)
     
     #get daily volume for searched ticker
     st.subheader("""Daily **volume** for """ + selected_stock)
     st.line_chart(stock_df.Volume)

     #checkbox to display stock actions for the searched ticker
     actions = st.checkbox("Stock Actions")
     if actions:
         st.subheader("""Stock **actions** for """ + selected_stock)
         display_action = (stock_data.actions)
         if display_action.empty == True:
             st.write("No data available at the moment")
         else:
             st.write(display_action)
     
     #checkbox to display quarterly financials for the searched ticker
     financials = st.checkbox("Quarterly Financials")
     if financials:
         st.subheader("""**Quarterly financials** for """ + selected_stock)
         display_financials = (stock_data.quarterly_financials)
         if display_financials.empty == True:
             st.write("No data available at the moment")
         else:
             st.write(display_financials)

     #checkbox to display list of institutional shareholders for searched ticker
     major_shareholders = st.checkbox("Institutional Shareholders")
     if major_shareholders:
         st.subheader("""**Institutional investors** for """ + selected_stock)
         display_shareholders = (stock_data.institutional_holders)
         if display_shareholders.empty == True:
             st.write("No data available at the moment")
         else:
             st.write(display_shareholders)

     #checkbox to display quarterly balance sheet for searched ticker
     balance_sheet = st.checkbox("Quarterly Balance Sheet")
     if balance_sheet:
         st.subheader("""**Quarterly balance sheet** for """ + selected_stock)
         display_balancesheet = (stock_data.quarterly_balance_sheet)
         if display_balancesheet.empty == True:
             st.write("No data available at the moment")
         else:
             st.write(display_balancesheet)

     #checkbox to display quarterly cashflow for searched ticker
     cashflow = st.checkbox("Quarterly Cashflow")
     if cashflow:
         st.subheader("""**Quarterly cashflow** for """ + selected_stock)
         display_cashflow = (stock_data.quarterly_cashflow)
         if display_cashflow.empty == True:
             st.write("No data available at the moment")
         else:
             st.write(display_cashflow)

     #checkbox to display quarterly earnings for searched ticker
     earnings = st.checkbox("Quarterly Earnings")
     if earnings:
         st.subheader("""**Quarterly earnings** for """ + selected_stock)
         display_earnings = (stock_data.quarterly_earnings)
         if display_earnings.empty == True:
             st.write("No data available at the moment")
         else:
             st.write(display_earnings)

     #checkbox to display list of analysts recommendation for searched ticker
     analyst_recommendation = st.checkbox("Analysts Recommendation")
     if analyst_recommendation:
         st.subheader("""**Analysts recommendation** for """ + selected_stock)
         display_analyst_rec = (stock_data.recommendations)
         if display_analyst_rec.empty == True:
             st.write("No data available at the moment")
         else:
             st.write(display_analyst_rec)
         st.subheader("""Daily **closing price** for """ + selected_stock)
         #get data on searched ticker
         stock_data = yf.Ticker(selected_stock)
         #get historical data for searched ticker
         stock_df = stock_data.history(period='1d', start='2010-01-01', end=None)
         #print line chart with daily closing prices for searched ticker
         st.line_chart(stock_df.Close)

         st.subheader("""Last **closing price** for """ + selected_stock)
         #define variable today 
         today = datetime.today().strftime('%Y-%m-%d')
         #get current date data for searched ticker
         stock_lastprice = stock_data.history(period='1d', start=today, end=today)
         #get current date closing price for searched ticker
         last_price = (stock_lastprice.Close)
         #if market is closed on current date print that there is no data available
         if last_price.empty == True:
             st.write("No data available at the moment")
         else:
             st.write(last_price)
         
         #get daily volume for searched ticker
         st.subheader("""Daily **volume** for """ + selected_stock)
         st.line_chart(stock_df.Volume)


 if __name__ == "__main__":
     main()



page_names_to_funcs = {
    "Home": intro,
    "Asset Return Comparison": asset_return,
    "Asset Price Comparison": price_comparison,
    "Assest Price Prediction": asset_price_prediction,
    "Monte Carlo Simulation": monte_carlo,
    "Equity Fundemental Analysis": equity_analysis
}

demo_name = st.sidebar.selectbox("Choose a dashboard", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()
